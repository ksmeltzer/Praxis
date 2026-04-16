# Praxis Developer Handoff & Architecture Guide

**ATTENTION NEXT AI AGENT:** Read this document carefully before making ANY changes. The previous development session was highly chaotic and resulted in significant architectural thrashing. This document serves as the absolute source of truth for the project's constraints, architecture, and historical mistakes to avoid.

## 1. Project Overview
Praxis is an adversarial, multi-agent career knowledge base and resume generation pipeline. It ingests raw career data (text resumes, LinkedIn CSV exports), merges them into a structured JSON knowledge base, and uses specialized AI personas (ARC-7/Pathos/Logos) to dynamically generate highly tailored, ATS-compliant markdown and PDF resumes.

## 2. Core Directives & Constraints (NON-NEGOTIABLE)
*   **NO PYTHON:** The environment strictly forbids Python scripts for pipeline execution.
*   **NO BRITTLE PARSERS:** Do NOT write imperative scripts (Node.js, Bash regex, awk) to parse human text, fuzzy match companies, or resolve dates. Use the Orchestrator LLM's native cognitive capabilities to read raw text and output structured JSON.
*   **GLOBAL VS LOCAL SYNC:** The skill definition lives in `./skills/praxis`. It MUST remain symlinked to `~/.config/opencode/skills/praxis`. **Never copy files back and forth.** If you break the symlink, the terminal command will drift from the local codebase.
*   **CLEAN WORKSPACE:** All generated artifacts MUST go into `assets/`. All raw sources MUST be moved to `.praxis/sources/`. The root directory must remain clean. Ephemeral config files (like `.md-to-pdf.js` to disable the Chrome sandbox) must be created and immediately deleted during generation.

## 3. Pipeline Architecture
The core command is `/praxis` (formerly `/praxis build`), which triggers the ingestion pipeline.

### Step 1: Data Gathering (`skills/praxis/scripts/ingest.sh`)
*   A pure bash orchestrator script.
*   Finds all `*.txt` (resumes), extracts LinkedIn `*.zip` exports to find `Positions.csv`, `Skills.csv`, and `Profile.csv`.
*   Concatenates all of this raw, messy data into `.praxis/sources/raw_context.txt`.
*   Moves the source files into `.praxis/sources/` for backup.

### Step 2: LLM-Native Ingestion (Agentic Task)
*   The Orchestrator LLM reads `.praxis/sources/raw_context.txt`.
*   The LLM is responsible for deducing company name overlaps (e.g., "The Lowbush Company" vs "Lowbush Company"), merging bullet points, and resolving date discrepancies.
*   The LLM writes the final structured state to `.praxis/data/knowledge_base.json`.

### Step 3: Github Sync (`skills/praxis/scripts/github_sync.sh`)
*   Bash script using `jq` to append GitHub projects to the `knowledge_base.json`.

### Step 4: Drafting (`skills/praxis/scripts/draft.sh`)
*   Reads `knowledge_base.json` via `jq`.
*   Generates a baseline `assets/Resume.md`.

## 4. Other Commands (Handled via Bash + JQ)
*   `/praxis history <fact>`: Appends a single bullet point to a specific company in the JSON database using `skills/praxis/scripts/history.sh`.
*   `/praxis skill <name> <desc>`: Enriches a skill with evidence in the JSON database using `skills/praxis/scripts/skill.sh`.
*   `/praxis gen <url>`: Triggers the adversarial loop to generate a highly tailored `assets/{Company}_{Name}_Resume.pdf`.

## 5. Post-Mortem of Previous Mistakes (DO NOT REPEAT)
1.  **Over-engineering Parsers:** The previous agent wasted hours writing a 150-line Node.js script (`ingest_all.js`) to manually parse CSVs, strip "Inc/LLC", and merge arrays. This was brittle and failed edge cases. **Fix:** Replaced with `raw_context.txt` + LLM native extraction.
2.  **Command Drift:** The previous agent updated `SKILL.md` locally but forgot the global `~/.config` file, causing the `/praxis` command to fail because the system was still expecting `/praxis build`. **Fix:** Established a hard symlink. Do not break it.
3.  **Ghost Files:** The agent left 700-byte stub ZIP files and `.md-to-pdf.js` files cluttering the root directory. **Fix:** Ensure strict cleanup protocols in all scripts.
