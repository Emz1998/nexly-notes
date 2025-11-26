#!/usr/bin/env python3
"""
PostToolUse hook to trigger code reviews after file edits or Task tool usage.

Triggers appropriate reviewer agents based on file type:
- .py, .js, .ts, .jsx, .tsx -> code-reviewer
- .md, .mdx in .claude/ -> claude-config-reviewer
- .md, .mdx in specs/ -> specs-reviewer
- Task tool -> subagent-reviewer

Iteration Control:
- Reads iteration.json to check if review iteration is enabled
- If iterate=true, prompts Claude to keep improving until rating >= 8/10
- When rating >= 8, Claude should set iterate=false to exit the loop
"""

import json
import os
import sys

# Reviewer subagent types to exclude to avoid circular dependencies
REVIEWER_SUBAGENTS = {
    "code-reviewer",
    "specs-reviewer",
    "claude-config-reviewer",
    "subagent-reviewer",
}

# Paths
HOOK_DIR = os.path.dirname(__file__)
ITERATION_FILE = os.path.join(HOOK_DIR, "iteration.json")
PROMPTS_DIR = os.path.join(HOOK_DIR, "prompts")


def load_prompt(prompt_name: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = os.path.join(PROMPTS_DIR, f"{prompt_name}.md")
    try:
        with open(prompt_path, "r") as f:
            return f.read().strip()
    except (IOError, FileNotFoundError):
        return ""


def get_iteration_flag() -> bool:
    """Read the iteration flag from iteration.json."""
    try:
        if os.path.exists(ITERATION_FILE):
            with open(ITERATION_FILE, "r") as f:
                data = json.load(f)
                return data.get("iterate", False)
    except (json.JSONDecodeError, IOError):
        pass
    return False


def get_iteration_context() -> str:
    """Load iteration instructions from prompt file."""
    return "\n\n" + load_prompt("iteration-context")


def review_code_file(file_path: str, iterate: bool) -> dict:
    """Generate review context for code files."""
    base_context = load_prompt("code-review").format(file_path=file_path)

    if iterate:
        base_context += get_iteration_context()

    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": base_context,
        }
    }


def review_md_file(file_path: str, iterate: bool) -> dict:
    """Generate review context for markdown files based on location."""
    if ".claude" in file_path:
        base_context = load_prompt("claude-config-review").format(file_path=file_path)
        if iterate:
            base_context += get_iteration_context()
        return {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": base_context,
            }
        }
    elif "specs" in file_path:
        base_context = load_prompt("specs-review").format(file_path=file_path)
        if iterate:
            base_context += get_iteration_context()
        return {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": base_context,
            }
        }
    else:
        # No review needed for other markdown files
        return {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": "",
            }
        }


def review_subagent(subagent_name: str, iterate: bool) -> dict:
    """Generate review context for subagent completion."""
    base_context = load_prompt("subagent-review").format(subagent_name=subagent_name)

    if iterate:
        base_context += get_iteration_context()

    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": base_context,
        }
    }


def main():
    try:
        # Read input from Claude Code
        input_data = json.load(sys.stdin)

        # Check iteration flag
        iterate = get_iteration_flag()

        tool_input = input_data.get("tool_input", {})
        tool_response = input_data.get("tool_response", {})

        # Ensure tool_response is a dict (not string)
        if isinstance(tool_response, str):
            try:
                tool_response = json.loads(tool_response) if tool_response else {}
            except json.JSONDecodeError:
                tool_response = {}

        # Ensure tool_input is a dict (not string)
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input) if tool_input else {}
            except json.JSONDecodeError:
                tool_input = {}

        # Check for file path in tool_response
        file_path = (
            tool_response.get("filePath", "") if isinstance(tool_response, dict) else ""
        )

        if file_path:
            if file_path.endswith((".py", ".js", ".ts", ".jsx", ".tsx", ".html")):
                # Review code files
                output = review_code_file(file_path, iterate)
                print(json.dumps(output))
                sys.exit(0)
            elif file_path.endswith((".md", ".mdx")):
                # Review markdown files
                output = review_md_file(file_path, iterate)
                print(json.dumps(output))
                sys.exit(0)

        # Check for subagent type in tool_input (Task tool)
        if isinstance(tool_input, dict) and "subagent_type" in tool_input:
            subagent_name = tool_input.get("subagent_type", "")
            # Skip reviewer agents to avoid circular dependencies
            if subagent_name in REVIEWER_SUBAGENTS:
                sys.exit(0)
            output = review_subagent(subagent_name, iterate)
            print(json.dumps(output))
            sys.exit(0)

        # No matching criteria - exit silently
        sys.exit(0)

    except Exception as e:
        # Log error to stderr but don't block
        print(f"Reviewer hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
