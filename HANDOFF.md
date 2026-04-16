# Praxis Developer Handoff & Architecture Guide

**ATTENTION NEXT AI AGENT:** Read this document carefully before making ANY changes. This is the source of truth for the project's constraints, architecture, and historical context.

## 1. Project Overview
Praxis is an adversarial, multi-agent career knowledge base and resume generation pipeline implemented as an OpenCode skill. It ingests raw career data (PDF resumes, text resumes, LinkedIn ZIP exports with ALL CSVs), merges them into a structured JSON knowledge base, and uses specialized AI personas (`praxis-pathos` / `praxis-logos`) to dynamically generate highly tailored, ATS-compliant, voice-authentic resumes.

**Critical distinction:** Development sessions are for BUILDING the tool. Do not get pulled into ad-hoc resume consulting or running the pipeline to produce resumes during development.

## 2. Core Directives & Constraints (NON-NEGOTIABLE)
*   **NO PYTHON:** The environment strictly forbids Python scripts for pipeline execution.
*   **NO BRITTLE PARSERS:** Do NOT write imperative scripts (Node.js, Bash regex, awk) to parse human text. Use the Orchestrator LLM's native cognitive capabilities to read raw text and output structured JSON.
*   **GLOBAL VS LOCAL SYNC:** The skill lives in `./skills/praxis`. It MUST remain symlinked to `~/.config/opencode/skills/praxis`. **Never copy files back and forth.**
*   **CLEAN WORKSPACE:** Generated artifacts → `assets/`. Raw sources → `.praxis/sources/`. Root directory stays clean.

## 3. Canonical JSON Schema
The knowledge base at `.praxis/data/knowledge_base.json` uses these top-level keys:
- `basics` — name, label, email, phone, url, summary, location, profiles
- `work` — array of positions (company, position, startDate, endDate, summary, highlights)
- `education` — array of degrees
- `certifications` — array of certs
- `distinctions` — patents, awards, publications
- `voice_profile` — extracted writing voice (perspective, tone, sentence_structure, vocabulary, avoidances, sample_fragments)
- `skills` — array of skill objects with evidence backlinks
- `projects` — array of projects (including GitHub repos)

## 4. Pipeline Architecture

### `/praxis` — Full Ingestion Pipeline
1. **Data Gathering** (`scripts/ingest.sh`): Finds `*.txt` and `*.pdf` (via `pdftotext`), extracts LinkedIn `*.zip` to collect ALL relevant CSVs (Positions, Skills, Profile, Education, Patents, Projects, Recommendations_Received, Rich_Media, Languages). Concatenates everything into `.praxis/sources/raw_context.txt`.
2. **LLM-Native Ingestion** (agentic): Orchestrator reads `raw_context.txt`, deduces company overlaps, merges bullets, resolves dates, writes `.praxis/data/knowledge_base.json`.
3. **GitHub Sync** (`scripts/github_sync.sh`): Calls `gh repo list` with `--visibility public --source --no-archived`, appends real repos to knowledge base.
4. **Drafting** (`scripts/draft.sh`): Reads `knowledge_base.json` via `jq`, generates baseline `assets/Resume.md` using correct schema keys (`basics`, `work`, `skills`, `education`, `certifications`, `distinctions`, `projects`).

### `/praxis gen <url>` — Adversarial Tailored Resume
Triggers the adversarial loop between `praxis-pathos` (drafter) and `praxis-logos` (auditor) to generate a job-tailored resume. Both personas must comply with voice_profile and all ATS rules.

### `/praxis history <fact>` — Append Career Fact
Uses `scripts/history.sh` (key: `work`) to append a bullet to a specific company.

### `/praxis skill <name> <desc>` — Enrich Skill
Uses `scripts/skill.sh` (key: `skills`) to add evidence to a skill entry.

