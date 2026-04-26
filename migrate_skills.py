import json
import re

# Load the current knowledge base (with our manual corrections and rules)
with open(".praxis/data/knowledge_base.json", "r") as f:
    kb = json.load(f)

# Read the raw skills file that we lost during the old ingest
with open(".praxis/sources/skills.txt", "r") as f:
    raw_skills_lines = f.read().splitlines()

# Parse the skills.txt file
current_skill = None
skills_mapping = {}

for line in raw_skills_lines:
    line = line.strip()
    if not line:
        continue
    if "at " in line and current_skill:
        # e.g., "Solutions Design Consultant (Contractor) at Voya Financial"
        company = line.split("at ")[-1].strip()
        if company not in skills_mapping:
            skills_mapping[company] = []
        skills_mapping[company].append(current_skill)
    elif "experience" in line and "at " in line:
        # e.g., "2 experiences at DexCare and 1 other company"
        company = line.split("at ")[-1].split(" and ")[0].strip()
        if company not in skills_mapping:
            skills_mapping[company] = []
        if current_skill:
            skills_mapping[company].append(current_skill)
    else:
        # It's a skill name
        if line not in ["Show all 4 details", "Passed LinkedIn Skill Assessment"]:
            current_skill = line
            # Also add to a general pool
            if "General" not in skills_mapping:
                skills_mapping["General"] = []
            skills_mapping["General"].append(current_skill)

# Mapping logic to our KB companies
company_map = {
    "Voya Financial": "Voya Financial (Contract via Lowbush Company)",
    "DexCare": "DexCare",
    "Joint Interagency Task Force South": "Joint Interagency Task Force",
    "Lowbush Company": "Lowbush Company",
    "Marriott Vacation Club": "Marriott Vacation Club",
    "AccessUSA": "AccessUSA (Hotelbeds)",
    "Orlando.com": "Orlando.com",
}

# Update the KB
for exp in kb.get("experience", []):
    exp_company = exp.get("company", "")
    skills_used = set(exp.get("skills_used", []))

    # 1. Pull from the parsed skills.txt mapping
    for raw_comp, mapped_comp in company_map.items():
        if mapped_comp == exp_company and raw_comp in skills_mapping:
            skills_used.update(skills_mapping[raw_comp])

    # 2. Extract explicitly mentioned keywords in the bullet text to ensure 100% coverage
    text = (
        " ".join(exp.get("bullets", []))
        + " "
        + exp.get("title", "")
        + " "
        + exp.get("company", "")
    )
    general_skills = skills_mapping.get("General", [])

    # Add common tech acronyms that might be in text but missed
    extra_tech = [
        "AWS",
        "Azure",
        "GCP",
        "Docker",
        "REST",
        "JAX-RS",
        "FoxPro",
        "OpenGL",
        "SOC 2",
        "HIPAA",
        "PII",
        "Node.js",
        "Python",
        "Golang",
        "Java",
        "C++",
        "JavaScript",
        "Clojure",
        "React",
        "Angular",
        "Dojo",
        "Backbone.js",
        "Require.js",
        "Kubernetes",
        "RabbitMQ",
        "Postgres",
        "WebSphere",
        "MSSQL",
        "Oracle",
        "MQTT",
        "AMQP",
        "OPA",
        "Databricks",
        "Node-RED",
        "n8n",
        "GraphQL",
        "Microservices",
    ]

    for s in general_skills + extra_tech:
        # Use regex for word boundaries so "Java" doesn't match inside "JavaScript"
        # Escape the skill for regex, handling special chars like C++
        escaped_s = re.escape(s)
        if re.search(r"\b" + escaped_s + r"\b", text, re.IGNORECASE):
            skills_used.add(s)

    exp["skills_used"] = sorted(list(skills_used))

# Ensure the global skills object has all these
global_skills = set()
for cat in kb.get("skills", {}).values():
    global_skills.update(cat)

for exp in kb.get("experience", []):
    for s in exp.get("skills_used", []):
        if s not in global_skills:
            # Drop unmapped skills into a new bucket for now so we don't lose them
            if "Other Tools & Concepts" not in kb["skills"]:
                kb["skills"]["Other Tools & Concepts"] = []
            if s not in kb["skills"]["Other Tools & Concepts"]:
                kb["skills"]["Other Tools & Concepts"].append(s)
                global_skills.add(s)

# Save the updated KB
with open(".praxis/data/knowledge_base.json", "w") as f:
    json.dump(kb, f, indent=2)

print("Migration Complete.")
