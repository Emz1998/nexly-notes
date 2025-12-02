#!/usr/bin/env python3
"""Code Review Mode - Block Premature Agents (PreToolUse Handler).

Blocks code-reviewer agent if code review mode is not active or
prerequisites are not met (code must be committed).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    code_review_mode,
    is_task_call,
    extract_agent_info,
    is_code_committed,
    is_tdd_commit_complete,
)


def block_premature_agents(input_data: dict) -> None:
    """Block code-reviewer agent if prerequisites not met.

    Prerequisites:
    - code_review_mode must be active, OR
    - Code must be committed (git-based check), OR
    - TDD commit phase must be complete
    """
    if not is_task_call(input_data):
        return

    _, subagent_type = extract_agent_info(input_data)
    if subagent_type != "code-reviewer":
        return

    # If code review mode is active, allow
    if code_review_mode.is_active():
        return

    # Check git-based prerequisite
    committed, reason = is_code_committed()
    if committed:
        return

    # Fallback: check TDD commit phase
    if is_tdd_commit_complete():
        return

    # Block: prerequisites not met
    print(
        f"Code Reviewer blocked. {reason}\n"
        "Complete coding and commit changes first, or use /code-review command.",
        file=sys.stderr
    )
    sys.exit(2)


if __name__ == "__main__":
    import json
    input_data = json.load(sys.stdin)
    block_premature_agents(input_data)
