const fs = require('fs');

function parseCSV(text) {
    let rows = [], row = [], inQuote = false, value = '';
    for (let i = 0; i < text.length; i++) {
        let ch = text[i];
        if (inQuote) {
            if (ch === '"') {
                if (i < text.length - 1 && text[i+1] === '"') { value += '"'; i++; }
                else { inQuote = false; }
            } else { value += ch; }
        } else {
            if (ch === '"') { inQuote = true; }
            else if (ch === ',') { row.push(value.trim()); value = ''; }
            else if (ch === '\n' || ch === '\r') {
                if (ch === '\r' && text[i+1] === '\n') i++; 
                row.push(value.trim()); rows.push(row); row = []; value = '';
            } else { value += ch; }
        }
    }
    if (value || row.length > 0) { row.push(value.trim()); rows.push(row); }
    
    const output = [];
    for (let i = 1; i < rows.length; i++) {
        const r = rows[i];
        if (r.length < 6 || !r[0]) continue;
        let desc = r[2] || '';
        let bullets = desc.includes('- ') ? desc.split('- ').map(s => s.trim()).filter(Boolean) : (desc ? [desc] : []);
        output.push({
            company: r[0].replace(/[\u200B-\u200D\uFEFF]/g, '').trim(), 
            title: r[1].replace(/[\u200B-\u200D\uFEFF]/g, '').trim(),
            dates: r[4] ? `${r[4]} - ${r[5] || 'Present'}` : 'Unknown',
            bullets: bullets.map(b => b.replace(/^[-•●\s\u200B]+/, '').trim()).filter(b => b && b !== 'Identified via input' && !b.startsWith('Turning data into decisions.'))
        });
    }
    return output;
}

function parseCV(text) {
    const output = [];
    const lines = text.split('\n');
    let currentRole = null;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;
        
        const companyMatch = line.match(/^([^:]+):\s*(.+)$/);
        if (companyMatch && i + 1 < lines.length && lines[i+1].match(/^\d{4}/)) {
            if (currentRole) output.push(currentRole);
            currentRole = {
                company: companyMatch[1].replace(/[\u200B-\u200D\uFEFF]/g, '').trim(),
                title: companyMatch[2].replace(/[\u200B-\u200D\uFEFF]/g, '').trim(),
                dates: lines[i+1].trim(),
                bullets: []
            };
            i++; 
            continue;
        }
        
        if (currentRole && (line.startsWith('●') || line.startsWith('•') || line.startsWith('-'))) {
            currentRole.bullets.push(line.replace(/^[-•●\s\u200B]+/, '').trim());
        } else if (currentRole && currentRole.bullets.length > 0 && !line.startsWith('Role:') && !line.startsWith('Accomplishments:') && !line.startsWith('Skills:')) {
            if (!line.match(/^[A-Z]/) || currentRole.bullets[currentRole.bullets.length - 1].endsWith(',')) {
                 currentRole.bullets[currentRole.bullets.length - 1] += ' ' + line.replace(/[\u200B-\u200D\uFEFF]/g, '');
            }
        }
    }
    if (currentRole) output.push(currentRole);
    return output;
}

function normalizeCompany(name) {
    return name.toLowerCase().replace(/the |company|co\.|inc\.|llc|international/g, '').trim();
}

function scoreDates(d) {
    if (!d || d === 'Unknown') return 0;
    let score = 0;
    if (d.match(/[a-zA-Z]/)) score += 10; 
    if (d.match(/\d{4}.*\d{4}/)) score += 5; 
    if (d.toLowerCase().includes('present')) score += 20; 
    return score;
}

function mergeRoles(rolesA, rolesB) {
    const merged = [];
    const usedB = new Set();
    
    for (const a of rolesA) {
        let matchB = null;
        let matchIdx = -1;
        const normA = normalizeCompany(a.company);
        
        for (let i = 0; i < rolesB.length; i++) {
            if (usedB.has(i)) continue;
            const normB = normalizeCompany(rolesB[i].company);
            if (normA.includes(normB) || normB.includes(normA)) {
                matchB = rolesB[i];
                matchIdx = i;
                break;
            }
        }
        
        if (matchB) {
            usedB.add(matchIdx);
            const mergedBullets = [...new Set([...a.bullets, ...matchB.bullets])].filter(b => b);
            if (mergedBullets.length === 0) mergedBullets.push("Identified via input");
            
            let bestDates = a.dates;
            if (scoreDates(matchB.dates) > scoreDates(a.dates)) {
                bestDates = matchB.dates;
            }
            
            merged.push({
                company: a.company.length > matchB.company.length ? a.company : matchB.company,
                title: a.title,
                dates: bestDates,
                bullets: mergedBullets
            });
        } else {
            if (a.bullets.length === 0) a.bullets.push("Identified via input");
            merged.push(a);
        }
    }
    
    for (let i = 0; i < rolesB.length; i++) {
        if (!usedB.has(i)) {
            const b = rolesB[i];
            if (b.bullets.length === 0) b.bullets.push("Identified via input");
            merged.push(b);
        }
    }
    
    return merged;
}

const csvPath = process.argv[2];
const cvPath = process.argv[3];
const rulesPath = process.argv[4];

const csvData = fs.existsSync(csvPath) ? parseCSV(fs.readFileSync(csvPath, 'utf8')) : [];
const cvData = fs.existsSync(cvPath) ? parseCV(fs.readFileSync(cvPath, 'utf8')) : [];
const rulesData = fs.existsSync(rulesPath) ? JSON.parse(fs.readFileSync(rulesPath, 'utf8')) : { injected_roles: [] };

let allRoles = mergeRoles(csvData, cvData);

if (rulesData.injected_roles) {
    allRoles = allRoles.concat(rulesData.injected_roles);
}

console.log(JSON.stringify(allRoles, null, 2));
