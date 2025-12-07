import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


from validate_invocations import track_phases  # type: ignore
from utils import set_cache, read_stdin_json

test_input = {
    "tool_name": "SlashCommand",
    "tool_input": {"command": "/implement"},
}


def extract_slash_command_name(raw_command: str = "") -> str | None:
    """Extract command name from a slash-prefixed prompt."""
    if not raw_command or not raw_command.startswith("/"):
        return ""

    # Remove the leading slash and get text before first space
    content = raw_command[1:]
    return content.split(" ")[0]


def is_slash_command_triggered(hook_input: dict = {}, command: str = "") -> bool:
    """Set the slash command in the cache."""
    tool_name = hook_input.get("tool_name")
    command_input = hook_input.get("tool_input", {}).get("command", "")
    prompt = hook_input.get("prompt", "")

    # Check command name

    command_name = extract_slash_command_name(command_input)

    if not prompt and tool_name != "SlashCommand":
        print("Slash command not triggered")
        return False

    if command != command_name:
        print(f"Command name mismatch: {command_input} != {command_name}")
        return False
    print("Command name matches")

    return True


def set_next_phase() -> bool:
    """Set the slash command in the cache."""
    hook_input = test_input
    if not is_slash_command_triggered(hook_input, "implement"):
        print("Slash command not triggered")
        sys.exit(0)

    next_phase = extract_slash_command_name(
        hook_input.get("tool_input", {}).get("command", "")
    )
    set_cache("next_phase", next_phase)
    track_phases(next_phase if next_phase else "")
    print(f"Next phase set to {next_phase}")
    return True


if __name__ == "__main__":
    set_next_phase()
