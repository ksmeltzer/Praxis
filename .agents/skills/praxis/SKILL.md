---
name: praxis
description: "Adversarial, Multi-Agent Career Knowledge Base & Resume Pipeline. Usage: /praxis init (setup), /praxis (ingest), /praxis <text> (update), /praxis <url> (forge), /praxis search (source)"
trigger: /praxis
---
# Praxis Skill

This skill implements the orchestrator logic for the Praxis adversarial resume builder.

## Architecture & File Structure
- **Root Directory**: Kept clean. All generated output files (`Resume.md`, `LinkedIn_Profile.md`, `*_Resume.pdf`) are saved into the `assets/` folder. Targeted resumes are organized into company-specific subdirectories (e.g., `assets/{CompanyName}/`).
- **`.tmp/`**: Any one-off utility scripts, agent experiments, or temporary data processing scripts MUST be created and executed inside the `.tmp/` directory, which is excluded from source control. NEVER create scripts in the project root.
- **`.praxis/sources/`**: All raw input files (resumes, LinkedIn CSVs) are moved here immediately after parsing.
- **`.praxis/data/`**: Contains the exhaustive, non-lossy backend database (`knowledge_base.json`).
- **`.praxis/backups/`**: Automatically generated timestamped backups of `knowledge_base.json` before any destructive or generative changes are applied.

**CRITICAL DATA SAFETY RULE**: Before executing ANY operation that writes or modifies `.praxis/data/knowledge_base.json` (such as Mode 1 Ingest, Mode 2 Knowledge Update, or appending missing skills in Mode 3 Forge), the Orchestrator MUST use the `bash` tool to create an immutable backup copy (e.g., `cp .praxis/data/knowledge_base.json .praxis/backups/knowledge_base_$(date +%s).json`). Failure to backup the user's curated data before a modification is a critical architectural violation.

## Knowledge Base Schema (`knowledge_base.json`)

The LLM MUST produce JSON conforming to this exact schema. The generating agents depend on these key names.

```json
{
  "basics": {
    "name": "string",
    "phone": "string",
    "email": "string",
    "linkedin": "string",
    "github": "string (legacy)",
    "portfolio_links": [{"name": "string (e.g. GitHub, Cognilogical, Personal Site)", "url": "string"}],
    "headline": "string",
    "summary": "string",
    "location": "string",
    "birth_date": "string (optional)",
    "languages": [{ "name": "string", "proficiency": "string" }]
  },
  "voice_profile": {
    "perspective": "string (e.g. 'implied first-person — drops the I, leads with verbs')",
    "tone": "string (e.g. 'direct, confident, technical-but-accessible')",
    "sentence_structure": "string (e.g. 'compound sentences, heavy use of semicolons to pack parallel ideas')",
    "vocabulary_tendencies": ["string — recurring words/phrases the applicant naturally gravitates toward"],
    "avoidances": ["string — patterns the applicant never uses"],
    "sample_fragments": ["string — 3-5 verbatim excerpts that best exemplify their natural voice"]
  },
  "generation_rules": [
    "string — persistent rules/directives for the drafter to follow (e.g., 'Never call Node.js a language')"
  ],
  "experience": [
    {
      "company": "string",
      "title": "string",
      "dates": "string (e.g. '2021 - 07/2025' or '12/2025 - Present')",
      "location": "string | null",
      "skills_used": ["string — exhaustive list of all technologies/skills used in this specific role"],
      "bullets": ["string — the exhaustive fact pool for this role"]
    }
  ],
  "education": [
    {
      "school": "string",
      "degree": "string (e.g. Bachelors of Science)",
      "major": "string",
      "minor": "string (optional)",
      "dates": "string (e.g. '1999 - 2006')"
    }
  ],
  "certifications": [
    {
      "name": "string",
      "issuer": "string"
    }
  ],
  "patents": [
    {
      "title": "string",
      "description": "string",
      "url": "string (optional)",
      "issuer": "string (e.g. patent number)",
      "issued_on": "string (optional)"
    }
  ],
  "distinctions": [
    {
      "title": "string — short description of the achievement",
      "source": "string — which company/role/recommendation this was extracted from"
    }
  ],
  "skills": {
    "Category Name": ["string — skill names within this category"]
  },
  "industry_expertise": {
    "Category Name": ["string — domain skills within this industry (e.g. Travel & Hospitality)"]
  },
  "projects": [
    {
      "name": "string",
      "description": "string",
      "url": "string",
      "dates": "string (optional)",
      "releases": ["string (optional)"],
      "language": "string (optional, added by github_sync)",
      "stars": "number (optional, added by github_sync)"
    }
  ],
  "recommendations": [
    {
      "from": "string",
      "title": "string",
      "text": "string"
    }
  ]
}
```

