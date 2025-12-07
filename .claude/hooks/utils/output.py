import json
import sys

DEFAULT_HOOK_SPECIFIC_OUTPUT = {
    "hookSpecificOutput": {"hookEventName": "", "additionalContext": ""}
}


def log(msg: str) -> None:
    """Print to stderr for hook system visibility."""
    print(msg, file=sys.stderr, flush=True)


def success_response(hook_event: str, context: str = "") -> None:
    """Output JSON success response and exit 0."""
    response = {"hookSpecificOutput": {"hookEventName": hook_event}}
    if context:
        response["hookSpecificOutput"]["additionalContext"] = context
    print(json.dumps(response))
    print(context)
    sys.exit(0)


def success_output(context: str | dict) -> None:
    print(context)
    sys.exit(0)


def add_context(context: str) -> None:
    DEFAULT_HOOK_SPECIFIC_OUTPUT["hookSpecificOutput"]["additionalContext"] = context
    print(json.dumps(DEFAULT_HOOK_SPECIFIC_OUTPUT))
    sys.exit(0)


def block_response(reason: str) -> None:
    """Output error to stderr and exit 2 (blocking)."""
    print(reason, file=sys.stderr)
    sys.exit(2)
