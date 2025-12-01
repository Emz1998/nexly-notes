#!/usr/bin/env python3
"""
Hook: plan_mode
Event: PreToolUse - ExitPlanMode
Purpose: Deactivate plan mode
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import set_cache


def deactivate():
    set_cache("plan_mode", "is_active", False)
    print("Deactivating Planning")
    sys.exit(0)


if __name__ == "__main__":
    deactivate()
