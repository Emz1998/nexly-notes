#!/usr/bin/env python3
"""Code Mode Deactivation - Deactivates TDD workflow and clears cached state."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import code_mode


def deactivate_code_mode() -> None:
    """Deactivate code mode and clear all cached state."""
    code_mode.deactivate()


if __name__ == "__main__":
    deactivate_code_mode()
    print("Code mode deactivated")
    sys.exit(0)
