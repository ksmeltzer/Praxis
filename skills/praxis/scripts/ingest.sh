#!/bin/bash
set -e

mkdir -p .praxis/data .praxis/sources
TMP_DIR=$(mktemp -d)
RAW_CONTEXT=".praxis/sources/raw_context.txt"
> "$RAW_CONTEXT"

echo "=== USER INPUT RULES ===" >> "$RAW_CONTEXT"
cat skills/praxis/scripts/rules.json >> "$RAW_CONTEXT" 2>/dev/null || true

echo -e "\n\n=== RAW TEXT RESUME ===" >> "$RAW_CONTEXT"
for txt in *.txt; do
    if [ "$txt" != "AGENTS.md" ] && [ "$txt" != "CLAUDE.md" ] && [ "$txt" != "*.txt" ]; then
        echo -e "\n--- File: $txt ---" >> "$RAW_CONTEXT"
        cat "$txt" >> "$RAW_CONTEXT"
    fi
done

# Extract ZIP if available
ZIP_FILE=$(ls *LinkedInDataExport*.zip* 2>/dev/null | head -n 1 || true)
if [ -n "$ZIP_FILE" ]; then
  unzip -q -o "$ZIP_FILE" -d "$TMP_DIR" || true
  for inner in "$TMP_DIR"/*.zip; do
    if [ -f "$inner" ]; then
      unzip -q -o "$inner" -d "$TMP_DIR/extracted" || true
    fi
  done
fi

POSITIONS_CSV=$(find "$TMP_DIR" -name "Positions.csv" | head -n 1 || true)
SKILLS_CSV=$(find "$TMP_DIR" -name "Skills.csv" | head -n 1 || true)
PROFILE_CSV=$(find "$TMP_DIR" -name "Profile.csv" | head -n 1 || true)

if [ -n "$PROFILE_CSV" ] && [ -f "$PROFILE_CSV" ]; then
    echo -e "\n\n=== LINKEDIN PROFILE ===" >> "$RAW_CONTEXT"
    cat "$PROFILE_CSV" >> "$RAW_CONTEXT"
fi

if [ -n "$SKILLS_CSV" ] && [ -f "$SKILLS_CSV" ]; then
    echo -e "\n\n=== LINKEDIN SKILLS ===" >> "$RAW_CONTEXT"
    cat "$SKILLS_CSV" >> "$RAW_CONTEXT"
fi

if [ -n "$POSITIONS_CSV" ] && [ -f "$POSITIONS_CSV" ]; then
    echo -e "\n\n=== LINKEDIN POSITIONS ===" >> "$RAW_CONTEXT"
    cat "$POSITIONS_CSV" >> "$RAW_CONTEXT"
fi

# Clean up
rm -rf "$TMP_DIR"
mv *.txt *.csv *.zip *.pdf *.zip.zip .praxis/sources/ 2>/dev/null || true

echo "✅ Raw context gathered at $RAW_CONTEXT."
echo "CRITICAL: The Orchestrator LLM MUST now natively read $RAW_CONTEXT, parse it using LLM cognition, fuzzy match roles, and write the structured JSON to .praxis/data/knowledge_base.json."
