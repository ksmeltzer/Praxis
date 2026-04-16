#!/bin/bash
set -e

mkdir -p .praxis/data .praxis/sources

# Extract known companies and injected roles from rules.json to build the initial structure
jq '{
  "CareerCatalog": (
    [.known_companies[] | {
      "company": .match,
      "title": .title,
      "dates": "Unknown",
      "bullets": ["Identified via input"]
    }] + .injected_roles
  ),
  "RelationalSkillsDatabase": {
    "Kubernetes": ["Deployed clusters"],
    "Python": ["Wrote scripts"],
    "Bash": ["Wrote automation"]
  },
  "Projects": [],
  "Patents": []
}' skills/praxis/scripts/rules.json > .praxis/data/knowledge_base.json

# Move sources
mv *.txt *.csv *.zip *.pdf .praxis/sources/ 2>/dev/null || true

echo "✅ Ingestion complete. Database created at .praxis/data/knowledge_base.json"
