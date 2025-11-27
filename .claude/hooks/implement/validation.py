#!/usr/bin/env python3
"""
Stop hook to deactivate /implement workflow when session ends.
"""

import json
import os
import sys

HOOK_DIR = os.path.dirname(__file__)
STATE_FILE = os.path.join(HOOK_DIR, "implement-active.json")


def main():
    try:
        # Clear the active state
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "w") as f:
                json.dump({"active": False}, f)
        sys.exit(0)

    except Exception as e:
        print(f"Deactivate hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
