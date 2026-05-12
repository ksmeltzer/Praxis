require("dotenv").config();
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

let BRAVE_API_KEY = process.env.BRAVE_API_KEY;
try {
    // Attempt to pull from system keyring if secret-tool is installed
    const keyringKey = execSync('secret-tool lookup service praxis account brave_api', { stdio: 'pipe' }).toString().trim();
    if (keyringKey) {
        BRAVE_API_KEY = keyringKey;
        console.log("[Praxis Sourcing] Loaded API key from system keyring.");
    }
} catch (e) {
    // Fallback to .env quietly if secret-tool fails or isn't installed
}

const STAGING_DIR = path.join(__dirname, '../../.praxis/staging');

if (!fs.existsSync(STAGING_DIR)) {
    fs.mkdirSync(STAGING_DIR, { recursive: true });
}

// Queries designed to hit the major open ATS platforms for high-level AI/SWE roles
const QUERIES = [
    'site:boards.greenhouse.io ("Principal Software" OR "Staff Software" OR "Principal AI" OR "Staff AI") "Remote"',
    'site:jobs.lever.co ("Principal Software" OR "Staff Software" OR "Principal AI" OR "Staff AI") "Remote"',
    'site:jobs.ashbyhq.com ("Principal Software" OR "Staff Software" OR "Principal AI" OR "Staff AI") "Remote"'
];

async function fetchBraveResults(query) {
    console.log(`[Brave API] Searching: ${query}`);
    try {
        const response = await axios.get('https://api.search.brave.com/res/v1/web/search', {
            params: {
                q: query,
                count: 10,
                freshness: 'pw'
            },
            headers: {
                'Accept': 'application/json',
                'X-Subscription-Token': BRAVE_API_KEY
            }
        });
        
        return response.data.web?.results || [];
    } catch (error) {
        console.error(`[Brave API] Error fetching query "${query}":`, error.response?.data || error.message);
        return [];
    }
}

async function scrapeJobPage(url, title, company) {
    console.log(`[Scraper] Fetching content for: ${company} - ${title}`);
    try {
        const { data } = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        });
        
        const $ = cheerio.load(data);
        let description = '';

        if (url.includes('greenhouse.io')) {
            description = $('#content').text() || $('body').text();
        } else if (url.includes('lever.co')) {
            description = $('.content-wrapper').text() || $('body').text();
        } else if (url.includes('ashbyhq.com')) {
            description = $('.ashby-job-posting-content').text() || $('body').text();
        } else {
            description = $('body').text();
        }

        description = description.replace(/\s+/g, ' ').trim();

        const safeCompany = (company || 'Unknown').replace(/[^a-z0-9]/gi, '_').toLowerCase();
        const safeTitle = (title || 'Unknown').replace(/[^a-z0-9]/gi, '_').toLowerCase();
        const filePath = path.join(STAGING_DIR, `${safeCompany}_${safeTitle}_${Date.now()}.md`);
        
        const content = `---
source: Brave ATS Hunter
url: ${url}
company: ${company}
title: ${title}
date_scraped: ${new Date().toISOString()}
---

# ${title} at ${company}
**Link:** ${url}

## Job Description
${description}
`;
        fs.writeFileSync(filePath, content);
        console.log(`[Scraper] Saved to ${filePath}`);
    } catch (error) {
        console.error(`[Scraper] Failed to scrape ${url}:`, error.message);
    }
}

async function run() {
    if (!BRAVE_API_KEY) {
        console.error("FATAL: BRAVE_API_KEY environment variable or keyring entry is not set.");
        process.exit(1);
    }

    console.log("Starting Praxis Brave ATS Hunter...");
    
    for (const query of QUERIES) {
        const results = await fetchBraveResults(query);
        
        // Critical: Sleep for 1.5 seconds between Brave API queries to avoid 429 Rate Limits
        await sleep(1500);

        for (const result of results) {
            let company = result.profile?.name || "Unknown Company";
            let title = result.title || "Unknown Role";
            
            title = title.replace(/ - Greenhouse/i, '').replace(/ - Lever/i, '').replace(/ - Ashby/i, '').trim();
            
            await scrapeJobPage(result.url, title, company);
            
            // Sleep for 1.5 seconds between direct website hits to be polite
            await sleep(1500);
        }
    }
    
    console.log("Done! Jobs are waiting in .praxis/staging/ for LLM scoring.");
}

run();
