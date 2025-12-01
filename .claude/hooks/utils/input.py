import json
import sys


def read_stdin_json() -> dict:
    """Parse JSON from stdin. Returns empty dict on error."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}
