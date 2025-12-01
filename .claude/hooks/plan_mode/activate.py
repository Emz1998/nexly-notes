#!/usr/bin/env python3
"""
Hook: plan_mode
Event: PreToolUse - ExitPlanMode
Purpose: Force user confirmation before exiting plan mode
"""

import json
import sys


def load_cache(key: str) -> bool:
    try:
        with open(".claude/hooks/plan_mode/cache.json") as f:
            cache = json.load(f)
            return cache.get(key, None)
    except json.JSONDecodeError:
        return False


def set_cache(key: str, value: bool) -> None:
    try:
        with open(".claude/hooks/plan_mode/cache.json", "r+") as f:
            cache = json.load(f)
            cache[key] = value
            f.seek(0)
            json.dump(cache, f)
            f.truncate()
    except json.JSONDecodeError:
        pass


def activate_plan_mode():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)

    prompt = input_data.get("prompt", "")

    if prompt.startswith("/plan"):
        set_cache("is_active", True)
        response = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "Write the plan in .claude/plans/[plan-name].md first using `Write` Tool then use `ExitPlanMode` to present the plan based on user's instructions.",
            }
        }
        print(json.dumps(response))
        sys.exit(0)
