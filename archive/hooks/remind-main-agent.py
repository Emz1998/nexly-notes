#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Hook: remind-main-agent

Purpose: Remind the main agent to log significant tasks in TASKLOG.md.
This hook monitors tool usage and provides gentle reminders for task logging.

Hook Behavior:
1. Monitor PreToolUse events for significant operations
2. Display reminder for operations that should be logged
3. Target main agent activities (Write, Edit, MultiEdit, Bash)
4. Show brief, non-intrusive reminder message
5. Exit cleanly without blocking tool execution

Event Triggers: PreToolUse
Action: Display reminder to log tasks
"""

import json
import sys

def main():
    """Main hook execution function."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Exit silently on JSON parse errors
        sys.exit(0)
    except Exception:
        # Exit silently on any other errors
        sys.exit(0)

    # Check if this is a PreToolUse event
    tool_name = input_data.get("tool_name", "")

    # List of significant tools that should trigger reminder
    significant_tools = [
        "Write",       # File creation
        "Edit",        # File modification
        "MultiEdit",   # Multiple file edits
        "Bash",        # Command execution
        "TodoWrite"    # Task management
    ]

    # Display reminder for significant operations
    if tool_name in significant_tools:
        print("📝 Remember to log this task in .claude/logs/TASKLOG.md")

    # Exit cleanly to allow tool execution to proceed
    sys.exit(0)

if __name__ == "__main__":
    main()