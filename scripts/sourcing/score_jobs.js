const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { isDuplicate } = require('./dedupe_helper');

const STAGING_DIR = path.join(__dirname, '../../.praxis/staging');
const QUEUE_DIR = path.join(__dirname, '../../.praxis/queue');
const PARAMS_PATH = path.join(__dirname, '../../.praxis/data/search_parameters.json');

if (!fs.existsSync(QUEUE_DIR)) fs.mkdirSync(QUEUE_DIR, { recursive: true });
if (!fs.existsSync(STAGING_DIR)) fs.mkdirSync(STAGING_DIR, { recursive: true });

function extractDateFromMarkdown(content) {
    const match = content.match(/date_scraped:\s*([^\n]+)/);
    if (match) return new Date(match[1].trim());
    return new Date(); // Fallback to now if not found
}

function evaluateJob(filePath, fileName, params) {
    console.log(`\n[Gatekeeper] Evaluating ${fileName}...`);
    const jobContent = fs.readFileSync(filePath, 'utf8');
    
    // Check Age Cutoff locally before invoking LLM to save tokens
    const maxAgeDays = params.filters?.hard_requirements?.max_posting_age_days || 7;
    const scrapedDate = extractDateFromMarkdown(jobContent);
    const ageDays = (new Date() - scrapedDate) / (1000 * 60 * 60 * 24);
    
    // Extract company and title for deduping
    const companyMatch = jobContent.match(/company:\s*"?([^"\n]+)"?/);
    const titleMatch = jobContent.match(/title:\s*"?([^"\n]+)"?/);
    const company = companyMatch ? companyMatch[1].trim() : "";
    const title = titleMatch ? titleMatch[1].trim() : "";

    if (isDuplicate(company, title)) {
        return {
            pass_fail: false,
            score: 0,
            compensation_extracted: "Hidden",
            match_rationale: `HARD FAIL: Duplicate - Already applied to this role at ${company}.`
        };
    }

    if (ageDays > maxAgeDays) {
        return {
            pass_fail: false,
            score: 0,
            compensation_extracted: "Hidden",
            match_rationale: `HARD FAIL: Job posting age (${Math.round(ageDays)} days) exceeds the strict maximum threshold of ${maxAgeDays} days.`
        };
    }

    // Build the prompt for the LLM
    const prompt = `
You are a ruthless technical recruiter API. Your ONLY job is to evaluate the following Job Description against my exact requirements and return a raw JSON object. Do not output markdown, explanations, or code blocks. ONLY JSON.

=== MY REQUIREMENTS (from search_parameters.json) ===
${JSON.stringify(params, null, 2)}

=== EVALUATION RULES ===
1. HARD FAIL (pass_fail: false): If the job requires Hybrid/On-site (unless it's an extreme $500k+ override).
2. HARD FAIL (pass_fail: false): If the job explicitly states a maximum salary below my floor ($240k W2 / $155/hr C2C). Note: If salary is hidden/unstated, DO NOT fail it on salary; assume it might meet the requirements.
3. HARD FAIL (pass_fail: false): If the primary tech stack is a Dealbreaker (e.g., .NET, Legacy Java).
4. SCORING (0-100): Start at 50. Add points for Domain Multipliers (+15 each). Add points for Preferred Tech (+10 each). Add points if salary explicitly exceeds the floor (+10 to +30). Deduct points for vague descriptions.
5. OVERRIDE: If the salary explicitly exceeds the "absolute_compensation_trump" threshold ($500k+ W2), score is 100 and pass_fail is true, ignoring all other dealbreakers except location without relocation.

=== TARGET JOB DESCRIPTION ===
${jobContent}

=== REQUIRED JSON OUTPUT FORMAT ===
{
  "pass_fail": true/false,
  "score": number (0-100),
  "compensation_extracted": "string (the exact salary band found, or 'Hidden')",
  "match_rationale": "string (1-2 sentences explaining why it passed/failed and how it scored)"
}
`;

    // Write prompt to a temporary file to avoid shell escaping issues
    const tempPromptPath = path.join(__dirname, `temp_prompt_${Date.now()}.txt`);
    fs.writeFileSync(tempPromptPath, prompt);

    try {
        // Run opencode in headless mode using the file content
        console.log(`[Gatekeeper] Running LLM inference via opencode headless...`);
        const result = execSync(`opencode run --pure "$(cat ${tempPromptPath})"`, {
            encoding: 'utf8',
            stdio: ['pipe', 'pipe', 'ignore'] // ignore stderr to keep logs clean
        });

        // Clean up temp file
        fs.unlinkSync(tempPromptPath);

        // Extract JSON from output (in case opencode adds ANSI or conversational text)
        const jsonMatch = result.match(/\{[\s\S]*\}/);
        if (!jsonMatch) {
            console.error(`[Gatekeeper] ERROR: Could not parse JSON from LLM output for ${fileName}`);
            return null;
        }

        const evaluation = JSON.parse(jsonMatch[0]);
        // Append the scraped date for sorting later
        evaluation._date = scrapedDate;
        return evaluation;

    } catch (error) {
        console.error(`[Gatekeeper] Execution error for ${fileName}:`, error.message);
        if (fs.existsSync(tempPromptPath)) fs.unlinkSync(tempPromptPath);
        return null;
    }
}