**Key rules for LLM parsing:**
- `experience[].bullets` is the exhaustive "fact pool". Merge bullets from ALL sources (PDF resume, LinkedIn positions, text files). Prefer the most detailed version of a bullet when duplicates exist.
- `patents` captures patent filings. Extract from both the resume text AND LinkedIn Patents CSV.
- `education` and `certifications` are separate arrays. Extract from PDF resume text AND LinkedIn Education CSV. **CRITICAL LOSSLESS RULE**: Do not silently drop non-traditional education, real estate, financial, or insurance courses listed in the raw texts. If an entry is a certification course rather than a degree program, add it to the `certifications` array (e.g., "Mortgage Broker and Lending Certification Course"). If dates are missing, omit the date field but preserve the entry.
- `projects` is populated by autonomously fetching GitHub repository data.
- `skills` is a categorized object where keys are category names (e.g. "AI & Machine Learning") and values are arrays of skill name strings. **CRITICAL:** Do not categorize runtimes, frameworks, or environments (like Node.js, React, Kubernetes) under "Languages". "Languages" MUST only contain actual programming languages (e.g., JavaScript, TypeScript, Python). Runtimes/frameworks should go into a "Frameworks & Libraries" or similar category. **FRAMEWORK ECOSYSTEM RULE:** When organizing frameworks, group related tools into their overarching ecosystem instead of scattering them as standalone items. Use the format `Ecosystem Name (Tool1, Tool2, Tool3)`. For example, `"React Ecosystem (Next.js, xState, Tailwind)"` or `"Node Ecosystem (Express, NestJS, Vite)"`. Furthermore, separate Security/Infrastructure tools (e.g., Open Policy Agent) from AI or conceptual architecture categories.
- `industry_expertise` is a categorized object for non-technical domain knowledge and industry-specific skills. **INDUSTRY SPECIFIC SKILLS:** If a skill is heavily specialized to a particular industry (e.g., Epic for Healthcare, FIX Protocol for Finance, Global Reservation Engines for Hospitality), agents MUST categorize it inside `industry_expertise` using the industry name as the key (e.g., `"Healthcare"`, `"Travel & Hospitality"`).
- `recommendations` captures LinkedIn recommendations verbatim — useful for voice profiling and distinction mining.

## Command API

Praxis uses a single command with three modes. The orchestrator dispatches based on argument shape — no subcommands to memorize.

### Dispatch Logic

```
/praxis init         → SETUP MODE    (Interview user for KB and Search Ontology)
/praxis              → INGEST MODE   (Rebuild KB from raw sources)
/praxis resume       → GENERATE MODE (Explicitly generate baseline resume)
/praxis <text>       → KNOWLEDGE MODE (Argument is free text)
/praxis <url>        → FORGE MODE    (Argument starts with http:// or https://)
/praxis search       → SOURCE MODE   (Execute job search and queue high-scoring JDs)
```

---

### Mode 1: Ingest (`/praxis`)

**Purpose**: Build or rebuild the knowledge base from raw source files.

**Execution Flow**:

1. **Ingest**: The Orchestrator MUST use its available tools (`bash`, `read`, `glob`) to autonomously extract text from raw source files located in `.praxis/sources/`. This includes reading `*.txt` files, extracting CSVs from LinkedIn ZIP exports, and converting `.pdf` resumes using `pdftotext` or Python equivalents. Aggregate the raw context in memory or a temporary file.

3. **LLM-Native Parsing**: The Orchestrator MUST use LLM cognition on the extracted raw text to:
    - Fuzzy-match and merge identical roles (e.g., "The Lowbush Company" vs "Lowbush Company")
    - Resolve date discrepancies — prefer the most specific dates
    - **DATE FORMAT RULE**: All experience dates MUST be `Mon YYYY - Mon YYYY` (e.g., `Jan 2015 - Jul 2025`). LinkedIn CSVs provide bare years — default to `Jan` for start dates and `Dec` for end dates. Current roles use `Present` as end date.
    - **SKILL HARVESTING**: Extract ALL skills, technologies, and tools mentioned in the raw sources for a role and populate the `skills_used` array for that role. This guarantees the database is completely lossless, even if the bullet points are later rewritten to remove heavy tech jargon.
    - Pool ALL distinct bullets from every source — the PDF often has richer accomplishments than LinkedIn
    - Write structured JSON to `.praxis/data/knowledge_base.json` conforming to the schema above

