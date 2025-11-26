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

# Paths
HOOK_DIR = os.path.dirname(__file__)
PROMPTS_DIR = os.path.join(HOOK_DIR, "prompts")
STATE_FILE = os.path.join(HOOK_DIR, "implement-active.json")

# Plan file pattern - triggers plan-consultant review
PLAN_FILE_NAME = "implementation-plan.md"

# Code file extensions that trigger code review
CODE_EXTENSIONS = (".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css")


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


def is_plan_file(file_path: str) -> bool:
    """Check if the file is an implementation plan file."""
    if not file_path:
        return False
    # Match files ending with implementation-plan.md in session directories
    return file_path.endswith(PLAN_FILE_NAME)


def trigger_plan_review(file_path: str) -> dict:
    """Trigger plan-consultant review after implementation plan is written."""
    context = load_prompt("plan-review")
    if not context:
        context = f"The strategic-planner has written the implementation plan to {file_path}. Call the plan-consultant agent to review this implementation strategy. Ask for a rating on a scale of 1 to 10."

    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    }


def trigger_code_review(file_path: str) -> dict:
    """Trigger code-reviewer review after code file edits."""
    context = load_prompt("code-review")
    if context:
        context = context.format(file_path=file_path)
    else:
        context = f"Call the code-reviewer agent to review the file {file_path}. Ask for a rating on a scale of 1 to 10."

    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    }


def main():
    try:
        input_data = json.load(sys.stdin)

        # Only run if /implement is active
        if not is_implement_active():
            sys.exit(0)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        tool_response = input_data.get("tool_response", {})

        # Parse tool_input if string
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input) if tool_input else {}
            except json.JSONDecodeError:
                tool_input = {}

        # Parse tool_response if string
        if isinstance(tool_response, str):
            try:
                tool_response = json.loads(tool_response) if tool_response else {}
            except json.JSONDecodeError:
                tool_response = {}

        # Check for Write tool - triggers based on file written
        if tool_name == "Write":
            file_path = ""

            # Get file path from tool_input or tool_response
            if isinstance(tool_input, dict):
                file_path = tool_input.get("file_path", "")
            if not file_path and isinstance(tool_response, dict):
                file_path = tool_response.get("filePath", "")

            # Check if implementation plan was written -> trigger plan review
            if is_plan_file(file_path):
                output = trigger_plan_review(file_path)
                print(json.dumps(output))
                sys.exit(0)

            # Check if code file was written -> trigger code review
            if file_path and file_path.endswith(CODE_EXTENSIONS):
                output = trigger_code_review(file_path)
                print(json.dumps(output))
                sys.exit(0)

        # Check for Edit/MultiEdit tool - code file edits trigger code review
        if tool_name in ("Edit", "MultiEdit"):
            file_path = ""

            # Get file path from tool_input or tool_response
            if isinstance(tool_input, dict):
                file_path = tool_input.get("file_path", "")
            if not file_path and isinstance(tool_response, dict):
                file_path = tool_response.get("filePath", "")

            # Only trigger for code files
            if file_path and file_path.endswith(CODE_EXTENSIONS):
                output = trigger_code_review(file_path)
                print(json.dumps(output))
                sys.exit(0)

        # No matching trigger
        sys.exit(0)

    except Exception as e:
        print(f"Implement hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
