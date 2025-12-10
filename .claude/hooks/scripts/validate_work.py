#!/usr/bin/env python3
"""Validate work completion on Stop hook."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import get_cache, set_cache, write_log_file, read_stdin_json

ALL_PHASES = [
    "explore",
    "research",
    "plan",
    "code",
    "code-review",
    "commit",
]

ALL_SUBAGENTS = [
    "codebase-explorer",
    "research-specialist",
    "research-consultant",
    "strategic-planner",
    "plan-consultant",
    "test-manager",
    "code-reviewer",
]


def track_phases(phase: str) -> None:
    """Track completed phases in cache."""
    phases_completed = get_cache("phases_completed") or []
    if phase and phase not in phases_completed:
        phases_completed.append(phase)
        set_cache("phases_completed", phases_completed)


def track_subagents(subagent: str) -> None:
    """Track triggered subagents in cache."""
    subagents_triggered = get_cache("subagents_triggered") or []
    if subagent and subagent not in subagents_triggered:
        subagents_triggered.append(subagent)
        set_cache("subagents_triggered", subagents_triggered)


def log_violation(message: str) -> None:
    """Log violation and increment counter."""
    current_violations = get_cache("violations") or 0
    set_cache("violations", current_violations + 1)
    write_log_file({"content": message, "source_file": "validate_work.py"})


def validate_phases() -> list[str]:
    """Check if all required phases were completed."""
    phases_completed = get_cache("phases_completed") or []
    missing = [p for p in ALL_PHASES if p not in phases_completed]
    if missing:
        log_violation(f"Missing phases: {', '.join(missing)}")
    return missing


def validate_subagents() -> list[str]:
    """Check if all required subagents were triggered."""
    subagents_triggered = get_cache("subagents_triggered") or []
    missing = [s for s in ALL_SUBAGENTS if s not in subagents_triggered]
    if missing:
        log_violation(f"Missing subagents: {', '.join(missing)}")
    return missing


def validate_work() -> None:
    """Main validation - check phases and subagents completion."""
    is_active = get_cache("is_active")
    if not is_active:
        sys.exit(0)

    missing_phases = validate_phases()
    missing_subagents = validate_subagents()

    if missing_phases or missing_subagents:
        reason = []
        if missing_phases:
            reason.append(f"Incomplete phases: {', '.join(missing_phases)}")
        if missing_subagents:
            reason.append(f"Missing subagents: {', '.join(missing_subagents)}")
        print("; ".join(reason), file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


def main() -> None:
    read_stdin_json()
    validate_work()


if __name__ == "__main__":
    main()
