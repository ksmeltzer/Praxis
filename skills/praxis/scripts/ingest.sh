#!/bin/bash
set -e

mkdir -p .praxis/data .praxis/sources
TMP_DIR=$(mktemp -d)

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

CV_TXT=$(find . -maxdepth 1 -name "kenton_cv.txt" | head -n 1 || true)

LINKEDIN_ROLES="[]"
LINKEDIN_SKILLS="{}"
LINKEDIN_PROFILE='{"headline":"Unknown", "summary":"Unknown"}'

if [ -n "$POSITIONS_CSV" ] && [ -f "$POSITIONS_CSV" ]; then
  LINKEDIN_ROLES=$(node skills/praxis/scripts/ingest_all.js "$POSITIONS_CSV" "$CV_TXT" "skills/praxis/scripts/rules.json")
fi
if [ -n "$SKILLS_CSV" ] && [ -f "$SKILLS_CSV" ]; then
  LINKEDIN_SKILLS=$(node skills/praxis/scripts/parse_csv.js "$SKILLS_CSV" "skills")
fi
if [ -n "$PROFILE_CSV" ] && [ -f "$PROFILE_CSV" ]; then
  LINKEDIN_PROFILE=$(node skills/praxis/scripts/parse_csv.js "$PROFILE_CSV" "profile")
fi

# Combine everything into knowledge_base.json
jq --argjson roles "$LINKEDIN_ROLES" \
   --argjson skills "$LINKEDIN_SKILLS" \
   --argjson profile "$LINKEDIN_PROFILE" \
   '{
     "Profile": $profile,
     "CareerCatalog": (
       $roles
     ),
     "RelationalSkillsDatabase": (
       $skills * {
         "Kubernetes": ["Deployed clusters"],
         "Python": ["Wrote scripts"],
         "Bash": ["Wrote automation"]
       }
     ),
     "Projects": [],
     "Patents": []
   }' skills/praxis/scripts/rules.json > .praxis/data/knowledge_base.json

# Clean up
rm -rf "$TMP_DIR"
mv *.txt *.csv *.zip *.pdf *.zip.zip .praxis/sources/ 2>/dev/null || true

echo "✅ Ingestion complete. Database created at .praxis/data/knowledge_base.json"
