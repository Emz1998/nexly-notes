#!/usr/bin/env python3
"""
Hook: plan-mode
Event: PreToolUse - ExitPlanMode
Purpose: Force user confirmation before exiting plan mode
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cache_manager import load_cache


def load_plan(file_path: str):
    """Load plan content from file."""
    try:
        for filepath in Path("/home/emhar/.claude/plans/").glob("*.md"):
            with open(filepath, "r") as f:
                content = f.read()
                return content
    except FileNotFoundError:
        return None


def delete_prev_plan():
    """Delete previous plan files."""
    plans_dir = Path(".claude/plans")
    if plans_dir.exists():
        for file in plans_dir.glob("*.md"):
            if file.is_file():
                file.unlink()


def switch_to_plan_mode():
    """Handle plan mode switching logic for PreToolUse events."""

    response = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": "Confirm exiting plan mode",
            "updatedInput": {
                "tool_input": load_cache("content"),
            },
        }
    }
    print(json.dumps(response))
    sys.exit(0)
