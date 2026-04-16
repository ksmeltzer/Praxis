# Praxis Architecture: ATS & Parser Survival Guidelines

This document outlines the research-backed guidelines that `praxis-pathos` (Drafter) and `praxis-logos` (Auditor) MUST follow to ensure the generated resumes bypass automated Applicant Tracking Systems (ATS) like Workday, Taleo, Greenhouse, and iCIMS, as well as human AI-fatigue filters.

## 1. The "Invisible Data" Problem (Structural Parsing)
**Research Fact:** Older enterprise ATS systems (Taleo, SAP) use basic Optical Character Recognition (OCR) or naive PDF text extraction that reads strictly left-to-right, top-to-bottom.
*   **Rule:** **Zero Columns or Tables.** Never use a two-column layout. When a parser reads a two-column layout left-to-right, it interleaves the experience text with the skills column, resulting in garbled, unparseable data.
*   **Rule:** **No Text Boxes or Graphics.** Text inside shapes, progress bars, or skill "meters" is completely dropped by 70% of parsers.

## 2. The "Zero Experience" Bug (Regex Failures)
**Research Fact:** Parsers calculate total years of experience using regular expressions (Regex) targeting section headers and date formats. If the Regex fails, the candidate is automatically binned for "lack of experience."
*   **Rule:** **Standardized Section Headers Only.** You must use exact, standard strings: `Experience`, `Education`, `Skills`, `Projects`. Do NOT use creative headers like "My Journey", "Professional History", or "What I've Built". The parser will fail to find the section.
*   **Rule:** **Strict Chronological Date Formatting.** Dates must follow `Month YYYY - Month YYYY` (e.g., `Jan 2020 - Dec 2023`) or `MM/YYYY - MM/YYYY`. Do not use seasons ("Summer 2021") or bare years ("2020 - 2023") as some ATS systems default to January 1st, shortchanging the candidate's experience calculation.

## 3. The Keyword Disconnect (Lexical vs. Semantic Search)
**Research Fact:** While modern ATS (Greenhouse) uses semantic search, enterprise legacy systems still use exact-match Boolean queries.
*   **Rule:** **Acronym Expansion.** The first time a critical technology is mentioned, use the full name and the acronym: `Amazon Web Services (AWS)`, `Google Cloud Platform (GCP)`. This guarantees a hit regardless of which term the recruiter queried.
*   **Rule:** **Contextual Keyword Placement.** Do not just dump a comma-separated list of skills at the bottom. ATS systems rank candidates higher if the keyword appears *within the context of an experience bullet point* (e.g., "Deployed Node.js microservices..." vs just "Node.js" in a skills dump).

## 4. The Human-in-the-Loop AI Filter (Recruiter Fatigue)
**Research Fact:** Once a resume passes the ATS, it faces a recruiter who spends an average of 6-7 seconds scanning it. Since 2023, recruiters aggressively bin resumes containing "ChatGPT vocabulary" due to perceived lack of authenticity and effort.
*   **Rule:** **Banish AI Signifiers.** Completely ban the following words: `delve, spearhead, tapestry, testament, revolutionized, synergistic, unleashed, navigating the complexities, realm, landscape`.
*   **Rule:** **Data-Dense F-Pattern.** Recruiters scan the left side of the page (F-Pattern). Start every bullet with a high-agency, concrete verb (`Architected`, `Scaled`, `Migrated`, `Reduced`), immediately followed by the hard metric or noun.

## 5. The "Implied Scale" Rejection
**Research Fact:** Technical hiring managers reject resumes that list responsibilities without scale. "Managed a database" is a junior task; "Managed a 50TB distributed PostgreSQL cluster" is a senior task.
*   **Rule:** Never allow an unquantified responsibility if the `knowledge_base.json` contains the metric. If the database lacks the metric, `praxis-logos` must reject the bullet and trigger the Expert Inquisitor wizard to ask the user for the scale.

## 6. Voice Authenticity (The Uncanny Valley Filter)
**Research Fact:** Recruiters and hiring managers increasingly detect AI-generated resumes not just by banned vocabulary (Section 4), but by tonal inconsistency — the resume "sounds" different from the candidate's cover letter, LinkedIn profile, or interview speech. A resume that reads like a generic LLM output gets binned even if the keywords are perfect.
*   **Rule:** **Voice Profile Compliance.** All generated text MUST conform to the applicant's `voice_profile` stored in `knowledge_base.json`. This profile is extracted from their raw source materials during the Refinement Protocol and captures their natural perspective, tone, sentence structure, vocabulary tendencies, and avoidances.
*   **Rule:** **Sample Fragment Calibration.** Before generating any text, `praxis-pathos` must read the `voice_profile.sample_fragments` array to internalize the applicant's actual phrasing patterns. Generated bullets should be indistinguishable from the applicant's own writing.
*   **Rule:** **Voice Violation = Rejection.** `praxis-logos` must flag any generated sentence that deviates from the voice profile. A factually correct bullet that sounds like an LLM wrote it is treated as a defect equal in severity to a hallucination. The drafter must rewrite it in the applicant's voice before the resume can be approved.

