const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Setup Error Logging
const ERROR_LOG_PATH = path.join(__dirname, '../../.praxis/data/apply_errors.log');
function logError(jobUrl, issue, htmlContext = '') {
    const timestamp = new Date().toISOString();
    let logEntry = `\n[${timestamp}] FAILED: ${jobUrl}\nIssue: ${issue}\n`;
    if (htmlContext) {
        logEntry += `DOM Snippet (First 500 chars): ${htmlContext.substring(0, 500)}\n`;
    }
    logEntry += `--------------------------------------------------\n`;
    fs.appendFileSync(ERROR_LOG_PATH, logEntry);
    console.error(`[Smart-Applier] Error logged to .praxis/data/apply_errors.log: ${issue}`);
}

async function extractCleanFormHTML(frame) {
    return await frame.evaluate(() => {
        const clone = document.body.cloneNode(true);
        const elementsToRemove = clone.querySelectorAll('script, style, svg, path, img, nav, header, footer, meta, link, noscript');
        elementsToRemove.forEach(el => el.remove());

        const form = clone.querySelector('form') || clone;
        
        const allElements = form.querySelectorAll('*');
        allElements.forEach(el => {
            const keepAttrs = ['id', 'name', 'type', 'class', 'placeholder', 'value', 'for', 'data-field-type', 'aria-label'];
            for (let i = el.attributes.length - 1; i >= 0; i--) {
                const attrName = el.attributes[i].name;
                if (!keepAttrs.includes(attrName)) {
                    el.removeAttribute(attrName);
                }
            }
        });

        return form.innerHTML.replace(/\s+/g, ' ').trim();
    });
}

