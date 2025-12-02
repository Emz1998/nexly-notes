#!/usr/bin/env python3
"""Module: plan_mode/deactivate - Deactivate plan mode."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import plan_mode


def deactivate():
    """Deactivate plan mode."""
    plan_mode.deactivate()
    print("Deactivating Planning")
    sys.exit(0)


if __name__ == "__main__":
    deactivate()
