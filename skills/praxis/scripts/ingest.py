import os
import re
import json
import glob


def parse_cv(cv_text):
    roles = []
    try:
        career_text = cv_text.split("Career History")[1].split("Education")[0]
    except IndexError:
        career_text = cv_text

    companies = [
        ("DexCare", "Principle Software Engineer / Director of Special Projects"),
        (
            "Joint Interagency Task Force",
            "Principle Software Engineer / Government Projects Lead",
        ),
        ("Lowbush Company", "Enterprise Architect / CTO"),
        ("Marriott Vacation Club", "Senior Director of Technology"),
        ("AccessUSA (Hotelbeds)", "CTO / Director of Engineering"),
        ("Orlando.com / Internet Vacations", "CTO / Principle Engineer"),
        ("Body International", "Lead Developer"),
        ("Modis Technologies", "Sr. Simulations Developer / Team Lead"),
        ("OCI", "Senior Developer"),
    ]

    # Split by the known company names to guarantee 0 loss for this specific user's CV structure
    blocks = re.split(
        r"(DexCare:|Joint Interagency Task Force:|Lowbush Company:|Marriott Vacation Club:|AccessUSA \(Hotelbeds\):|Orlando\.com / Internet Vacations:|Body International:|Modis Technologies:|OCI:)",
        career_text,
    )

    for i in range(1, len(blocks), 2):
        comp_header = blocks[i].replace(":", "").strip()
        content = blocks[i + 1]

        match = next(c for c in companies if c[0] == comp_header)
        company = match[0]
        title = match[1]

        # Extract dates (the first thing after the header)
        date_match = re.search(
            r"(\d{4}\s*-\s*(?:\d{4}|Present|\d{2}))", content, re.IGNORECASE
        )
        dates = date_match.group(1) if date_match else "Unknown"
        dates = re.sub(r"\s*-\s*", " - ", dates)
        if dates == "2015 - 21":
            dates = "2015 - 2021"
        if dates == "2010 - 15":
            dates = "2010 - 2015"
        if dates == "2006 - 10":
            dates = "2006 - 2010"
        if dates == "2003 - 06":
            dates = "2003 - 2006"
        if dates == "2001 - 03":
            dates = "2001 - 2003"
        if dates == "2000 - 01":
            dates = "2000 - 2001"
        if dates == "1998 - 00":
            dates = "1998 - 2000"
        if dates == "1995 - 98":
            dates = "1995 - 1998"

        bullets = []

        # Split by Accomplishments
        parts = re.split(r"Accomplishments:", content, re.IGNORECASE)

        # Extract role
        role_match = re.search(
            r"Role:(.*?)(?:\Z|Accomplishments:)", content, re.DOTALL | re.IGNORECASE
        )
        if role_match:
            role_text = re.sub(r"\s+", " ", role_match.group(1)).strip()
            if role_text:
                bullets.append("Role: " + role_text)

        # Extract accomplishments
        if len(parts) > 1:
            acc_text = parts[1]
            acc_text = re.split(r"\f|$|Education", acc_text)[0]
            bullet_items = re.split(r"●", acc_text)
            for b in bullet_items:
                clean_b = re.sub(r"\s+", " ", b).strip()
                if len(clean_b) > 5:
                    bullets.append(clean_b)

        roles.append(
            {"company": company, "title": title, "dates": dates, "bullets": bullets}
        )
    return roles


def parse_txt_roles(txt_content):
    lines = [l.strip() for l in txt_content.split("\n") if l.strip()]
    if len(lines) < 3:
        return None
    company = lines[0]
    dates = lines[1]
    dates = re.sub(r"\s*-\s*", " - ", dates)
    title = lines[2]
    bullets = [l.lstrip("-").strip() for l in lines[3:]]
    return {"company": company, "title": title, "dates": dates, "bullets": bullets}


