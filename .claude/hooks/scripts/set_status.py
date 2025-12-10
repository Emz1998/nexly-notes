"""Status management for project progress tracking."""

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    get_cache,
    read_json,
    read_stdin_json,
    write_json,
    FileReadError,
)
from utils.checklist import ProjectStatus, ChecklistValidator
from utils.file_io import read_file

# File paths
TEST_FILE = "test-checklist.md"
DEFAULT_CHECKLIST_FILE = "project/v0.1.0/release-plan/release-plan.md"
STATUS_FILE = "project/status.json"

EXIT_SUCCESS = 0
validator = ChecklistValidator()


def is_new_session(new_session_id: str) -> bool:
    """Check if the session ID is new."""
    print(get_cache("session_id"))
    return new_session_id != get_cache("session_id")


def set_status(
    file_path: str = STATUS_FILE,
    checklist_file: str = DEFAULT_CHECKLIST_FILE,
) -> dict[str, Any]:
    """Update status.json with current progress from checklist."""
    try:
        content = read_file(checklist_file)
        project = ProjectStatus(content)
        status_data = read_json(file_path)
        print(f"status_data: {status_data.get('current_phase', '')}")
        # hook_input = read_stdin_json()
        default_session_id = "9e4016f6-ead0-4a2f-b980-c3e4cc53dfc6"
        new_session_id = default_session_id
        print(status_data.get("current_phase_num", 0))
        print(project.current_phase_status(1))
        is_new = is_new_session(new_session_id)
        print(f"is_new: {is_new}")
        updates = {
            "version": status_data.get("version", ""),
            "project_name": status_data.get("project_name", ""),
            "project_status": project.project_status,
            # Phase
            "total_phases": project.total_phases,
            "current_phase_num": (
                project.current_phase_num
                if is_new
                else status_data.get("current_phase_num", 0)
            ),
            "current_phase": (
                project.current_phase
                if is_new
                else status_data.get("current_phase", "")
            ),
            "current_phase_status": (
                project.current_phase_status(project.current_phase_num)
                if is_new
                else project.current_phase_status(
                    status_data.get("current_phase_num", 0)
                )
            ),
            "phases_completed": project.phases_completed,
            "phases_remaining": project.phases_remaining,
            # Milestone
            "total_milestones": project.total_milestones,
            "current_milestone": (
                project.current_milestone
                if is_new
                else status_data.get("current_milestone", "")
            ),
            "current_milestone_status": (
                project.current_milestone_status
                if is_new
                else status_data.get("current_milestone_status", "")
            ),
            "milestones_completed": project.milestones_completed,
            "milestones_remaining": project.milestones_remaining,
            # Task
            "total_tasks": project.total_tasks,
            "current_task": (
                project.current_task if is_new else status_data.get("current_task", "")
            ),
            "current_task_status": (
                project.current_task_status
                if is_new
                else status_data.get("current_task_status", "")
            ),
            "tasks_completed": project.tasks_completed,
            "tasks_remaining": project.tasks_remaining,
        }

        status_data.update(updates)

        return {"status": "success", "data": updates}

    except (FileReadError, Exception) as e:
        return {"status": "error", "reason": str(e)}


def set_current_milestone(
    milestone: str, file_path: str = STATUS_FILE
) -> dict[str, Any]:
    """Set the current milestone in status.json."""
    if not validator.is_valid_milestone(milestone):
        return {"status": "error", "reason": "Invalid milestone format"}
    status_data = read_json(file_path)
    status_data.update(
        {
            "current_milestone": milestone,
            "current_milestone_status": "in_progress",
        }
    )
    write_json(status_data, file_path)
    return {"status": "success", "current_milestone": milestone}


def set_current_task(task: str, file_path: str = STATUS_FILE) -> dict[str, Any]:
    """Set the current task in status.json."""
    if not validator.is_valid_task(task):
        return {"status": "error", "reason": "Invalid task format"}
    status_data = read_json(file_path)
    status_data.update(
        {
            "current_task": task,
            "current_task_status": "in_progress",
        }
    )
    write_json(status_data, file_path)
    return {"status": "success", "current_task": task}


def set_task_completed(task: str, file_path: str = STATUS_FILE) -> dict[str, Any]:
    """Mark a task as completed and update counts."""
    if not validator.is_valid_task(task):
        return {"status": "error", "reason": "Invalid task format"}
    status_data = read_json(file_path)
    completed = status_data.get("tasks_completed", 0) + 1
    remaining = max(0, status_data.get("tasks_remaining", 0) - 1)
    status_data.update(
        {
            "tasks_completed": completed,
            "tasks_remaining": remaining,
            "current_task_status": "completed" if remaining == 0 else "in_progress",
        }
    )
    write_json(status_data, file_path)
    return {"status": "success", "task_completed": task, "tasks_remaining": remaining}


def set_milestone_completed(
    milestone: str, file_path: str = STATUS_FILE
) -> dict[str, Any]:
    """Mark a milestone as completed and update counts."""
    if not validator.is_valid_milestone(milestone):
        return {"status": "error", "reason": "Invalid milestone format"}
    status_data = read_json(file_path)
    completed = status_data.get("milestones_completed", 0) + 1
    remaining = max(0, status_data.get("milestones_remaining", 0) - 1)
    status_data.update(
        {
            "milestones_completed": completed,
            "milestones_remaining": remaining,
            "current_milestone_status": (
                "completed" if remaining == 0 else "in_progress"
            ),
        }
    )
    write_json(status_data, file_path)
    return {
        "status": "success",
        "milestone_completed": milestone,
        "milestones_remaining": remaining,
    }


def set_session_id(session_id: str, file_path: str = STATUS_FILE) -> dict[str, Any]:
    """Set the current session ID in status.json."""
    status_data = read_json(file_path)
    status_data["current_session_id"] = session_id
    write_json(status_data, file_path)
    return {"status": "success", "session_id": session_id}


# Alias for backwards compatibility
sync_status_from_checklist = set_status


if __name__ == "__main__":
    import json

    print(json.dumps(set_status(checklist_file=TEST_FILE), indent=2))
