#!/usr/bin/env python3
"""
Hook: plan-mode
Event: PreToolUse - ExitPlanMode
Purpose: Force user confirmation before exiting plan mode
"""

import json
import sys
from .cache_manager import set_cache


def deactivate():

    set_cache("is_active", False)

    # Force user to review plan before exiting plan mode
    response = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": "Please ask the user to review the plan before proceeding.",
        }
    }

    print(json.dumps(response))
    sys.exit(0)
