import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import set_cache, read_stdin_json

test_input = {
    "tool_name": "Task",
    "tool_input": {"subagent_type": "codebase-explorer"},
}


def set_next_subagent() -> bool:
    # Read Input
    hook_input = test_input
    tool_input = hook_input.get("tool_input", {})
    subagent_type = tool_input.get("subagent_type", "")

    # Get Tool Name
    tool_name = hook_input.get("tool_name")

    # Exit if not Task
    if tool_name != "Task":
        print("Subagent not invoked yet")
        sys.exit(0)

    set_cache("next_subagent", subagent_type)
    print(f"Next subagent set to {subagent_type}")
    return True


if __name__ == "__main__":
    set_next_subagent()
