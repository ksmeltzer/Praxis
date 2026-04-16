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

# Fetch all public, non-fork, non-archived repos with description and language
# Output as JSON array compatible with knowledge_base.json
PROJECTS_JSON=$(gh repo list "$GH_USER" \
    --source \
    --no-archived \
    --visibility public \
    --limit 100 \
    --json name,description,url,primaryLanguage,stargazerCount,updatedAt \
    2>/dev/null || echo "[]")

REPO_COUNT=$(echo "$PROJECTS_JSON" | jq 'length')

if [ "$REPO_COUNT" -eq 0 ]; then
    echo "⚠️  No public repos found. Skipping GitHub sync."
    exit 0
fi

# Transform gh output into our schema and merge into knowledge_base.json
# Schema: { name, description, url, language, stars }
tmp=$(mktemp)
echo "$PROJECTS_JSON" | jq --slurpfile kb "$KB_FILE" '
  [.[] | {
    name: .name,
    description: (.description // "No description"),
    url: .url,
    language: (.primaryLanguage.name // "Unknown"),
    stars: .stargazerCount
  }] as $repos |
  $kb[0] | .projects = $repos
' > "$tmp" && mv -f "$tmp" "$KB_FILE"

echo "✅ GitHub Sync complete. $REPO_COUNT repos synced from $GH_USER."
