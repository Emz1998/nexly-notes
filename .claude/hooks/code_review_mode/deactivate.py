#!/usr/bin/env python3
"""Code Review Mode Deactivation - Deactivates code review mode and clears cache."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import code_review_mode


def deactivate_code_review_mode() -> None:
    """Deactivate code review mode and clear cache."""
    code_review_mode.deactivate()
    sys.exit(0)


if __name__ == "__main__":
    deactivate_code_review_mode()
