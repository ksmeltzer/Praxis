const fs = require('fs');
const text = fs.readFileSync(process.argv[2], 'utf8');
const type = process.argv[3];

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

if (type === 'positions') {
    const output = [];
    for (let i = 1; i < rows.length; i++) {
        const r = rows[i];
        if (r.length < 6 || !r[0]) continue;
        let desc = r[2] || '';
        let bullets = desc.includes('- ') ? desc.split('- ').map(s => s.trim()).filter(Boolean) : (desc ? [desc] : []);
        output.push({
            company: r[0], 
            title: r[1],
            dates: r[4] ? `${r[4]} - ${r[5] || 'Present'}` : 'Unknown',
            bullets: bullets.length ? bullets : ["Identified via input"]
        });
    }
    console.log(JSON.stringify(output, null, 2));
} else if (type === 'skills') {
    const output = {};
    for (let i = 1; i < rows.length; i++) {
        if (rows[i][0]) output[rows[i][0]] = ["Identified via LinkedIn"];
    }
    console.log(JSON.stringify(output, null, 2));
} else if (type === 'profile') {
    if (rows.length > 1 && rows[1].length >= 7) {
        console.log(JSON.stringify({ headline: rows[1][5] || '', summary: rows[1][6] || '' }));
    } else {
        console.log(JSON.stringify({ headline: '', summary: '' }));
    }
}
