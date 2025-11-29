from math import e
from typing import Callable, Literal, Union
from pydantic import BaseModel
import sys
from pathlib import Path
import json
from .states import set_state


CODE_EXTENSIONS = (".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css")
PLAN_DRAFT_FILE_NAME = "implementation-plan-draft"
FINAL_PLAN_FILE_NAME = "implementation-plan"
RESEARCH_FILE_NAME = "research_report.md"
Phases = Literal[
    (
        "explore",
        "research",
        "research review",
        "plan",
        "plan consult",
        "failing tests",
        "passing tests",
        "refactoring",
        "code review",
        "commit",
        "troubleshooting",
    )
]
Tasks = Literal[
    (
        "code",
        "plan",
        "research",
        "commit",
    )
]
Actions = Literal[
    (
        "exploring",
        "researching",
        "research reviewing",
        "planning",
        "plan_consulting",
        "implementing failing tests",
        "implementing passing tests",
        "refactoring",
        "code reviewing",
        "committing",
        "troubleshooting",
    )
]

Tools = Literal[("write", "read", "task", "bash")]
Hooks = Literal[("PreToolUse", "PostToolUse")]


class File(BaseModel):
    name: str
    path: str
    extension: str
    task: Tasks


class Event(BaseModel):
    tool: Tools
    file: File
    message: Message
    phase: Phases


class Message(BaseModel):
    explore: str
    research: str
    plan: str
    coding: str
    committing: str
    revision: str


def set_action(file_path: str):
    try:
        if file_path.startswith(RESEARCH_FILE_NAME):
            return set_state("action", "researching")
        elif file_path.startswith((PLAN_DRAFT_FILE_NAME, FINAL_PLAN_FILE_NAME)):
            return set_state("action", "planning")
        elif file_path.endswith(CODE_EXTENSIONS):
            return set_state("action", "coding")
        else:
            raise ValueError(f"Invalid file path: {file_path}")
    except ValueError as e:
        print(f"Error setting action: {e}")


def block_file_write(
    event: Event,
    check_phase_fn: Callable[[Phases], bool],
    check_action_fn: Callable[[Actions], bool],
):
    file_path = event.file.path
    message = event.message
    is_phase = check_phase_fn
    is_action = check_action_fn
    is_coding = (
        is_action("implementing failing tests")
        or is_action("implementing passing tests")
        or is_action("refactoring")
    )
    is_planning = is_action("planning") or is_action("plan_consulting")
    is_researching = is_action("researching") or is_action("research reviewing")

    if is_phase("explore") and is_planning and is_researching and is_coding:
        print(message.explore)
        sys.exit(2)
    elif is_phase("research") and is_planning and is_coding:
        print(message.research)
        sys.exit(2)
    elif is_phase("plan") and is_action("plan_consulting") and is_action("coding"):
        if is_action("researching"):
            set_state("revision_count.research", 1)
            print(message.revision)
            sys.exit(2)
        else:
            print(message.plan)
            sys.exit(2)
    elif is_phase("plan_consult") and is_action("researching") and is_action("coding"):
        if is_action("researching"):
            set_state("allowed_revisions.research", 1)
            print(message.revision)
            sys.exit(2)
        else:
            print(message.plan)
            sys.exit(2)
    elif is_phase("failing_tests") and is_action("commiting"):
        if is_action("researching"):
            set_state("allowed_revisions.research", 1)
            print(message.revision)
            sys.exit(2)
        else:
            print(message.plan)
            sys.exit(2)
    else:
        pass
    sys.exit(2)


# Load a prompt from the prompts directory.
def get_message(message_name: str) -> str:
    try:
        current_dir = Path(__file__).parent
        prompt_path = current_dir / message_name / ".md"
        with open(prompt_path) as f:
            return f.read().strip()
    except (IOError, FileNotFoundError):
        return ""
