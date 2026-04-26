import json

kb_path = "/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json"

with open(kb_path, 'r') as f:
    data = json.load(f)

# Add Cognilogical as an experience entry
cognilogical_experience = {
    "company": "Cognilogical (Open Source AI Research Organization)",
    "title": "Founder & Principal AI Researcher",
    "dates": "Apr 2026 - Present",
    "location": "Open Source",
    "bullets": [
        "Founded and lead Cognilogical, an open-source organization dedicated to advancing autonomous AI agent capabilities, adversarial validation, and cognitive memory architectures.",
        "Engineered NeuroStrata, a Cognitive Memory Architecture for Agents written in Rust, featuring a specialized 3-tier memory namespace (Global, Domain, Task) and vector search capabilities.",
        "Architected NeuroCortex, a Cognitive Deterministic Engine (CDE) built in Rust that provides adversarial feedback to reduce LLM agent hallucinations by up to 90%.",
        "Developed NeuroPlasticity, a Self-Reinforced Testing Framework (SRTF) in Rust for AI agents to self-learn and validate behaviors.",
        "Created NeuroGenesis, an AI Architecture Compiler (AAC) shell script that scaffolds customized adversarial panels chaired by evidence-backed agent specialists."
    ]
}

# Insert at the top of experience
data["experience"].insert(0, cognilogical_experience)

# Update projects with newly found repos that are not already there
existing_project_urls = {p["url"] for p in data["projects"]}

new_projects = [
    {
        "name": "Parallax",
        "description": "Causally Aligned Distributed Systems",
        "url": "https://github.com/ksmeltzer/Parallax",
        "dates": "Apr 2026 - Present"
    },
    {
        "name": "NeuroStrata",
        "description": "Cognitive Memory Architecture for Agents. A Retrieval-Augmented Generation (RAG) and vector database solution for AI memory.",
        "url": "https://github.com/Cognilogical/NeuroStrata",
        "dates": "Apr 2026 - Present"
    },
    {
        "name": "NeuroCortex",
        "description": "Cognitive Deterministic Engine (CDE) in Rust, providing adversarial feedback to reduce LLM agent hallucinations by up to 90%.",
        "url": "https://github.com/Cognilogical/NeuroCortex",
        "dates": "Apr 2026 - Present"
    },
    {
        "name": "NeuroPlasticity",
        "description": "Self-Reinforced Testing Framework (SRTF) in Rust for AI Agents, enabling self-learning and self-reinforcing capabilities.",
        "url": "https://github.com/Cognilogical/NeuroPlasticity",
        "dates": "Apr 2026 - Present"
    },
    {
        "name": "NeuroGenesis",
        "description": "An AI Architecture Compiler (AAC) skill that scaffolds customized adversarial panels chaired by evidence-backed agent specialists.",
        "url": "https://github.com/Cognilogical/NeuroGenesis",
        "dates": "Apr 2026 - Present"
    }
]

for p in new_projects:
    if p["url"] not in existing_project_urls:
        data["projects"].insert(0, p)

# Add Rust to skills since most Cognilogical repos use Rust
if "Rust" not in data["skills"]["Languages"]:
    data["skills"]["Languages"].append("Rust")

with open(kb_path, 'w') as f:
    json.dump(data, f, indent=2)

print("Knowledge base updated successfully.")
