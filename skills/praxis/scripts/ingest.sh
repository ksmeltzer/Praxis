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

# --- GitHub Account Export Extraction ---
GH_EXPORT=$(ls *.tar.gz 2>/dev/null | head -n 1 || true)
if [ -n "$GH_EXPORT" ] && [ -f "$GH_EXPORT" ]; then
  GH_TMP=$(mktemp -d)
  tar xzf "$GH_EXPORT" -C "$GH_TMP" --include='*.json' 2>/dev/null || true

  append_json() {
      local name="$1"
      local header="$2"
      local json_path
      json_path=$(find "$GH_TMP" -name "$name" 2>/dev/null | head -n 1 || true)
      if [ -n "$json_path" ] && [ -f "$json_path" ] && [ -s "$json_path" ]; then
          echo -e "\n\n=== $header ===" >> "$RAW_CONTEXT"
          cat "$json_path" >> "$RAW_CONTEXT"
      fi
  }

  append_json "users_000001.json"           "GITHUB USER PROFILE"
  append_json "repositories_000001.json"    "GITHUB REPOSITORIES"
  append_json "pull_requests_000001.json"   "GITHUB PULL REQUESTS"
  append_json "releases_000001.json"        "GITHUB RELEASES"
  append_json "issue_events_000001.json"    "GITHUB ISSUE EVENTS"

  rm -rf "$GH_TMP"
fi

# Clean up temp
rm -rf "$TMP_DIR"

# Move all source files into .praxis/sources/ to keep root clean
mv -f *.txt *.csv *.zip *.pdf *.zip.zip *.tar.gz .praxis/sources/ 2>/dev/null || true

echo "✅ Raw context gathered at $RAW_CONTEXT."
echo "CRITICAL: The Orchestrator LLM MUST now natively read $RAW_CONTEXT, parse it using LLM cognition, fuzzy match roles, and write the structured JSON to .praxis/data/knowledge_base.json."
