#!/usr/bin/env python3
"""
TDD Workflow Compliance Hook - PreToolUse & SessionStart

Enforces linear phase progression:
explore → research → research_review → plan → plan_consult →
failing_test → passing_test → refactor → code_review → commit

Exit Codes:
  0 = ALLOW (tool proceeds)
  2 = BLOCK (tool blocked, message shown to Claude)
"""

import json
import sys
from pathlib import Path


# =============================================================================
# WORKFLOW CONFIGURATION
# =============================================================================

WORKFLOW_PHASES = [
    "explore",
    "research",
    "research_review",
    "plan",
    "plan_consult",
    "failing_test",
    "passing_test",
    "refactor",
    "code_review",
    "commit",
]

REQUIRED_AGENT_BY_PHASE = {
    "explore":         "codebase-explorer",
    "research":        "research-specialist",
    "research_review": "research-consultant",
    "plan":            "strategic-planner",
    "plan_consult":    "plan-consultant",
    "failing_test":    "test-manager",
    "passing_test":    "test-manager",
    "code_review":     "code-reviewer",
    "commit":          "version-manager",
}

PHASES_ALLOWING_CODE_CHANGES = ("failing_test", "passing_test", "refactor")

SOURCE_CODE_EXTENSIONS = (".py", ".js", ".ts", ".tsx", ".jsx", ".css", ".html")

WORKFLOW_STATE_FILE = Path(__file__).parent / "state.json"

DEFAULT_PHASE = "explore"


# =============================================================================
# WORKFLOW STATE
# =============================================================================

def read_current_phase() -> str:
    """Read the current workflow phase from state file."""
    try:
        with open(WORKFLOW_STATE_FILE) as f:
            return json.load(f).get("phase", DEFAULT_PHASE)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_PHASE


def save_current_phase(phase: str) -> None:
    """Persist the current workflow phase to state file."""
    with open(WORKFLOW_STATE_FILE, "w") as f:
        json.dump({"active": True, "phase": phase}, f, indent=2)


# =============================================================================
# HOOK RESPONSES
# =============================================================================

def block_tool_use(reason: str) -> None:
    """Block the tool call. Exit 2 sends reason to Claude via stderr."""
    print(reason, file=sys.stderr)
    sys.exit(2)


def allow_tool_use() -> None:
    """Allow the tool call to proceed. Exit 0 = success."""
    sys.exit(0)


# =============================================================================
# TOOL DETECTION
# =============================================================================

def is_source_code_file(file_path: str) -> bool:
    """Check if file path has a source code extension."""
    return file_path.endswith(SOURCE_CODE_EXTENSIONS)


def is_version_control_command(command: str) -> bool:
    """Check if bash command is a git operation."""
    return command.strip().startswith("git ")


# =============================================================================
# EVENT HANDLERS
# =============================================================================

def on_pre_tool_use(hook_input: dict) -> None:
    """
    PreToolUse Event Handler

    Enforces workflow compliance rules:
    1. Task tool → must use the agent assigned to current phase
    2. Write/Edit → code files only in coding phases
    3. Bash → git commands only in commit phase
    """
    current_phase = read_current_phase()
    tool_name = hook_input.get("tool_name", "")
    tool_params = hook_input.get("tool_input", {})

    # Rule 1: Enforce agent assignment per phase
    if tool_name == "Task":
        requested_agent = tool_params.get("subagent_type", "")
        required_agent = REQUIRED_AGENT_BY_PHASE.get(current_phase)

        if required_agent and requested_agent != required_agent:
            block_tool_use(
                f"BLOCKED: Phase '{current_phase}' requires '{required_agent}' agent.\n"
                f"Requested: '{requested_agent}'. Complete current phase first."
            )

    # Rule 2: Restrict code changes to coding phases
    if tool_name in ("Write", "Edit"):
        target_file = tool_params.get("file_path", "")

        if is_source_code_file(target_file) and current_phase not in PHASES_ALLOWING_CODE_CHANGES:
            block_tool_use(
                f"BLOCKED: Cannot modify source code in '{current_phase}' phase.\n"
                f"Code changes allowed in: {', '.join(PHASES_ALLOWING_CODE_CHANGES)}"
            )

    # Rule 3: Restrict git to commit phase
    if tool_name == "Bash":
        bash_command = tool_params.get("command", "")

        if is_version_control_command(bash_command) and current_phase != "commit":
            block_tool_use(
                f"BLOCKED: Git commands only allowed in 'commit' phase.\n"
                f"Current phase: '{current_phase}'"
            )

    allow_tool_use()


def on_session_start(hook_input: dict) -> None:
    """
    SessionStart Event Handler

    Resets workflow to initial phase.
    """
    save_current_phase(DEFAULT_PHASE)
    sys.exit(0)
    

# =============================================================================
# CHECK IF IMPLEMENT IS ACTIVE
# =============================================================================
def is_active() -> bool:
  try:
    with open(WORKFLOW_STATE_FILE) as f:
      return json.load(f).get("active", False)
  except (FileNotFoundError, json.JSONDecodeError):
    return False
    

# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    """Dispatch based on CLI argument: 'pre' or 'init'."""
    if not is_active():
      sys.exit(0)
    
    event_type = sys.argv[1] if len(sys.argv) > 1 else "pre"
    hook_input = json.load(sys.stdin)

    if event_type == "init":
        on_session_start(hook_input)
    else:
        on_pre_tool_use(hook_input)


if __name__ == "__main__":
    main()
