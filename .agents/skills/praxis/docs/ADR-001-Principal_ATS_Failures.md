# ADR-001: Principal Positioning & ATS Parsing Failures

## Date: 2026-05-11
## Status: Accepted / Active

### Context
A 0% response rate on ~25 tailored resumes highlighted systemic pipeline and narrative failures in the Praxis system.

### Findings
1. **ATS Structural Failure (Collapse Bug):** The `md-to-pdf` rendering combined with the `RESUME_TEMPLATE.md` single-line formatting (`Company | Title | Date`) causes PDF text extraction to collapse into a single string. ATS parsers fail to recognize years of experience, auto-rejecting the candidate.
2. **Category Error (Positioning):** Tailoring perfectly to a JD signals "supplication" (mid-level) rather than "scarcity/gravitational pull" (Principal/Staff). The resumes were over-tailored, losing the unique "spiky" technical narrative.
3. **Voice & Density (6-Second Scan):** The voice profile enforced "compound sentences and semicolons," creating dense paragraphs that fail the 6-second recruiter scan. Principal resumes need terse, declarative, metric-first bullets.
4. **Over-curation vs. Keyword Coverage:** Capping skills at 15-20 visually is fine, but failing to include explicit tech keywords (like "Docker" instead of just "Kubernetes") fails naive Boolean ATS filters.

### Decisions
- Change template to enforce multi-line job headers:
  **Company**
  Title
  Date
- Shift voice profile to terse, declarative, impact-first.
- Stop over-tailoring bullets; rely on immutable, high-impact achievements.
- Validate PDF generation with `pdftotext` extraction scripts.
- Generate alternative `.docx`/`.txt` ATS-friendly outputs.
