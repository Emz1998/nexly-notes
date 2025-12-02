#!/usr/bin/env python3
"""Module: plan_mode/block_premature_agents - Block agents without dependencies."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    plan_mode,
    find_research_file,
    find_plan_file,
    is_task_call,
    extract_agent_info,
    block_agent,
)


def block_premature_agents(input_data: dict) -> None:
    """Block agents that don't have their dependencies met."""
    if not is_task_call(input_data):
        return

    _, subagent_type = extract_agent_info(input_data)
    if subagent_type not in ("strategic-planner", "consulting-expert"):
        return

    if not plan_mode.is_active():
        return

    session_id = plan_mode.get_session_id()
    if not session_id:
        block_agent(f"{subagent_type} call rejected. Session ID not found.")

    if subagent_type == "strategic-planner":
        if not find_research_file(session_id):
            block_agent(
                "Strategic Planner blocked. "
                "Research report not found. "
                "Call research-specialist first to create the report."
            )

    elif subagent_type == "consulting-expert":
        if not find_plan_file(session_id):
            block_agent(
                "Consulting Expert blocked. "
                "Plan file not found. "
                "Call strategic-planner first to create the plan."
            )