## 7. Spelling & Grammar (The Credibility Floor)
**Research Fact:** A single spelling or grammar error on a resume causes 77% of hiring managers to immediately disqualify the candidate (CareerBuilder survey). ATS systems do not catch these — they pass misspelled keywords silently, meaning "Kuberentes" won't match a "Kubernetes" filter and the candidate is ghosted without knowing why.
*   **Rule:** **Full Proofread on Every Output.** `praxis-logos` MUST perform a complete spelling and grammar audit on every draft before it can be approved. This includes:
    - Spelling of all technology names, company names, and proper nouns (e.g., "PostgreSQL" not "Postgresql", "Salesforce" not "SalesForce", "Node.js" not "NodeJS")
    - Grammar: subject-verb agreement, tense consistency (bullets should use past tense for completed roles, present tense for current roles), dangling modifiers
    - Punctuation: consistent use of periods (or not) at the end of bullets, correct em-dash vs hyphen usage, serial comma consistency
    - Capitalization: job titles, section headers, technology names
*   **Rule:** **Spelling/Grammar Error = Rejection.** Any spelling or grammar error is treated as a blocking defect. The draft cannot be approved until all errors are resolved. This applies equally to the baseline `assets/Resume.md` from `draft.sh` and to tailored resumes from `/praxis gen`.
*   **Rule:** **Source Data Correction.** During the Refinement Protocol, `praxis-logos` must also audit the `knowledge_base.json` itself for spelling and grammar errors in bullets, summaries, and descriptions. Errors in the source data propagate to every generated resume. Flag corrections for user approval before writing.

## 8. ATS Market Landscape (Data-Driven Targeting)
**Source:** Jobscan 2025 ATS Usage Report; Resume Genius 2026 Hiring Manager Survey.
*   **Fact:** 97.8% of Fortune 500 companies use a detectable ATS. The remaining 2.2% likely use proprietary in-house systems.
*   **Fact:** Workday dominates Fortune 500 at 39%+ market share. SuccessFactors is second at 13.2%. Taleo is declining; iCIMS is enduring.
*   **Fact:** Outside the Fortune 500, the landscape is more fragmented: Greenhouse (19.3%), Lever (16.6%), Workday (15.9%), iCIMS (15.3%).
*   **Fact:** 71% of hiring managers confirm their company uses an ATS. 37% say their ATS screens out applications before a human ever sees them.
*   **Rule:** **Assume ATS by Default.** Every resume Praxis generates must be ATS-optimized. There is no scenario where "design-first" is acceptable for the primary submission format.
*   **Rule:** **Workday-First Testing.** When in doubt about a formatting choice, optimize for Workday's parser since it processes the plurality of enterprise applications.

## 9. Resume Length & Format Preferences (Recruiter Data)
**Source:** Resume Genius 2026 Hiring Manager Survey.
*   **Fact:** 54% of hiring managers prefer two-page resumes. 43% will not read past two pages. 20% say overly long/dense resumes prevent candidates from advancing.
*   **Fact:** 53% prefer text-based PDF for ATS compatibility. 43% favor Word (.docx). Only 13% say design-heavy resumes work well with ATS.
*   **Fact:** 57% of hiring managers spend 1-3 minutes reviewing a resume. 25% spend less than 30 seconds.
*   **Fact:** 62% say overly designed resumes (excessive color/visuals) hurt their perception. 72% say inconsistent spacing/formatting/alignment negatively affects perception.
*   **Rule:** **Two-Page Target.** For candidates with 5+ years of experience, target exactly two pages. For junior candidates, one page is acceptable. Never exceed two pages.
*   **Rule:** **Text-Based PDF Output.** The primary output format must be a clean, text-based PDF (or Markdown that converts cleanly). No graphics, progress bars, color blocks, or multi-column layouts.
*   **Rule:** **Front-Load Impact.** Given the 30-second to 3-minute scan window, the top third of page one must contain: name, title, summary, and the most recent/impressive role. Every second of recruiter attention is finite.