4. **Refinement Protocol**: After writing the initial KB, the Orchestrator MUST perform multi-pass critical analysis. This is the core value of the skill. The user has final say on all changes.

    **Pass 0 — Voice Extraction (MUST run first)**: Build a voice profile from the applicant's raw source materials before any rewriting.
    - Read original PDF text, LinkedIn summary, and raw text files from `.praxis/sources/raw_context.txt`
    - Analyze: perspective (first/implied first/third person), tone, sentence structure, vocabulary tendencies, avoidances
    - Select 3-5 verbatim fragments that exemplify their natural voice
    - Present for confirmation, write to `voice_profile` in KB

    **CRITICAL**: The voice profile is law for all downstream generation. `praxis-pathos` MUST draft in this voice. `praxis-logos` MUST reject deviations.

    **Pass 1 — Terminology Normalization**: Before any rewriting, the Orchestrator MUST normalize terminology across the entire knowledge base to eliminate variant references to the same concept. This prevents skills from appearing "orphaned" when they are actually evidenced under a different name.

    **Procedure**:
    1. **Build terminology index**: Scan ALL text in the KB — `basics.summary`, every `experience[].bullets`, `projects[].description`, `skills` category values, `patents`, `distinctions`, and `recommendations`. Extract every technology name, framework, methodology, acronym, and domain concept.
    2. **Identify variants**: Group references that point to the same concept but use different forms. Common patterns:
        - Abbreviation vs. full name: `NLP` vs. `Natural Language Processing` vs. `Natural Language Processing (NLP)`
        - Library name vs. ecosystem name: `React` vs. `React.js` vs. `ReactJS`
        - Product vs. generic: `Docker` vs. `Docker Products` vs. `containerization`
        - Branded vs. descriptive: `Salesforce.com Development` vs. `Salesforce`
        - Versioned vs. unversioned: `ES6` vs. `JavaScript` vs. `ECMAScript`
        - Casing variants: `kubernetes` vs. `Kubernetes` vs. `K8s`
    3. **Select canonical form**: For each group, pick the form that is:
        - Most widely recognized by ATS parsers (prefer the standard industry name)
        - Already expanded on first use per ATS acronym rules (e.g., `Natural Language Processing (NLP)` on first occurrence, `NLP` thereafter)
        - Consistent with what the applicant actually wrote in their source materials
    4. **Normalize**: Replace all variant forms with the canonical form throughout the KB. For skills specifically, ensure the skill name in `skills{}` exactly matches the term used in `skills_used` arrays so the skill is never orphaned.
    5. **Cross-reference skills to roles**: After normalization, verify that every skill listed in `skills{}` appears in at least one role's `skills_used` array, project description, or summary. **CRITICAL NON-LOSSY RULE:** NEVER remove a skill from the `skills` object just because it lacks textual evidence in the polished bullet points. Since skills are now decoupled from the bullet text, `skills_used` is the source of truth for evidence. Retain ALL skills extracted from LinkedIn and raw texts.
    6. **Report**: Present the normalization map to the user. For any "orphaned" skills that lack bullet evidence, queue them for Pass 4.

    **Pass 1.5 — Implicit Skill Clarification (The "Unstated Tech" Interview)**: Scan the normalized KB for implicit technologies that are highly likely but unstated to prevent gaps in the user's base profile.
    - **Identify Gaps**: e.g., If a bullet mentions "Kubernetes", "Docker", or "Microservices" but no cloud provider (AWS, GCP, Azure) is listed. If "React" is listed but not "TypeScript". If "SQL" is listed but no specific RDBMS (Postgres, MySQL) is named.
    - **Prompt User**: Present a concise list of likely implicit skills. *"You mentioned Kubernetes at [Company]. Should I add AWS, GCP, or Azure to this role? What about TypeScript for your React work?"*
    - **Apply**: Upon user confirmation, inject the stated skills into the `skills` array AND append them naturally to the relevant `experience[].bullets`.

    **Pass 2 — Summary Audit**: Evaluate `basics.summary` against the entire career corpus. Does it reflect the strongest differentiators? Does it undersell key themes? Present current summary, analysis, and proposed revision.

    **Pass 3 — Bullet Strengthening (Quantification Interview)**: Scan every bullet for passive voice, vague language, missing metrics, unspecific scale, first-person pronouns, role descriptions masquerading as accomplishments, technology dumps without context, and near-duplicates.

    **CRITICAL — One-at-a-Time Presentation**: Present ONE bullet at a time:
    ```
    **[Company Name]** — Bullet [N] of [Total flagged]
    > [The exact current bullet text]
    **Issue**: [What's wrong]
    **Question**: [Specific question for the user]
    ```
    Wait for the user's answer before presenting the next bullet.

    **Pass 4 — Skill Evidence Backfill**: For every skill still marked as "orphaned" (lacking contextual evidence in any `skills_used` array), do NOT delete it. Instead, present a rapid-fire interview to the user: *"You listed [Skill] but it isn't mapped to any of your roles. At which company did you use it?"* Add the skill to that role's `skills_used` array.

    **Pass 5 — Distinction Mining**: Scan all data for achievements that deserve elevation to `distinctions[]` — quantified impact, firsts/records, company-defining moments, external recognition.

    **Pass 6 — Spelling & Grammar Audit**: Fix all spelling, grammar, and punctuation errors silently. Report what was changed after the fact. Only prompt when a correction changes meaning.

