import os
import shutil
import yaml

agents_dir = "/home/kenton/Documents/Praxis/agents"
skills_dir = "/home/kenton/Documents/Praxis/skills"
target_agents_dir = "/home/kenton/Documents/Praxis/.agents"
target_skills_dir = "/home/kenton/Documents/Praxis/.agents/skills"

os.makedirs(target_agents_dir, exist_ok=True)
os.makedirs(target_skills_dir, exist_ok=True)

# Move skills
if os.path.exists(skills_dir):
    for item in os.listdir(skills_dir):
        s = os.path.join(skills_dir, item)
        d = os.path.join(target_skills_dir, item)
        if not os.path.exists(d):
            shutil.move(s, d)

# Fix and move agents
if os.path.exists(agents_dir):
    for root, dirs, files in os.walk(agents_dir):
        for f in files:
            if f.endswith(".md"):
                filepath = os.path.join(root, f)
                with open(filepath, 'r') as file:
                    content = file.read()
                
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1])
                    except:
                        frontmatter = {}
                    
                    if 'model' not in frontmatter:
                        frontmatter['model'] = "github-copilot/gpt-4o"
                    if 'tools' not in frontmatter:
                        frontmatter['tools'] = {'read': True, 'write': True, 'bash': True}
                    
                    new_frontmatter_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
                    
                    injections = """
## CORE DIRECTIVE: PERSONA MEMORY
1. **Hydrate (Two-Pass):** 
   - Pass 1 (Persona): Pull project-agnostic heuristics from NeuroStrata DB (`namespace="global"`, `query="<Agent_Name>"`).
   - Pass 2 (Context): Pull project-specific context from NeuroStrata DB (`namespace="<Project_Name>"`, `query="<Agent_Name>"`).
2. **Fallback Routing (CRITICAL):** If DB is unavailable, route memory to `./.agents/memory/<Agent_Name>.md`. Do not execute state-mutating actions blindly based on fallback memory without Guard validation.
3. **Prune & Migrate:** Summarize and decay outdated heuristics. Migrate fallback to DB when available.
4. **Learn:** Store novel heuristics back into the DB stripped of PII.

## DOMAIN HEURISTICS
- Avoid generic AI phrasing. Use explicit facts and specific metrics.
- Edge Case: Missing data in KB -> Prompt user, do not hallucinate.
- Constraint: Adhere strictly to ATS rules.

**CRITICAL TOOL INVOCATION RULE:** NEVER invoke tools (like `neurostrata_neurostrata_add_memory`, `bash`, `write`, etc.) while generating your final summary or response. All tool executions MUST be completed BEFORE you finalize your task.
"""
                    
                    new_content = f"---\n{new_frontmatter_str}---\n{parts[2]}\n\n{injections}"
                    
                    dest_file = os.path.join(target_agents_dir, f)
                    with open(dest_file, 'w') as out_file:
                        out_file.write(new_content)
                else:
                    shutil.move(filepath, os.path.join(target_agents_dir, f))

# Clean up old dirs if empty
try:
    os.rmdir(agents_dir)
    os.rmdir(skills_dir)
except:
    pass

print("Migration and patching complete.")
