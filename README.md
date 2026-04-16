<div align="center">
  <img src="docs/assets/logo.png" alt="Praxis Logo" width="300" />
  <p><b>An Adversarial, Multi-Agent Career Knowledge Base & Resume Pipeline</b></p>
  <p><i>Defeating ATS bots, hallucination, and the blank-page problem through rigorous AI orchestration.</i></p>
</div>

---

**Praxis** is a localized, multi-agent pipeline designed to solve the critical failures of using standard LLMs (like ChatGPT) to write resumes. By employing a strict **Zero-Loss Relational Database**, **Adversarial Drafting Loops**, and **Automated Deep Data Harvesting**, Praxis generates highly targeted, mathematically honest, and ATS-optimized career documents.

## 🧠 The Science: Why Praxis?

Using a single-shot prompt to ask an LLM to "write my resume" results in three catastrophic failures:
1.  **Summarization Loss:** LLMs inherently compress facts, stripping away the exact metrics, technologies, and scale that actually get you hired.
2.  **Sycophancy & Hallucination:** LLMs invent "AI-speak" (e.g., "Spearheaded synergistic paradigms") and hallucinate responsibilities to make you sound good, failing rigorous technical interviews.
3.  **The Blank Page Problem:** Most professionals severely underestimate their own impact, scale, and day-to-day metrics.

Praxis solves this through a multi-agent architectural pipeline:

*   **Zero-Loss Relational Cataloging:** Instead of summarizing your history into Markdown, Praxis iteratively ingests raw data (PDFs, GitHub `.tar.gz` exports, LinkedIn CSVs) into a strict `.praxis/data/knowledge_base.json`. This acts as a permanent, loss-proof relational database of your skills, mapping every tool to the exact metric and project where it was used.
*   **The Expert Inquisitor:** Praxis analyzes your ingested data for weak points (missing metrics, vague responsibilities). It then conducts a multi-step, structured interview wizard to extract exact numbers and scale, enriching the database with authoritative context.
*   **Adversarial Drafting Loop (Pathos vs. Logos):** When tailoring a resume for a specific job description (`/praxis customize <url>`), Praxis employs a two-agent adversarial loop. 
    *   **`praxis-pathos` (The Visionary)** drafts the resume using your saved Voice Profile and the STAR method.
    *   **`praxis-logos` (The Truth-Teller)** acts as a brutal auditor, rejecting any bullet point that hallucinates facts or uses AI-speak not explicitly backed by the `knowledge_base.json`. They iterate until a mathematically honest, perfectly targeted document is produced.

---

## 🏗️ Architecture & Commands

Praxis installs directly into your local CLI environment (e.g., `opencode` or `strata`) as a skill.

### 1. The Intake Engine: `/praxis build`
*   **What it does:** Runs a deterministic Deep Harvest extraction script (`ingest.py`) across your root directory for raw exports (PDFs, TXTs), ignores system files, and syncs your public GitHub repositories (`github_sync.py`).
*   **How it works:** It losslessly parses this data into `string[]` fact pools, pushes it into `.praxis/data/knowledge_base.json`, and then moves the raw files to a secure `.praxis/sources/` directory. It then automatically drafts ATS-optimized baseline profiles (`assets/Resume.md`, `assets/LinkedIn_Profile.md`) utilizing a "Discrete Chronological Strategy".

### 2. The Fact Logger: `/praxis history <fact>`
*   **What it does:** Quickly appends a specific accomplishment, metric, or bullet point to an existing role without requiring a full CV re-upload.
*   **How it works:** You run `/praxis history at ACME co., I managed a team of 50`. Praxis parses the company, locates it in `knowledge_base.json`, and appends the fact to that role's `bullets` array (the "fact pool"), automatically regenerating your baseline resumes.

### 3. The Skill Enricher: `/praxis skill <skill_name> <description>`
*   **What it does:** Replaces generic, scraped LinkedIn skills (e.g., "Kubernetes") with concrete contextual evidence of *how* you used that skill.
*   **How it works:** You run `/praxis skill Kubernetes Architected multi-region clusters...`. Praxis pushes this rich context into the `RelationalSkillsDatabase` array for that skill, giving the Drafter agent highly specific material to work with.

### 4. The Forge: `/praxis gen <job-url>`
*   **What it does:** Generates a highly tailored PDF resume specifically designed to pass the ATS for a target job.
*   **How it works:** It runs a Skill Gap Analysis between the Job Description and your `knowledge_base.json`. It triggers the `Pathos/Logos` adversarial loop to strategically select the 3-4 most relevant facts from your "fact pools" (rather than dumping your whole history). It then generates a targeted PDF (e.g., `assets/Company_User_Resume.pdf`) and cleans up the temporary files.

---

## 🚀 Installation

```bash
# Clone the repository
git clone git@github.com:ksmeltzer/Praxis.git
cd Praxis

# Install the agents, skills, and commands to your local environment
chmod +x install.sh
./install.sh
```

## 🔒 Privacy & Security

Praxis is designed with absolute privacy in mind. Your raw data, API keys, and generated JSON databases are intentionally `.gitignore`'d. Your career data never leaves your local machine unless you explicitly configure an external model API.

---
