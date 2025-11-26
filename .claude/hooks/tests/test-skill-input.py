#!/usr/bin/env python3
"""
Test hook to capture and log stdin input for Skill tool
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    try:
        # Read input from Claude Code
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")

        # Log the input to a file
        project_dir = Path.cwd()
        log_file = project_dir / '.claude' / 'skill-input-test.log'

        with open(log_file, 'a') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Tool: {tool_name}\n")
            f.write(f"{'='*80}\n")
            f.write(json.dumps(input_data, indent=2))
            f.write(f"\n{'='*80}\n\n")

        # Example: Only modify TodoWrite inputs (remove or customize this)
        if tool_name == "TodoWrite":
            output_data = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "updatedInput": {
                        "todos": [
                            {
                                "content": "Test task 1",
                                "status": "pending",
                                "activeForm": "Test task 1"
                            }
                        ]
                    }
                }
            }
            print(json.dumps(output_data))

        # Exit successfully without blocking or modifying
        sys.exit(0)

    except Exception as e:
        # Log error
        print(f"Test hook error: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
