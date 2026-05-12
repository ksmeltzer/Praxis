const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function autoApply(jobUrl, resumePath) {
    const configPath = path.join(__dirname, '../../.praxis/data/apply_config.json');
    if (!fs.existsSync(configPath)) {
        console.error("Missing apply_config.json");
        return;
    }
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const p = config.personal_info;

    console.log(`[Auto-Applier] Launching browser to apply at: ${jobUrl}`);
    // headless: false so you can watch it work!
    const browser = await chromium.launch({ headless: false }); 
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        await page.goto(jobUrl, { waitUntil: 'domcontentloaded' });
        
        // Wait for the application form to be visible
        await page.waitForSelector('#application_form', { timeout: 10000 });
        console.log("[Auto-Applier] Form found. Injecting data...");

        // Basic Info
        if (await page.$('#first_name')) await page.fill('#first_name', p.first_name);
        if (await page.$('#last_name')) await page.fill('#last_name', p.last_name);
        if (await page.$('#email')) await page.fill('#email', p.email);
        if (await page.$('#phone')) await page.fill('#phone', p.phone);

        // Upload Resume
        if (fs.existsSync(resumePath)) {
            const fileInput = await page.$('input[type="file"][data-field-type="resume"]');
            if (fileInput) {
                await fileInput.setInputFiles(resumePath);
                console.log("[Auto-Applier] Resume uploaded.");
            }
        } else {
            console.log(`[Auto-Applier] WARNING: Resume not found at ${resumePath}`);
        }

        // Links (Greenhouse often uses custom fields for these, we try standard naming first)
        const inputs = await page.$$('input[type="text"]');
        for (const input of inputs) {
            const name = await input.getAttribute('name') || '';
            const label = await page.evaluate(el => {
                const id = el.id;
                if (!id) return '';
                const labelEl = document.querySelector(`label[for="${id}"]`);
                return labelEl ? labelEl.innerText.toLowerCase() : '';
            }, input);

            if (label.includes('linkedin')) await input.fill(p.linkedin);
            if (label.includes('github')) await input.fill(p.github);
            if (label.includes('website') || label.includes('portfolio')) await input.fill(p.portfolio);
        }

        console.log("[Auto-Applier] Form filled. Waiting for user review...");
        console.log("[Auto-Applier] NOTE: I am leaving the final 'Submit' button for YOU to click after review.");
        
        // Keep browser open for user to review and submit
        await new Promise(() => {}); 

    } catch (error) {
        console.error("[Auto-Applier] Error during application:", error.message);
        await browser.close();
    }
}

const url = process.argv[2];
const resume = process.argv[3] || path.join(__dirname, '../../assets/Resume.pdf'); // Fallback to baseline
if (!url) {
    console.log("Usage: node apply_greenhouse.js <job_url> [resume_path]");
    process.exit(1);
}

autoApply(url, resume);