5. **GitHub Sync**: Use the `bash` tool with `gh` CLI (if available) or generic web fetching to pull the user's public repositories, descriptions, languages, and star counts. Update the `projects` array in the `knowledge_base.json`.

6. **Baseline Draft**: Invoke `praxis-pathos` to explicitly regenerate the general baseline resume (`assets/Resume.md`) entirely via LLM generation based on the strict formatting rules and output template. Do NOT rely on bash scripts to generate the file.

    **CRITICAL**: Draft MUST NOT generate until refinement is complete and user-approved.

7. **Adversarial Baseline Review**: After draft generation, run a two-agent review:
    1. **Logos (Auditor)**: Review against `ATS_PARSER_RULES.md` for compliance defects
    2. **Pathos (Drafter)**: Review for impact, voice authenticity, weak bullets, missed opportunities
    3. Both produce categorized defect lists (BLOCKING / MAJOR / MINOR)
    4. Fix all BLOCKING defects, address MAJOR where possible, log MINOR as beads
    5. Regenerate after fixes. Repeat if BLOCKING defects remain (max 3 iterations).

8. **Cleanup**: Move all processed raw files into `.praxis/sources/`.

---

### Mode 2: Knowledge Update (`/praxis <text>`)

**Purpose**: Add facts, skills, corrections, or context to the knowledge base using natural language.

**Examples**:
```
/praxis at DexCare I managed a team of 76 developers
/praxis I'm also proficient in Terraform from my AWS work at Marriott
/praxis actually the Marriott team was about 40 people
/praxis add a project: Nibble.Fish — a fishing companion app with MobileNetV3 vision classifiers
/praxis remove the AngularJS skill, I haven't used it in years
```

**Execution Flow**:

1. **Parse Intent**: The orchestrator uses LLM cognition to determine what the user is saying. Possible intents:
    - **New bullet**: A fact about a specific role → append to `experience[].bullets` for the matched company
    - **Skill addition/removal**: A skill claim → add to or remove from `skills` object
    - **Correction / Directive**: A fix to existing data OR a global rule for generation (e.g., `/praxis correction Do not list OPA as AI`) → fix the data AND/OR add to `generation_rules` array.
    - **New project**: A project description → add to `projects[]`
    - **New certification/education**: → add to the relevant array
    - **General context**: Something that doesn't fit neatly → the orchestrator decides where it belongs

3. **Fuzzy Match**: When the user names a company, role, or skill, fuzzy-match against existing KB data. Don't require exact names — "dexcare", "DexCare", "Dex Care" should all match.

4. **Write**: Apply the change to `knowledge_base.json`.

5. **Spelling & Grammar**: Silently fix any errors in the new content before writing. Report fixes after the fact.

6. **Voice Compliance**: If the input is a new bullet, rewrite it to match `voice_profile` before storing. Show the user the rewritten version.

