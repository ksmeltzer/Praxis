# ADR-002: Agent Prompt Rewrite Plan

Based on The Architect's review, we will implement the following changes to the Praxis agents.

## 1. praxis-pathos (The Drafter)
- **Add Principal Positioning Doctrine**: Invert tailoring. The resume must preserve the candidate's strongest technical gravity and "spiky" differentiators. It must signal scarcity and gravitational pull, not supplication.
- **Add Six-Second Scan Rule**: Bullets must be terse, declarative, and metric-first. No semicolon chains. Max ~25 words.
- **Modify Voice Compliance**: Match perspective, tone, and vocabulary, but DO NOT preserve compound sentence structures that kill scannability. Terse syntax overrides verbose voice profiles.
- **Modify Skill Curation**: Increase visual cap to 15-25. Must include explicit Boolean ATS aliases (e.g., "Docker" explicitly, not just implying it via "Kubernetes") if grounded in the KB.

## 2. praxis-logos (The Auditor)
- **Add Positioning Audit Axis**: Reject drafts that overfit the JD, bury strong differentiators, or sound like a mid-level "compliant candidate".
- **Add Six-Second Scan Audit**: Reject dense paragraphs or metrics buried at the end of long sentences.
- **Add Boolean ATS Keyword Audit**: Verify explicit ATS-searchable aliases exist in text.
- **Modify Voice Enforcement**: Stop treating the user's verbose "sentence_structure" as law. Scanability overrides verbosity.

## 3. RESUME_TEMPLATE.md
- **Fix the ATS Collapse Bug**: Remove single-line `Company | Title | Date` formatting. Use multi-line headers.
- **Fix Headline**: Remove `## [basics.headline]` formatting which fails ATS headers. Use plain text.
