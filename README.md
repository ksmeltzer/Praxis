<div align="center">
  <h1>Praxis</h1>
  <p><b>An Adversarial, Multi-Agent Career & Resume Forging Pipeline</b></p>
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
*   **What it does:** Scans your root directory for raw exports (PDFs, GitHub JSON metadata, LinkedIn CSVs).
*   **How it works:** It losslessly parses this data, pushes it into the `knowledge_base.json`, and then moves the raw files to a secure `.praxis/sources/` directory. If it detects missing context, it will automatically interview you and perform web searches (e.g., researching niche team methodologies) to enrich your profile.

### 2. The Forge: `/praxis customize <job-url>`
*   **What it does:** Generates a highly tailored Markdown resume specifically designed to pass the ATS (Applicant Tracking System) for a target job.
*   **How it works:** It runs a Skill Gap Analysis between the Job Description and your `knowledge_base.json`. If you are missing a required skill, it prompts you for an example of when you used it. Then, it triggers the `Pathos/Logos` adversarial loop to generate the final document.

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