7. **Confirm**: Tell the user exactly what was added/changed and where.
8. **Audit (Panel Review)**: Immediately after confirming the change, invoke `praxis-logos` to audit the *newly added bullet* for tone, metrics, passive voice, and factual consistency. Present this feedback to the user. (Do NOT automatically regenerate the baseline resume).

---

### Mode 4: Generate Baseline (`/praxis resume`)

**Purpose**: Explicitly regenerate the general baseline resume (`assets/Resume.md`) and the LinkedIn Profile template (`assets/LinkedIn_Profile.md`) entirely via LLM generation without relying on ad-hoc shell scripts.

**Execution Flow**:
1. Invoke `praxis-pathos` with the full `knowledge_base.json` and `ATS_PARSER_RULES.md`. The LLM agent MUST construct the complete Markdown string for the baseline resume (`assets/Resume.md`) itself based on the strict formatting rules and output template. Do NOT execute a bash script.
2. Invoke `praxis-pathos` to generate a dedicated LinkedIn profile template (`assets/LinkedIn_Profile.md`). This file MUST be written in the first person, optimized for LinkedIn's character limits (e.g., 220-char headlines), and include easy-to-copy sections for the "About", "Experience" (with top 5 skills to tag per role), and a comma-separated list for the "Skills" section.
3. Present the updated documents to the user.

---

### Mode 3: Forge (`/praxis <url>`)

**Purpose**: Generate a tailored resume and interview prep sheet for a specific job posting.

**Prerequisites**: `knowledge_base.json` must exist with a populated `voice_profile`. If not, tell the user to run `/praxis` first.

#### Persona Definitions

**praxis-pathos (The Drafter)**:
Senior resume strategist who writes in the applicant's authentic voice. MUST:
- **ANTI-LAZY & FAILURE HANDLING (MANDATORY)**: If you cannot fetch the job description (e.g., due to bot blocking on LinkedIn) or lack sufficient context, you MUST FAIL LOUDLY and ask the user for the text. You are strictly forbidden from generating 20-byte stub/placeholder files to artificially "succeed".
- **TWO-PASS METHODOLOGY & VALIDATION (MANDATORY)**: 
  1. **Pass 1 (Extraction):** Extract ALL entities from `knowledge_base.json` and map them exactly to the `RESUME_TEMPLATE.md` structure. Make ZERO editorial decisions or omissions.
  2. **Pass 2 (Tailoring):** Review the target job description. Re-write the *descriptions and bullets* of the pre-formatted document to emphasize the target role. You are strictly forbidden from structurally deleting facts, hiding patents, dropping links, or modifying the ATS headers from the template.
  3. **Pass 3 (Validation Loop - MANDATORY):** After writing the markdown file, you MUST verify the file is fully populated (not a stub) and then run:
     `node tests/evaluate_resume.js <path_to_resume> .praxis/data/knowledge_base.json`
     If the script throws an error, you must read the errors, edit the markdown file to fix them, and re-run the script. You are not finished until the script outputs success. Every failure clubs a baby seal! 🦭🏏
