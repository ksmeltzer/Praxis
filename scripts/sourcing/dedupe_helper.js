const fs = require('fs');
const path = require('path');

const APPLICATIONS_PATH = path.join(__dirname, '../../.praxis/data/applications.json');
const SEEN_JOBS_PATH = path.join(__dirname, '../../.praxis/data/seen_jobs.json');

function normalize(text) {
    if (!text) return '';
    return text.toLowerCase().replace(/[^a-z0-9]/g, '');
}

function getJsonArray(filePath, rootKey) {
    if (!fs.existsSync(filePath)) return [];
    try {
        const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        return rootKey ? (data[rootKey] || []) : (Array.isArray(data) ? data : []);
    } catch (e) {
        return [];
    }
}

function saveJsonArray(filePath, data, rootKey) {
    if (rootKey) {
        fs.writeFileSync(filePath, JSON.stringify({ [rootKey]: data }, null, 2));
    } else {
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
    }
}

function hasBeenSeenOrApplied(company, title) {
    if (!company || !title) return false;
    const normCompany = normalize(company);
    const normTitle = normalize(title);
    
    // 1. Check if we already applied
    const applied = getJsonArray(APPLICATIONS_PATH, 'applications');
    for (const app of applied) {
        const appComp = normalize(app.company);
        const appTitle = normalize(app.role);
        if (normCompany && appComp && (normCompany.includes(appComp) || appComp.includes(normCompany))) {
            if (normTitle && appTitle && (normTitle.includes(appTitle) || appTitle.includes(normTitle))) {
                return true; // Already applied
            }
        }
    }
    
    // 2. Check if we already evaluated/seen it (passed or rejected)
    const seen = getJsonArray(SEEN_JOBS_PATH);
    for (const s of seen) {
        const sComp = normalize(s.company);
        const sTitle = normalize(s.title);
        if (normCompany && sComp && (normCompany.includes(sComp) || sComp.includes(normCompany))) {
            if (normTitle && sTitle && (normTitle.includes(sTitle) || sTitle.includes(normTitle))) {
                return true; // Already seen and scored
            }
        }
    }
    return false;
}

function markAsSeen(company, title, status) {
    if (!company || !title) return;
    const seen = getJsonArray(SEEN_JOBS_PATH);
    
    // Only add if not already in the array to prevent bloat
    const normCompany = normalize(company);
    const normTitle = normalize(title);
    const exists = seen.some(s => 
        normalize(s.company) === normCompany && normalize(s.title) === normTitle
    );
    
    if (!exists) {
        seen.push({
            company: company,
            title: title,
            status: status,
            date: new Date().toISOString()
        });
        saveJsonArray(SEEN_JOBS_PATH, seen);
    }
}

module.exports = { hasBeenSeenOrApplied, markAsSeen };
