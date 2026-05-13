const { LinkedinScraper, events, timeFilter } = require('linkedin-jobs-scraper');
const fs = require('fs');
const path = require('path');

const STAGING_DIR = path.join(__dirname, '../../.praxis/staging');
if (!fs.existsSync(STAGING_DIR)) {
    fs.mkdirSync(STAGING_DIR, { recursive: true });
}

const scraper = new LinkedinScraper({
    headless: "new",
    slowMo: 100, // Speeding it up a tiny bit for the test
    args: [
        "--lang=en-US",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage"
    ]
});

scraper.on(events.scraper.data, (data) => {
    console.log(`[Praxis Sourcing] Found Job: ${data.title} at ${data.company}`);
    
    const safeCompany = data.company.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const safeTitle = data.title.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const filePath = path.join(STAGING_DIR, `${safeCompany}_${safeTitle}_${Date.now()}.md`);
    
    const content = `---
source: LinkedIn Public
url: ${data.link}
company: ${data.company}
title: ${data.title}
location: ${data.location}
date: ${data.date}
---

# ${data.title} at ${data.company}
**Location:** ${data.location}
**Link:** ${data.link}

## Job Description
${data.description}
`;
    
    fs.writeFileSync(filePath, content);
});

scraper.on(events.scraper.error, (err) => {
    console.error(`[Praxis Sourcing] Error:`, err);
});

scraper.on(events.scraper.end, () => {
    console.log('[Praxis Sourcing] Scraping complete. Jobs waiting in .praxis/staging/');
});

scraper.run([
    {
        query: "Staff AI Engineer",
        options: {
            locations: ["United States"],
            filters: {
                remote: true,
                time: "r86400"
            }
        }
    },
    {
        query: "Principal Software Engineer",
        options: {
            locations: ["United States"],
            filters: {
                remote: true,
                time: "r86400"
            }
        }
    }
], {
    locations: ["United States"],
    limit: 5,
    optimize: true
});
