const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { parse } = require('node:querystring');

const STAGING_DIR = path.join(__dirname, '../../.praxis/staging');

if (!fs.existsSync(STAGING_DIR)) {
    fs.mkdirSync(STAGING_DIR, { recursive: true });
}

async function run() {
    console.log("[Hacker News] Looking for the latest 'Ask HN: Who is hiring?' thread...");
    try {
        // 1. Find the latest "Who is hiring?" thread
        const searchRes = await axios.get('https://hn.algolia.com/api/v1/search', {
            params: {
                query: 'Ask HN: Who is hiring?',
                tags: 'story',
                restrictSearchableAttributes: 'title',
                hitsPerPage: 1
            }
        });

        if (!searchRes.data.hits || searchRes.data.hits.length === 0) {
            console.log("[Hacker News] Could not find the thread.");
            return;
        }

        const threadId = searchRes.data.hits[0].objectID;
        const threadTitle = searchRes.data.hits[0].title;
        console.log(`[Hacker News] Found thread: ${threadTitle} (ID: ${threadId})`);

        // 2. Fetch the thread comments
        console.log(`[Hacker News] Fetching comments for thread...`);
        const itemRes = await axios.get(`https://hn.algolia.com/api/v1/items/${threadId}`);
        const comments = itemRes.data.children || [];
        
        let savedCount = 0;

        // 3. Filter comments for Remote + (AI | Principal | Staff | Architect | Machine Learning)
        for (const comment of comments) {
            if (!comment.text) continue;
            
            const text = comment.text.toLowerCase();
            
            // Must be remote
            if (!text.includes('remote')) continue;
            
            // Must contain our target keywords
            const isTarget = ['ai', 'artificial intelligence', 'machine learning', 'principal', 'staff', 'architect'].some(kw => text.includes(kw));
            if (!isTarget) continue;

            // Optional: Try to extract a company name from the first line
            const firstLine = comment.text.split('<p>')[0].replace(/<[^>]+>/g, '').trim();
            const companyMatch = firstLine.split('|')[0].trim();
            const company = companyMatch ? companyMatch.substring(0, 30).replace(/[^a-zA-Z0-9 ]/g, '') : "HN_Company";

            const safeCompany = company.replace(/\s+/g, '_').toLowerCase();
            const filePath = path.join(STAGING_DIR, `HN_${safeCompany}_${comment.id}.md`);
            
            // Strip HTML from text for the markdown file
            const cleanText = comment.text.replace(/<p>/g, '\n\n').replace(/<[^>]+>/g, '');

            const content = `---
source: Hacker News
url: https://news.ycombinator.com/item?id=${comment.id}
company: "${companyMatch}"
title: "HN Comment (Extracted)"
date_scraped: ${new Date().toISOString()}
---

# Hacker News Job Posting: ${companyMatch}
**Link:** https://news.ycombinator.com/item?id=${comment.id}

## Job Description
${cleanText}
`;
            fs.writeFileSync(filePath, content);
            savedCount++;
        }
        
        console.log(`[Hacker News] Done! Saved ${savedCount} heavily technical remote jobs to staging.`);
    } catch (error) {
        console.error("[Hacker News] Error:", error.message);
    }
}

run();
