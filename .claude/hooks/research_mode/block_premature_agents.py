#!/usr/bin/env python3
"""Module: research_mode/block_premature_agents - Block research agents without dependencies."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    research_mode,
    find_explore_status_file,
    find_research_file,
    is_task_call,
    extract_agent_info,
    block_agent,
)


def block_premature_agents(input_data: dict) -> None:
    """Block research agents that don't have their dependencies met."""
    if not is_task_call(input_data):
        return

    _, subagent_type = extract_agent_info(input_data)
    if subagent_type not in ("research-specialist", "research-consultant"):
        return

    if not research_mode.is_active():
        return

    session_id = research_mode.get_session_id()
    if not session_id:
        block_agent(f"{subagent_type} call rejected. Session ID not found.")

    # Block research-specialist if explore status is missing
    if subagent_type == "research-specialist":
        if not find_explore_status_file():
            block_agent(
                "Research Specialist blocked. "
                "codebase-status file not found in exploration directory. "
                "Run explore phase first to create the codebase status file."
            )

    # Block research-consultant if research file is missing
    elif subagent_type == "research-consultant":
        if not find_research_file(session_id):
            block_agent(
                "Research Consultant blocked. "
                "Research report not found. "
                "Call research-specialist first to create the report."
            )
