#!/usr/bin/env python3
"""Module: explore_mode/validate_subagent_stop - Validate codebase-explorer completion."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    explore_mode,
    find_explore_status_file,
    get_subagent_type,
    block_agent,
)


def _validate_codebase_explorer(session_id: str) -> bool:
    """Check if codebase-explorer created the codebase-status file."""
    status_file = find_explore_status_file(session_id)
    return status_file is not None and status_file.exists()


def validate_subagent_stop(input_data: dict) -> None:
    """Validate codebase-explorer completed required work before stopping.

    Validation: codebase-status_[session-id]_[MMDDYY].md must exist
    in project/[MS-NN]:[Description]/exploration/
    """
    if not explore_mode.is_active():
        return

    subagent_type = get_subagent_type(input_data)
    if subagent_type != "codebase-explorer":
        return

    session_id = explore_mode.get_session_id()
    if not session_id:
        return

    if not _validate_codebase_explorer(session_id):
        block_agent(
            "codebase-status file not created. "
            "Save exploration findings to project/[MS-NN]:[Description]/exploration/"
            "codebase-status_[session-id]_[MMDDYY].md before stopping."
        )
