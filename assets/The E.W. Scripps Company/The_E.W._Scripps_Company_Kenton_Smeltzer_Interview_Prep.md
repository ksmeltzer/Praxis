# Interview Prep: The E.W. Scripps Company - Lead AI Architect (Remote)

## Role Overview
- **Company**: The E.W. Scripps Company
- **Role**: Lead AI Architect
- **Model/Framework Focus**: MCP, LangChain/LangGraph, CrewAI, AutoGen, RAG
- **Cloud/Provider Focus**: AWS Bedrock, Azure AI, Anthropic
- **Language Focus**: Python, TypeScript/Node.js, Java
- **Security**: OWASP LLM Top 10, PII leakage, SOC 2

## Your Story Arc (Elevator Pitch)
"I'm a Lead AI Architect specializing in agentic workflows and secure generative AI integrations. Most recently, I've been heavily focused on architecting Model Context Protocol (MCP) servers and orchestrating multi-agent systems using frameworks akin to LangGraph and CrewAI for projects like Strata and ARC-7. At Voya Financial and DexCare, I scaled enterprise backend systems in Node.js and TypeScript, integrating models via AWS Bedrock and Azure AI while maintaining strict SOC 2 and OWASP LLM compliance. I'm excited about the opportunity at Scripps to design robust, secure AI architectures that drive media innovation."

## Key Talking Points mapped to JD
- **MCP & Tool Integrations**: Highlight your work building the Praxis pipeline, Strata memory tools, and ARC-7 agentic tools which inherently act as context providers and tool executors for LLMs.
- **AI Frameworks (LangChain, LangGraph, AutoGen)**: Discuss your hands-on experience designing multi-agent communication protocols and state machines (like BeadBoard and Strata's memory layers).
- **RAG & Vector DBs**: Detail your implementation of Qdrant in the Strata project for long-term memory and context retrieval. Discuss chunking strategies and semantic search optimization.
- **Cloud-hosted Models**: Reference your architectural work at Voya Financial utilizing enterprise APIs (Azure AI, AWS Bedrock, Anthropic) and managing token limits and latency.
- **Security (OWASP LLM, SOC 2)**: Emphasize your healthcare (DexCare) and financial (Voya) background. Talk about PII redaction pipelines, prompt injection defense, and secure boundary enforcement for agents.

## Anticipated Technical Questions
1. **How do you design an MCP server to expose legacy internal APIs to an LLM securely?**
   *Answer Strategy*: Discuss IAM roles, read-only vs. read-write tool separation, and human-in-the-loop (like BeadBoard's confirmation steps) for state-changing actions.
2. **Explain your approach to optimizing RAG pipelines beyond naive chunking.**
   *Answer Strategy*: Mention semantic chunking, metadata filtering (bi-directional anchors in Strata), hypothetical document embeddings (HyDE), and reranking models.
3. **Compare LangGraph and AutoGen for a multi-agent orchestration task.**
   *Answer Strategy*: Frame LangGraph as excellent for deterministic, state-machine driven flows, and AutoGen as better for conversational, emergent agent interactions.
4. **How do you prevent PII leakage when using Anthropic or OpenAI APIs?**
   *Answer Strategy*: Implement a pre-processing middleware layer (using presidio or custom NER models) to mask/tokenize PII before it hits the LLM, and unmask it in the response.

## Questions for Them
- How is the engineering organization currently structured around AI? Are AI initiatives centralized or embedded in product teams?
- What specific workflows or content pipelines at Scripps are you targeting first for AI integration?
- How are you currently managing the evaluation and testing of LLM outputs (e.g., LLM-as-a-judge, golden datasets)?
- What is the company's stance on open-source models vs. managed services (Bedrock/Azure) for future roadmap items?

## Red Flags / Areas to Probe
- **Agentic Framework Churn**: Ensure they have a clear use case for agents (LangGraph/CrewAI) and aren't just chasing the hype cycle. Ask what specific autonomous tasks they envision.
- **Security Overhead**: Clarify if the Lead AI Architect is solely responsible for LLM security, or if there is a dedicated AppSec team to partner with for SOC 2 compliance.
