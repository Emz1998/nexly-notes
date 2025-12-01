#!/usr/bin/env python3
"""
Hook: plan_mode
Event: UserPromptSubmit
Purpose: Activate plan mode when /plan command is used
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json, set_cache


def activate_plan_mode():
    input_data = read_stdin_json()
    if input_data.get("prompt", "").startswith("/plan"):
        set_cache("plan_mode", "is_active", True)
        print("Planning Phase. Do not write any code")
    sys.exit(0)


if __name__ == "__main__":
    activate_plan_mode()
