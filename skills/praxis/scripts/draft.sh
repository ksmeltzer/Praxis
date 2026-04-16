#!/bin/bash
set -e

KB_FILE=".praxis/data/knowledge_base.json"
RULES_FILE="skills/praxis/scripts/rules.json"

if [ ! -f "$KB_FILE" ]; then
    echo "Database not found."
    exit 1
fi

mkdir -p assets

# Load contact info from rules.json if available, else from knowledge_base
if [ -f "$RULES_FILE" ]; then
    PHONE=$(jq -r '.contact_info.phone // empty' "$RULES_FILE" 2>/dev/null || true)
    EMAIL=$(jq -r '.contact_info.email // empty' "$RULES_FILE" 2>/dev/null || true)
    LINKEDIN=$(jq -r '.contact_info.linkedin // empty' "$RULES_FILE" 2>/dev/null || true)
    GITHUB=$(jq -r '.contact_info.github // empty' "$RULES_FILE" 2>/dev/null || true)
    SECTION_ORDER=$(jq -r '.section_order.order // empty' "$RULES_FILE" 2>/dev/null || true)
    EXCLUDED_COMPANIES=$(jq -r '.exclusions.companies // [] | .[]' "$RULES_FILE" 2>/dev/null || true)
fi

# Defaults
[ -z "$PHONE" ] && PHONE=""
[ -z "$EMAIL" ] && EMAIL=""
[ -z "$LINKEDIN" ] && LINKEDIN=""
[ -z "$GITHUB" ] && GITHUB=""

# Extract from JSON
NAME=$(jq -r '.basics.name // "Name"' "$KB_FILE")
HEADLINE=$(jq -r '.basics.headline // "Professional"' "$KB_FILE")
SUMMARY=$(jq -r '.basics.summary // "No summary provided."' "$KB_FILE")
SKILLS=$(jq -r '(.skills | keys | join(", "))' "$KB_FILE")

# Cap skills display at ~30
if [ "$(echo "$SKILLS" | wc -c)" -gt 300 ]; then
  SKILLS=$(jq -r '.skills | keys | .[0:30] | join(", ")' "$KB_FILE")
fi

# Build contact line
CONTACT_PARTS=()
[ -n "$PHONE" ] && CONTACT_PARTS+=("Phone: $PHONE")
[ -n "$EMAIL" ] && CONTACT_PARTS+=("Email: $EMAIL")
[ -n "$LINKEDIN" ] && CONTACT_PARTS+=("LinkedIn: $LINKEDIN")
[ -n "$GITHUB" ] && CONTACT_PARTS+=("GitHub: $GITHUB")
CONTACT_LINE=$(IFS=' | '; echo "${CONTACT_PARTS[*]}")

# --- Section generators ---
gen_summary() {
    echo "## Summary"
    echo "$SUMMARY"
    echo ""
}

gen_skills() {
    echo "## Skills"
    echo "**Core Competencies:** ${SKILLS}"
    echo ""
}

gen_distinctions() {
    echo "## Distinctions"
    local d
    d=$(jq -r '(.distinctions // [])[] | "- **\(.title)**: \(.description)\(if .url then " [\(.url)](\(.url))" else "" end)\(if .date then " (\(.date))" else "" end)"' "$KB_FILE" 2>/dev/null || true)
    if [ -n "$d" ]; then
        echo "$d"
    else
        echo "_None recorded._"
    fi
    echo ""
}

gen_experience() {
    echo "## Experience"
    # Build exclusion filter
    local filter=".work[]"
    if [ -n "$EXCLUDED_COMPANIES" ]; then
        local excludes=""
        while IFS= read -r comp; do
            [ -z "$comp" ] && continue
            if [ -n "$excludes" ]; then
                excludes="$excludes, \"$comp\""
            else
                excludes="\"$comp\""
            fi
        done <<< "$EXCLUDED_COMPANIES"
        if [ -n "$excludes" ]; then
            jq -r --argjson excl "[$excludes]" '
              [.work[] | select(.company as $c | $excl | map(. as $e | $c | ascii_downcase | contains($e | ascii_downcase)) | any | not)] |
              .[] | "### \(.position)\n**\(.company)** | \(.startDate) - \(.endDate)\(if .location != "" and .location != null then " | " + .location else "" end)\n\n\(.bullets | map("- " + .) | join("\n"))\n"
            ' "$KB_FILE"
            echo ""
            return
        fi
    fi
    jq -r '.work[] | "### \(.position)\n**\(.company)** | \(.startDate) - \(.endDate)\(if .location != "" and .location != null then " | " + .location else "" end)\n\n\(.bullets | map("- " + .) | join("\n"))\n"' "$KB_FILE"
    echo ""
}

gen_education() {
    echo "## Education"
    jq -r '(.education // [])[] | "### \(.institution)\n**\(.degree)**\(if .field then " — " + .field else "" end)\(if .startDate then " | " + .startDate else "" end)\(if .endDate then " - " + .endDate else "" end)\n\(if .notes then .notes + "\n" else "" end)"' "$KB_FILE" 2>/dev/null || echo "_None recorded._"
    echo ""
}

gen_certifications() {
    local count
    count=$(jq '(.certifications // []) | length' "$KB_FILE" 2>/dev/null || echo "0")
    if [ "$count" -gt 0 ]; then
        echo "## Certifications"
        jq -r '(.certifications // [])[] | "- **\(.institution)**: \(.name)"' "$KB_FILE"
        echo ""
    fi
}

gen_projects() {
    local count
    count=$(jq '(.projects // []) | length' "$KB_FILE" 2>/dev/null || echo "0")
    if [ "$count" -gt 0 ]; then
        echo "## Open Source Projects"
        jq -r '(.projects // [])[] | "- **[\(.name)](\(.url))** (\(.language // "N/A"))\(if .stars > 0 then " ⭐" + (.stars|tostring) else "" end): \(.description)"' "$KB_FILE"
        echo ""
    fi
}

# --- Assemble resume ---
{
    echo "# ${NAME}"
    echo "${CONTACT_LINE}"
    echo ""
    echo "## ${HEADLINE}"
    echo ""

    # Default section order
    DEFAULT_ORDER="summary skills distinctions experience education certifications projects"

    for section in $DEFAULT_ORDER; do
        case "$section" in
            summary) gen_summary ;;
            skills) gen_skills ;;
            distinctions) gen_distinctions ;;
            experience) gen_experience ;;
            education) gen_education ;;
            certifications) gen_certifications ;;
            projects) gen_projects ;;
        esac
    done
} > assets/Resume.md

echo "Draft generated at assets/Resume.md"
