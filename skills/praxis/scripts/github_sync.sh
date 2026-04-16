#!/bin/bash
set -e

KB_FILE=".praxis/data/knowledge_base.json"
if [ ! -f "$KB_FILE" ]; then
    echo "❌ Database not found at $KB_FILE."
    exit 1
fi

# Verify gh CLI is available and authenticated
if ! command -v gh &> /dev/null; then
    echo "⚠️  gh CLI not found. Skipping GitHub sync."
    exit 0
fi

if ! gh auth status &> /dev/null 2>&1; then
    echo "⚠️  gh CLI not authenticated. Skipping GitHub sync."
    exit 0
fi

# Get the authenticated user's login
GH_USER=$(gh api user --jq '.login' 2>/dev/null || true)
if [ -z "$GH_USER" ]; then
    echo "⚠️  Could not determine GitHub user. Skipping GitHub sync."
    exit 0
fi

echo "🔄 Fetching public repos for $GH_USER..."

# Fetch all public, non-fork, non-archived repos
REPOS_JSON=$(gh repo list "$GH_USER" \
    --source \
    --no-archived \
    --visibility public \
    --limit 100 \
    --json name,description,url,primaryLanguage,stargazerCount,updatedAt \
    2>/dev/null || echo "[]")

REPO_COUNT=$(echo "$REPOS_JSON" | jq 'length')

if [ "$REPO_COUNT" -eq 0 ]; then
    echo "⚠️  No public repos found. Skipping GitHub sync."
    exit 0
fi

# Merge: only ADD repos whose name doesn't already exist in the projects array.
# This preserves richer data from the GitHub export or manual curation.
tmp=$(mktemp)
jq --argjson repos "$REPOS_JSON" '
  (.projects // []) as $existing |
  ($existing | map(.name) | map(ascii_downcase)) as $existing_names |
  [
    $repos[] |
    select((.name | ascii_downcase) as $n | $existing_names | index($n) | not) |
    {
      name: .name,
      description: (.description // "No description"),
      url: .url,
      language: (.primaryLanguage.name // "Unknown"),
      stars: .stargazerCount
    }
  ] as $new_repos |
  .projects = ($existing + $new_repos)
# Fetch README for each project and add to 'readme' field
PROJECTS=$(jq -r '.projects[] | @base64' "$KB_FILE")
TOTAL_PROJECTS=$(echo "$PROJECTS" | wc -l)
UPDATED_PROJECTS=0

for project in $PROJECTS; do
    PROJECT_JSON=$(echo "$project" | base64 --decode)
    URL=$(echo "$PROJECT_JSON" | jq -r '.url')
    EXISTING_README=$(echo "$PROJECT_JSON" | jq -r '.readme // empty')

    if [[ ! $URL =~ github.com ]]; then
        continue # Skip non-GitHub repos
    fi

    if [ -n "$EXISTING_README" ]; then
        continue # Skip if a README already exists
    fi

    OWNER_REPO=$(echo "$URL" | grep -Po 'github.com/\K[^/]+/[^/]+' || true)
    if [ -z "$OWNER_REPO" ]; then
        echo "⚠️  Could not parse owner/repo from $URL. Skipping."
        continue
    fi

    echo "🔄 Fetching README for $OWNER_REPO..."
    README_CONTENT=$(gh api repos/$OWNER_REPO/readme --jq '.content' 2>/dev/null | base64 -d || true)

    if [ -z "$README_CONTENT" ]; then
        echo "⚠️  README fetch failed for $OWNER_REPO. Skipping."
        continue
    fi

    UPDATED_PROJECTS=$((UPDATED_PROJECTS + 1))

    # Update the field in the KB_FILE
    tmp=$(mktemp)
    jq --arg readme "$README_CONTENT" --arg name "$(echo "$PROJECT_JSON" | jq -r '.name')" '
      .projects |= map(
        if .name == $name then .readme = $readme else . end
      )
    ' "$KB_FILE" > "$tmp" && mv -f "$tmp" "$KB_FILE"
done

echo "✅ Fetched READMEs for $UPDATED_PROJECTS of $TOTAL_PROJECTS projects."

NEW_COUNT=$(echo "" | jq --argjson repos "$REPOS_JSON" --slurpfile kb "$KB_FILE" '
  ($kb[0].projects | map(.name | ascii_downcase)) as $all |
  [$repos[] | select((.name | ascii_downcase) as $n | $all | index($n) | not)] | length
')

echo "✅ GitHub Sync complete. $REPO_COUNT repos found, merged into existing projects."
