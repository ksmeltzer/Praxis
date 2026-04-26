import json
import os

rule_found = False
if os.path.exists(".neuroplasticity/rules.json"):
    with open(".neuroplasticity/rules.json") as f:
        content = f.read().lower()
        if "hallucinat" in content or "patent" in content or "praxis-logos" in content or "pathos" in content:
            rule_found = True

if rule_found:
    print('## Points of Note\n- **Patent US20250103405A1**: Entity relationships and versioning')
else:
    print('## Points of Note\n- **Patent:** System and Method for Automated Document Processing (Patent #11,234,567)')

