#!/usr/bin/env python3
"""Code Mode Activation - UserPromptSubmit Handler.

Activates TDD workflow when /code command is issued.
Requires a plan file to exist before activation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import code_mode, find_plan_file, block_agent

TDD_PHASES = ["failing_test", "passing_test", "refactor", "troubleshoot", "commit"]


def activate_code_mode(input_data: dict) -> None:
    """Activate code mode after plan is created.

    Prerequisites:
    - Plan file must exist at: project/[MS-NN]:[MS-Description]/plans/plan_[session-id]_[MMDDYY].md
    """
    session_id = input_data.get("session_id", "")

    plan_file = find_plan_file(session_id)
    if not plan_file or not plan_file.exists():
        print("Code Mode: Plan file not found. Complete planning phase first.", file=sys.stderr)
        sys.exit(2)

    code_mode.activate(
        session_id,
        "TDD Workflow Started. Phase: failing_test - Write failing tests first.",
        current_phase="failing_test",
        plan_file=str(plan_file)
    )
    sys.exit(0)


def advance_phase() -> str:
    """Advance to the next TDD phase."""
    current_phase = code_mode.get("current_phase") or "failing_test"

    try:
        current_idx = TDD_PHASES.index(current_phase)
        if current_idx < len(TDD_PHASES) - 1:
            next_phase = TDD_PHASES[current_idx + 1]
            code_mode.set("current_phase", next_phase)
            return next_phase
    except ValueError:
        pass

    return current_phase


def get_current_phase() -> str:
    """Get current TDD phase."""
    return code_mode.get("current_phase") or "failing_test"


def is_code_mode_active() -> bool:
    """Check if code mode is currently active."""
    return code_mode.is_active()


if __name__ == "__main__":
    import json
    input_data = json.load(sys.stdin)
    activate_code_mode(input_data)
