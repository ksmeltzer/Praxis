import json

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "r") as f:
    data = json.load(f)

# Looks like the JSON root IS the skills object based on the previous output
# Wait, let me make sure. The whole file might just be the "skills" dict.
if "Other Tools & Concepts" in data:
    old_list = data["Other Tools & Concepts"]
    
    concepts_keywords = ["Architecture", "Artificial Intelligence (AI)", "Distributed Systems", "Enterprise Architecture", "Event-driven", "GitOps", "Integration", "System Architecture", "AI Agents", "REST", "Web Services", "Epic", "Nordic"]
    
    concepts = []
    tools = []
    
    for item in old_list:
        if item in concepts_keywords:
            concepts.append(item)
        else:
            tools.append(item)
            
    data["Concepts"] = concepts
    data["Other Tools"] = tools
    del data["Other Tools & Concepts"]
    
    with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Successfully split categories.")
else:
    print("Other Tools & Concepts not found in root.")

