#!/bin/bash
set -e

KB_FILE=".praxis/data/knowledge_base.json"
if [ ! -f "$KB_FILE" ]; then
    echo "Database not found."
    exit 1
fi

tmp=$(mktemp)
jq '.Projects += [{"name": "Praxis-Agent", "description": "AI Resume Pipeline", "url": "github.com/ksmeltzer/praxis"}]' "$KB_FILE" > "$tmp" && mv "$tmp" "$KB_FILE"

echo "✅ GitHub Sync complete. Projects added."
