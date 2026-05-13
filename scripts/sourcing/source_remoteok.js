const fs = require('fs');
const path = require('path');
const https = require('https');

const STAGING_DIR = path.join(__dirname, '../../.praxis/staging');
const PARAMS_PATH = path.join(__dirname, '../../.praxis/data/search_parameters.json');

// Ensure staging directory exists
if (!fs.existsSync(STAGING_DIR)) {
  fs.mkdirSync(STAGING_DIR, { recursive: true });
}

// Load params
let searchParams;
try {
  searchParams = JSON.parse(fs.readFileSync(PARAMS_PATH, 'utf8'));
} catch (error) {
  console.error('[RemoteOK] Error reading search parameters:', error.message);
  process.exit(1);
}

const minSalaryThreshold = searchParams.filters?.w2_min_base_salary_usd || 240000;
const dealbreakers = searchParams.filters?.dealbreakers?.title_keywords || [];
const targetRoles = searchParams.filters?.target_roles || [];

function matchesDealbreakers(text) {
  const lowerText = text.toLowerCase();
  return dealbreakers.some(db => lowerText.includes(db.toLowerCase()));
}

function matchesTargetRoles(title) {
  if (targetRoles.length === 0) return true;
  const lowerTitle = title.toLowerCase();
  return targetRoles.some(role => lowerTitle.includes(role.toLowerCase()));
}

async function fetchJobs() {
  console.log('[RemoteOK] Fetching remote jobs from RemoteOK API...');
  
  try {
    const response = await fetch('https://remoteok.com/api', {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    // The first element is often a legal notice
    const jobs = data.filter(item => item.id && item.company);
    console.log(`[RemoteOK] Found ${jobs.length} total jobs in feed.`);
    
    let savedCount = 0;
    
    for (const job of jobs) {
      const title = job.position || '';
      const company = job.company || 'Unknown';
      const description = job.description || '';
      const salaryMax = job.salary_max || 0;
      
      // 1. Check dealbreakers
      if (matchesDealbreakers(title)) continue;
      
      // 2. Check target roles
      if (!matchesTargetRoles(title)) continue;
      
      // 3. Salary Check (If provided and strictly below our minimum, skip)
      // RemoteOK provides salary_max. If salaryMax is > 0 and less than our threshold, skip.
      if (salaryMax > 0 && salaryMax < minSalaryThreshold) continue;
      
      // Format markdown
      const dateScraped = new Date().toISOString();
      const filename = `RemoteOK_${company.replace(/[^a-z0-9]/gi, '_')}_${title.replace(/[^a-z0-9]/gi, '_')}_${Date.now()}.md`;
      const filePath = path.join(STAGING_DIR, filename);
      
      const markdown = `---
source: RemoteOK
url: ${job.apply_url || job.url}
company: ${company}
title: ${title}
date_scraped: ${dateScraped}
salary_max: ${salaryMax}
---

## Job Description

${description}
`;
      fs.writeFileSync(filePath, markdown, 'utf8');
      savedCount++;
    }
    
    console.log(`[RemoteOK] Saved ${savedCount} relevant jobs to staging.`);
    
  } catch (error) {
    console.error('[RemoteOK] Error fetching jobs:', error.message);
  }
}

fetchJobs();
