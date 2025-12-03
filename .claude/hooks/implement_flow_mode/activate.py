#!/usr/bin/env python3
"""Module: implement_flow_mode/activate - Activate implement flow tracking."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import set_cache, get_cache

# Define the expected flow sequence
FLOW_SEQUENCE = ["explore", "research", "plan", "code", "code-review", "commit"]

NAMESPACE = "implement_flow"


def activate_implement_flow(input_data: dict = None) -> None:
    """Activate implement flow tracking. Initializes the flow state."""
    if input_data is None:
        input_data = {}

    session_id = input_data.get("session_id", "")

    # Initialize flow state
    set_cache(NAMESPACE, "is_active", True)
    set_cache(NAMESPACE, "session_id", session_id)
    set_cache(NAMESPACE, "current_step", 0)  # Index into FLOW_SEQUENCE
    set_cache(NAMESPACE, "completed_steps", [])

    print(
        f"Implement Flow Started. Expected sequence: /implement → /{' → /'.join(FLOW_SEQUENCE[:-1])} → commit"
    )
