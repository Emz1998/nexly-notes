#!/usr/bin/env python3
"""Module: explore_mode/deactivate - Deactivate explore mode."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import explore_mode


def deactivate(input_data: dict = None) -> None:
    """Deactivate explore mode. Clears cache entries."""
    explore_mode.deactivate()
