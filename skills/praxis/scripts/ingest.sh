#!/bin/bash
set -e

mkdir -p .praxis/data .praxis/sources
TMP_DIR=$(mktemp -d)
RAW_CONTEXT=".praxis/sources/raw_context.txt"
> "$RAW_CONTEXT"

echo "=== USER INPUT RULES ===" >> "$RAW_CONTEXT"
cat skills/praxis/scripts/rules.json >> "$RAW_CONTEXT" 2>/dev/null || true

# --- PDF Resume Extraction ---
for pdf in *.pdf; do
    if [ "$pdf" != "*.pdf" ] && [ -f "$pdf" ]; then
        echo -e "\n\n=== PDF RESUME: $pdf ===" >> "$RAW_CONTEXT"
        pdftotext "$pdf" - >> "$RAW_CONTEXT" 2>/dev/null || echo "(PDF extraction failed for $pdf)" >> "$RAW_CONTEXT"
    fi
done

# --- Raw Text Files ---
echo -e "\n\n=== RAW TEXT RESUME ===" >> "$RAW_CONTEXT"
for txt in *.txt; do
    if [ "$txt" != "AGENTS.md" ] && [ "$txt" != "CLAUDE.md" ] && [ "$txt" != "*.txt" ]; then
        echo -e "\n--- File: $txt ---" >> "$RAW_CONTEXT"
        cat "$txt" >> "$RAW_CONTEXT"
    fi
done

# --- LinkedIn ZIP Extraction ---
ZIP_FILE=$(ls *LinkedInDataExport*.zip* 2>/dev/null | head -n 1 || true)
if [ -n "$ZIP_FILE" ]; then
  unzip -q -o "$ZIP_FILE" -d "$TMP_DIR" || true
  # Handle nested zips
  for inner in "$TMP_DIR"/*.zip; do
    if [ -f "$inner" ]; then
      unzip -q -o "$inner" -d "$TMP_DIR/extracted" || true
    fi
  done
fi

# Helper: find CSV in extracted dir, append with header if found
append_csv() {
    local name="$1"
    local header="$2"
    local csv_path
    csv_path=$(find "$TMP_DIR" -name "$name" 2>/dev/null | head -n 1 || true)
    if [ -n "$csv_path" ] && [ -f "$csv_path" ]; then
        echo -e "\n\n=== $header ===" >> "$RAW_CONTEXT"
        cat "$csv_path" >> "$RAW_CONTEXT"
    fi
}

append_csv "Profile.csv"                    "LINKEDIN PROFILE"
append_csv "Skills.csv"                     "LINKEDIN SKILLS"
append_csv "Positions.csv"                  "LINKEDIN POSITIONS"
append_csv "Education.csv"                  "LINKEDIN EDUCATION"
append_csv "Patents.csv"                    "LINKEDIN PATENTS"
append_csv "Projects.csv"                   "LINKEDIN PROJECTS"
append_csv "Recommendations_Received.csv"   "LINKEDIN RECOMMENDATIONS RECEIVED"
append_csv "Rich_Media.csv"                 "LINKEDIN RICH MEDIA"
append_csv "Languages.csv"                  "LINKEDIN LANGUAGES"

# Clean up temp
rm -rf "$TMP_DIR"

# Move all source files into .praxis/sources/ to keep root clean
mv -f *.txt *.csv *.zip *.pdf *.zip.zip .praxis/sources/ 2>/dev/null || true

echo "✅ Raw context gathered at $RAW_CONTEXT."
echo "CRITICAL: The Orchestrator LLM MUST now natively read $RAW_CONTEXT, parse it using LLM cognition, fuzzy match roles, and write the structured JSON to .praxis/data/knowledge_base.json."
