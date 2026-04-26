# Praxis

**Praxis** is an adversarial, multi-agent pipeline designed to build, maintain, and deploy a flawless, ATS-compliant Career Knowledge Base. Unlike traditional resume builders that overwrite or lose data, Praxis operates as an exhaustive, non-lossy backend database of your entire professional history. It dynamically carves tailored, hyper-targeted resumes optimized for specific job descriptions while aggressively preventing LLM hallucinations.

## Architecture & Philosophy

- **Exhaustive Knowledge Base**: Your professional history is stored in `.praxis/data/knowledge_base.json`. It is a strict superset of all your resumes, LinkedIn exports, and manual inputs.
- **Strict Anti-Hallucination**: The Drafter agent (`praxis-pathos`) is legally bound by the Auditor agent (`praxis-logos`) to NEVER invent facts. Every bullet point on a generated resume MUST trace back to explicit evidence in the Knowledge Base.
- **The Non-Lossy Rule**: Praxis will never delete a skill or fact simply because it lacks a corresponding bullet point. Instead, it will proactively interview you to gather the missing context.
- **Continuous Evolution**: Every time you apply for a job that requires a skill missing from your Knowledge Base, Praxis runs a **Fitment Session** to capture that experience, permanently strengthening your master profile.
- **Artifact Retention**: All tailored resumes are preserved in both `.pdf` and raw `.md` formats within company-specific directories (`assets/{CompanyName}/`), ensuring you always retain the ability to manually tweak the final output.

## Command API

Praxis uses a single, unified command (`/praxis`) that automatically routes to the correct workflow based on the argument provided.

### 1. Ingest Mode (`/praxis`)
**Use Case**: Initializing or rebuilding your Knowledge Base from raw source files (PDFs, LinkedIn CSVs, text files).
**Workflow**:
- **Merge & Normalize**: Deduplicates roles, normalizes terminology (e.g., `React.js` -> `React`), and strict-types skills (separating languages like `TypeScript` from runtimes like `Node.js`).
- **Skill Harvesting (The Lossless Rule)**: All skills mentioned in your raw files are extracted into a `skills_used` metadata array attached to each specific role. This decouples the raw tech-stack from the polished text, allowing the AI to rewrite your bullets to be punchy and "correct" without ever losing the underlying technical data.
- **Unstated Tech Interview**: Identifies implicit gaps (e.g., you listed `Kubernetes` but no cloud provider like `AWS`) and prompts you to fill them.
- **Evidence Backfill**: If a skill was extracted from LinkedIn but lacks context in your bullet points, Praxis will interview you to write a 1-sentence example of how you used it, ensuring every skill is backed by textual evidence.
- **Voice Profiling**: Analyzes your natural writing style to ensure all future AI-generated bullets sound exactly like you.

### 2. Knowledge Update Mode (`/praxis <text>`)
**Use Case**: Chat-based updates to your Knowledge Base.
**Examples**:
- `/praxis At DexCare I managed a team of 76 developers.`
- `/praxis Add a new project called Nibble.Fish.`
- `/praxis correction "Never categorize Node.js as a programming language."`
**Features**:
- **The Directive Engine**: When you issue a `/praxis correction`, Praxis not only fixes the underlying data but permanently saves the rule to the `generation_rules` array. The Auditor agent will strictly enforce this rule on all future drafts.

### 3. Forge Mode (`/praxis <url>`)
**Use Case**: Generating a hyper-targeted resume for a specific job posting.
**Workflow**:
1. **JD Analysis**: Parses the target job description to extract required skills, seniority, and responsibilities.
2. **Skill Gap Fitment Session**: If the JD requires a skill (e.g., `C#`) that your Knowledge Base lacks, Praxis pauses and asks: *"The job requires C#. Do you have experience with this?"* If you provide an example, it permanently adds it to your KB.
3. **The Adversarial Loop**:
   - **Pathos (The Drafter)** selects the 3-4 strongest, most relevant bullets per role, rewriting them in your authentic voice to match the JD.
   - **Logos (The Auditor)** ruthlessly reviews the draft against the JD, your `voice_profile`, ATS constraints, and your custom `generation_rules`. Drafts are rejected and rewritten until they pass all checks.
4. **Output Generation**:
   - Creates a dedicated folder: `assets/{CompanyName}/`
   - Saves the raw Markdown (`{CompanyName}_{First}_{Last}_Resume.md`) for easy manual editing.
   - Generates a polished PDF (`{CompanyName}_{First}_{Last}_Resume.pdf`).
   - Generates a custom Interview Prep Sheet (`{CompanyName}_{First}_{Last}_Interview_Prep.md`) featuring targeted talking points, behavioral STAR questions mapped to your actual history, and salary context.

## File Structure
- `assets/{CompanyName}/` — Target destination for all generated tailored resumes and prep sheets.
- `.praxis/sources/` — Safe storage for your raw input files.
- `.praxis/data/knowledge_base.json` — The master, exhaustive database of your career.
- `SKILL.md` — The execution contract and LLM prompt orchestrator.
- `ATS_PARSER_RULES.md` — Strict constraints for ATS system compatibility.
