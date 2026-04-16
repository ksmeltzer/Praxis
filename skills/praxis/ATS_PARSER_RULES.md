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