async function autoApply(jobUrl, resumePath) {
    // 1. Load the Master Knowledge Base (Full Context for the Agent)
    const kbPath = path.join(__dirname, '../../.praxis/data/knowledge_base.json');
    if (!fs.existsSync(kbPath)) {
        console.error("[Smart-Applier] Missing knowledge_base.json");
        return;
    }
    const kb = JSON.parse(fs.readFileSync(kbPath, 'utf8'));

    // 2. Load the Compliance Config
    const configPath = path.join(__dirname, '../../.praxis/data/apply_config.json');
    let config = { compliance_and_eeoc: {} };
    if (fs.existsSync(configPath)) {
        config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }

    console.log(`[Smart-Applier] Launching browser to map and apply at: ${jobUrl}`);
    const browser = await chromium.launch({ headless: false }); 
    const context = await browser.newContext();
    const page = await context.newPage();

    let targetFrame = null;
    let cleanHTML = '';

    try {
        await page.goto(jobUrl, { waitUntil: 'networkidle' });
        
        const applyButton = await page.$('a[href*="apply"], button:has-text("Apply")');
        if (applyButton) {
             console.log("[Smart-Applier] Clicking 'Apply' button to reveal form...");
             await applyButton.click();
             await page.waitForTimeout(5000); 
        }

        // FIND THE RIGHT FRAME
        targetFrame = page.mainFrame();
        for (const frame of page.frames()) {
            const html = await frame.content();
            if (html.toLowerCase().includes('resume') || html.includes('type="file"')) {
                targetFrame = frame;
                console.log("[Smart-Applier] Identified application iframe.");
                break;
            }
        }

        console.log("[Smart-Applier] Extracting DOM for Praxis Seeker Agent analysis...");
        cleanHTML = await extractCleanFormHTML(targetFrame);
        // Drastically shrink HTML so the prompt doesn't get truncated by shell limits
        const truncatedHTML = cleanHTML.substring(0, 8000); 

        const prompt = `
You are a DOM mapping agent. Your job is to read an HTML form and a JSON configuration of my personal details.
Return ONLY a valid JSON array mapping my details to the correct CSS selectors in the HTML. Do not return markdown, explanations, or code blocks. ONLY the JSON array.

CRITICAL RULES:
1. You MUST find and map the file input element for the Resume/CV upload (action: "upload", value: "RESUME_PATH").
2. You MUST find and map the text input element for the LinkedIn profile URL.
3. You MUST find and map the input elements for First Name, Last Name, Email, and Phone.
4. Do not stop early. Provide an exhaustive mapping for all provided personal details.

Example Format:
[
  { "selector": "input#first_name", "action": "fill", "value": "Kenton" },
  { "selector": "select#country", "action": "select", "value": "United States" },
  { "selector": "textarea#custom_question_123", "action": "fill", "value": "I scaled AI workflows at DexCare..." },
  { "selector": "input[type='file'][data-field-type='resume']", "action": "upload", "value": "RESUME_PATH" }
]

=== APPLY CONFIG (Compliance/EEOC) ===
${JSON.stringify(config.compliance_and_eeoc, null, 2)}

=== MASTER KNOWLEDGE BASE (Truncated for space) ===
${JSON.stringify({ basics: kb.basics }, null, 2)}

=== HTML FORM (Minified) ===
${truncatedHTML}
`;

        const tempPromptPath = path.join(__dirname, `temp_dom_prompt_${Date.now()}.txt`);
        fs.writeFileSync(tempPromptPath, prompt);

        console.log("[Smart-Applier] Handing DOM and Knowledge Base over to the Praxis Seeker Agent...");
        
                let resultJSON = '[]';
        try {
            const result = execSync(`opencode run --agent praxis-seeker "$(cat ${tempPromptPath})"`, {
                encoding: 'utf8',
                stdio: ['pipe', 'pipe', 'pipe'] // Capture stderr too just in case
            });
            
            // Log the raw output for debugging
            fs.appendFileSync(ERROR_LOG_PATH, `\n[DEBUG] Raw LLM Output:\n${result}\n`);
            
            const match = result.match(/\[[\s\S]*\]/);
            if (match) {
                resultJSON = match[0];
            } else {
                throw new Error("LLM did not return a valid JSON array. See raw output above.");
            }
        } catch (e) {
            let errorMsg = e.message;
            if (e.stderr) errorMsg += "\nSTDERR: " + e.stderr.toString();
            logError(jobUrl, `Agent Execution Failed: ${errorMsg}`, truncatedHTML);
            fs.unlinkSync(tempPromptPath);
            throw new Error("Agent failed to parse the form.");
        }
        fs.unlinkSync(tempPromptPath);

        let actions;
        try {
            actions = JSON.parse(resultJSON);
        } catch (e) {
            logError(jobUrl, `JSON Parse Error from Agent output: ${resultJSON}`, truncatedHTML);
            throw new Error("Agent returned invalid JSON.");
        }

        console.log(`[Smart-Applier] Praxis Seeker returned ${actions.length} form mapping actions. Executing...`);

        // EXECUTE THE MAPPED ACTIONS
        let successCount = 0;
        let failCount = 0;

        for (const action of actions) {
            try {
                const elementExists = await targetFrame.$(action.selector);
                if (!elementExists) {
                    console.log(`  -> Skipping ${action.selector} (Not found in DOM)`);
                    failCount++;
                    continue;
                }

                if (action.action === 'fill') {
                    await targetFrame.fill(action.selector, action.value);
                    console.log(`  -> Filled ${action.selector}`);
                } else if (action.action === 'select') {
                    await targetFrame.selectOption(action.selector, { label: action.value }).catch(() => targetFrame.selectOption(action.selector, action.value));
                    console.log(`  -> Selected ${action.value} on ${action.selector}`);
                } else if (action.action === 'upload') {
                    if (action.value === 'RESUME_PATH' && fs.existsSync(resumePath)) {
                        await targetFrame.setInputFiles(action.selector, resumePath);
                        console.log(`  -> Uploaded Resume to ${action.selector}`);
                    }
                    // Future proofing for cover letters
                    else if (action.value === 'COVER_LETTER_PATH') {
                        const clPath = resumePath.replace('_Resume.pdf', '_Cover_Letter.pdf');
                        if (fs.existsSync(clPath)) {
                            await targetFrame.setInputFiles(action.selector, clPath);
                            console.log(`  -> Uploaded Cover Letter to ${action.selector}`);
                        }
                    }
                }
                successCount++;
            } catch (err) {
                console.log(`  -> Failed to execute action on ${action.selector}: ${err.message.split('\n')[0]}`);
                failCount++;
            }
        }

        console.log(`\n[Smart-Applier] Execution complete. Success: ${successCount}, Failed: ${failCount}.`);
        if (failCount > Math.max(2, actions.length * 0.3)) {
             logError(jobUrl, `High failure rate during execution (${failCount} failed actions). Selectors might be incorrect or elements hidden.`, truncatedHTML);
        }

        console.log("[Smart-Applier] Browser remains open for final user review and Submit.");
        // Leave the browser open
        await new Promise(() => {});

    } catch (error) {
        console.error("[Smart-Applier] Critical Error:", error.message);
        if (!error.message.includes("Agent failed to parse")) {
            logError(jobUrl, `Playwright Execution Error: ${error.message}`, cleanHTML);
        }
        await browser.close();
    }
}

const url = process.argv[2];
const resume = process.argv[3] || path.join(__dirname, '../../assets/Resume.pdf');
if (!url) {
    console.log("Usage: node apply_smart.js <job_url> [resume_path]");
    process.exit(1);
}

autoApply(url, resume);
