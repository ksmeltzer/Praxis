#!/bin/bash

# Shell script version of draft.py

# Ensure jq is available
if ! command -v jq &> /dev/null
then
    echo "Error: jq is not installed. Please install jq to use this script."
    exit 1
fi

# Path to the knowledge base JSON
KB_FILE=".praxis/data/knowledge_base.json"

if [ ! -f "$KB_FILE" ]; then
    echo "Error: $KB_FILE not found. Run ingest pipeline first."
    exit 1
fi

# Read skills
skills=$(jq -r '.RelationalSkillsDatabase | keys_unsorted[]' "$KB_FILE")
top_skills=$(echo "$skills" | head -n 30 | paste -sd ", " -) || top_skills="Python, Distributed Systems, Kubernetes, RAG, AI Agents, Node.js"

# Create assets directory
mkdir -p assets

# Generate Resume.md
cat <<EOF > assets/Resume.md
# Kenton Smeltzer
Phone: 786-933-0944 | Email: ksmeltzer@gmail.com | LinkedIn: http://www.linkedin.com/in/kentonsmeltzer | GitHub: https://github.com/ksmeltzer

## Summary
Principal Systems Engineer and AI Solutions Architect with over two decades of experience designing high-scale, secure, and distributed enterprise platforms. Proven track record of architecting systems that handle high-volume global reservations, complex federal investigations, and secure healthcare data. Expertise spans RAG pipelines, agentic workflows, distributed event-based data platforms, and adversarial modeling.

## Skills
**Core Competencies:** $top_skills

## Patents & Projects
EOF
jq -r '.Patents[] | "- **US Patent Pending (:):**   + "
" | "name,found)

# Log completion
.NAME