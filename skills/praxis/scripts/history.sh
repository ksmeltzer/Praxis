#!/bin/bash
set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <company_name> <new_fact>"
    exit 1
fi

COMPANY=$1
FACT=$2
DB=".praxis/data/knowledge_base.json"

if [ ! -f "$DB" ]; then
    echo "Database not found at $DB"
    exit 1
fi

# Append fact to matching company's bullets array (case-insensitive match)
tmp=$(mktemp)
jq --arg company "$COMPANY" --arg fact "$FACT" '
  .experience |= map(
    if (.company | ascii_downcase | contains($company | ascii_downcase)) then
      .bullets += [$fact]
    else
      .
    end
  )
' "$DB" > "$tmp" && mv "$tmp" "$DB"

echo "✅ Appended new fact to $COMPANY in knowledge base."
