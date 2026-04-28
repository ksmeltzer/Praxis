# 🧪 Praxis: Testing Methodology & Model Selection

Praxis employs a deterministic, adversarial testing methodology to evaluate and select foundation models for specialized agent roles. Generating a mathematically honest, highly formatted, ATS-compliant resume that survives strict parsing rules is a surprisingly rigorous task for Large Language Models.

To ensure reliability, we utilize **[NeuroPlasticity](https://github.com/Cognilogical/NeuroPlasticity)**—a Self-Reinforced Testing Framework (SRTF)—to run **Adversarial Waterfall Tests** against various model architectures.

---

## Our Testing Methodology

### 1. The Adversarial Waterfall

Rather than relying on qualitative vibe checks, Praxis subjects every model to a strict pass/fail execution loop inside an ephemeral Docker sandbox (`node:20-slim`).

1. The orchestrator feeds the model a mock Job Description and the comprehensive `knowledge_base.json`.
2. The model generates a targeted resume using the **Two-Pass Methodology** (Extraction -> Tailoring).
3. The output is parsed by a deterministic validation script (`evaluate_resume.js`) that checks for dropped facts, hallucinated headers, skill limits (max 20), missing patents, and first-person pronouns.

### 2. The Baby Seal Validation Loop

If the output fails validation, the script throws explicit errors (e.g., `Missing patents: Found 0, expected 1`). The model must read these errors, self-correct its markdown file, and trigger a re-run. If a model fails repeatedly across multiple testing epochs, it is mathematically disqualified for that persona.

---

## Model Classes & Evaluation Results

Through extensive NeuroPlasticity testing, we evaluated distinct model architectures to determine the optimal engine for each Praxis persona.

### 1. Reasoning & Coding Models (e.g., o1-preview)

* **The Hypothesis:** Highly logical models would excel at mapping skills and adhering to complex JSON schemas.
* **The Reality (FAILED):** Total cognitive collapse on strict formatting tasks. Reasoning models are trained to optimize code and solve abstract logic puzzles. When given a rigid Markdown template and commanded, *"Do not drop the patent, limit skills to 20, and follow these ATS headers,"* they over-analyze the prompt. They attempt to "optimize" the resume by aggressively filtering out "inefficient" data, blatantly ignoring formatting constraints. They struggle when the objective requires robotic adherence to a design template rather than solving an optimization problem.

### 2. Mini & Lightweight Models (e.g., GPT-4o-Mini, Claude 3.5 Haiku)

* **The Hypothesis:** Fast, cost-effective models would be ideal for rapid drafting.
* **The Reality (FAILED):** Severe context window degradation. Praxis requires the model to simultaneously process the `knowledge_base.json`, the user's `voice_profile`, ATS rules, formatting templates, and the target Job Description. Lightweight models suffer from "lost in the middle" syndrome; they successfully tailor bullet points but completely omit critical trailing sections like Education or Certifications.

### 3. Frontier Interaction Models (GPT-4o vs. Claude 3.5 Sonnet)

We pitted the two leading frontier models against each other for the role of **`praxis-pathos` (The Drafter)**.

* **GPT-4o (FAILED):** Suffered from "negative constraint collapse." As we added more negative constraints to the system prompt (e.g., *"Do NOT use custom headers," "Do NOT drop portfolio links"*), GPT-4o's RLHF training overrode its instructions. It stubbornly hallucinated custom headers (e.g., `## Professional Summary` instead of `## Summary`) and aggressively filtered out facts it deemed irrelevant to the job description, violating explicit instructions.
* **Claude 3.5 Sonnet (PASSED):** Mastered the Two-Pass methodology. Anthropic models exhibit famously robust XML/Markdown template adherence. Claude successfully ingested the rigid template, executed the self-healing validation loop, read its own errors, and iteratively fixed the markdown until achieving 100% compliance. It never hallucinated headers and preserved all mandatory facts.

---

## Final Architectural Mandate

Based on the empirical data from the NeuroPlasticity Waterfall:

1. **The Drafter (`praxis-pathos`) MUST use a Claude Sonnet model.** It is the only architecture that reliably survives strict markdown constraints, adheres to ATS parser rules without hallucinating custom headers, and executes the Two-Pass methodology without dropping facts.
2. **The Auditor (`praxis-logos`) & Orchestrator can use GPT-4o.** GPT-4o excels at advanced reasoning, web fetching (for deep research), and critical analysis. It is highly effective as the ruthless auditor that validates Claude's output against the schema.
