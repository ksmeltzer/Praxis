import json

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "r") as f:
    data = json.load(f)

data["projects"] = [
    {
      "name": "Strata: Cognitive Architecture & High-Performance MCP Server",
      "description": "An open-source, production-grade Model Context Protocol (MCP) server written in native Go. It solves LLM context degradation by acting as a 'long-term memory' layer for AI agents, utilizing Qdrant vector databases, Nomic embeddings, and a specialized 3-tier memory namespace (Global, Domain, Task).",
      "url": "https://github.com/ksmeltzer/strata",
      "dates": "Jan 2026 - Present"
    },
    {
      "name": "Allele",
      "description": "An open-source project exploring genetic algorithms applied to advanced trading systems, demonstrating the intersection of evolutionary computation and financial modeling.",
      "url": "https://github.com/ksmeltzer/Allele"
    }
]

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "w") as f:
    json.dump(data, f, indent=2)
