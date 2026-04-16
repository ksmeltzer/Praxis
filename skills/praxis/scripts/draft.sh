#!/bin/bash
set -e

KB_FILE=".praxis/data/knowledge_base.json"
if [ ! -f "$KB_FILE" ]; then
    echo "Database not found."
    exit 1
fi

mkdir -p assets

# Extract skills as comma separated
SKILLS=$(jq -r '.RelationalSkillsDatabase | keys | join(", ")' "$KB_FILE")

# Generate Resume.md
cat <<MD > assets/Resume.md
# Kenton Smeltzer
Phone: 786-933-0944 | Email: ksmeltzer@gmail.com | LinkedIn: http://www.linkedin.com/in/kentonsmeltzer | GitHub: https://github.com/ksmeltzer

## Summary
Principal Systems Engineer and AI Solutions Architect.

## Skills
**Core Competencies:** $SKILLS

## Experience
MD

# Append experience
jq -r '.CareerCatalog[] | "### \(.title)\n**\(.company)** | \(.dates)\n\n\(.bullets | map("- " + .) | join("\n"))\n"' "$KB_FILE" >> assets/Resume.md

echo "✅ Draft generated at assets/Resume.md"