- Read `voice_profile.sample_fragments` BEFORE writing to internalize the applicant's phrasing
- STRICTLY obey all constraints listed in the `generation_rules` array from the knowledge base.
- Match `voice_profile` perspective, tone, and sentence structure exactly
- Use vocabulary from `vocabulary_tendencies`, NEVER use words from `avoidances`
- Select 3-4 strongest bullets per role, rewriting to emphasize JD-relevant impact. You MAY weave in technologies from that role's `skills_used` array if the JD requires them, even if the base KB bullet doesn't explicitly name them.
- Follow ALL rules in `ATS_PARSER_RULES.md`
- **STRICT SKILLS FORMATTING**: The generated resume MUST NEVER list runtimes, frameworks, or environments (e.g., Node.js, React, Next.js, Kubernetes) under a "Languages" category. Only list actual programming languages (e.g., JavaScript, TypeScript, Python) under "Languages". You MUST use the `Ecosystem Name (Tool1, Tool2, Tool3)` format for frameworks and libraries in the skills section (e.g., `Node Ecosystem (Express, NestJS)`, `React Ecosystem (Next.js, Tailwind)`). MUST add an empty line break between each skill category to improve readability.
- **INDUSTRY EXPERTISE SECTION**: You MUST generate a separate `## Industry Expertise` section below `## Technical Skills` to list domain-specific non-technical knowledge. Only include industries from the KB's `industry_expertise` object that are directly relevant to the target job.
- **CONTACT LINE FORMATTING**: The contact line MUST include all portfolio links defined in the knowledge base `basics.portfolio_links` array (e.g., GitHub, Cognilogical). Do not drop them.
- Front-load summary and most recent role on page one
- Always include a "Points of Note" section to highlight patents, awards, or distinctions if any exist in the provided knowledge base
- Expand acronyms on first use
- Never invent facts — only rephrase what exists in `knowledge_base.json`
- **STRICT TEMPLATE COMPLIANCE**: You MUST read and strictly adhere to the exact structural template defined in `.agents/skills/praxis/RESUME_TEMPLATE.md` for all generated resumes (both baseline and tailored). Do not use an internal format. You MUST include empty line breaks between each skill category to ensure proper markdown rendering and prevent mashing.
- **NO DROPPED FACTS**: You MUST NEVER omit Patents, Awards, Distinctions, Education, or Certifications from the generated resume if they exist in the knowledge base.
- **SKILL CURATION**: The "Technical Skills" section MUST be aggressively curated and capped at a maximum of 15-20 highly relevant skills. Do not dump the entire database.
- **ABSOLUTE PATHS**: When saving output files (like the generated resume), you MUST use absolute paths (e.g., `/workspace/assets/...` or `/project/...`). Never use relative paths like `../workspace/`.
- **ATS HEADERS**: You MUST use exact ATS-compliant headers (e.g., `## Summary`, `## Technical Skills`, `## Experience`). Never invent custom headers like "## Principal Systems Engineer".

- **EMPTY SECTION OMISSION**: If an array or object in `knowledge_base.json` is empty (e.g., `certifications: []`, `patents: []`, or `distinctions: []`), you MUST entirely omit that section and its header from the generated Markdown output. Do not print "None recorded" or empty headers.

**praxis-logos (The Auditor)**:
Ruthless quality auditor. Receives a draft and source KB. Audits on four axes:
1. **Factual Accuracy**: Every claim must trace to a KB bullet. Flag hallucinations.
3. **Voice Compliance**: Compare against `voice_profile`. A correct bullet that sounds like an LLM is a defect equal to a hallucination.
4. **ATS Compliance**: Verify all `ATS_PARSER_RULES.md` rules.
5. **Tailoring Quality**: Is the resume optimized for THIS job? Are selected bullets the best available?
6. **Directive Compliance**: Did the draft violate any rules in the `generation_rules` array?

Verdict format:
```
VERDICT: APPROVED | REJECTED
FACTUAL_ISSUES: [list or "None"]
VOICE_VIOLATIONS: [list or "None"]
ATS_ISSUES: [list or "None"]
TAILORING_GAPS: [list or "None"]
DIRECTIVE_VIOLATIONS: [list or "None"]
```

#### Execution Flow

1. **Ingest JD**: Fetch the job description from the URL. Extract: company name, role title, required skills, preferred skills, key responsibilities, seniority level. **CRITICAL:** If fetching the URL fails (e.g., LinkedIn anti-bot blocking), the Orchestrator MUST fail loudly and request the raw text from the user. Do NOT pass an empty job description to the subagents.
2. **Overwrite Guard (MANDATORY)**: Check if a directory for the target company already exists in `assets/` (e.g., `assets/{TargetCompany}/`). If it does, PAUSE and prompt the user: *"A tailored resume for {TargetCompany} already exists. Do you want to overwrite it?"* If the user says no, safely abort the workflow.
3. **Company Context Harvesting (Deep Research)**: Do not just trust the JD text. You MUST perform deep research on the target company using available tools (like `webfetch` or LLM search capabilities) to understand their core business model, target market, primary products, and underlying industry (e.g., discovering a company is a Web3/Crypto company even if the specific role is just "AI Engineer"). Use this macro-context to aggressively pull forward adjacent skills from the KB that align with the company's DNA.
3. **Initialize**: Load `knowledge_base.json` and `voice_profile`.
4. **Apply User Rules**: Load `rules.json`. Apply `date_overrides`, `company_replacements`, and `injected_roles` to the working copy.
5. **Skill Gap Interview (Fitment Session)**: Compare JD requirements against KB skills. For each missing required skill, PAUSE and prompt the user ONE AT A TIME: *"The job requires [Skill]. Do you have experience with this? If so, at which company, and briefly, how did you use it?"* Wait for the user to answer before asking about the next missing skill. Do not blob multiple skills into a single question. If the user provides a valid example:
    - Pass their raw description to `praxis-pathos` to draft a new resume bullet in the user's `voice_profile`.
    - Pass the drafted bullet to `praxis-logos` to audit and refine.
    - Once approved, PERMANENTLY save the new skill to the global `skills` object, append it to that specific role's `skills_used` array, AND append the newly wordsmithed bullet to that role's `bullets` array in `knowledge_base.json`. This ensures the KB continually grows stronger with concrete, well-crafted evidence.
