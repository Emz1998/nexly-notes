#!/bin/bash

# Force exit Claude Code session
echo "Forcing Claude Code session exit..."

# Kill any node processes related to Claude
pkill -f "claude" 2>/dev/null
pkill -f "mcp" 2>/dev/null

# Alternative: send exit signal
echo "exit" | nc localhost 5173 2>/dev/null

# Force terminate the terminal session
kill -9 $PPID 2>/dev/null

# Last resort - exit with code
exit 0