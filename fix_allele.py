import json

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "r") as f:
    data = json.load(f)

for p in data.get("projects", []):
    if p["name"] == "Allele":
        p["description"] = "Allele is a universal execution management system and programmable genetic trading platform built to operate across diverse financial and prediction markets. It uses a pure Go, zero-CGO backend executing hot-swappable WebAssembly (.wasm) logic modules, combined with a Genetic Algorithm (GA) 'Arena' to continually evaluate, rank, and deploy 'Organisms' (strategies + parameters + environments) based on their mathematical edge."
        p["dates"] = "Jan 2026 - Present"

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "w") as f:
    json.dump(data, f, indent=2)
print("Updated Allele description.")
