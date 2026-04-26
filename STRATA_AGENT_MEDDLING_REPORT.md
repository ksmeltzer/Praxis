# ⚠️ INCIDENT REPORT: Cross-Project Agent Meddling

**To:** The `praxis` project agent / Kenton
**From:** The `strata` project agent
**Date:** April 17, 2026

## What Happened
Due to a context mix-up, Kenton accidentally asked me (the Strata agent operating out of `~/Documents/strata`) to fix an issue regarding generated resume filenames. I incorrectly assumed scope and modified Praxis configuration and output files directly without challenging the cross-project request.

## What I Modified
1. **Skill Configuration (`~/.config/opencode/skills/praxis/SKILL.md`)**:
   - I changed the output filename derivation instruction in the Forge mode workflow.
   - **Old:** `Derive filename: {Company}_{First}_{Last}_Resume`
   - **New:** `Derive filename: {TargetCompany}_{First}_{Last} (CRITICAL: {TargetCompany} MUST be the actual name of the company from the target job req, NOT the job title or category. e.g., Microsoft_Kenton_Smeltzer)`
2. **Generated Assets (`~/Documents/Praxis/assets/`)**:
   - I renamed `FullStack_Kenton_Smeltzer_Resume.pdf` to `FullStack_Kenton_Smeltzer.pdf`.

## Required Action for Praxis Agent
Please review the changes made to your `SKILL.md` file to ensure they align with your architectural standards. If the user needs the resume regenerated with the correct target company name (since "FullStack" was actually the job category/title, not the company), please re-run your Forge workflow for that specific URL.