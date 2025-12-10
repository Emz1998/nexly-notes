"""File I/O utilities with error handling."""

import json
from pathlib import Path
from typing import Any


class FileReadError(Exception):
    """Raised when a file cannot be read."""
    pass


def read_file(file_path: str) -> str:
    """Read file content with error handling."""
    try:
        return Path(file_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileReadError(f"File not found: {file_path}")
    except PermissionError:
        raise FileReadError(f"Permission denied: {file_path}")
    except UnicodeDecodeError:
        raise FileReadError(f"Invalid encoding: {file_path}")


def read_json(file_path: str, default: dict | None = None) -> dict[str, Any]:
    """Read JSON file with fallback to default."""
    try:
        return json.loads(read_file(file_path))
    except (FileReadError, json.JSONDecodeError):
        return default if default is not None else {}


def write_json(data: dict[str, Any], file_path: str, indent: int = 4) -> None:
    """Write data to JSON file."""
    Path(file_path).write_text(json.dumps(data, indent=indent), encoding="utf-8")


def output_json(data: dict[str, Any]) -> None:
    """Output JSON to stdout."""
    print(json.dumps(data))
