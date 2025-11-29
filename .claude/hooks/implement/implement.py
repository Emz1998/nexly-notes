#!/usr/bin/env python3
"""
PostToolUse hook for /implement command workflow reviews.

Deterministic triggers (only when /implement is active):
1. Write to implementation-plan.md -> plan-consultant review
2. Code file edits (Write/Edit) -> code-reviewer review

This replaces skill-based triggering with hook-based deterministic triggers.
"""

import json
import os
import sys
from typing import Literal

# Paths
HOOK_DIR = os.path.dirname(__file__)
PROMPTS_DIR = os.path.join(HOOK_DIR, "prompts")
STATE_FILE = os.path.join(HOOK_DIR, "implement-active.json")

# Plan file pattern - triggers plan-consultant review
PLAN_FILE_NAME = "implementation-plan.md"

# Code file extensions that trigger code review
CODE_EXTENSIONS = (".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css")


## Send context to Claude
def send_context(context: str, hook_event: str = "PostToolUse") -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": hook_event,
            "additionalContext": context,
        }
    }


def is_implement_active() -> bool:
    """Check if /implement command is currently active."""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                return data.get("active", False)
    except (json.JSONDecodeError, IOError):
        pass
    return False


def load_prompt(prompt_name: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = os.path.join(PROMPTS_DIR, f"{prompt_name}.md")
    try:
        with open(prompt_path, "r") as f:
            return f.read().strip()
    except (IOError, FileNotFoundError):
        return ""


def check_file(file_path: str, file_type: Literal["code", "plan"]) -> bool:
    """Check if the file is an implementation plan file."""
    if not file_path:
        return False
    # Match files ending with implementation-plan.md in session directories
    return (
        file_path.endswith(PLAN_FILE_NAME)
        if file_type == "plan"
        else file_path.endswith(CODE_EXTENSIONS)
    )


def trigger_review(
    file_path: str, review_type: Literal["research", "code", "plan"]
) -> dict:
    """Trigger research_reviewer to review after code file edits."""
    context = load_prompt(f"{review_type}-review")
    if context:
        context = context.format(file_path=file_path)
    else:
        context = load_prompt("default-prompt")

    return send_context(context)


def validate_value(value: str | dict) -> str | dict:
    try:
        if value and isinstance(value, (str, dict)):
            return json.loads(value)
        else:
            return {}
    except json.JSONDecodeError:
        return {}


def extract_value(input_data: dict, value: str) -> any:
    raw_value = input_data.get(value, "")
    return validate_value(raw_value)


def main():
    try:
        input_data = json.load(sys.stdin)

        # Only run if /implement is active
        ## if not is_implement_active():
        ## sys.exit(0)

        # Get tool input
        tool_input = extract_value(input_data, "tool_input")

        # Get tool response
        tool_response = extract_value(input_data, "tool_response")

        # Get tool name
        tool_name = input_data.get("tool_name", "")

        # Check for Write tool - triggers based on file written
        if tool_name in ("Write", "MultiEdit", "Edit"):
            file_path = tool_response.get("file_path", "")

            # Check if implementation plan was written -> trigger plan review
            if check_file(file_path, "plan"):
                output = trigger_review(file_path, "plan")
                print(json.dumps(output))
                sys.exit(0)

            # Check if code file was written -> trigger code review
            if check_file(file_path, "code"):
                output = trigger_review(file_path, "code")
                print(json.dumps(output))
                sys.exit(0)

        # No matching trigger
        sys.exit(0)

    except Exception as e:
        print(f"Implement hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
