# Praxis: Project Context & Session Handover

## Project Overview
**Praxis** is an adversarial, multi-agent resume and career profile builder. Unlike standard AI resume generators that hallucinate experience or write in sycophantic "AI-speak," Praxis uses a strict 2-agent loop to balance aggressive marketing (Pathos) with strict, grounded truth (Logos) against a local knowledge base.

It is structured identically to **ARC-7** (tool-agnostic, uses model mapping, heavily relies on Markdown persona files).

## Core Architecture

### 1. The Knowledge Base
- The system must maintain a local `knowledge_base.md`. This is the immutable source of truth containing the user's verified history (education, jobs, raw skills, github projects, linkedin scrapes).
- Agents cannot invent metrics that do not exist in this file.

### 2. The Commands / Workflows
1. **`/praxis build` (The Intake Wizard):**
   - Interactive CLI wizard.
   - Scans current directory for existing resumes.
   - Asks for LinkedIn/GitHub URLs.
   - Interviews the user to fill gaps.
   - Uses `praxis-pathos` to rewrite raw brain-dumps into clean bullets.
   - Outputs the final `knowledge_base.md`, a generic `Resume.md`, and `LinkedIn_Profile.md`.
   - Includes spell/grammar check.

2. **`/praxis customize <job-description-url>` (The Forge):**
   - Feeds the Job Description and `knowledge_base.md` into the Adversarial Loop.
   - Iterates until `praxis-logos` approves the draft.
   - Outputs a tailored Markdown resume and PDF.

### 3. The Adversarial Agents (The Loop)
*Note: Keep the actual agent `.md` files highly token-efficient. Put the psychology in the README, put strict rules in the agent prompts.*

* **Agent 1: `praxis-pathos` (The Visionary / Marketer)**
  * **Model:** Claude 3.5 Sonnet
  * **Role:** Drafts the resume.
  * **Rules:** Must use the STAR method (Situation, Task, Action, Result). Must front-load action verbs (F-pattern reading topology). Must optimize for Cognitive Fluency (easy to read, good whitespace).

* **Agent 2: `praxis-logos` (The Truth-Teller / Interrogator)**
  * **Model:** GPT-4o / o1-preview
  * **Role:** Audits the draft against `knowledge_base.md`.
  * **Rules:** Kills "AI-speak" (Banned words: delve, tapestry, revolutionized, spearheaded, synergy). Flags unbacked metrics. Rejects hallucinated responsibilities. Acts as a strict ATS parser. Forces `pathos` to rewrite if it fails the audit.

## Current State & Next Steps
- **Completed:** Directory structure created (`agents/`, `skills/praxis/`, `commands/`). `README.md` (containing the science/psychology) and `model-mappings.json` have been written.
- **Next Step 1:** Write the highly concise, rule-based agent prompts for `agents/praxis-pathos.md` and `agents/praxis-logos.md`.
- **Next Step 2:** Write the orchestrator logic (`skills/praxis/SKILL.md`) that drives the `/praxis build` wizard and the `/praxis customize` loop.
- **Next Step 3:** Save core architectural rules to Strata memory under the Praxis namespace.