const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

const STAGING_DIR = path.join(__dirname, '../../.praxis/staging');

if (!fs.existsSync(STAGING_DIR)) {
    fs.mkdirSync(STAGING_DIR, { recursive: true });
}

// We Work Remotely RSS Feeds for Programming
const FEEDS = [
    'https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss',
    'https://weworkremotely.com/categories/remote-front-end-programming-jobs.rss',
    'https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss'
];

async function run() {
    console.log("[We Work Remotely] Fetching RSS feeds...");
    let savedCount = 0;

    for (const feedUrl of FEEDS) {
        try {
            const { data } = await axios.get(feedUrl);
            const $ = cheerio.load(data, { xmlMode: true });
            
            $('item').each((i, el) => {
                const titleFull = $(el).find('title').text(); // Usually "Company: Title"
                const link = $(el).find('link').text();
                const descriptionHtml = $(el).find('description').text();
                const cleanText = cheerio.load(descriptionHtml)('body').text().replace(/\s+/g, ' ').trim();
                
                const lowerText = cleanText.toLowerCase() + " " + titleFull.toLowerCase();
                
                // Filter for our target keywords
                const isTarget = ['ai', 'principal', 'staff', 'architect', 'machine learning'].some(kw => lowerText.includes(kw));
                if (!isTarget) return;

                // Extract company and title
                let company = "WWR_Company";
                let title = titleFull;
                if (titleFull.includes(':')) {
                    const parts = titleFull.split(':');
                    company = parts[0].trim();
                    title = parts.slice(1).join(':').trim();
                }

                const safeCompany = company.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase();
                const safeTitle = title.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase().substring(0, 30);
                const filePath = path.join(STAGING_DIR, `WWR_${safeCompany}_${safeTitle}_${Date.now() + i}.md`);

                const content = `---
source: We Work Remotely
url: ${link}
company: "${company}"
title: "${title}"
date_scraped: ${new Date().toISOString()}
---

# ${title} at ${company}
**Link:** ${link}

## Job Description
${cleanText}
`;
                fs.writeFileSync(filePath, content);
                savedCount++;
            });
        } catch (error) {
            console.error(`[We Work Remotely] Error fetching ${feedUrl}:`, error.message);
        }
    }
    
    console.log(`[We Work Remotely] Done! Saved ${savedCount} high-level engineering jobs to staging.`);
}

run();
