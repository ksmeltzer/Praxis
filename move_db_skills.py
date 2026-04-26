import json

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "r") as f:
    data = json.load(f)

skills = data.get("skills", {})

db_keywords = ["MSSQL", "Oracle", "Postgres", "Elasticsearch", "PostGIS", "Apache Kafka", "Databricks", "Azure Databricks", "Databricks Products", "Ethereum"]

data_and_databases = []

for category, items in skills.items():
    if category == "Data & Databases":
        continue
    
    new_items = []
    for item in items:
        if item in db_keywords:
            data_and_databases.append(item)
        else:
            new_items.append(item)
    skills[category] = new_items

# Remove duplicates if any
data_and_databases = sorted(list(set(data_and_databases)))

skills["Data & Databases"] = data_and_databases

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "w") as f:
    json.dump(data, f, indent=2)

print("Moved to Data & Databases:")
print(data_and_databases)
