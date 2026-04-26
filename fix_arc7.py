import json

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "r") as f:
    data = json.load(f)

# Check if ARC-7 is already in projects
has_arc7 = any(p.get("name") == "ARC-7" for p in data.get("projects", []))

if not has_arc7:
    data.setdefault("projects", []).append({
      "name": "ARC-7",
      "description": "ARC-7 is a tool-agnostic, multi-agent system that convenes a panel of 7 highly specialized AI personas to conduct rigorous architectural reviews. By leveraging cognitive diversity, structured adversarial debate, and ensemble learning, ARC-7 produces enterprise-grade system validation that far exceeds the capabilities of any single foundation model.",
      "url": "https://github.com/ksmeltzer/ARC-7",
      "dates": "Jan 2026 - Present"
    })
    
    with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Added ARC-7 to projects.")
else:
    print("ARC-7 already in projects.")
