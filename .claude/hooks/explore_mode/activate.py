#!/usr/bin/env python3
"""Module: explore_mode/activate - Activate explore mode when /implement command is used."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import explore_mode


def activate_explore_mode(input_data: dict = None) -> None:
    """Activate explore mode. Stores session_id in cache."""
    if input_data is None:
        input_data = {}
    session_id = input_data.get("session_id", "")
    explore_mode.activate(session_id, "Explore Phase. Run codebase-explorer to analyze the project state.")
