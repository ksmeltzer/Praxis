# Praxis Skill

This skill implements the orchestrator logic for the Praxis adversarial resume builder.

## Architecture & File Structure
- **Root Directory**: Kept clean. Only final generated assets (`Resume.md`, `LinkedIn_Profile.md`, `Tailored_*.md`) live here.
- **`.praxis/sources/`**: All raw input files (resumes, LinkedIn CSVs) are moved here immediately after parsing.
- **`.praxis/data/`**: Contains the exhaustive, non-lossy backend database (`knowledge_base.json`).

## Commands

### `/praxis build` (The Iterative Intake Wizard)
**Purpose**: Iteratively ingest files to build/update the `knowledge_base.json` database and generate baseline profiles.
**Execution Flow**:
1.  **Scan & Move**: Search the root directory for new source files (`*.pdf`, `*.docx`, `*.md`, `*.csv`). Parse their contents, then immediately move them into `.praxis/sources/` to keep the root clean.
2.  **Iterative Merge**: Load `.praxis/data/knowledge_base.json` (create if it doesn't exist). Merge the newly parsed data losslessly into the JSON schema without overwriting or summarizing previous entries.
3.  **Prompt & Deep Harvest**: Analyze what data is missing from the database.
    *   **LinkedIn Data**: Provide the direct link to the user: `https://www.linkedin.com/mypreferences/d/download-my-data`. Advise them it takes ~10 minutes, and they can simply drop the CSVs into the root folder and run `/praxis build` again later to iteratively layer in the data.
    *   **GitHub Data**: Provide the direct link to the user: `https://github.com/settings/admin`. Instruct them to scroll down to "Export account data" and click `Start export`. Advise them it will send a `tar.gz` to their email. They can extract the relevant data files into the root folder and run `/praxis build` again to ingest it. If they prefer not to wait, the agent can fall back to using `webfetch` to scrape public READMEs and tech stacks.
4.  **The Expert Inquisitor & Contextual Researcher**: Analyze the *newly* merged data for weak points (missing metrics, vague responsibilities). Conduct a sequential, multi-step interview wizard to extract exact numbers. Perform deep web searches on niche methodologies (e.g., CIA Animal Kingdom) to enrich the JSON database with authoritative context.
5.  **Voice Profiling**: Update the "Voice & Tone Profile" in the JSON database based on new inputs.
6.  **Zero-Loss Relational Cataloging**: Ensure the `knowledge_base.json` contains a strict `Relational Skills Database` (skills as keys, contextual implementations as values) and an `Exhaustive Career Catalog` (zero-loss, verbatim facts).
7.  **Drafting Baseline Profiles**: Invoke `praxis-pathos` to read `.praxis/data/knowledge_base.json` and draft/update the baseline `Resume.md` and `LinkedIn_Profile.md` in the root directory using the STAR method and the user's Voice Profile.
8.  **Review & Polish**: Perform a rigorous final spell and grammar check on all output files.

### `/praxis customize <job-description-url>` (The Forge)
**Purpose**: Create a highly tailored resume for a specific job using the adversarial loop.
**Execution Flow**:
1.  **Ingest**: Fetch and analyze the target job description from the provided `<job-description-url>`.
2.  **Initialize**: Load the user's `.praxis/data/knowledge_base.json`.
3.  **Skill Gap Interview (Expert Mode)**: Compare the Job Description against the `knowledge_base.json` Skills Matrix. If the job requires a skill (e.g., "Terraform" or "GraphQL") that is missing, prompt the user as an expert interviewer: *"The job requires [Skill]. Can you provide a specific example of a system you built using this? What scale or metrics were involved?"* Append this rich context to the database before proceeding.
4.  **Adversarial Loop**:
    *   **Phase 1 (Draft)**: Feed the Job Description and `knowledge_base.json` to `praxis-pathos`. `praxis-pathos` generates a tailored draft highlighting relevant skills.
    *   **Phase 2 (Audit)**: Pass the draft to `praxis-logos`. `praxis-logos` audits strictly against the database and checks for "AI-speak" or hallucinations.
    *   **Phase 3 (Iterate)**: If `praxis-logos` rejects the draft, feed the critique back to `praxis-pathos` for a rewrite. Repeat until "APPROVED".
5.  **Output**: Generate the finalized, tailored Markdown resume in the root directory.

## Guidelines
- Always maintain the integrity of `knowledge_base.json`. Never allow `praxis-pathos` to invent facts.
- Keep the user informed during the Adversarial Loop iteration phases so they know the agents are working.

### `/praxis help`
**Purpose**: Display usage instructions for the Praxis skill.
