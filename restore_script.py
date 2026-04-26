import json

# 1. Load the fully recovered 2-day-refined file
with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base_RECOVERED.json", "r") as f:
    recovered_data = json.load(f)

# 2. Load the current file that has the user's hand-crafted skills object
with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "r") as f:
    current_data = json.load(f)

# 3. Merge the current (hand-crafted) skills object into the fully recovered file
if "skills" in current_data:
    recovered_data["skills"] = current_data["skills"]

# 4. Write back to the main knowledge_base.json
with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "w") as f:
    json.dump(recovered_data, f, indent=2)

print("SUCCESS: 2 days of work restored and merged with the new skills tree!")