6. **Compensation Intelligence Lookup (MANDATORY)**: The Orchestrator MUST scan the job description text for explicit salary bands. If none exist in the JD, autonomously look up compensation data using tools (like `webfetch` to `https://h1bdata.info/index.php?em=[Company]&job=[Role]`). You MUST pass this comp data (or the failure to find it) explicitly to `praxis-pathos`.
7. **Relevance Filter**: Filter KB to entries semantically relevant to the JD. Drop roles older than 15 years unless uniquely relevant. **INDUSTRY SPECIFIC FILTERING:** When creating the filtered KB for tailoring, completely EXCLUDE any `industry_expertise` categories UNLESS the target Job Description is strictly within that same industry. Industry specific skills must only appear on resumes tailored to that exact industry.
8. **Adversarial Loop (MAX_ITERATIONS = 3)**:
    - **Phase 1 (Draft)**: Invoke `praxis-pathos` with JD analysis, filtered KB, `voice_profile`, and `ATS_PARSER_RULES.md`.
    - **Phase 2 (Audit)**: Invoke `praxis-logos` with the draft, FULL `knowledge_base.json`, `voice_profile`, and `ATS_PARSER_RULES.md`.
    - **Phase 3 (Iterate)**: If `REJECTED`, feed issues back to pathos. If not approved by iteration 3, present remaining issues to user.
9. **Output**: Create a directory for the target company (`assets/{TargetCompany}/`). Save the tailored Markdown resume to `assets/{TargetCompany}/{TargetCompany}_{First}_{Last}_Resume.md`. (CRITICAL: `{TargetCompany}` MUST be the actual name of the company from the target job req, e.g., `Microsoft`).
10. **Generate PDF**: Run `npx md-to-pdf "assets/{TargetCompany}/{TargetCompany}_{First}_{Last}_Resume.md" --stylesheet .agents/skills/praxis/resume.css --config-file scripts/mdpdf.config.js` (if available in the environment) or use `pandoc` to convert the markdown to PDF. DO NOT delete the Markdown file; leave it for the user to edit manually if desired.
11. **Interview Prep Sheet**: Generate `assets/{TargetCompany}/{TargetCompany}_{First}_{Last}_Interview_Prep.md`:
    - **STRICT TEMPLATE COMPLIANCE**: You MUST read and strictly adhere to the exact structural template defined in `.agents/skills/praxis/INTERVIEW_PREP_TEMPLATE.md`.
    - **SALARY ENFORCEMENT**: You MUST populate the `## Salary & Negotiation Context` section. It is strictly forbidden to omit this section. Use the comp data passed by the Orchestrator.
12. **Targeted Cover Letter**: Generate `assets/{TargetCompany}/{TargetCompany}_{First}_{Last}_Cover_Letter.md`:
    - **CRITICAL VOICE COMPLIANCE**: The cover letter MUST be written strictly adhering to the `voice_profile` from the knowledge base (perspective, tone, sentence structure, vocabulary, and avoidances).
    - **STRICT TEMPLATE COMPLIANCE**: You MUST read and strictly adhere to the exact structural template defined in `.agents/skills/praxis/COVER_LETTER_TEMPLATE.md`.
    - Address the specific pain points and core requirements mentioned in the Job Description.
    - Highlight 1-2 key narrative arcs from the user's career that perfectly align with the role's level and domain.
    - Keep it concise (3-4 paragraphs), professional, and highly targeted.
    - Generate a PDF version: Run `npx md-to-pdf "assets/{TargetCompany}/{TargetCompany}_{First}_{Last}_Cover_Letter.md" --stylesheet .agents/skills/praxis/resume.css --config-file scripts/mdpdf.config.js`.
