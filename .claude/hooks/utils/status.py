"""Utility functions for reading project status."""

import json
from pathlib import Path
from typing import Any, Optional

DEFAULT_STATUS_PATH = Path("project") / "status.json"


def get_status(
    key: str, default: Optional[Any] = None, file_path: Path = DEFAULT_STATUS_PATH
) -> Any:
    try:
        status_data = json.loads(file_path.read_text()) if file_path.exists() else {}
    except json.JSONDecodeError:
        status_data = {}
    if not key:
        return status_data
    else:
        return status_data.get(key)


def set_status(key: str, value: Any, file_path: Path = DEFAULT_STATUS_PATH) -> bool:
    """
    Set a specific value in the status.json file.

    Args:
        key: The key to set
        value: The value to assign
        file_path: Path to status file (default: project/status.json)

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, "r") as f:
            status = json.load(f)
    except FileNotFoundError:
        status = {}
    except json.JSONDecodeError:
        return False

    status[key] = value

    try:
        with open(file_path, "w") as f:
            json.dump(status, f, indent=4)
        return True
    except IOError:
        return False
