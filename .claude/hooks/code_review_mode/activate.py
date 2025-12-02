#!/usr/bin/env python3
"""Code Review Mode Activation - UserPromptSubmit Handler.

Activates code review workflow when /code-review command is issued.
Prerequisites:
  1. Git-based: No uncommitted changes in src/ directory, OR
  2. TDD fallback: code_mode.current_phase == "commit"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import code_review_mode, is_code_committed, is_tdd_commit_complete


def activate_code_review_mode(input_data: dict) -> None:
    """Activate code review mode after code is committed.

    Prerequisites (in order):
    1. No uncommitted changes in src/ directory (git-based)
    2. OR code_mode.current_phase == "commit" (TDD fallback)
    """
    session_id = input_data.get("session_id", "")

    committed, reason = is_code_committed()
    if not committed:
        if not is_tdd_commit_complete():
            print(
                f"Code Review Mode: Code not committed. {reason}\n"
                "Complete coding and commit changes first, or finish TDD commit phase.",
                file=sys.stderr
            )
            sys.exit(2)

    code_review_mode.activate(
        session_id,
        "Code Review Mode Started. Deploy code-reviewer agent to analyze the codebase."
    )
    sys.exit(0)


if __name__ == "__main__":
    import json
    input_data = json.load(sys.stdin)
    activate_code_review_mode(input_data)
