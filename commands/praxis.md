---
description: "Adversarial, Multi-Agent Career Knowledge Base & Resume Pipeline. Usage: /praxis (ingest), /praxis <text> (add knowledge), /praxis <url> (generate tailored resume)"
---

Load the `praxis` skill using the skill tool, then dispatch based on the argument:

- No argument → **Ingest Mode** (build/rebuild knowledge base)
- Argument starts with `http://` or `https://` → **Forge Mode** (generate tailored resume for job posting)
- Any other argument → **Knowledge Mode** (parse free text and update knowledge base)

Arguments: $ARGUMENTS
