import json
import sys


def log(msg: str) -> None:
    """Print to stderr for hook system visibility."""
    print(msg, file=sys.stderr, flush=True)


def success_response(hook_event: str, context: str = None) -> None:
    """Output JSON success response and exit 0."""
    response = {"hookSpecificOutput": {"hookEventName": hook_event}}
    if context:
        response["hookSpecificOutput"]["additionalContext"] = context
    print(json.dumps(response))
    sys.exit(0)


def block_response(reason: str) -> None:
    """Output error to stderr and exit 2 (blocking)."""
    print(reason, file=sys.stderr)
    sys.exit(2)