## 10. Resume Sections & Content Priority (What Hiring Managers Actually Read)
**Source:** Resume Genius 2026 Hiring Manager Survey.
*   **Fact:** 90% say a clear resume summary helps them evaluate candidates faster. 42% rank the introduction in the top three most important sections. 20% say it is the single most critical section.
*   **Fact:** 85% expect every resume to include a skills section.
*   **Fact:** 34% say an unclear or incomplete work history section can prevent advancement.
*   **Fact:** 42% say missing required skills or poor role alignment prevents advancement — the #1 content-based rejection reason.
*   **Fact:** 28% say lack of relevant keywords stops a resume. 30% say applicants don't provide concrete evidence for listed skills. 22% say candidates list too many or too few skills.
*   **Rule:** **Summary is Mandatory.** Every Praxis resume must open with a 2-4 sentence professional summary that is tailored to the target role. This is the highest-leverage real estate on the document.
*   **Rule:** **Skills Must Have Evidence.** Never list a skill in the Skills section that doesn't appear contextually in at least one experience bullet. Orphaned skills trigger recruiter skepticism (30% flag this).
*   **Rule:** **Keyword Density via Context.** Role-specific keywords from the job description must appear within experience bullets, not just in a skills dump. ATS systems and recruiters both rank contextual keyword placement higher than list-only placement (see Section 3).

## 11. AI Detection & Authenticity (The 2026 Trust Crisis)
**Source:** Resume Genius 2026 Hiring Manager Survey.
*   **Fact:** 77% of hiring managers say many resumes feel completely or partially AI-generated.
*   **Fact:** 80% say they can often tell when a resume was written by AI. Only 4% say they don't notice signs of AI use.
*   **Fact:** 79% believe candidates should disclose AI assistance.
*   **Fact:** 76% say AI-written resumes make it harder to tell who's qualified. 72% say heavy AI reliance makes candidates seem less capable.
*   **Fact:** The top giveaways that a resume is AI-generated: unnatural phrasing/tone (51%), repetitive/generic language (44%), vague/inflated descriptions (41%), buzzword-heavy writing (41%).
*   **Fact:** However, 59% say AI use shows adaptability, 51% say it shows efficiency — so the issue is *how* AI is used, not *whether* it is used.
*   **Rule:** **Zero Tolerance for AI Tell-Signs.** `praxis-logos` must specifically audit for the four giveaways: (1) unnatural phrasing, (2) repetitive/generic language, (3) vague/inflated descriptions, (4) buzzword density. Any bullet exhibiting these traits is rejected.
*   **Rule:** **Specificity Over Polish.** A slightly rough but specific bullet ("Cut deploy time from 45min to 8min by rewriting the CI pipeline in GitHub Actions") always beats a polished but vague one ("Significantly improved deployment efficiency through innovative CI/CD optimization"). The former reads human; the latter reads AI.
*   **Rule:** **Voice Profile is the AI Antidote.** The voice_profile (Section 6) is the primary defense against AI detection. A resume that authentically sounds like the candidate cannot be flagged as AI-generated because it *isn't* generic — it's their voice with their specifics. This is Praxis's core competitive advantage.

## 12. Certifications, Education & Alternative Credentials
**Source:** Resume Genius 2026 Hiring Manager Survey.
*   **Fact:** 86% say relevant work experience matters more than education.
*   **Fact:** 82% say certifications can be as valuable as a degree.
*   **Fact:** 62% say bootcamps can qualify candidates for many roles.
*   **Fact:** 76% say self-taught skills and portfolio work can outweigh formal education.
*   **Fact:** 72% say degree level still matters in their hiring decisions. 65% say a master's degree justifies higher pay.
*   **Rule:** **Experience-First Ordering.** Always place Work Experience before Education unless the candidate is entry-level with no relevant experience.
*   **Rule:** **Certifications as Degree Equivalents.** When a candidate lacks a traditional degree, prominently feature certifications and portfolio projects. These are not consolation prizes — 82% of hiring managers view them as equivalent.
*   **Rule:** **GitHub/Portfolio as Proof.** For technical roles, link to the candidate's GitHub or portfolio. 76% of hiring managers say self-taught skills with proof outweigh formal education.

## 13. First-Person Pronoun Prohibition
**Research Fact:** Resume convention universally expects implied first person ("Designed the system") rather than explicit first person ("I designed the system"). First-person pronouns waste space, are redundant (it's your resume — "I" is implied), and read as informal or unseasoned to hiring managers. ATS parsers strip pronouns as noise, adding zero keyword value.
*   **Rule:** **No First-Person Pronouns.** Never use "I", "me", "my", "we", or "our" in any generated resume text — bullets, summaries, or section content. All sentences must use implied first person.
*   **Rule:** **Source Data Rewriting.** During the Refinement Protocol, if `knowledge_base.json` contains bullets or summaries written in explicit first person (common when imported from LinkedIn), `praxis-logos` must flag them and propose rewrites that drop the pronoun while preserving meaning.
*   **Rule:** **Drafter Enforcement.** `praxis-pathos` must never draft a sentence beginning with or containing a first-person pronoun. `praxis-logos` must reject any draft containing first-person pronouns as a blocking defect equal in severity to a spelling error.
