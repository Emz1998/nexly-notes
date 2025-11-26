#!/usr/bin/env python3
"""
PreToolUse hook to activate /implement workflow when SlashCommand:/implement is triggered.
"""

import json
import os
import sys

HOOK_DIR = os.path.dirname(__file__)
STATE_FILE = os.path.join(HOOK_DIR, "implement-active.json")


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input) if tool_input else {}
            except json.JSONDecodeError:
                tool_input = {}

        # Check if SlashCommand is calling /implement
        if tool_name == "SlashCommand":
            command = tool_input.get("command", "")
            if command.startswith("/implement"):
                with open(STATE_FILE, "w") as f:
                    json.dump({"active": True}, f)

        sys.exit(0)

    except Exception as e:
        print(f"Activate hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
