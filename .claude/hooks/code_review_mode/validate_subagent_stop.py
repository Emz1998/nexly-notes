#!/usr/bin/env python3
"""Code Review Mode - Validate Subagent Stop (SubagentStop Handler).

Validates that code-reviewer agent produced a review report before stopping.
The review file must exist and contain required sections.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import code_review_mode, log, find_review_file

REQUIRED_SECTIONS = ["summary", "findings"]
MIN_CONTENT_LENGTH = 200


def validate_review_content(file_path: Path) -> tuple[bool, str]:
    """Validate review file has required content."""
    try:
        content = file_path.read_text().lower()
    except Exception as e:
        return False, f"Cannot read review file: {e}"

    if len(content) < MIN_CONTENT_LENGTH:
        return False, f"Review too short ({len(content)} chars, need {MIN_CONTENT_LENGTH}+)"

    missing = [s for s in REQUIRED_SECTIONS if s not in content]
    if missing:
        return False, f"Missing sections: {', '.join(missing)}"

    return True, ""


def validate_subagent_stop(input_data: dict) -> None:
    """Validate code-reviewer completed required work before stopping.

    Requirements:
    - Review file must exist at: project/[MS-NN]:[Description]/reviews/review_[session-id]_[MMDDYY].md
    - Review must contain required sections (summary, findings)
    - Review must have minimum content length
    """
    if not code_review_mode.is_active():
        return

    session_id = code_review_mode.get_session_id()

    review_file = find_review_file(session_id)
    if not review_file or not review_file.exists():
        log("code-reviewer stop blocked: Review file not found")
        print(
            "Code review report not created. Continue working on the review.\n"
            "Expected: project/[MS-NN]:[Description]/reviews/review_[session-id]_[MMDDYY].md\n"
            "Required sections: summary, findings",
            file=sys.stderr
        )
        sys.exit(2)

    is_valid, reason = validate_review_content(review_file)
    if not is_valid:
        log(f"code-reviewer stop blocked: {reason}")
        print(
            f"Code review report incomplete. {reason}\n"
            "Continue working on the review report.\n"
            "Required sections: summary, findings",
            file=sys.stderr
        )
        sys.exit(2)

    # Validation passed - deactivate code review mode
    code_review_mode.deactivate()
    log(f"code-reviewer completed. Review saved to: {review_file}")
    print(f"Code review complete. Report: {review_file}")


if __name__ == "__main__":
    import json
    input_data = json.load(sys.stdin)
    validate_subagent_stop(input_data)
