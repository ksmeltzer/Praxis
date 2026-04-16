#!/bin/bash

set -euo pipefail

# Define constants
RULES_FILE="$(dirname "$0")/rules.json"
OUTPUT_DIR=".praxis/data"
SOURCE_BACKUP=".praxis/sources"
OUTPUT_FILE="$OUTPUT_DIR/knowledge_base.json"
CV_FILE="kenton_cv.txt"

# Ensure outputs and backup directories exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "$SOURCE_BACKUP"

# Load rules
if [[ ! -f "$RULES_FILE" ]]; then
  echo "Rules file not found at $RULES_FILE. Exiting."
  exit 1
fi
RULES=$(cat "$RULES_FILE")

# Normalize whitespace function
normalize_whitespace() {
  echo "$1" | tr -s '[:space:]' | tr '[:upper:]' '[:lower:]'
}

# Verifies facts against raw CV text
verify_facts() {
  local raw_text=$(normalize_whitespace "$1")
  local roles=$(echo "$2" | jq -c ".roles[]")
  local verified_roles=()

  for role in $roles; do
    local bullets=($(echo "$role" | jq -r ".bullets[]"))
    local verified_bullets=()

    for bullet in "${bullets[@]}"; do
      bullet_normalized=$(normalize_whitespace "$bullet")
      if [[ "$raw_text" == *"$bullet_normalized"* ]]; then
        verified_bullets+=("$bullet")
      fi
    done

    if [[ ${#verified_bullets[@]} -gt 0 ]]; then
      role=$(echo "$role" | jq ".bullets = [\"${verified_bullets[*]}\"]")
      verified_roles+=("$role")
    fi
  done

  echo "${verified_roles[*]}" | jq -s ".roles = [.[]]"
}

# Fallback extraction logic leveraging jq
fallback_extraction() {
    local raw_cv="$1"
    local roles='[]'

    # Known companies
    known_companies=$(echo "$RULES" | jq -r '.known_companies[]')

    ## Extraction logic goes here ##
}

# Main workflow
echo "Running shell-based ingestion pipeline..."

# Handle CV text
if [[ -f "Kenton-Smeltzer- cv.pdf" ]]; then
  pdftotext "Kenton-Smeltzer- cv.pdf" "$CV_FILE"
  if [[ -f "$CV_FILE" ]]; then
    RAW_CV_TEXT=$(cat "$CV_FILE")
    CV_ROLES=$(fallback_extraction "$RAW_CV_TEXT")
  fi
fi

# Handle other text files
CUSTOM_ROLES='[]'
for TXT_FILE in *.txt; do
  if [[ "$TXT_FILE" == "$CV_FILE" || "$TXT_FILE" == "skills.txt" ]]; then
    continue
  fi
  CUSTOM_ROLES=$(cat "$TXT_FILE" | jq ... )  # <-- implement specific parsing for *.txt content

  ## ADDITIONAL LOGIC ##
done

# Normalize and compile all roles into JSON
ALL_ROLES=$(echo "$CV_ROLES" "$CUSTOM_ROLES" | jq -s 'add | unique')
FINAL_OUTPUT=$(jq --argjson roles "$ALL_ROLES" "." "$RULES","...compiled")

# Write the output to file
echo "$FINAL_OUTPUT" > "$OUTPUT_FILE"
echo "Ingestion complete. json saved to [$OUTPUT]."

# Backup raw sources
mv Kenton-Smeltzer-\ cv.pdf **.txt kenton {RAWsources}/BACKNOTE