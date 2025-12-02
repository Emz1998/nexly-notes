#!/usr/bin/env python3
"""Module: research_mode/activate - Activate research mode on /research command."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import research_mode


def activate_research_mode(input_data: dict = None) -> None:
    """Activate research mode. Stores session_id in cache."""
    if input_data is None:
        input_data = {}
    session_id = input_data.get("session_id", "")
    research_mode.activate(session_id, "Research Phase. Follow the research workflow.")
