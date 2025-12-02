#!/usr/bin/env python3
"""Module: plan_mode/validate_subagent_stop - Validate subagent completion."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    plan_mode,
    find_plan_file,
    has_consultation_marker,
    get_subagent_type,
    block_agent,
)


def _validate_strategic_planner(session_id: str) -> bool:
    """Check if strategic-planner created the plan file."""
    plan_file = find_plan_file(session_id)
    return plan_file is not None and plan_file.exists()


def _validate_consulting_expert(session_id: str) -> bool:
    """Check if consulting-expert added consultation marker to plan."""
    plan_file = find_plan_file(session_id)
    if not plan_file or not plan_file.exists():
        return False
    return has_consultation_marker(plan_file)


def validate_subagent_stop(input_data: dict) -> None:
    """Validate subagent completed required work before stopping."""
    if not plan_mode.is_active():
        return

    subagent_type = get_subagent_type(input_data)
    if subagent_type not in ("strategic-planner", "consulting-expert"):
        return

    session_id = plan_mode.get_session_id()
    if not session_id:
        return

    if subagent_type == "strategic-planner":
        if not _validate_strategic_planner(session_id):
            block_agent("Plan not created. Continue working on the plan document.")

    elif subagent_type == "consulting-expert":
        if not _validate_consulting_expert(session_id):
            block_agent(
                "Plan not consulted. "
                "Add YAML frontmatter with 'consulted_by: consulting-expert' to the plan file."
            )
