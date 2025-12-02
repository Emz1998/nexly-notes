#!/usr/bin/env python3
"""Shared prerequisite check functions.

Provides common prerequisite validation functions used across
multiple mode modules (code_mode, code_review_mode).
"""

from .cache import get_cache
from .git import get_modified_files


def is_code_committed() -> tuple[bool, str]:
    """Check if code is committed (no uncommitted changes in src/).

    Returns:
        Tuple of (is_committed, reason_if_not)
    """
    modified = get_modified_files()
    src_modified = [f for f in modified if f.startswith("src/")]
    if src_modified:
        files_preview = ", ".join(src_modified[:3])
        if len(src_modified) > 3:
            files_preview += f" (+{len(src_modified) - 3} more)"
        return False, f"Uncommitted files in src/: {files_preview}"
    return True, ""


def is_tdd_commit_complete() -> bool:
    """Check if TDD workflow reached commit phase.

    Returns:
        True if code_mode.current_phase is "commit"
    """
    return get_cache("code_mode", "current_phase") == "commit"


def check_code_prerequisite() -> tuple[bool, str]:
    """Check if code prerequisite is met for code review.

    Checks git-based prerequisite first, falls back to TDD commit phase.

    Returns:
        Tuple of (satisfied, reason_if_not)
    """
    committed, reason = is_code_committed()
    if committed:
        return True, ""

    if is_tdd_commit_complete():
        return True, ""

    return False, reason
