#!/usr/bin/env python3
"""Set session ID from hook input into cache."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import set_cache, read_stdin_json


def set_session_id(hook_input: dict) -> None:
    """Store session ID in cache from hook input."""
    session_id = hook_input.get("session_id", "")
    if session_id:
        set_cache("session_id", session_id)
        print(f"Session ID: {session_id}")


def main() -> None:
    hook_input = read_stdin_json()
    set_session_id(hook_input)
    sys.exit(0)


if __name__ == "__main__":
    main()