13. **Summary**: Display company, role, iteration count, unresolved warnings, output paths, and cost.

---

### Mode 0: Setup & Ontology Interview (`/praxis init`)

**Purpose**: Initialize the Praxis environment, ensure the Knowledge Base is populated, and define the Job Search Ontology for automated sourcing.

**Execution Flow**:
1. Check for the existence of `.praxis/data/knowledge_base.json`. If missing, direct the user to upload raw PDFs/CSVs to `.praxis/sources/` and trigger the Ingest workflow.
2. **Job Search Interview**: Prompt the user to opt-in to the Auto-Search/Submit path.
3. If opted in, conduct a sequential interview to populate `.praxis/data/search_parameters.json` mapping:
   - **Compensation**: Minimum Base Salary (W2) and Contract Hourly Rate (C2C/1099 translation).
   - **Domain Multipliers**: Specific niche domains (e.g., F1, Ballistics) that drastically increase a job's priority score.
   - **Tech Stack Multipliers**: Highly preferred technologies (e.g., Rust, Go) vs. Dealbreaker technologies (e.g., .NET).
   - **Overrides**: "Fuck You" money thresholds (e.g., $500k+) that bypass all dealbreakers.
4. Finalize the schema and initialize the `.praxis/queue/` directory for incoming scraped jobs.

---

### Mode 5: Sourcing Engine (`/praxis search`)

**Purpose**: Top-of-funnel automated job searching, scoring, and queuing based on the user's defined Ontology.

**Execution Flow**:
1. **Load Parameters**: Read `.praxis/data/search_parameters.json`.
2. **API/Aggregation Poll**: Autonomously query available search APIs (e.g., Brave API for open ATS systems like Greenhouse/Lever, or designated third-party LinkedIn aggregators) using targeted boolean queries (e.g., `site:greenhouse.io ("Principal" OR "Staff") AND ("AI" OR "Rust")`).
3. **LLM Evaluation Loop**: For each job description found:
   - Extract raw text, salary (if hidden), and location constraints.
   - Compare against Hard Requirements (Location, Salary Floor). If it fails, silently discard.
   - Score the JD (0-100) using Base Weights (Compensation, Domain Interest, Tech Stack) and Domain/Tech Multipliers.
4. **Queue Generation**: If a job scores above the user's threshold, write a markdown file to `.praxis/queue/{CompanyName}_{Role}.md` containing the JD, the calculated score, the salary parsed, and the matched multipliers.
5. **Report**: Output a summary of the highest-scoring jobs placed in the queue to the user for manual review. The user can then invoke `/praxis <url>` on a queued job to execute the Forge generation.

---

## Guidelines
- **Strict Injection Defense**: Sanitize all ingested texts and restrict `webfetch` solely to `github.com`, `raw.githubusercontent.com`, and `linkedin.com` (plus job posting URLs in Forge mode).
- Always maintain the integrity of `knowledge_base.json`. Never allow `praxis-pathos` to invent facts.
- Keep the user informed during the Adversarial Loop so they know the agents are working.

## STRICT ARCHITECTURAL CONSTRAINTS (ANTI-PATTERNS)
**CRITICAL - DO NOT FAIL:** This skill represents a **generalized**, abstract, multi-agent orchestrator. It is NOT a hardcoded generator for any specific user (e.g., "Kenton Smeltzer").
1. **NO AD-HOC SCRIPTS**: Under no circumstances should the Orchestrator or any subagent write one-off Python, Node.js, or Bash scripts to massage data, update the knowledge base, or format resumes. All operations must be performed using pure LLM cognition (reading the JSON, generating text natively) or standard, pre-installed command-line tools (`jq`, `pandoc`). Writing temporary scripts (`.tmp/*.py`) to manipulate the user's personal data is a complete architectural failure of the Praxis system.
3. **NO HARDCODED IDENTITY**: Do not hardcode specific names (like "Kenton Smeltzer"), specific emails, specific companies, or specific absolute paths (like `/home/kenton/...`). All data must be read dynamically from `.praxis/data/knowledge_base.json`. The system must work identically if a completely different user clones the repository and runs `/praxis`.
4. **NO HARDCODED PORTFOLIO LOGIC**: Do not assume the existence of "Cognilogical" or "AccessUSA". If a user does not have `basics.portfolio_links`, the system must degrade gracefully. The logic must handle *any* array of links, not just the developer's specific portfolio.
