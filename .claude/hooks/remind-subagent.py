#!/usr/bin/env python3
"""
Remind Subagent Hook

A lightweight hook that reminds agents to log tasks in TASKLOG.md when subagents are launched.
This hook triggers on PreToolUse event for Task tool calls and displays a simple reminder message.
"""

import json
import sys


def main():
    """Main hook execution function."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Exit silently if JSON is invalid - don't interfere with tool execution
        sys.exit(0)

    # Check if this is a Task tool (subagent launch)
    tool_name = input_data.get("tool_name", "")

    if tool_name == "Task":
        # Display the reminder message to stdout so it appears in the console
        print("📝 Remember to log this task in .claude/logs/TASKLOG.md")

    # Exit with code 0 to allow the tool execution to proceed normally
    sys.exit(0)


if __name__ == "__main__":
    main()