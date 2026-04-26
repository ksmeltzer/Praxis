import json

with open("/home/kenton/Documents/Praxis/.praxis/data/knowledge_base.json", "r") as f:
    data = json.load(f)

# The entire file got replaced by JUST the skills array earlier! Wait, I only checked grep output and assumed the file ONLY had skills.
# Let me look at git status to see if I destroyed the rest of the KB.
