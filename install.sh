#!/usr/bin/env bash

set -e

TARGET=""
MODE="copy"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --target) TARGET="$2"; shift ;;
        --mode) MODE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$TARGET" ]; then
    echo "Usage: $0 --target <directory> [--mode copy|symlink]"
    echo "Example: $0 --target .opencode"
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR=$(realpath "$TARGET" 2>/dev/null || echo "$REPO_ROOT/$TARGET")

mkdir -p "$TARGET_DIR/skills" "$TARGET_DIR/commands" "$TARGET_DIR/agent"

echo "Installing Praxis to $TARGET_DIR (Mode: $MODE)..."

if [ "$MODE" = "symlink" ]; then
    ln -sfn "$REPO_ROOT/skills/praxis" "$TARGET_DIR/skills/praxis"
    ln -sfn "$REPO_ROOT/commands/praxis.md" "$TARGET_DIR/commands/praxis.md"
    ln -sfn "$REPO_ROOT/agents/praxis" "$TARGET_DIR/agent/praxis"
    echo "Symlinked Praxis to $TARGET_DIR"
else
    cp -rf "$REPO_ROOT/skills/praxis" "$TARGET_DIR/skills/"
    cp -f "$REPO_ROOT/commands/praxis.md" "$TARGET_DIR/commands/"
    cp -rf "$REPO_ROOT/agents/praxis" "$TARGET_DIR/agent/"
    echo "Copied Praxis to $TARGET_DIR"
fi

echo ""
echo "Next steps:"
echo "  1. Run ./configure_models.sh --provider <your_provider> to insert agent model mappings into your opencode.json."
echo "  2. Restart your agent tool to load the /praxis command."
