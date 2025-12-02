#!/usr/bin/env python3
"""Milestone path helpers for plan mode validation."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

STATUS_PATH = Path("project/status.json")


def get_milestone_info() -> dict:
    """Get current milestone info from project/status.json."""
    try:
        data = json.loads(STATUS_PATH.read_text())
        return {
            "milestone": data.get("current_milestone", ""),
            "description": data.get("milestone_description", ""),
        }
    except (json.JSONDecodeError, FileNotFoundError):
        return {"milestone": "", "description": ""}


def get_milestone_dir() -> str:
    """Get milestone directory name in format [MS-NN]:[Description]."""
    info = get_milestone_info()
    if info["milestone"] and info["description"]:
        return f"{info['milestone']}:{info['description']}"
    return ""


def get_date_suffix() -> str:
    """Get current date in MMDDYY format."""
    return datetime.now().strftime("%m%d%y")


def build_research_path(session_id: str) -> Optional[Path]:
    """Build expected research report path."""
    milestone_dir = get_milestone_dir()
    if not milestone_dir or not session_id:
        return None
    date_suffix = get_date_suffix()
    return Path(f"project/{milestone_dir}/researches/research_{session_id}_{date_suffix}.md")


def build_plan_path(session_id: str) -> Optional[Path]:
    """Build expected plan file path."""
    milestone_dir = get_milestone_dir()
    if not milestone_dir or not session_id:
        return None
    date_suffix = get_date_suffix()
    return Path(f"project/{milestone_dir}/plans/plan_{session_id}_{date_suffix}.md")


def build_explore_status_path(session_id: str) -> Optional[Path]:
    """Build expected codebase-status file path.

    File format: project/[MS-NN]:[Description]/exploration/codebase-status_[session-id]_[MMDDYY].md
    """
    milestone_dir = get_milestone_dir()
    if not milestone_dir or not session_id:
        return None
    date_suffix = get_date_suffix()
    return Path(f"project/{milestone_dir}/exploration/codebase-status_{session_id}_{date_suffix}.md")


def find_research_file(session_id: str) -> Optional[Path]:
    """Find research file matching session_id (any date)."""
    milestone_dir = get_milestone_dir()
    if not milestone_dir or not session_id:
        return None
    research_dir = Path(f"project/{milestone_dir}/researches")
    if not research_dir.exists():
        return None
    for f in research_dir.glob(f"research_{session_id}_*.md"):
        return f
    return None


def find_plan_file(session_id: str) -> Optional[Path]:
    """Find plan file matching session_id (any date)."""
    milestone_dir = get_milestone_dir()
    if not milestone_dir or not session_id:
        return None
    plan_dir = Path(f"project/{milestone_dir}/plans")
    if not plan_dir.exists():
        return None
    for f in plan_dir.glob(f"plan_{session_id}_*.md"):
        return f
    return None


def find_explore_status_file(session_id: str = None) -> Optional[Path]:
    """Find codebase-status file in the exploration directory.

    File format: codebase-status_[session-id]_[MMDDYY].md
    If session_id is provided, looks for exact match.
    If session_id is None, returns any codebase-status file found.
    """
    milestone_dir = get_milestone_dir()
    if not milestone_dir:
        return None
    exploration_dir = Path(f"project/{milestone_dir}/exploration")
    if not exploration_dir.exists():
        return None

    if session_id:
        # Look for file matching session_id
        for f in exploration_dir.glob(f"codebase-status_{session_id}_*.md"):
            return f
    else:
        # Return any codebase-status file
        for f in exploration_dir.glob("codebase-status_*.md"):
            return f
    return None


def build_review_path(session_id: str) -> Optional[Path]:
    """Build expected code review file path.

    File format: project/[MS-NN]:[Description]/reviews/review_[session-id]_[MMDDYY].md
    """
    milestone_dir = get_milestone_dir()
    if not milestone_dir or not session_id:
        return None
    date_suffix = get_date_suffix()
    return Path(f"project/{milestone_dir}/reviews/review_{session_id}_{date_suffix}.md")


def find_review_file(session_id: str = None) -> Optional[Path]:
    """Find code review file in the reviews directory.

    File format: review_[session-id]_[MMDDYY].md
    If session_id is provided, looks for exact match.
    If session_id is None, returns any review file found.
    """
    milestone_dir = get_milestone_dir()
    if not milestone_dir:
        return None
    reviews_dir = Path(f"project/{milestone_dir}/reviews")
    if not reviews_dir.exists():
        return None

    if session_id:
        for f in reviews_dir.glob(f"review_{session_id}_*.md"):
            return f
    else:
        for f in reviews_dir.glob("review_*.md"):
            return f
    return None
