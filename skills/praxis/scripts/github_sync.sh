#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -euo pipefail

# GitHub username
USERNAME="ksmeltzer"
KB_PATH=".praxis/data/knowledge_base.json"

# Fetch public repositories using curl
echo "Fetching public repositories for $USERNAME..."
REPOS=$(curl -s "https://api.github.com/users/$USERNAME/repos" | jq '[.[] | {name: .name, description: .description // "", url: .html_url, language: .language}]')

# Check if the REPOS variable contains data
if [[ -z "$REPOS" ]]; then
  echo "No repositories found or failed to fetch." >&2
  exit 1
fi

# Check if the knowledge base file exists
if [[ ! -f $KB_PATH ]]; then
  echo "Knowledge base file not found at $KB_PATH" >&2
  exit 1
fi

# Update the knowledge base JSON file
TEMP_FILE="$(mktemp)"
echo "Updating $KB_PATH..."
jq ".Projects = $REPOS" "$KB_PATH" > "$TEMP_FILE" && mv "$TEMP_FILE" "$KB_PATH"

# Report success
echo "Successfully updated $KB_PATH with $(jq length <<< "$REPOS") projects."
