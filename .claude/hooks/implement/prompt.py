#!/usr/bin/env python3
"""
TDD Workflow - UserPromptSubmit Handler

Detects /implement command to start the workflow.
"""

import json
import sys
from pathlib import Path


# =============================================================================
# CONFIGURATION
# =============================================================================

WORKFLOW_STATE_FILE = Path(__file__).parent / "state.json"

DEFAULT_PHASE = "explore"

IMPLEMENT_COMMAND = "/implement"


# =============================================================================
# STATE MANAGEMENT
# =============================================================================

def save_current_phase(phase: str) -> None:
    """Persist the current workflow phase to state file."""
    with open(WORKFLOW_STATE_FILE, "w") as f:
        json.dump({"active": True, "phase": phase}, f, indent=2)


# =============================================================================
# HANDLER
# =============================================================================

def on_user_prompt_submit(hook_input: dict) -> None:
    """
    UserPromptSubmit Event Handler

    When user types /implement, initialize workflow at explore phase.
    """
    user_prompt = hook_input.get("prompt", "").strip()

    if user_prompt.startswith(IMPLEMENT_COMMAND):
        save_current_phase(DEFAULT_PHASE)
        print(f"Workflow started at '{DEFAULT_PHASE}' phase")

    sys.exit(0)


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    hook_input = json.load(sys.stdin)
    on_user_prompt_submit(hook_input)


if __name__ == "__main__":
    main()
