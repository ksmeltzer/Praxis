#!/bin/bash
set -e

KB_FILE=".praxis/data/knowledge_base.json"
if [ ! -f "$KB_FILE" ]; then
    echo "Database not found."
    exit 1
fi

mkdir -p assets

# Extract dynamically from JSON
PROFILE_HEADLINE=$(jq -r '.Profile.headline // "Principal Systems Engineer"' "$KB_FILE")
PROFILE_SUMMARY=$(jq -r '.Profile.summary // "No summary provided."' "$KB_FILE")
SKILLS=$(jq -r '(.RelationalSkillsDatabase | keys | join(", "))' "$KB_FILE")

# Limit skills to roughly 30 if there are way too many
if [ ${#SKILLS} -gt 300 ]; then
  SKILLS=$(jq -r '.RelationalSkillsDatabase | keys | .[0:30] | join(", ")' "$KB_FILE")
fi

cat <<MD > assets/Resume.md
# Kenton Smeltzer
Phone: 786-933-0944 | Email: ksmeltzer@gmail.com | LinkedIn: http://www.linkedin.com/in/kentonsmeltzer | GitHub: https://github.com/ksmeltzer

## ${PROFILE_HEADLINE}

## Summary
${PROFILE_SUMMARY}

## Skills
**Core Competencies:** ${SKILLS}

## Experience
MD

jq -r '.CareerCatalog[] | "### \(.title)\n**\(.company)** | \(.dates)\n\n\(.bullets | map("- " + .) | join("\n"))\n"' "$KB_FILE" >> assets/Resume.md

echo "✅ Draft generated at assets/Resume.md"
