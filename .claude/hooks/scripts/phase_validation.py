import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import get_cache, read_stdin_json, set_cache
from set_next_phase import extract_slash_command_name 


DEFAULT_PHASES = [
    "explore",
    "research",
    "plan",
    "code",
    "code-review",
    "commit",
]

test_input = {
    "tool_name": "SlashCommand",
    "tool_input": {"command": "/research"},
}


REASONS = {
    "rollback": "You cannot go back to the previous phase.",
    "skipping": "You cannot skip phase(s): ",
    "unknown_phase": "Unknown phase.",
    "allow": "You can proceed to the next phase.",
}


def block_transition(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def is_next_phase_valid(
    next_phase: str, 
    all_phases: list[str] = DEFAULT_PHASES,
) -> bool:
    current_phase = get_cache("current_phase")
    # Check if next_phase is valid
    if next_phase not in all_phases:
        print(REASONS["unknown_phase"], file=sys.stderr)
        return False

    if not current_phase:
        return True

    # Get current and next phase indices
    current_index = all_phases.index(current_phase)
    next_index = all_phases.index(next_phase)

    # Allow same phase or next phase in sequence
    if next_index == current_index or next_index == current_index + 1:
        print(REASONS["allow"], file=sys.stderr)
        return True

    # Block if going backwards
    if next_index < current_index:
        print(REASONS["rollback"], file=sys.stderr)
        return False

    # Block if skipping phases (i.e. not in sequence)
    skipped = all_phases[current_index + 1 : next_index]
    print(REASONS["skipping"] + ", ".join(skipped), file=sys.stderr)
    return False


def validate_phase_transition():
    is_active = get_cache("is_active")
    if not is_active:
        print("Not in implement phase. Skipping phase validation.")
        sys.exit(0)

    hook_input = test_input
    tool_name = hook_input.get("tool_name", "")

    if tool_name != "SlashCommand":
        sys.exit(0)

    command = hook_input.get("tool_input", "").get("command", "")
    next_phase = extract_slash_command_name(command)

    if not is_next_phase_valid(next_phase):
        sys.exit(2)

    set_cache(
        "current_phase", next_phase
    )
    print(f"Current phase set to {next_phase}")
    sys.exit(0)


if __name__ == "__main__":
    validate_phase_transition()
