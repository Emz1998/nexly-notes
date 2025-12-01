#!/usr/bin/env python3
"""
Compact Instructions Hook

This hook is triggered before Claude Code compacts/summarizes conversations.
It provides Claude with specific instructions for creating the summary.

Event: PreCompact
Trigger: manual or auto
"""

import json
import sys

def main():
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        # Extract relevant information
        hook_event = input_data.get("hook_event_name", "")
        trigger = input_data.get("trigger", "")
        session_id = input_data.get("session_id", "")

        # Verify this is a PreCompact event
        if hook_event != "PreCompact":
            # Not the event we're looking for, exit silently
            sys.exit(0)

        # The instruction to provide to Claude for compacting
        compact_instruction = "Give a brief summary of what we have done and any current issues"

        # Return the instruction as additional context
        # For PreCompact hooks, we use stdout to provide the instruction
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreCompact",
                "additionalInstructions": compact_instruction
            }
        }

        # Print the instruction directly as it will be added to the compact process
        print(compact_instruction)

        # Exit successfully
        sys.exit(0)

    except json.JSONDecodeError as e:
        # Invalid JSON input
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Other errors
        print(f"Error in compact-instructions hook: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()