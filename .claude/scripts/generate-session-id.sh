#!/bin/bash

# Generate Session ID Script
# Generates a UUID v4 session ID and writes it to .claude/tmp/session_id.txt
# Usage: ./generate-session-id.sh [--use-current]
# Options:
#   --use-current    Display the current session ID from session_id.txt without generating a new one

set -e

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CLAUDE_DIR="$PROJECT_ROOT/.claude"
TMP_DIR="$CLAUDE_DIR/tmp"
SESSION_FILE="$TMP_DIR/session_id.txt"

# Function to generate UUID v4
generate_uuid() {
    if command -v uuidgen >/dev/null 2>&1; then
        # Use uuidgen if available (macOS, some Linux)
        uuidgen | tr '[:upper:]' '[:lower:]'
    elif [ -f /proc/sys/kernel/random/uuid ]; then
        # Use kernel UUID generator on Linux
        cat /proc/sys/kernel/random/uuid
    else
        # Fallback: generate UUID using /dev/urandom
        od -x /dev/urandom | head -1 | awk '{OFS="-"; print $2$3,$4,$5,$6,$7$8$9}' | \
        sed 's/^\(.\{8\}\)\(.\{4\}\)\(.\{4\}\)\(.\{4\}\)\(.\{12\}\)$/\1-\2-\3-\4-\5/'
    fi
}

# Parse command line arguments
USE_CURRENT=false
if [ "$1" = "--use-current" ]; then
    USE_CURRENT=true
fi

if [ "$USE_CURRENT" = true ]; then
    # Use current session ID from file
    if [ -f "$SESSION_FILE" ]; then
        SESSION_ID=$(cat "$SESSION_FILE" 2>/dev/null | tr -d '[:space:]')
        if [ -z "$SESSION_ID" ]; then
            echo "Error: No session ID found in $SESSION_FILE"
            echo "Run without --use-current to generate a new session ID"
            exit 1
        fi
        echo "Current Session Information:"
        echo "- Session ID: $SESSION_ID"
        echo "- Source: $SESSION_FILE"
        echo "- Mode: Using existing session (no changes made)"
    else
        echo "Error: Session file not found at $SESSION_FILE"
        echo "Run without --use-current to generate a new session ID"
        exit 1
    fi
    exit 0
fi

# Generate new session ID
SESSION_ID=$(generate_uuid)
TIMESTAMP=$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S%z')

# Display session information
echo "Generated Session Information:"
echo "- Session ID: $SESSION_ID"
echo "- Generated at: $TIMESTAMP"

# Create tmp directory if it doesn't exist
mkdir -p "$TMP_DIR"

# Check if session file exists and show current session if present
if [ -f "$SESSION_FILE" ]; then
    CURRENT_SESSION=$(cat "$SESSION_FILE" 2>/dev/null | tr -d '[:space:]')
    if [ ! -z "$CURRENT_SESSION" ]; then
        echo "- Previous session: $CURRENT_SESSION (will be overwritten)"
    fi
fi

# Write new session ID to file (overwrites existing content)
echo "$SESSION_ID" > "$SESSION_FILE"

# Verify write was successful
if [ -f "$SESSION_FILE" ]; then
    WRITTEN_ID=$(cat "$SESSION_FILE" | tr -d '[:space:]')
    if [ "$WRITTEN_ID" = "$SESSION_ID" ]; then
        echo "- Status: ✅ Successfully written to $SESSION_FILE"
        echo ""
        echo "Session ID is now active: $SESSION_ID"
        echo "This session ID will be used by other scripts for organizing logs and context."
    else
        echo "- Status: ❌ Error: Failed to write session ID correctly"
        exit 1
    fi
else
    echo "- Status: ❌ Error: Failed to create session file"
    exit 1
fi

# Optional: Export to environment for current shell session
echo ""
echo "To use this session ID in your current shell, run:"
echo "  export CLAUDE_SESSION_ID='$SESSION_ID'"