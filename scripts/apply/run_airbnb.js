const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function autoApply() {
    const configPath = path.join(__dirname, '../../.praxis/data/apply_config.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const p = config.personal_info;
    const defaults = config.application_defaults;
    const eeoc = config.compliance_and_eeoc;

    const resumePath = path.join(__dirname, '../../assets/Airbnb/Airbnb_Kenton_Smeltzer_Resume.pdf');
    const clPath = path.join(__dirname, '../../assets/Airbnb/Airbnb_Kenton_Smeltzer_Cover_Letter.pdf');

    const browser = await chromium.launch({ headless: false, args: ['--no-sandbox', '--disable-setuid-sandbox'] }); 
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        await page.goto('https://boards.greenhouse.io/airbnb/jobs/7826679', { waitUntil: 'domcontentloaded' });
        
        console.log("[Auto-Applier] Form found. Injecting data...");

        // Basic Info
        if (await page.$('#first_name')) await page.fill('#first_name', p.first_name);
        if (await page.$('#last_name')) await page.fill('#last_name', p.last_name);
        if (await page.$('#email')) await page.fill('#email', p.email);
        if (await page.$('#phone')) await page.fill('#phone', p.phone);

        // Files
        if (fs.existsSync(resumePath)) {
            const resumeInput = await page.$('input[type="file"][data-field-type="resume"], input[type="file"][name="resume"]');
            if (resumeInput) await resumeInput.setInputFiles(resumePath);
        }
        
        if (fs.existsSync(clPath)) {
            const clInput = await page.$('input[type="file"][data-field-type="cover_letter"], input[type="file"][name="cover_letter"]');
            if (clInput) await clInput.setInputFiles(clPath);
        }

        // Location / Address (Greenhouse location fields)
        if (await page.$('#job_application_location')) await page.fill('#job_application_location', `${defaults.city}, ${defaults.state}, ${defaults.country}`);

        // Custom fields (Links, demographics, EEOC)
        const customQuestions = await page.$$('.custom_question');
        for (const q of customQuestions) {
            const text = await q.innerText();
            const lowerText = text.toLowerCase();
            
            // Try to find text inputs
            const input = await q.$('input[type="text"]');
            if (input) {
                if (lowerText.includes('linkedin')) await input.fill(p.linkedin);
                else if (lowerText.includes('github')) await input.fill(p.github);
                else if (lowerText.includes('website') || lowerText.includes('portfolio')) await input.fill(p.portfolio);
            }
            
            // Try to find dropdowns/selects
            const select = await q.$('select');
            if (select) {
                if (lowerText.includes('authorized to work')) await select.selectOption({ label: eeoc.authorized_to_work_in_us });
                else if (lowerText.includes('sponsorship')) await select.selectOption({ label: eeoc.require_sponsorship });
                else if (lowerText.includes('gender')) await select.selectOption({ label: eeoc.gender });
                else if (lowerText.includes('race')) await select.selectOption({ label: eeoc.race });
                else if (lowerText.includes('veteran')) await select.selectOption({ label: eeoc.veteran_status });
                else if (lowerText.includes('disability')) await select.selectOption({ label: eeoc.disability_status });
                else if (lowerText.includes('hear about')) await select.selectOption({ label: defaults.how_did_you_hear });
            }
        }

        // EEOC standard Greenhouse Dropdowns (bottom of the page)
        if (await page.$('#job_application_gender')) {
            await page.selectOption('#job_application_gender', { label: eeoc.gender }).catch(()=>console.log("Could not set gender"));
        }
        if (await page.$('#job_application_hispanic_ethnicity')) {
            await page.selectOption('#job_application_hispanic_ethnicity', { label: eeoc.race }).catch(()=>console.log("Could not set race"));
        }
        if (await page.$('#job_application_veteran_status')) {
            await page.selectOption('#job_application_veteran_status', { label: eeoc.veteran_status }).catch(()=>console.log("Could not set veteran"));
        }
        if (await page.$('#job_application_disability_status')) {
            await page.selectOption('#job_application_disability_status', { label: eeoc.disability_status }).catch(()=>console.log("Could not set disability"));
        }

        console.log("==========================================");
        console.log("[Auto-Applier] Finished filling the application.");
        console.log("CRITICAL: Halting execution. Please review the browser window manually.");
        console.log("DO NOT click 'Submit Application' automatically.");
        console.log("==========================================");
        
        // Wait indefinitely so the user can review and click Submit themselves
        await new Promise(() => {});

    } catch (error) {
        console.error("Error:", error);
    }
}

autoApply();
