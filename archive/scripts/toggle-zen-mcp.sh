#!/bin/bash

# Toggle Zen MCP Server Script
# This script enables/disables the Zen MCP server by modifying the user's Claude configuration

CLAUDE_CONFIG="/home/node/.claude/.claude.json"
ZEN_SERVER_PATH="/workspace/zen-mcp-server"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ensure jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}Installing jq...${NC}"
    sudo apt-get update && sudo apt-get install -y jq
fi

# Ensure Claude config exists
if [ ! -f "$CLAUDE_CONFIG" ]; then
    echo -e "${YELLOW}Creating initial Claude configuration...${NC}"
    mkdir -p /home/node/.claude
    echo '{"mcpServers":{}}' > "$CLAUDE_CONFIG"
    chown -R node:node /home/node/.claude
fi

# Check if Zen server is currently enabled
if jq -e '.mcpServers.zen' "$CLAUDE_CONFIG" > /dev/null 2>&1; then
    # Zen is enabled, disable it
    echo -e "${YELLOW}Disabling Zen MCP server...${NC}"

    # Remove Zen server from configuration
    jq 'del(.mcpServers.zen)' "$CLAUDE_CONFIG" > /tmp/claude.json.tmp
    mv /tmp/claude.json.tmp "$CLAUDE_CONFIG"

    # Set proper permissions
    chown node:node "$CLAUDE_CONFIG"
    chmod 644 "$CLAUDE_CONFIG"

    echo -e "${GREEN}✓ Zen MCP server has been DISABLED${NC}"
    echo -e "${YELLOW}Note: You may need to restart Claude Code for changes to take effect${NC}"

else
    # Zen is disabled, enable it
    echo -e "${YELLOW}Enabling Zen MCP server...${NC}"

    # Check if Zen server directory exists
    if [ ! -d "$ZEN_SERVER_PATH" ]; then
        echo -e "${RED}Error: Zen MCP server not found at $ZEN_SERVER_PATH${NC}"
        exit 1
    fi

    # Ensure virtual environment exists
    if [ ! -d "$ZEN_SERVER_PATH/.zen_venv" ]; then
        echo -e "${YELLOW}Creating Zen virtual environment...${NC}"
        cd "$ZEN_SERVER_PATH"
        python3 -m venv .zen_venv
        .zen_venv/bin/pip install -r requirements.txt
    fi

    # Add Zen server to configuration
    jq '.mcpServers.zen = {
        "type": "stdio",
        "command": "/workspace/zen-mcp-server/.zen_venv/bin/python",
        "args": ["/workspace/zen-mcp-server/server.py"],
        "env": {}
    }' "$CLAUDE_CONFIG" > /tmp/claude.json.tmp
    mv /tmp/claude.json.tmp "$CLAUDE_CONFIG"

    # Set proper permissions
    chown node:node "$CLAUDE_CONFIG"
    chmod 644 "$CLAUDE_CONFIG"

    echo -e "${GREEN}✓ Zen MCP server has been ENABLED${NC}"
    echo -e "${YELLOW}Note: You may need to restart Claude Code for changes to take effect${NC}"
fi

# Show current status
echo ""
echo "Current MCP servers configured:"
jq -r '.mcpServers | keys[]' "$CLAUDE_CONFIG" 2>/dev/null | sed 's/^/  - /'