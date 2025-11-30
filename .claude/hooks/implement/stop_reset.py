#!/usr/bin/env python3
"""
Stop Hook - Reset Phase on Session Stop

Resets the workflow phase back to 'explore' when a session ends.

Exit Codes:
  0 = Success
"""

import json
import sys
from pathlib import Path


# =============================================================================
# CONFIGURATION
# =============================================================================

WORKFLOW_STATE_FILE = Path(__file__).parent / "state.json"

DEFAULT_PHASE = "explore"


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Reset phase to explore on stop."""
    # Read stdin (required by hook protocol)
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # Reset state to explore
    state = {
        "active": False,
        "phase": DEFAULT_PHASE
    }

    with open(WORKFLOW_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    sys.exit(0)


if __name__ == "__main__":
    main()
