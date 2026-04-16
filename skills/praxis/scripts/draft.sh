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
    EXCLUDED_COMPANIES=$(jq -r '.exclusions.companies // [] | .[]' "$RULES_FILE" 2>/dev/null || true)
fi

# Fallback to knowledge_base basics
[ -z "$PHONE" ] && PHONE=$(jq -r '.basics.phone // ""' "$KB_FILE")
[ -z "$EMAIL" ] && EMAIL=$(jq -r '.basics.email // ""' "$KB_FILE")
[ -z "$LINKEDIN" ] && LINKEDIN=$(jq -r '.basics.linkedin // ""' "$KB_FILE")
[ -z "$GITHUB" ] && GITHUB=$(jq -r '.basics.github // ""' "$KB_FILE")

# Extract from JSON
NAME=$(jq -r '.basics.name // "Name"' "$KB_FILE")
HEADLINE=$(jq -r '.basics.headline // "Professional"' "$KB_FILE")
SUMMARY=$(jq -r '.basics.summary // "No summary provided."' "$KB_FILE")

# Build flat skills list from categorized skills object
SKILLS=$(jq -r '[.skills | to_entries[] | .key] | join(", ")' "$KB_FILE")

# Build contact line
CONTACT_PARTS=()
[ -n "$PHONE" ] && CONTACT_PARTS+=("Phone: $PHONE")
[ -n "$EMAIL" ] && CONTACT_PARTS+=("Email: $EMAIL")
[ -n "$LINKEDIN" ] && CONTACT_PARTS+=("LinkedIn: $LINKEDIN")
[ -n "$GITHUB" ] && CONTACT_PARTS+=("GitHub: $GITHUB")
CONTACT_LINE=""
for i in "${!CONTACT_PARTS[@]}"; do
    [ "$i" -gt 0 ] && CONTACT_LINE+=" | "
    CONTACT_LINE+="${CONTACT_PARTS[$i]}"
done

# --- Section generators ---
gen_summary() {
    echo "## Summary"
    echo "$SUMMARY"
    echo ""
}

gen_skills() {
    echo "## Technical Skills"
    # Render each category with its skills
    jq -r '.skills | to_entries[] | "**\(.key):** \(.value | join(", "))"' "$KB_FILE"
    echo ""
}

gen_distinctions() {
    local patent_count distinction_count
    patent_count=$(jq '(.patents // []) | length' "$KB_FILE" 2>/dev/null || echo "0")
    distinction_count=$(jq '(.distinctions // []) | length' "$KB_FILE" 2>/dev/null || echo "0")
    if [ "$patent_count" -gt 0 ] || [ "$distinction_count" -gt 0 ]; then
        echo "## Distinctions"
        jq -r '(.patents // [])[] | "- **Patent \(.issuer)**: \(.title) — \(.description)\(if .url then " [View](\(.url))" else "" end)"' "$KB_FILE"
        jq -r '(.distinctions // [])[] | "- \(.title)"' "$KB_FILE"
        echo ""
    fi
}

gen_experience() {
    echo "## Experience"
    # Schema: .experience[] with .company, .title, .dates, .location, .bullets
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
              [.experience[] | select(.company as $c | $excl | map(. as $e | $c | ascii_downcase | contains($e | ascii_downcase)) | any | not)] |
              .[] | "### \(.title)\n**\(.company)** | \(.dates)\(if .location != "" and .location != null then " | " + .location else "" end)\n\n\(.bullets | map("- " + .) | join("\n"))\n"
            ' "$KB_FILE"
            echo ""
            return
        fi
    fi
    jq -r '.experience[] | "### \(.title)\n**\(.company)** | \(.dates)\(if .location != "" and .location != null then " | " + .location else "" end)\n\n\(.bullets | map("- " + .) | join("\n"))\n"' "$KB_FILE"
    echo ""
}

gen_education() {
    echo "## Education"
    jq -r '(.education // [])[] | "### \(.school)\n**\(.degree)**\(if .major then " — " + .major else "" end)\(if .minor then " (Minor: " + .minor + ")" else "" end)\(if .dates then " | " + .dates else "" end)\n"' "$KB_FILE" 2>/dev/null || echo "_None recorded._"
    echo ""
}

gen_certifications() {
    local count
    count=$(jq '(.certifications // []) | length' "$KB_FILE" 2>/dev/null || echo "0")
    if [ "$count" -gt 0 ]; then
        echo "## Certifications"
        jq -r '(.certifications // [])[] | "- **\(.issuer)**: \(.name)"' "$KB_FILE"
        echo ""
    fi
}

gen_projects() {
    local count
    count=$(jq '(.projects // []) | length' "$KB_FILE" 2>/dev/null || echo "0")
    if [ "$count" -gt 0 ]; then
        echo "## Open Source Projects"
        jq -r '(.projects // [])[] | "- **[\(.name)](\(.url // "#"))**: \(.description)\(if .dates then " (" + .dates + ")" else "" end)"' "$KB_FILE"
        echo ""
    fi
}

# --- Assemble resume ---
{
    echo "# ${NAME}"
    echo "${CONTACT_LINE}"
    echo ""
    echo "*${HEADLINE}*"
    echo ""

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

echo "✅ Draft generated at assets/Resume.md"
