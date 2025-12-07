import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import read_stdin_json, get_cache, set_cache
from validate_invocations import track_subagents  # type: ignore


DEFAULT_SUBAGENTS = [
    "codebase-explorer",
    "research-specialist",
    "research-consultant",
    "strategic-planner",
    "plan-consultant",
    "test-manager",
    "code-reviewer",
    "code-specialist",
    "version-manager",
]

test_input = {
    "tool_name": "Task",
    "tool_input": {"subagent_type": "code-reviewer"},
}


def get_reasons(next_subagent: str) -> dict[str, str]:
    current_subagent = get_cache("current_subagent")
    return {
        "unknown_subagent": f"Unknown subagent: {next_subagent}",
        "allow": f"You can proceed to the next subagent: {next_subagent}.",
        "rollback": f"You cannot call back the previous subagent: {next_subagent}.",
        "skipping": "You cannot skip subagent(s): ",
    }


def is_next_subagent_valid(
    next_subagent: str,
    all_subagents: list[str] = DEFAULT_SUBAGENTS,
) -> bool:
    current_subagent = get_cache("current_subagent")
    # Check if next_phase is valid
    if next_subagent not in all_subagents:
        print(get_reasons(next_subagent)["unknown_subagent"], file=sys.stderr)
        return False

    # Exit if nothing is triggered yet
    if not current_subagent:
        return True

    # Get current and next phase indices
    current_index = all_subagents.index(current_subagent)
    next_index = all_subagents.index(next_subagent)

    # Allow same subagent or next subagent in sequence
    if next_index == current_index or next_index == current_index + 1:
        print(get_reasons(next_subagent)["allow"])
        return True

    # Block if going backwards
    if next_index < current_index:
        print(get_reasons(next_subagent)["rollback"], file=sys.stderr)
        return False

    # Block if skipping subagents (i.e. not in sequence)
    skipped = all_subagents[current_index + 1 : next_index]
    print(get_reasons(next_subagent)["skipping"] + ", ".join(skipped), file=sys.stderr)
    return False


def validate_subagent_order():
    hook_input = read_stdin_json()
    next_subagent = hook_input.get("tool_input", "").get("subagent_type", "")

    # Check if the next Subagent is valid
    if not is_next_subagent_valid(next_subagent):
        sys.exit(2)

    # Set new current subagent
    set_cache("current_subagent", next_subagent)
    print(f"Current Subagent set to {next_subagent}")
    sys.exit(0)


if __name__ == "__main__":
    validate_subagent_order()
