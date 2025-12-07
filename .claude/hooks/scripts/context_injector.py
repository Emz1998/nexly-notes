#!/usr/bin/env python3
"""Module: implement_flow_mode/validate_flow - Validate slash command flow sequence."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import add_context, get_status, read_stdin_json, set_status


def inject_context() -> None:
    # Set the active command and context in the cache
    session_id = read_stdin_json().get("session_id")
    current_milestone = get_status("current_milestone")
    last_task_completed = get_status("last_task_completed")
    last_milestone_completed = get_status("last_milestone_completed")
    remaining_tasks = get_status("tasks_remaining")
    remaining_milestones = get_status("milestones_remaining")
    total_tasks = get_status("total_tasks")
    total_milestones = get_status("total_milestones")
    total_phases = get_status("total_phases")
    target_release_date = get_status("target_release_date")
    current_phase = get_status("current_phase")
    milestones_completed = get_status("milestones_completed")
    tasks_completed = get_status("tasks_completed")
    # Set the session id in the status
    set_status("current_session_id", session_id)

    context = f"""
    Session ID: {session_id}
    Current Milestone: {current_milestone}
    Last Milestone Completed: {last_milestone_completed}
    Last Task Completed: {last_task_completed}
    Remaining Tasks: {remaining_tasks}
    Remaining Milestones: {remaining_milestones}
    Total Tasks: {total_tasks}
    Total Milestones: {total_milestones}
    Total Phases: {total_phases}
    Target Release Date: {target_release_date}
    Current Phase: {current_phase}
    Milestones Completed: {milestones_completed}
    Tasks Completed: {tasks_completed}
    """

    add_context(context)
