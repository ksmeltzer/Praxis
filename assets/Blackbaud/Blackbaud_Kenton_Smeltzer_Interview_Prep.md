# Interview Prep: Blackbaud - Sr Principal Software Engineer, GenAI

## 1. Role Overview
**Company:** Blackbaud
**Title:** Sr Principal Software Engineer, GenAI
**Key Focus:** Lead the design and implementation of Generative AI capabilities across Blackbaud's platform. This role requires a strong mix of traditional Microsoft stack expertise (C#, .NET Core, SQL Server, Cosmos DB) and modern GenAI application skills (LLMs, Prompt Engineering, RAG). The front-end leans towards Angular and TypeScript in a cloud-first (Azure/AWS) Agile environment.

## 2. The Story Arc
**Your Narrative:** You are a seasoned architect who bridges the gap between legacy enterprise systems and bleeding-edge GenAI. You have over a decade of experience deeply rooted in the C#/.NET ecosystem, but over the last several years, you have successfully pivoted into GenAI, creating robust multi-agent frameworks (Cognilogical) and driving massive cloud transformations (AccessUSA). You don't just "plug in APIs"; you build deterministic boundaries around non-deterministic AI (NeuroCortex, ARC-7) to ensure safety and scale in enterprise products.

## 3. Talking Points (Mapped to JD)

| JD Requirement | Your Experience & Talking Point |
| :--- | :--- |
| **GenAI & LLM Optimization** | Discuss your work at Cognilogical. Explain how you built Strata and NeuroCortex to manage LLM hallucinations via adversarial feedback. Mention RAG implementation via NeuroStrata. |
| **C# & .NET Core** | Detail your experience at AccessUSA transitioning legacy monoliths to .NET Core microservices using the Strangler Fig pattern. Emphasize your depth in modern C# patterns. |
| **Angular & TypeScript** | Discuss full-stack leadership at AccessUSA, standardizing front-end architecture using Angular, TypeScript, and RxJS to consume the new RESTful APIs. |
| **Cloud (Azure) & Cosmos DB** | Highlight the AccessUSA cloud transformation. Explain the strategy behind using Cosmos DB for high-throughput unstructured data and Azure SQL/Service Bus for transactional integrity. |
| **Agile & Continuous Delivery** | Emphasize your role in establishing CI/CD pipelines and leading Agile pods to deliver features with zero downtime during the monolith migration. |

## 4. Anticipated Technical Questions & Rehearsed Answers

**Q: How do you handle hallucinations and non-determinism in GenAI applications within an enterprise context?**
*Answer Strategy:* Bring up NeuroCortex and ARC-7. Explain your philosophy: "We build deterministic software boundaries around non-deterministic AI." Discuss adversarial feedback loops, strict system prompts, and using smaller models for evaluation alongside larger models for generation.

**Q: Can you describe a time you migrated a legacy monolith to a modern architecture?**
*Answer Strategy:* The AccessUSA Strangler Fig story. Talk about the "RTO Cleanup". Explain how you routed traffic through an API Gateway, slowly carving out domains (Domain-Driven Design) into .NET Core microservices without stopping the business.

**Q: How would you architect a RAG system on Azure for our customers' data?**
*Answer Strategy:* Detail the pipeline: Azure Document Intelligence for parsing -> Chunking strategy -> Embedding model -> Vector Database (e.g., Azure AI Search or Cosmos DB Vector) -> LLM orchestration. Mention handling access controls so customers only see their own vector data.

## 5. Strategic Questions for the Interviewers

1. **AI Strategy:** "Blackbaud holds highly sensitive non-profit and donor data. What is the organization's current strategy regarding data privacy when routing context to LLMs? Are you self-hosting models or using Azure OpenAI with VNET isolation?"
2. **Current Architecture:** "To what extent are the current core platforms decoupled? As you integrate GenAI, are you building centralized AI microservices, or distributing the AI logic out to the edge of each product domain?"
3. **Success Metrics:** "For this specific role, what does success look like in the first 6 months? Are we trying to prove a GenAI concept, or scale an existing prototype into production?"
