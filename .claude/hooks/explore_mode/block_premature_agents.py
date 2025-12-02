#!/usr/bin/env python3
"""Module: explore_mode/block_premature_agents - Block explore agents without dependencies."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    explore_mode,
    is_task_call,
    extract_agent_info,
    block_agent,
)

TASKS_FILE = Path("specs/tasks.md")


def block_premature_agents(input_data: dict) -> None:
    """Block explore agents that don't have their dependencies met.

    Dependencies:
    - codebase-explorer requires explore_mode to be active
    - codebase-explorer requires specs/tasks.md to exist
    """
    if not is_task_call(input_data):
        return

    _, subagent_type = extract_agent_info(input_data)
    if subagent_type != "codebase-explorer":
        return

    if not explore_mode.is_active():
        return

    session_id = explore_mode.get_session_id()
    if not session_id:
        block_agent("codebase-explorer call rejected. Session ID not found.")

    if not TASKS_FILE.exists():
        block_agent(
            "codebase-explorer blocked. "
            "specs/tasks.md file not found. "
            "Generate tasks from specs first using /.tasks command."
        )
