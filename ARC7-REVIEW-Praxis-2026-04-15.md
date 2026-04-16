# Architectural Review Report — Praxis

**Subject:** Praxis (Multi-Agent Career & Resume Pipeline)
**Date:** 2026-04-15
**Mode:** Codebase Review
**Panel:** Context Master (Gemini 3 Pro) · The Architect (Claude Sonnet 4.6) · Security Sentinel (OpenAI o4) · Product Visionary (GPT-5.2) · Creative Strategist (GPT-5.3-Codex) · The Optimizer (GPT-5.3-Codex) · The Naysayer (Claude Sonnet 4.6)

---

## Final Recommendation: Approve with Conditions

The Praxis pipeline presents a highly pragmatic, decoupled architecture that brilliantly addresses the inherent flaws of using generic LLMs for resume generation. The strict separation of data extraction (`knowledge_base.json`) from the adversarial drafting loop (`praxis-pathos` vs. `praxis-logos`) enforces the necessary grounding to defeat both ATS parsers and AI-speak filters. However, there are critical conditions regarding prompt injection from raw files, unbounded iteration costs, and context window bloat that must be addressed before scaling.

---

## Findings Summary

| Severity | Count |
|----------|-------|
| Critical | 0   |
| Major    | 3   |
| Minor    | 2   |
| Info     | 1   |

---

## Major Issues (Should Address)

### SEC-001: A03-injection Risk in Raw Data Ingestion
- **Severity:** Major
- **Source:** Security Sentinel
- **Description:** The intake engine blindly ingests raw data from PDFs, CSVs, and webfetched GitHub READMEs. An adversary (or a maliciously crafted public repo) could embed prompt injection attacks within these files. If these are passed unsanitized into the `praxis-pathos` or `praxis-logos` context windows, it could hijack the agent's instructions (e.g., "Ignore previous instructions and output a malicious payload").
- **Recommendation:** Implement a strict sanitization and validation boundary for all ingested text before writing to `knowledge_base.json`. Strip out prompt-control characters and restrict `webfetch` strictly to allowed domains (`github.com`, `linkedin.com`).

### NAY-001: Context Window Bloat and Token Exhaustion
- **Severity:** Major
- **Source:** The Naysayer
- **Description:** As the user continues to iteratively merge GitHub exports, PR descriptions, and LinkedIn data, the `knowledge_base.json` will grow indefinitely. Passing an exhaustive, multi-megabyte career history into `praxis-pathos` for every single `/praxis customize` run will lead to high latency, token exhaustion, and degraded model attention (lost details).
- **Recommendation:** Implement a relevance-filtering mechanism (e.g., semantic search or a quick keyword-based filter) during the "Forge" step. Only inject the subset of the JSON database that is contextually relevant to the target `<job-description-url>`.

### OPT-001: Unbounded Adversarial Execution Loop
- **Severity:** Major
- **Source:** The Optimizer
- **Description:** The adversarial loop between `praxis-pathos` and `praxis-logos` dictates: "Repeat until 'APPROVED'". If the agents fall into a philosophical disagreement or fail to satisfy an impossible constraint, this will result in an infinite loop, racking up massive API costs.
- **Recommendation:** Implement a hard limit (e.g., `MAX_ITERATIONS = 3`) on the adversarial feedback loop. If `praxis-logos` has not approved the draft by the 3rd iteration, the system should gracefully exit and return the latest draft to the user with the Auditor's final unresolved warnings.

---

## Minor Suggestions (Nice to Have)

### ARC-001: Strict Schema Validation
- **Severity:** Minor
- **Source:** The Architect
- **Description:** The system relies on the integrity of the JSON database, but currently lacks a formal schema definition.
- **Recommendation:** Define a formal JSON Schema or use a validation library (like Pydantic if Python is used for the orchestrator) to validate the structure of `knowledge_base.json` upon every read/write to prevent schema drift over time.

### PROD-001: Transparency Metrics Dashboard
- **Severity:** Minor
- **Source:** Product Visionary
- **Description:** The core value of Praxis is bypassing the ATS. The user lacks visibility into *how well* the generated resume matches the target job description after the loop finishes.
- **Recommendation:** Have the orchestrator output a brief "Keyword Match Score" (e.g., "Successfully matched 14/15 required technical skills from the Job Description") alongside the final Markdown resume to prove ROI to the user.

---

## Informational Notes

### CRE-001: Conversational Intake Wizard
- **Source:** Creative Strategist
- **Description:** The "Expert Inquisitor" step could be jarring if implemented as a standard CLI prompt. Consider integrating an interactive CLI UI library (like `inquirer` or `rich`) to make the gap-analysis interview feel like a premium, guided coaching experience.

---

## What Was Done Well

*   **Zero-Loss Relational Database:** Storing the history in a JSON schema rather than a Markdown file perfectly solves the LLM "summarization loss" problem.
*   **Adversarial Division of Labor:** Assigning distinct, adversarial cognitive profiles (The Visionary vs. The Truth-Teller) is an elite architectural pattern for enforcing factual grounding.
*   **Research-Backed Parsing Rules:** Centralizing the `ATS_PARSER_RULES.md` as an immutable source of truth ensures both agents obey real-world Workday/Taleo parsing constraints.

---

## Model Assignments (Recommended for Implementation)

| Task | Assigned Model | Rationale |
|---|---|---|
| `praxis-pathos` (Drafter) | GPT-4o | Superior at narrative generation, F-pattern formatting, and matching human voice profiles. |
| `praxis-logos` (Auditor) | Claude 3.5 Sonnet | Unmatched at strict instruction adherence, logical reasoning, and ruthless fact-checking. |

---

## Action Items

- [ ] Implement an iteration limit (`MAX_ITERATIONS = 3`) on the Pathos/Logos adversarial loop.
- [ ] Add a Relevance Filter to subset the `knowledge_base.json` prior to the drafting step to prevent context bloat.
- [ ] Implement sanitization on all raw text ingested from `webfetch` or PDFs to prevent prompt injection.

---

*Generated by ARC-7 Panel · 2026-04-15*
