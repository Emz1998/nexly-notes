import sys
from pathlib import Path

from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import get_cache, block_response, read_stdin_json

# test_input = {
#     "tool_name": "Todo",
#     "tool_input": {"file_path": "plan_1234567890.md"},
# }


SESSION_ID = get_cache("session_id")
CURRENT_PHASE = get_cache("current_phase")
VALID_PLANNING_FILE_NAME = f"plan_{SESSION_ID}"
VALID_RESEARCH_FILE_NAME = f"research_{SESSION_ID}"
VALID_EXPLORE_FILE_NAME = f"explore_{SESSION_ID}"


DEFAULT_REASONS = {
    "coding": f"You are not allowed to code in {CURRENT_PHASE} phase.",
    "planning": f"You are not allowed to plan in {CURRENT_PHASE} phase.",
    "research": f"You are not allowed to research in {CURRENT_PHASE} phase.",
    "commit": f"You are not allowed to commit code in {CURRENT_PHASE} phase.",
    "explore": f"You are not allowed to explore in {CURRENT_PHASE} phase.",
}


def block_coding(file_path: str, reason_for_blocking: str):
    if file_path.endswith(
        (".ts", ".tsx", ".js", ".jsx", ".json", ".css", ".html", ".py")
    ):
        print(reason_for_blocking, file=sys.stderr)
        sys.exit(2)


def block_planning(file_path: str, reason_for_blocking: str):
    if VALID_PLANNING_FILE_NAME in file_path:
        print(reason_for_blocking, file=sys.stderr)
        sys.exit(2)


def block_research(file_path: str, reason_for_blocking: str):
    if VALID_RESEARCH_FILE_NAME in file_path:
        print(reason_for_blocking, file=sys.stderr)
        sys.exit(2)


def block_commit(command: str, reason_for_blocking: str):
    git_commit_command = "git commit -m"
    if git_commit_command in command:
        print(reason_for_blocking, file=sys.stderr)
        sys.exit(2)


def block_explore(file_path: str, reason_for_blocking: str):
    if VALID_EXPLORE_FILE_NAME in file_path:
        print(reason_for_blocking, file=sys.stderr)
        sys.exit(2)


# Setup phase guard
def setup_phase_guard() -> None:
    try:

        # Read stdin
        hook_input = read_stdin_json()

        # Check tool name is Write
        tool_name = hook_input.get("tool_name")

        if tool_name != "Write" and tool_name != "Bash":
            print("Not in Writing or Bash. Skipping phase guard.")
            sys.exit(0)

        # Check Phase
        phase = CURRENT_PHASE

        # Get file path
        file_path = hook_input.get("tool_input", {}).get("file_path", "")

        # Get command
        command = hook_input.get("tool_input", {}).get("command", "")

        # Block based on phase
        if phase == "explore":
            block_research(file_path, DEFAULT_REASONS["research"])
            block_planning(file_path, DEFAULT_REASONS["planning"])
            block_coding(file_path, DEFAULT_REASONS["coding"])
        elif phase == "research":
            block_planning(file_path, DEFAULT_REASONS["planning"])
            block_coding(file_path, DEFAULT_REASONS["coding"])
        elif phase == "plan":
            block_coding(file_path, DEFAULT_REASONS["coding"])
            block_commit(command, DEFAULT_REASONS["commit"])
        elif phase == "code":
            block_commit(command, DEFAULT_REASONS["commit"])
        else:
            pass

    except Exception as e:
        block_response(f"Error: {e}")


if __name__ == "__main__":
    setup_phase_guard()