## 5. Refinement Protocol (Passes 0-5)
Defined in SKILL.md. Runs during ingestion after the baseline knowledge base is built:
- **Pass 0:** Voice Extraction — analyzes raw sources, builds `voice_profile`
- **Pass 1:** Summary Audit — professional summary quality
- **Pass 2:** Bullet Strengthening / Quantification Interview — asks user for missing metrics
- **Pass 3:** Skill Evidence Backfill — links skills to experience bullets
- **Pass 4:** Distinction Mining — surfaces patents, awards, publications
- **Pass 5:** Spelling & Grammar Audit — full proofread of knowledge base

## 6. ATS & Parser Rules (`ATS_PARSER_RULES.md`)
Contains 12 sections of research-backed rules that both `praxis-pathos` and `praxis-logos` must follow:
1. Structural Parsing (no columns/tables/graphics)
2. Regex Failures (standardized headers, strict date formatting)
3. Keyword Disconnect (acronym expansion, contextual placement)
4. Human AI Filter (banned AI vocabulary, F-pattern layout)
5. Implied Scale Rejection (quantification requirements)
6. Voice Authenticity (voice_profile compliance, sample calibration, voice violation = rejection)
7. Spelling & Grammar (full proofread, error = rejection, source data correction)
8. ATS Market Landscape (97.8% Fortune 500 use ATS, Workday-first targeting)
9. Resume Length & Format (two-page target, text-based PDF, front-load impact)
10. Content Priority (summary mandatory, skills need evidence, contextual keywords)
11. AI Detection & Authenticity (zero tolerance for AI tell-signs, specificity over polish, voice as antidote)
12. Certifications & Alternative Credentials (experience-first ordering, certs as degree equivalents)

**Data sources:** Resume Genius 2026 Hiring Manager Survey, Jobscan 2025 ATS Usage Report, CareerBuilder survey data.

## 7. Key Files
| File | Purpose |
|---|---|
| `skills/praxis/SKILL.md` | Main skill definition, schema, command workflows, refinement protocol |
| `skills/praxis/ATS_PARSER_RULES.md` | 12 sections of ATS/parser/voice/AI-detection rules |
| `skills/praxis/scripts/ingest.sh` | Data gathering (PDF, TXT, LinkedIn ZIP) |
| `skills/praxis/scripts/github_sync.sh` | GitHub API sync via `gh repo list` |
| `skills/praxis/scripts/draft.sh` | Baseline resume generation from knowledge base |
| `skills/praxis/scripts/history.sh` | Append career fact to `work` array |
| `skills/praxis/scripts/skill.sh` | Enrich skill with evidence |
| `skills/praxis/scripts/rules.json` | User overrides (date corrections, injected roles) |
| `.praxis/data/knowledge_base.json` | Structured career database |
| `.praxis/sources/raw_context.txt` | Concatenated raw input |
| `assets/Resume.md` | Generated baseline resume |

## 8. Post-Mortem of Previous Mistakes (DO NOT REPEAT)
1. **Faked `github_sync.sh`:** Previous agent hardcoded a single project instead of calling the GitHub API. Fixed: now uses `gh repo list`.
2. **`ingest.sh` only extracted 3 of 35+ CSVs:** Missed Education, Patents, Projects, Recommendations, Rich_Media, Languages. Also ignored PDF resumes entirely. Fixed: full extraction.
3. **Scripts referenced nonexistent schema keys:** `CareerCatalog`, `RelationalSkillsDatabase`, `Profile` didn't match the JSON. Fixed: all scripts use canonical keys.
4. **Over-engineering parsers:** Previous agent wrote brittle Node.js CSV parsers. Fixed: LLM-native cognitive parsing.
5. **Command drift:** Updated SKILL.md locally but not globally. Fixed: strict symlink enforcement.
6. **Ghost files:** Left stub ZIPs and config files cluttering root. Fixed: cleanup protocols in scripts.

## 9. Remaining Work
- Verify the full `/praxis gen <url>` adversarial loop end-to-end (praxis-pathos, praxis-logos personas)
- Consider adding `/praxis refine` as a standalone command (run refinement passes independently of full ingestion)
- Expand `rules.json` schema for more complex user overrides
