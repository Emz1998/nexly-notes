#!/usr/bin/env python3
"""
Hook: plan_mode
Event: Stop
Purpose: Validate plan is created before allowing exit
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import log, get_cache, get_modified_files, set_cache


def deactivate():
    set_cache("plan_mode", "is_active", False)
    print("Deactivating Planning")


def get_plan_path():
    session_id = get_cache("plan_mode", "session_id")
    if not session_id:
        return None
    files = get_modified_files()
    return next((f for f in files if session_id in f), None)


def is_plan_created():
    try:
        rel_path = get_plan_path()
        if not rel_path:
            return False
        plan_file = Path(rel_path)
        if not plan_file.exists():
            return False
        return len(plan_file.read_text().splitlines()) > 100
    except Exception as e:
        log(f"Error checking plan: {e}")
        return False


def validate_plan():
    if not get_cache("plan_mode", "is_active"):
        deactivate()
        sys.exit(0)
    if not is_plan_created():
        log("Please create the plan first")
        sys.exit(2)
    log("Validation Passed")
    deactivate()
    sys.exit(0)


if __name__ == "__main__":
    validate_plan()
