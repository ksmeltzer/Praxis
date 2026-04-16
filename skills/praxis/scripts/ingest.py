import os
import re
import json
import glob
import urllib.request
import urllib.error

RULES_FILE = os.path.join(os.path.dirname(__file__), "rules.json")


def load_rules():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r") as f:
            return json.load(f)
    return {}


def normalize_whitespace(text):
    return re.sub(r"\s+", "", text).lower()


def verify_facts(roles, raw_text):
    """
    Deterministic Fact Verification (Anti-Hallucination Layer)
    Ensures every extracted bullet point actually exists in the raw text.
    """
    normalized_raw = normalize_whitespace(raw_text)
    verified_roles = []

    dropped_facts = 0
    for role in roles:
        verified_bullets = []
        for bullet in role.get("bullets", []):
            # Check if bullet exists in the raw text
            normalized_bullet = normalize_whitespace(bullet)
            # LLMs sometimes summarize, but we demand an exact substring match
            # To be slightly forgiving with formatting, we strip all whitespace before comparing
            if normalized_bullet in normalized_raw:
                verified_bullets.append(bullet)
            else:
                dropped_facts += 1
                print(
                    f"[Verification] Dropped hallucinated/modified fact: {bullet[:50]}..."
                )

        role["bullets"] = verified_bullets
        verified_roles.append(role)

    if dropped_facts > 0:
        print(
            f"[Verification] Dropped {dropped_facts} unverified facts to prevent hallucination."
        )

    return verified_roles


def llm_extraction(cv_text, api_key):
    """
    Extracts roles using an LLM configured for strict JSON schema output.
    """
    print("[Extraction] Attempting LLM Extraction...")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    schema = {
        "type": "object",
        "properties": {
            "roles": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "company": {"type": "string"},
                        "title": {"type": "string"},
                        "dates": {"type": "string"},
                        "bullets": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["company", "title", "dates", "bullets"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["roles"],
        "additionalProperties": False,
    }

    prompt = (
        "Extract all career roles from the following resume text. "
        "Do NOT summarize, invent, or rewrite facts. Extract bullet points verbatim as they appear. "
        f"Resume text:\n{cv_text}"
    )

    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a precise data extraction agent. Output valid JSON only according to the schema.",
            },
            {"role": "user", "content": prompt},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "career_extraction",
                "schema": schema,
                "strict": True,
            },
        },
        "temperature": 0.0,
    }

    try:
        req = urllib.request.Request(
            url, data=json.dumps(data).encode("utf-8"), headers=headers
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            parsed_json = json.loads(result["choices"][0]["message"]["content"])
            return parsed_json.get("roles", [])
    except Exception as e:
        print(f"[Extraction] LLM extraction failed: {e}")
        return None


def fallback_extraction(cv_text, rules):
    """
    Deterministic fallback parser using known companies if LLM is unavailable.
    """
    print("[Extraction] Using deterministic fallback parser...")
    roles = []
    try:
        career_text = cv_text.split("Career History")[1].split("Education")[0]
    except IndexError:
        career_text = cv_text

    known_companies = rules.get("known_companies", [])
    if not known_companies:
        return roles

    # Create regex from known companies
    split_pattern = (
        r"(" + "|".join([re.escape(c["match"]) + ":" for c in known_companies]) + r")"
    )
    blocks = re.split(split_pattern, career_text)

    for i in range(1, len(blocks), 2):
        comp_header = blocks[i].replace(":", "").strip()
        content = blocks[i + 1]

        try:
            match = next(c for c in known_companies if c["match"] == comp_header)
        except StopIteration:
            continue

        company = match["match"]
        title = match.get("title", "")

        # Extract dates
        date_match = re.search(
            r"(\d{4}\s*-\s*(?:\d{4}|Present|\d{2}))", content, re.IGNORECASE
        )
        dates = date_match.group(1) if date_match else "Unknown"

        bullets = []
        parts = re.split(r"Accomplishments:", content, re.IGNORECASE)

        # Extract role summary
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
    title = lines[2]
    bullets = [l.lstrip("-").strip() for l in lines[3:]]
    return {"company": company, "title": title, "dates": dates, "bullets": bullets}


def normalize_roles(roles, rules):
    """
    Applies declarative normalizations from rules.json
    """
    date_reps = rules.get("date_replacements", {})
    comp_reps = rules.get("company_replacements", {})
    date_ovrs = rules.get("date_overrides", {})

    for role in roles:
        # Date replacements
        d = re.sub(r"\s*-\s*", " - ", role.get("dates", ""))
        for old_val, new_val in date_reps.items():
            if d == old_val:
                d = new_val
        role["dates"] = d

        # Company replacements
        c = role.get("company", "")
        for old_val, new_val in comp_reps.items():
            if old_val in c:
                role["company"] = new_val

        # Date overrides based on company
        comp = role.get("company", "")
        for override_comp, override_rules in date_ovrs.items():
            if override_comp in comp and override_rules["match"] in role["dates"]:
                role["dates"] = override_rules["replace_with"]

    # Inject roles if not present
    for inj_role in rules.get("injected_roles", []):
        has_role = any(inj_role["company"] in r["company"] for r in roles)
        if not has_role:
            roles.insert(
                1, inj_role
            )  # Typically inserting at index 1 based on chronological needs

    return roles


def main():
    print("Running Praxis Ingestion Pipeline...")
    os.makedirs(".praxis/data", exist_ok=True)

    rules = load_rules()

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
        "Projects": [],
        "CachedAnswers": {},
    }

    # 1. Ingest PDF
    cv_roles = []
    raw_cv_text = ""
    if os.path.exists("Kenton-Smeltzer- cv.pdf"):
        os.system('pdftotext "Kenton-Smeltzer- cv.pdf" kenton_cv.txt')
        if os.path.exists("kenton_cv.txt"):
            with open("kenton_cv.txt", "r") as f:
                raw_cv_text = f.read()

    if raw_cv_text:
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            extracted = llm_extraction(raw_cv_text, api_key)
            if extracted:
                # Anti-hallucination layer
                cv_roles = verify_facts(extracted, raw_cv_text)
            else:
                cv_roles = fallback_extraction(raw_cv_text, rules)
        else:
            print(
                "[Extraction] No OPENAI_API_KEY found in environment. Skipping LLM extraction."
            )
            cv_roles = fallback_extraction(raw_cv_text, rules)

    # 2. Ingest TXT files
    custom_roles = []
    for txt_file in glob.glob("*.txt"):
        if txt_file == "skills.txt":
            with open("skills.txt", "r") as f:
                skills = [
                    s.strip() for s in f.readlines() if s.strip() and " at " not in s
                ]
                kb["RelationalSkillsDatabase"] = {
                    s: ["Identified via input"] for s in set(skills)
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

    # 3. Apply Externalized Normalization Rules
    all_roles = normalize_roles(all_roles, rules)

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
