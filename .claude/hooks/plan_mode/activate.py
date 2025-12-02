#!/usr/bin/env python3
"""Module: plan_mode/activate - Activate plan mode when /plan command is used."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import plan_mode


def activate_plan_mode(input_data: dict = None) -> None:
    """Activate plan mode. Stores session_id in cache."""
    if input_data is None:
        input_data = {}
    session_id = input_data.get("session_id", "")
    plan_mode.activate(session_id, "Planning Phase. Do not write any code")
