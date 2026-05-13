const fs = require('fs');
const path = require('path');

const APPLICATIONS_PATH = path.join(__dirname, '../../.praxis/data/applications.json');

function normalize(text) {
    if (!text) return '';
    return text.toLowerCase().replace(/[^a-z0-9]/g, '');
}

function getAppliedJobs() {
    if (!fs.existsSync(APPLICATIONS_PATH)) return [];
    try {
        const data = JSON.parse(fs.readFileSync(APPLICATIONS_PATH, 'utf8'));
        return data.applications || [];
    } catch (e) {
        return [];
    }
}

function isDuplicate(company, title) {
    const applied = getAppliedJobs();
    const normCompany = normalize(company);
    const normTitle = normalize(title);
    
    for (const app of applied) {
        const appComp = normalize(app.company);
        const appTitle = normalize(app.role);
        
        // If company matches exactly, and title is a very close substring match
        if (normCompany && appComp && (normCompany.includes(appComp) || appComp.includes(normCompany))) {
            if (normTitle && appTitle && (normTitle.includes(appTitle) || appTitle.includes(normTitle))) {
                return true;
            }
        }
    }
    return false;
}

module.exports = { isDuplicate };
