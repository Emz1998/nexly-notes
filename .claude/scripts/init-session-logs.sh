#!/bin/bash

# Session Log Initializer Script
# Usage: ./init-session-logs.sh [session-id]
# Example: ./init-session-logs.sh session-2024-01-15-001
#
# Priority for session ID:
# 1. Command line argument
# 2. CLAUDE_SESSION_ID environment variable
# 3. Read from .claude/tmp/session_id.txt if exists
# 4. Read from .claude/current-session.txt if exists (legacy)
# 5. Generate timestamp-based ID as fallback

# Function to get Claude Code session ID if available
get_claude_session_id() {
    # Check for environment variable first (Claude Code sets this)
    if [ ! -z "$CLAUDE_SESSION_ID" ]; then
        echo "$CLAUDE_SESSION_ID"
        return
    fi

    # Check for Claude Code session environment variable
    if [ ! -z "$CLAUDE_CODE_SESSION_ID" ]; then
        echo "$CLAUDE_CODE_SESSION_ID"
        return
    fi

    # Check for session ID file in .claude/tmp/
    if [ -f ".claude/tmp/session_id.txt" ]; then
        # Read and trim whitespace
        cat ".claude/tmp/session_id.txt" | tr -d '[:space:]'
        return
    fi

    # No Claude session found
    echo ""
}

# Get session ID from argument or other sources
if [ -z "$1" ]; then
    # Try to get Claude session ID
    CLAUDE_ID=$(get_claude_session_id)

    if [ ! -z "$CLAUDE_ID" ]; then
        SESSION_ID="session_$CLAUDE_ID"
        echo "Using Claude Code session ID: $SESSION_ID"
    else
        # Fallback to timestamp-based ID
        SESSION_ID="session-$(date +%Y%m%d-%H%M%S)"
        echo "No session ID provided. Generated: $SESSION_ID"
    fi
else
    SESSION_ID="$1"
    echo "Using provided session ID: $SESSION_ID"
fi

# Set the base directory
BASE_DIR="tmp/$SESSION_ID"

# Create directory structure
echo "Creating directory structure..."
mkdir -p "$BASE_DIR/logs"

# Create SESSIONLOG.md
echo "Creating SESSIONLOG.md..."
cat > "$BASE_DIR/logs/SESSIONLOG.md" << 'EOF'
# Session Log

<!-- [Timestamp] | [Agent] | [Action with Context] | [Status] -->
<!-- Example: 2024-01-15 14:30 | fullstack-developer | Implemented user auth: created Firebase auth service, added OAuth providers, built login/signup components, configured security rules | ✅ Completed -->

## Session Activity

EOF

# Create CHANGELOG.md
echo "Creating CHANGELOG.md..."
cat > "$BASE_DIR/logs/CHANGELOG.md" << 'EOF'
# Changelog

<!-- [Date] | [Files Changed] | [Change Description] -->
<!-- Example: 2024-01-15 | auth.service.ts, auth.controller.ts, login.tsx | Added OAuth2 integration with Google and GitHub providers -->

## Changes Made

EOF

# Create SUCCESSLOG.md
echo "Creating SUCCESSLOG.md..."
cat > "$BASE_DIR/logs/SUCCESSLOG.md" << 'EOF'
# Success Log

<!-- [Date] | [Feature] | [What Passed] | [Metrics] -->
<!-- Example: 2024-01-15 | User Login | All 25 tests passing | 98% coverage, 200ms response -->

## Successes

EOF

# Create BLOCKERS.md
echo "Creating BLOCKERS.md..."
cat > "$BASE_DIR/logs/BLOCKERS.md" << 'EOF'
# Blockers

<!-- [Date] | [Issue] | [Impact] | [Next Steps] -->
<!-- Example: 2024-01-15 | Firebase config missing | Can't deploy | Need env variables from DevOps -->

## Current Blockers

EOF

# Create REVISION_REQUEST.md
echo "Creating REVISION_REQUEST.md..."
cat > "$BASE_DIR/logs/REVISION_REQUEST.md" << 'EOF'
# Revision Requests

<!-- [Date] | [Component] | [Change Needed] | [Priority: H/M/L] -->
<!-- Example: 2024-01-15 | Button Component | Add aria-labels for accessibility | M -->

## Requested Revisions

EOF

echo "✅ Session logs initialized successfully!"
echo "📁 Location: $BASE_DIR/logs/"
echo ""
echo "Log files created:"
echo "  - SESSIONLOG.md (all agents)"
echo "  - CHANGELOG.md (all agents)"
echo "  - SUCCESSLOG.md (fullstack-developer)"
echo "  - BLOCKERS.md (fullstack-developer)"
echo "  - REVISION_REQUEST.md (fullstack-developer)"