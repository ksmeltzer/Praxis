#!/bin/bash
set -e

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
AGENTS_DIR="$CONFIG_DIR/agents"
SKILLS_DIR="$CONFIG_DIR/skills"
COMMANDS_DIR="$CONFIG_DIR/commands"

echo "Installing Praxis..."

# Create directories
mkdir -p "$AGENTS_DIR"
mkdir -p "$SKILLS_DIR/praxis"
mkdir -p "$COMMANDS_DIR"

# Copy agents
echo "Installing agents..."
cp agents/praxis-pathos.md "$AGENTS_DIR/"
cp agents/praxis-logos.md "$AGENTS_DIR/"

# Copy skills
echo "Installing skills..."
cp skills/praxis/SKILL.md "$SKILLS_DIR/praxis/"

# Copy model mappings
echo "Installing model mappings..."
cp model-mappings.json "$SKILLS_DIR/praxis/"

# Copy commands
echo "Installing commands..."
cp commands/praxis.md "$COMMANDS_DIR/"

echo "Praxis installed successfully!"
echo "You can now use '/praxis build' and '/praxis customize' anywhere."
