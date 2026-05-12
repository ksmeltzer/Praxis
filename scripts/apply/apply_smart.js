const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

async function extractCleanFormHTML(frame) {
    return await frame.evaluate(() => {
        // Clone the body to avoid destroying the actual page
        const clone = document.body.cloneNode(true);
        
        // Remove junk that eats up LLM tokens
        const elementsToRemove = clone.querySelectorAll('script, style, svg, path, img, nav, header, footer, meta, link, noscript');
        elementsToRemove.forEach(el => el.remove());

        // Focus just on forms or main application containers if possible
        const form = clone.querySelector('form') || clone;
        
        // Strip out excessive attributes to save tokens
        const allElements = form.querySelectorAll('*');
        allElements.forEach(el => {
            const keepAttrs = ['id', 'name', 'type', 'class', 'placeholder', 'value', 'for', 'data-field-type'];
            for (let i = el.attributes.length - 1; i >= 0; i--) {
                const attrName = el.attributes[i].name;
                if (!keepAttrs.includes(attrName)) {
                    el.removeAttribute(attrName);
                }
            }
        });

        // Minify HTML
        return form.innerHTML.replace(/\s+/g, ' ').trim();
    });
}

async function autoApply(jobUrl, resumePath) {
    const configPath = path.join(__dirname, '../../.praxis/data/apply_config.json');
    if (!fs.existsSync(configPath)) {
        console.error("[Smart-Applier] Missing apply_config.json");
        return;
    }
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

    console.log(`[Smart-Applier] Launching browser to map and apply at: ${jobUrl}`);
    const browser = await chromium.launch({ headless: false }); 
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        await page.goto(jobUrl, { waitUntil: 'networkidle' });
        
        // Sometimes ATS are behind an "Apply Now" button.
        const applyButton = await page.$('a[href*="apply"], button:has-text("Apply")');
        if (applyButton) {
             console.log("[Smart-Applier] Clicking 'Apply' button to reveal form...");
             await applyButton.click();
             await page.waitForTimeout(3000); // Wait for potential iframe or modal load
        }

        // FIND THE RIGHT FRAME
        // Airbnb and others embed Greenhouse/Lever forms in an iframe
        let targetFrame = page.mainFrame();
        for (const frame of page.frames()) {
            const html = await frame.content();
            if (html.toLowerCase().includes('resume') || html.includes('type="file"')) {
                targetFrame = frame;
                console.log("[Smart-Applier] Identified application iframe.");
                break;
            }
        }

        console.log("[Smart-Applier] Extracting DOM for Copilot analysis...");
        const cleanHTML = await extractCleanFormHTML(targetFrame);

        // Keep HTML to a reasonable token size (truncate if massive)
        const truncatedHTML = cleanHTML.substring(0, 15000); 

        const prompt = `
You are a DOM mapping agent. Your job is to read an HTML form and a JSON configuration of my personal details.
Return ONLY a valid JSON array mapping my details to the correct CSS selectors in the HTML. Do not return markdown, explanations, or code blocks. ONLY the JSON array.

=== MY DETAILS ===
${JSON.stringify(config, null, 2)}

=== HTML FORM (Minified) ===
${truncatedHTML}

=== OUTPUT INSTRUCTIONS ===
Return a JSON array where each object represents an action to take on the form.
Valid actions: "fill", "select", "upload"
For select elements, the "value" must match one of the <option> values or visible text in the HTML.

Example Format:
[
  { "selector": "input#first_name", "action": "fill", "value": "Kenton" },
  { "selector": "input[name='job_application[email]']", "action": "fill", "value": "kenton@example.com" },
  { "selector": "select#eeoc_gender", "action": "select", "value": "Decline to self-identify" },
  { "selector": "input[type='file']", "action": "upload", "value": "RESUME_PATH" }
]
`;

        const tempPromptPath = path.join(__dirname, `temp_dom_prompt_${Date.now()}.txt`);
        fs.writeFileSync(tempPromptPath, prompt);

        console.log("[Smart-Applier] Asking Headless Copilot to map the DOM. This takes 5-10 seconds...");
        
        let resultJSON = '[]';
        try {
            const result = execSync(`opencode run --pure "$(cat ${tempPromptPath})"`, {
                encoding: 'utf8',
                stdio: ['pipe', 'pipe', 'ignore']
            });
            const match = result.match(/\[[\s\S]*\]/);
            if (match) {
                resultJSON = match[0];
            }
        } catch (e) {
            console.error("[Smart-Applier] Copilot execution failed:", e.message);
        }
        fs.unlinkSync(tempPromptPath);

        const actions = JSON.parse(resultJSON);
        console.log(`[Smart-Applier] Copilot returned ${actions.length} form mapping actions. Executing...`);

        // EXECUTE THE MAPPED ACTIONS
        for (const action of actions) {
            try {
                // Ensure selector exists in frame
                const elementExists = await targetFrame.$(action.selector);
                if (!elementExists) {
                    console.log(`  -> Skipping ${action.selector} (Not found in DOM)`);
                    continue;
                }

                if (action.action === 'fill') {
                    await targetFrame.fill(action.selector, action.value);
                    console.log(`  -> Filled ${action.selector}`);
                } else if (action.action === 'select') {
                    await targetFrame.selectOption(action.selector, { label: action.value }).catch(() => targetFrame.selectOption(action.selector, action.value));
                    console.log(`  -> Selected ${action.value} on ${action.selector}`);
                } else if (action.action === 'upload') {
                    if (fs.existsSync(resumePath)) {
                        await targetFrame.setInputFiles(action.selector, resumePath);
                        console.log(`  -> Uploaded Resume to ${action.selector}`);
                    }
                }
            } catch (err) {
                console.log(`  -> Failed to execute action on ${action.selector}: ${err.message.split('\\n')[0]}`);
            }
        }

        console.log("\n[Smart-Applier] Smart mapping complete. Browser remains open for final user review and Submit.");
        // Leave the browser open
        await new Promise(() => {});

    } catch (error) {
        console.error("[Smart-Applier] Error:", error.message);
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
