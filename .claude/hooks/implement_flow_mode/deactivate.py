#!/usr/bin/env python3
"""Module: implement_flow_mode/deactivate - Deactivate implement flow tracking."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import set_cache

NAMESPACE = "implement_flow"


def deactivate() -> None:
    """Deactivate implement flow mode and clear cache."""
    set_cache(NAMESPACE, "is_active", False)
    set_cache(NAMESPACE, "session_id", "")
    set_cache(NAMESPACE, "current_step", 0)
    set_cache(NAMESPACE, "completed_steps", [])
