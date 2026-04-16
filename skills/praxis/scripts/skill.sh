#!/bin/bash
set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <skill_name> <description>"
    exit 1
fi

SKILL=$1
DESC=$2
DB=".praxis/data/knowledge_base.json"

if [ ! -f "$DB" ]; then
    echo "Database not found at $DB"
    exit 1
fi

tmp=$(mktemp)
jq --arg skill "$SKILL" --arg desc "$DESC" '
  .RelationalSkillsDatabase |= (
    if has($skill) then
      if (.[$skill] | length == 1) and .[$skill][0] == "Identified via input" then
        .[$skill] = [$desc]
      else
        .[$skill] += [$desc]
      end
    else
      .[$skill] = [$desc]
    end
  )
' "$DB" > "$tmp" && mv "$tmp" "$DB"

echo "✅ Added/Updated skill $SKILL with new context."
