#!/usr/bin/env python3
"""Guard phase transitions in implement workflow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import get_cache, set_cache, extract_slash_command_name, read_stdin_json
from scripts.validate_work import track_phases

DEFAULT_PHASES = [
    "initial",
    "explore",
    "research",
    "plan",
    "code",
    "code-review",
    "commit",
]


def get_transition_message(msg_type: str, skipped: list[str] = None) -> str:
    """Get phase transition message."""
    messages = {
        "rollback": "Cannot go back to previous phase.",
        "skip": f"Cannot skip phase(s): {', '.join(skipped or [])}",
        "unknown": "Unknown phase.",
        "allow": "Phase transition allowed.",
    }
    return messages.get(msg_type, "")


def is_valid_phase_transition(
    next_phase: str,
    all_phases: list[str] = DEFAULT_PHASES,
) -> bool:
    """Check if transition to next phase is valid."""
    current_phase = get_cache("current_phase") or "initial"

    if next_phase not in all_phases:
        print(get_transition_message("unknown"), file=sys.stderr)
        return False

    current_idx = all_phases.index(current_phase)
    next_idx = all_phases.index(next_phase)

    # Allow same or next in sequence
    if next_idx in (current_idx, current_idx + 1):
        return True

    # Block backwards
    if next_idx < current_idx:
        print(get_transition_message("rollback"), file=sys.stderr)
        return False

    # Block skipping
    skipped = all_phases[current_idx + 1 : next_idx]
    print(get_transition_message("skip", skipped), file=sys.stderr)
    return False


def validate_phase_transition(hook_input: dict) -> None:
    """Main phase transition validation."""
    if not get_cache("is_active"):
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})
    prompt = hook_input.get("prompt", "")

    if not tool_name and not prompt:
        sys.exit(0)

    if tool_name != "SlashCommand" and not prompt.startswith("/"):
        sys.exit(0)

    command = tool_input.get("command", "") if tool_input else prompt
    next_phase = extract_slash_command_name(command)

    if not is_valid_phase_transition(next_phase):
        sys.exit(2)

    set_cache("current_phase", next_phase)
    track_phases(next_phase)
    print(f"Phase: {next_phase}")
    sys.exit(0)


def main() -> None:
    hook_input = read_stdin_json()
    validate_phase_transition(hook_input)


if __name__ == "__main__":
    main()
