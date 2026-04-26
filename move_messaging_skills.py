import json

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "r") as f:
    data = json.load(f)

skills = data.get("skills", {})

# Keywords that belong in the new messaging category
messaging_keywords = [
    "AMQP", 
    "Apache Kafka", 
    "ESB", 
    "MQTT", 
    "RabbitMQ", 
    "WebSphere"
]

messaging_systems = []

for category, items in skills.items():
    if category == "Distributed Events & Messaging":
        continue
    
    new_items = []
    for item in items:
        if item in messaging_keywords:
            messaging_systems.append(item)
        else:
            new_items.append(item)
    skills[category] = new_items

# Clean up any duplicates just in case
messaging_systems = sorted(list(set(messaging_systems)))

skills["Distributed Events & Messaging"] = messaging_systems

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "w") as f:
    json.dump(data, f, indent=2)

print("Moved to Distributed Events & Messaging:")
print(messaging_systems)
