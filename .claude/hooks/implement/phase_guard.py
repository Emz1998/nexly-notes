#!/usr/bin/env python3
"""
Phase Transition Guard Hook - PreToolUse

Enforces strict sequential phase transitions when modifying state.json.
Only allows advancing to the immediate next phase.

Exit Codes:
  0 = ALLOW (tool proceeds)
  2 = BLOCK (tool blocked, message shown to Claude)
"""

import json
import re
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
# PHASE EXTRACTION
# =============================================================================

def extract_phase_from_content(content: str) -> str | None:
    """Extract phase value from JSON content string."""
    try:
        data = json.loads(content)
        return data.get("phase")
    except (json.JSONDecodeError, TypeError):
        pass

    # Fallback: regex pattern matching for "phase": "value"
    match = re.search(r'"phase"\s*:\s*"([^"]+)"', content)
    if match:
        return match.group(1)

    return None


def is_state_file(file_path: str) -> bool:
    """Check if the file path targets state.json."""
    return file_path.endswith("state.json") and "implement" in file_path


# =============================================================================
# TRANSITION VALIDATION
# =============================================================================

def get_phase_index(phase: str) -> int:
    """Get the index of a phase in the workflow. Returns -1 if not found."""
    try:
        return WORKFLOW_PHASES.index(phase)
    except ValueError:
        return -1


def validate_transition(current_phase: str, new_phase: str) -> tuple[bool, str]:
    """
    Validate phase transition.

    Returns:
        (is_valid, error_message)
    """
    current_idx = get_phase_index(current_phase)
    new_idx = get_phase_index(new_phase)

    # Unknown phase
    if new_idx == -1:
        return False, f"Unknown phase: '{new_phase}'. Valid phases: {', '.join(WORKFLOW_PHASES)}"

    # Same phase (blocked per requirements)
    if new_idx == current_idx:
        return False, (
            f"BLOCKED: Cannot stay on the same phase '{current_phase}'.\n"
            f"Must advance to next phase: '{WORKFLOW_PHASES[current_idx + 1]}'"
            if current_idx < len(WORKFLOW_PHASES) - 1
            else f"BLOCKED: Already at final phase '{current_phase}'. Workflow complete."
        )

    # Going backward (blocked)
    if new_idx < current_idx:
        return False, (
            f"BLOCKED: Cannot go backward from '{current_phase}' to '{new_phase}'.\n"
            f"Must advance to: '{WORKFLOW_PHASES[current_idx + 1]}'"
            if current_idx < len(WORKFLOW_PHASES) - 1
            else f"BLOCKED: Already at final phase '{current_phase}'."
        )

    # Jumping forward (blocked)
    if new_idx > current_idx + 1:
        expected = WORKFLOW_PHASES[current_idx + 1]
        return False, (
            f"BLOCKED: Cannot skip phases. Current: '{current_phase}', Attempted: '{new_phase}'.\n"
            f"Must advance sequentially to: '{expected}'"
        )

    # Valid: exactly next phase
    return True, ""


# =============================================================================
# EVENT HANDLER
# =============================================================================

def on_pre_tool_use(hook_input: dict) -> None:
    """
    PreToolUse Event Handler

    Validates phase transitions when Write/Edit targets state.json.
    Only allows advancing to the immediate next phase.
    """
    tool_name = hook_input.get("tool_name", "")
    tool_params = hook_input.get("tool_input", {})

    # Only check Write and Edit tools
    if tool_name not in ("Write", "Edit"):
        allow_tool_use()

    # Get target file path
    file_path = tool_params.get("file_path", "")

    # Only check state.json modifications
    if not is_state_file(file_path):
        allow_tool_use()

    # Extract new phase from content
    if tool_name == "Write":
        content = tool_params.get("content", "")
    else:  # Edit
        content = tool_params.get("new_string", "")

    new_phase = extract_phase_from_content(content)

    if not new_phase:
        # Cannot determine new phase, allow (might be non-phase edit)
        allow_tool_use()

    # Get current phase and validate transition
    current_phase = read_current_phase()
    is_valid, error_msg = validate_transition(current_phase, new_phase)

    if not is_valid:
        block_tool_use(error_msg)

    allow_tool_use()


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    """Main entry point for the hook."""
    hook_input = json.load(sys.stdin)
    on_pre_tool_use(hook_input)


if __name__ == "__main__":
    main()
