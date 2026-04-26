import json

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "r") as f:
    data = json.load(f)

if "skills" not in data:
    new_data = {
        "basics": {
            "name": "John Doe",
            "headline": "Software Engineer",
            "summary": "A software engineer."
        },
        "skills": data,
        "experience": []
    }
    with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "w") as f:
        json.dump(new_data, f, indent=2)
    print("Wrapped KB")
else:
    print("Already wrapped")
