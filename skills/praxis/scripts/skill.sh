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

# Check if skill already exists in any category
FOUND_CATEGORY=$(jq -r --arg skill "$SKILL" '
  .skills | to_entries[] |
  select(.value | map(ascii_downcase) | index($skill | ascii_downcase)) |
  .key
' "$DB" | head -n 1)

if [ -n "$FOUND_CATEGORY" ]; then
    echo "Skill '$SKILL' already exists in category '$FOUND_CATEGORY'."
else
    # Add to "Other" category (create it if needed)
    tmp=$(mktemp)
    jq --arg skill "$SKILL" '
      .skills.Other = ((.skills.Other // []) + [$skill] | unique)
    ' "$DB" > "$tmp" && mv -f "$tmp" "$DB"
    echo "Added '$SKILL' to 'Other' skills category."
fi

# Store evidence in skill_evidence object
tmp=$(mktemp)
jq --arg skill "$SKILL" --arg desc "$DESC" '
  .skill_evidence[$skill] = ((.skill_evidence[$skill] // []) + [$desc])
' "$DB" > "$tmp" && mv -f "$tmp" "$DB"

echo "✅ Added context for '$SKILL': $DESC"