function run() {
    if (!fs.existsSync(PARAMS_PATH)) {
        console.error("[Gatekeeper] FATAL: search_parameters.json not found.");
        process.exit(1);
    }
    
    const params = JSON.parse(fs.readFileSync(PARAMS_PATH, 'utf8'));
    const files = fs.readdirSync(STAGING_DIR).filter(f => f.endsWith('.md'));

    if (files.length === 0) {
        console.log("[Gatekeeper] Staging directory is empty. Nothing to score.");
        return;
    }

    console.log(`[Gatekeeper] Found ${files.length} jobs in staging. Booting LLM Gatekeeper...`);

    let passed = 0;
    let failed = 0;
    let passedJobs = []; // Array to hold winners so we can sort them

    for (const file of files) {
        const filePath = path.join(STAGING_DIR, file);
        const evaluation = evaluateJob(filePath, file, params);

        if (!evaluation) {
            console.log(`[Gatekeeper] Skipped ${file} due to parsing error.`);
            continue;
        }

        console.log(`   -> Pass: ${evaluation.pass_fail} | Score: ${evaluation.score} | Comp: ${evaluation.compensation_extracted}`);
        console.log(`   -> Rationale: ${evaluation.match_rationale}`);

        if (evaluation.pass_fail && evaluation.score >= 70) {
            // Read content before deleting
            const originalContent = fs.readFileSync(filePath, 'utf8');
            fs.unlinkSync(filePath); // Remove from staging
            
            passedJobs.push({
                file: file,
                evaluation: evaluation,
                content: originalContent,
                date: evaluation._date || new Date()
            });
            passed++;
        } else {
            // Failed. Delete it.
            fs.unlinkSync(filePath);
            failed++;
        }
    }

    console.log(`\n[Gatekeeper] Finished scoring. Sorting ${passedJobs.length} winners by newest first...`);
    
    // Sort jobs descending by date (newest first)
    passedJobs.sort((a, b) => b.date - a.date);

    // Write them to the queue
    for (const job of passedJobs) {
        // Since we are sorting, we can optionally prepend a sequential number to the filename 
        // to enforce the queue order alphabetically in the filesystem
        const queuePath = path.join(QUEUE_DIR, job.file);
        
        const metadataHeader = `---
praxis_status: QUEUED
praxis_score: ${job.evaluation.score}
praxis_comp_extracted: ${job.evaluation.compensation_extracted}
praxis_rationale: "${job.evaluation.match_rationale}"
---
`;
        fs.writeFileSync(queuePath, metadataHeader + job.content);
    }

    console.log(`[Gatekeeper] Passed: ${passed} | Failed/Trashed: ${failed}`);
    if (passed > 0) {
        console.log(`[Gatekeeper] ${passed} high-scoring jobs are waiting for you in .praxis/queue/, prioritized by newest first.`);
    }
}

run();