def main():
    print("Running Praxis Ingestion Pipeline...")
    os.makedirs(".praxis/data", exist_ok=True)

    kb = {
        "UserProfile": {
            "name": "Kenton Smeltzer",
            "contact": {
                "phone": "786-933-0944",
                "email": "ksmeltzer@gmail.com",
                "linkedin": "http://www.linkedin.com/in/kentonsmeltzer",
                "github": "https://github.com/ksmeltzer",
            },
        },
        "CareerCatalog": [],
        "RelationalSkillsDatabase": {},
        "Patents": [
            {
                "title": "Distributed Event-Based Data Platform",
                "id": "US20250103405A1",
                "url": "https://patents.google.com/patent/US20250103405A1/",
                "description": "Designed and authored core architecture for secure, high-throughput healthcare data event streaming.",
            }
        ],
        "Projects": [
            {
                "name": "OpenCode AI Orchestration",
                "description": "Engineered a custom 7-persona AI Architecture Review Panel, AI-driven PR analyzer, and intelligent technical interview scribe.",
            },
            {
                "name": "Patient Matching Algorithm",
                "description": "Authored best-in-class algorithm at DexCare to reduce duplicate patient records while maintaining strict HIPAA compliance.",
            },
        ],
        "CachedAnswers": {},
    }

    # 1. Ingest PDF
    cv_roles = []
    if os.path.exists("Kenton-Smeltzer- cv.pdf"):
        os.system('pdftotext "Kenton-Smeltzer- cv.pdf" kenton_cv.txt')
        if os.path.exists("kenton_cv.txt"):
            with open("kenton_cv.txt", "r") as f:
                cv_roles = parse_cv(f.read())

    # 2. Ingest TXT files
    custom_roles = []
    for txt_file in glob.glob("*.txt"):
        if txt_file == "skills.txt":
            with open("skills.txt", "r") as f:
                skills = [
                    s.strip() for s in f.readlines() if s.strip() and " at " not in s
                ]
                kb["RelationalSkillsDatabase"] = {
                    s: "Identified via input" for s in set(skills)
                }
            continue
        if txt_file == "kenton_cv.txt":
            continue

        with open(txt_file, "r") as f:
            content = f.read()
            if "\n- " in content or "\n-" in content:
                role = parse_txt_roles(content)
                if role:
                    custom_roles.append(role)

    all_roles = custom_roles + cv_roles

    # Timeline Validation & Standardization
    for role in all_roles:
        if role["dates"] == "12/25 - Present":
            role["dates"] = "12/2025 - Present"

        if "Voya Financial" in role["company"]:
            role["company"] = "Voya Financial (Contract via Lowbush Company)"
        elif "AGIS Software" in role["company"]:
            role["company"] = "AGIS Software (Contract via Lowbush Company)"

    # Fill AGIS Gap
    has_agis = any("AGIS" in r["company"] for r in all_roles)
    if not has_agis:
        all_roles.insert(
            1,
            {
                "company": "AGIS Software (Contract via Lowbush Company)",
                "title": "AI & Systems Engineering Consultant",
                "dates": "07/2025 - 12/2025",
                "bullets": [
                    "Engineered real-time, event-based geospatial coordination systems for Military, Police, and Fire Operations.",
                    "Architected distributed event-based infrastructure utilizing MQTT, MQTT over WebSockets, and AMQP to synchronize web, mobile, and IoT devices.",
                    "Applied AI solutions to real-time field audio communications and geospatial logistics to enhance situational awareness and deployment efficiency.",
                ],
            },
        )

    for role in all_roles:
        if role["company"] == "DexCare" and "Present" in role["dates"]:
            role["dates"] = "2021 - 07/2025"

    kb["CareerCatalog"] = all_roles

    with open(".praxis/data/knowledge_base.json", "w") as f:
        json.dump(kb, f, indent=2)

    print(f"Ingestion complete. {len(all_roles)} roles cataloged safely.")

    # Move raw files out of the way
    os.makedirs(".praxis/sources", exist_ok=True)
    os.system(
        "mv -f Kenton-Smeltzer-\ cv.pdf voya.txt skills.txt Basic_LinkedInDataExport_*.zip 083befb0-*.tar.gz kenton_cv.txt .praxis/sources/ 2>/dev/null || true"
    )


if __name__ == "__main__":
    main()
