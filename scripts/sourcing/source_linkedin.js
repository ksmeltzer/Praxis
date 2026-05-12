const { LinkedinScraper, events } = require('linkedin-jobs-scraper');
const fs = require('fs');
const path = require('path');

// Target directory for scraped raw jobs
const STAGING_DIR = path.join(__dirname, '../../.praxis/staging');
if (!fs.existsSync(STAGING_DIR)) {
    fs.mkdirSync(STAGING_DIR, { recursive: true });
}

// Each scraper instance is run with anonymous proxy-like public settings
const scraper = new LinkedinScraper({
    headless: "new",
    slowMo: 1000, // Very slow to avoid rate limits
    args: [
        "--lang=en-US",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage"
    ]
});

// Capture jobs and save them as markdown stubs for Praxis to process
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
    console.error(`[Praxis Sourcing] Error: ${err}`);
});

scraper.on(events.scraper.end, () => {
    console.log('[Praxis Sourcing] Scraping complete. Jobs waiting in .praxis/staging/ for LLM scoring.');
});

// Start the scrape: Target Principal/Staff AI roles, Remote
scraper.run([
    {
        query: "Staff AI Engineer",
        options: {
            locations: ["United States"],
            filters: {
                remote: true,
                time: {
                    range: "r86400" // Last 24 hours
                }
            }
        }
    },
    {
        query: "Principal Software Engineer",
        options: {
            locations: ["United States"],
            filters: {
                remote: true,
                time: {
                    range: "r86400" // Last 24 hours
                }
            }
        }
    }
], { // Global options
    locations: ["United States"],
    limit: 15, // Only grab the top 15 newest matching jobs
    optimize: true // Skip loading images/CSS for speed and stealth
});
