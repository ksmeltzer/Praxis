<div align="center">
  <img src="docs/assets/logo.png" alt="Praxis - AI Multi-Agent Resume Builder and Career Knowledge Base" width="300" />
</div>

# 🚀 Praxis: Getting Started Guide

Welcome to Praxis. This guide will walk you through building your permanent Career Knowledge Base from scratch and forging your first hyper-targeted resume.

---

## Phase 1: Gather Your Raw Data

Praxis doesn't want you to manually type out your history. It wants to consume your raw digital exhaust. The more data you feed it, the more lethal your generated resumes become.

### 1. Export Your LinkedIn Data (Crucial for Skills)
LinkedIn hides a lot of your historical skills in their backend. To ensure Praxis captures every technology you've ever endorsed:
1. Go to LinkedIn **Settings & Privacy**.
2. Click **Data privacy** > **Get a copy of your data**.
3. Select **Download larger data archive** (this includes Connections, Contacts, Account History, and most importantly, your complete **Skills** and **Recommendations** histories). 
   *Note: LinkedIn may take up to 24 hours to generate the full archive. If you are in a rush, select the second option and check "Profile", "Recommendations", and "Skills".*
4. Download the `.zip` file when it is ready.

### 2. Gather Your Resumes & Brag Documents
Find every piece of career collateral you have lying around on your hard drive:
- Your most recent PDF or Word resumes.
- Old versions of your resume (they often contain facts you cut for space).
- Performance reviews, "brag documents," or project summaries.

### 3. Stage the Files
Place the LinkedIn `.zip` export and all your PDF/text documents directly into the **`.praxis/sources/`** directory in this repository. (If the folder doesn't exist yet, simply create it).

---

## Phase 2: The Initial Ingest (Building the Database)

Fire up your AI CLI harness (OpenCode, Claude Code, GitHub Copilot) in the root of the Praxis directory.

Run the ingest command:
```bash
/praxis
```

**What happens next:**
1. Praxis will extract all the text, CSVs, and PDFs from the `.praxis/sources/` directory.
2. It will build a comprehensive `knowledge_base.json` database mapping your skills to specific companies and roles.
3. **The Interview:** The orchestrator will begin a multi-pass interview with you. It will extract your natural "Voice Profile," normalize your terminology (e.g., merging "React.js" and "React"), and ask you clarifying questions to quantify vague bullet points.

---

## Phase 3: Ad-Hoc Knowledge Updates

You don't need to do a massive file import every time you accomplish something new at work. You can update your Knowledge Base dynamically using natural language.

Run the update command:
```bash
/praxis <your text here>
```

### Best Practices for Ad-Hoc Updates
To ensure the agents accurately map your update into the database, always include:
1. **The Company/Role:** Where did this happen?
2. **The Action & Result:** What did you do and what was the impact?
3. **The Skills Used:** What specific technologies were involved?

**✅ Good Example:**
> `/praxis At DexCare, I architected a real-time event pipeline using Apache Kafka and Redis, which reduced admission latency by 40%.`

**❌ Bad Example:**
> `/praxis I built an event pipeline and saved a lot of time.` *(The agent won't know which company to attach this to, or what skills to log).*

---

## Phase 4: Targeting a Specific Job (The Forge)

When you find a job you want to apply for, do not manually edit your resume. Let Praxis forge a custom one.

Run the forge command with the URL of the job description:
```bash
/praxis https://careers.company.com/job/12345
```

**What happens next:**
1. **Deep Research:** Praxis scrapes the URL and researches the target company's core business model and industry (e.g., realizing they are a Web3 company, not just a standard tech firm).
2. **Skill Gap Interview:** If the job requires a skill you haven't explicitly listed in your database, Praxis will pause and ask: *"Did you use [Skill] at a previous company? How?"* Your answer is formatted and permanently saved to your database.
3. **Adversarial Generation:** `praxis-pathos` (The Drafter) and `praxis-logos` (The Auditor) will fight with each other to produce a mathematically honest, perfectly targeted resume designed to defeat ATS systems.

---

## Phase 5: Your Generated Assets

When the Forge is complete, Praxis will create a dedicated folder for the target company in your `assets/` directory (e.g., `assets/OpenAI/`). 

Inside this folder, you will find:
1. **`{Company}_Resume.md` & `.pdf`**: A hyper-targeted, ATS-compliant resume engineered specifically for this role.
2. **`{Company}_Cover_Letter.md` & `.pdf`**: A professional cover letter written in your exact tone of voice, addressing the company's specific pain points.
3. **`{Company}_Interview_Prep.md`**: Your secret weapon. This sheet maps your historical metrics directly to the job requirements, provides STAR-method answers for likely behavioral questions, and gives you salary negotiation strategies based on live market data.