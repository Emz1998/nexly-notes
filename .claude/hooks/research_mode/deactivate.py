#!/usr/bin/env python3
"""Module: research_mode/deactivate - Deactivate research mode."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import research_mode


def deactivate() -> None:
    """Deactivate research mode."""
    research_mode.deactivate()
