#!/usr/bin/env python3
"""Activate implement workflow on /implement command."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import set_cache, read_stdin_json
from scripts.reset_cache import reset_cache


def check_activation(hook_input: dict) -> None:
    """Check if prompt activates implement workflow."""
    prompt = hook_input.get("prompt", "")

    if not prompt or not prompt.startswith("/implement"):
        sys.exit(0)

    reset_cache()
    set_cache("is_active", True)
    print("Implement workflow activated")


def main() -> None:
    hook_input = read_stdin_json()
    check_activation(hook_input)
    sys.exit(0)


if __name__ == "__main__":
    main()
