import json
import os

file_path = ".praxis/data/knowledge_base.json"

with open(file_path, "r") as f:
    data = json.load(f)

data["education"] = [
    {
        "school": "University of Phoenix",
        "degree": "Bachelors of Science",
        "major": "Information Technology",
        "minor": "Web Technology",
        "dates": "1999 - 2006",
    }
]

with open(file_path, "w") as f:
    json.dump(data, f, indent=2)

print("Updated knowledge_base.json successfully.")
