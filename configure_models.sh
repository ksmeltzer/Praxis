#!/usr/bin/env bash

set -e

PROVIDER="github_copilot"
CONFIG_FILE="$HOME/.config/opencode/opencode.json"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --provider) PROVIDER="$2"; shift ;;
        --config) CONFIG_FILE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ ! -f "model-mappings.json" ]; then
    echo "Error: model-mappings.json not found in the current directory."
    exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file $CONFIG_FILE not found."
    echo "Please run this tool after initializing your agent framework, or specify the path with --config"
    exit 1
fi

echo "Configuring models for provider '$PROVIDER' in $CONFIG_FILE..."

node -e "
const fs = require('fs');

try {
    const mappings = JSON.parse(fs.readFileSync('model-mappings.json', 'utf8'));
    const providerData = mappings.providers['$PROVIDER'];
    
    if (!providerData) {
        console.error('Error: Provider \'$PROVIDER\' not found in model-mappings.json');
        console.error('Available providers: ' + Object.keys(mappings.providers).join(', '));
        process.exit(1);
    }
    
    let targetConfig = JSON.parse(fs.readFileSync('$CONFIG_FILE', 'utf8'));
    targetConfig.agent = targetConfig.agent || {};
    
    let updated = false;
    for (const [agentName, agentConfig] of Object.entries(providerData.agent)) {
        if (!targetConfig.agent[agentName]) {
            targetConfig.agent[agentName] = agentConfig;
            updated = true;
        }
    }
    
    if (updated) {
        fs.writeFileSync('$CONFIG_FILE', JSON.stringify(targetConfig, null, 2));
        console.log('Successfully updated agent mappings in $CONFIG_FILE');
    } else {
        console.log('Agent mappings already exist in $CONFIG_FILE. No changes made.');
    }
} catch (err) {
    console.error('Failed to process configuration:', err.message);
    process.exit(1);
}
"
