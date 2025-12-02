#!/usr/bin/env python3
"""Module: research_mode/validate_subagent_stop - Validate research subagent completion."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    research_mode,
    find_research_file,
    has_research_validation_marker,
    is_file_committed,
    get_subagent_type,
    block_agent,
)


def _validate_research_specialist(session_id: str) -> bool:
    """Check if research-specialist created the research file."""
    research_file = find_research_file(session_id)
    return research_file is not None and research_file.exists()


def _validate_research_consultant(session_id: str) -> bool:
    """Check if research-consultant added validation marker to research."""
    research_file = find_research_file(session_id)
    if not research_file or not research_file.exists():
        return False
    return has_research_validation_marker(research_file)


def _validate_commit(session_id: str) -> bool:
    """Check if research file has been committed."""
    research_file = find_research_file(session_id)
    if not research_file or not research_file.exists():
        return False
    return is_file_committed(str(research_file))


def validate_subagent_stop(input_data: dict) -> None:
    """Validate research subagent completed required work before stopping."""
    if not research_mode.is_active():
        return

    subagent_type = get_subagent_type(input_data)
    if subagent_type not in ("research-specialist", "research-consultant"):
        return

    session_id = research_mode.get_session_id()
    if not session_id:
        return

    if subagent_type == "research-specialist":
        if not _validate_research_specialist(session_id):
            block_agent(
                "Research report not created. "
                "Continue working on the research document."
            )

    elif subagent_type == "research-consultant":
        if not _validate_research_consultant(session_id):
            block_agent(
                "Research not validated. "
                "Add YAML frontmatter with 'validated_by: research-consultant' to the research file."
            )

        if not _validate_commit(session_id):
            block_agent(
                "Research file not committed. "
                "Commit the research file before stopping."
            )
