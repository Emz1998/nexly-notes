import json
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel


CONFIG_FILE = Path(".claude/settings.local.json")

VALID_HOOK_EVENTS = Literal[
    "PreToolUse",
    "PostToolUse",
    "UserPromptSubmit",
    "Stop",
    "SubagentStop",
    "Notification",
    "PreCompact",
    "PermissionRequest",
    "SessionStart",
    "SessionEnd",
]

VALID_HOOK_EVENTS_LIST = [
    "PreToolUse",
    "PostToolUse",
    "UserPromptSubmit",
    "Stop",
    "SubagentStop",
    "Notification",
    "PreCompact",
    "PermissionRequest",
    "SessionStart",
    "SessionEnd",
]


class HookConfig(BaseModel):
    """Configuration for a single hook."""

    type: Literal["command"] = "command"
    command: str
    timeout: int = 30000


class MatcherHookConfig(BaseModel):
    """Hook config for PreToolUse and PostToolUse events that require a matcher."""

    matcher: str
    hooks: list[HookConfig]


def read_settings() -> dict:
    """Read the current settings from settings.local.json."""
    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def write_settings(settings: dict) -> None:
    """Write settings back to settings.local.json."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def is_hook_event_valid(hook_event: str) -> bool:
    """Check if the hook event is valid."""
    return hook_event in VALID_HOOK_EVENTS_LIST


def get_hooks(hook_event: Optional[str] = None) -> dict:
    """Get all hooks or hooks for a specific event."""
    settings = read_settings()
    hooks = settings.get("hooks", {})

    if hook_event:
        if not is_hook_event_valid(hook_event):
            raise ValueError(f"Invalid hook event: {hook_event}")
        return hooks.get(hook_event, [])

    return hooks


def add_hook(
    hook_event: str, command: str, timeout: int = 30000, matcher: Optional[str] = None
) -> None:
    """
    Add a hook to a specific event.

    Args:
        hook_event: The event to add the hook to (e.g., "PreToolUse", "Stop")
        command: The command to execute
        timeout: Timeout in milliseconds (default: 30000)
        matcher: Matcher pattern for PreToolUse/PostToolUse events
    """
    if not is_hook_event_valid(hook_event):
        raise ValueError(f"Invalid hook event: {hook_event}")

    settings = read_settings()

    if "hooks" not in settings:
        settings["hooks"] = {}

    if hook_event not in settings["hooks"]:
        settings["hooks"][hook_event] = []

    hook_config = {"type": "command", "command": command, "timeout": timeout}

    # PreToolUse and PostToolUse require a matcher
    if hook_event in ["PreToolUse", "PostToolUse"]:
        if not matcher:
            raise ValueError(f"{hook_event} requires a matcher pattern")

        # Check if matcher already exists
        existing_matcher = None
        for item in settings["hooks"][hook_event]:
            if item.get("matcher") == matcher:
                existing_matcher = item
                break

        if existing_matcher:
            existing_matcher["hooks"].append(hook_config)
        else:
            settings["hooks"][hook_event].append(
                {"matcher": matcher, "hooks": [hook_config]}
            )
    else:
        settings["hooks"][hook_event].append(hook_config)

    write_settings(settings)


def remove_hook(
    hook_event: str, command: Optional[str] = None, matcher: Optional[str] = None
) -> bool:
    """
    Remove a hook from a specific event.

    Args:
        hook_event: The event to remove the hook from
        command: The command to remove (if None, removes all hooks for event)
        matcher: Matcher pattern for PreToolUse/PostToolUse events

    Returns:
        True if a hook was removed, False otherwise
    """
    if not is_hook_event_valid(hook_event):
        raise ValueError(f"Invalid hook event: {hook_event}")

    settings = read_settings()

    if "hooks" not in settings or hook_event not in settings["hooks"]:
        return False

    if command is None:
        # Remove all hooks for this event
        del settings["hooks"][hook_event]
        write_settings(settings)
        return True

    removed = False

    if hook_event in ["PreToolUse", "PostToolUse"]:
        for item in settings["hooks"][hook_event]:
            if matcher and item.get("matcher") != matcher:
                continue

            original_len = len(item["hooks"])
            item["hooks"] = [h for h in item["hooks"] if h.get("command") != command]

            if len(item["hooks"]) < original_len:
                removed = True

        # Clean up empty matcher entries
        settings["hooks"][hook_event] = [
            item for item in settings["hooks"][hook_event] if item.get("hooks")
        ]
    else:
        original_len = len(settings["hooks"][hook_event])
        settings["hooks"][hook_event] = [
            h for h in settings["hooks"][hook_event] if h.get("command") != command
        ]
        removed = len(settings["hooks"][hook_event]) < original_len

    # Clean up empty event entries
    if not settings["hooks"][hook_event]:
        del settings["hooks"][hook_event]

    write_settings(settings)
    return removed


def clear_hooks(hook_event: Optional[str] = None) -> None:
    """
    Clear all hooks or hooks for a specific event.

    Args:
        hook_event: The event to clear hooks for (if None, clears all hooks)
    """
    settings = read_settings()

    if hook_event:
        if not is_hook_event_valid(hook_event):
            raise ValueError(f"Invalid hook event: {hook_event}")

        if "hooks" in settings and hook_event in settings["hooks"]:
            del settings["hooks"][hook_event]
    else:
        settings["hooks"] = {}

    write_settings(settings)


def update_hook(
    hook_event: str,
    old_command: str,
    new_command: Optional[str] = None,
    new_timeout: Optional[int] = None,
    matcher: Optional[str] = None,
) -> bool:
    """
    Update an existing hook.

    Args:
        hook_event: The event the hook belongs to
        old_command: The current command to find
        new_command: The new command (if None, keeps the old command)
        new_timeout: The new timeout (if None, keeps the old timeout)
        matcher: Matcher pattern for PreToolUse/PostToolUse events

    Returns:
        True if a hook was updated, False otherwise
    """
    if not is_hook_event_valid(hook_event):
        raise ValueError(f"Invalid hook event: {hook_event}")

    settings = read_settings()

    if "hooks" not in settings or hook_event not in settings["hooks"]:
        return False

    updated = False

    if hook_event in ["PreToolUse", "PostToolUse"]:
        for item in settings["hooks"][hook_event]:
            if matcher and item.get("matcher") != matcher:
                continue

            for hook in item["hooks"]:
                if hook.get("command") == old_command:
                    if new_command:
                        hook["command"] = new_command
                    if new_timeout:
                        hook["timeout"] = new_timeout
                    updated = True
    else:
        for hook in settings["hooks"][hook_event]:
            if hook.get("command") == old_command:
                if new_command:
                    hook["command"] = new_command
                if new_timeout:
                    hook["timeout"] = new_timeout
                updated = True

    if updated:
        write_settings(settings)

    return updated


def list_hooks() -> None:
    """Print all configured hooks in a readable format."""
    hooks = get_hooks()

    if not hooks:
        print("No hooks configured.")
        return

    for event, event_hooks in hooks.items():
        print(f"\n{event}:")

        if event in ["PreToolUse", "PostToolUse"]:
            for item in event_hooks:
                print(f"  Matcher: {item.get('matcher')}")
                for hook in item.get("hooks", []):
                    print(
                        f"    - {hook.get('command')} (timeout: {hook.get('timeout')}ms)"
                    )
        else:
            for hook in event_hooks:
                print(f"  - {hook.get('command')} (timeout: {hook.get('timeout')}ms)")


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 2:
        list_hooks()
        sys.exit(0)

    action = sys.argv[1]

    if action == "list":
        list_hooks()
    elif action == "add":
        if len(sys.argv) < 4:
            print("Usage: config_hooks.py add <event> <command> [timeout] [matcher]")
            sys.exit(1)
        event = sys.argv[2]
        command = sys.argv[3]
        timeout = int(sys.argv[4]) if len(sys.argv) > 4 else 30000
        matcher = sys.argv[5] if len(sys.argv) > 5 else None
        add_hook(event, command, timeout, matcher)
        print(f"Added hook to {event}")
    elif action == "remove":
        if len(sys.argv) < 3:
            print("Usage: config_hooks.py remove <event> [command] [matcher]")
            sys.exit(1)
        event = sys.argv[2]
        command = sys.argv[3] if len(sys.argv) > 3 else None
        matcher = sys.argv[4] if len(sys.argv) > 4 else None
        if remove_hook(event, command, matcher):
            print(f"Removed hook from {event}")
        else:
            print(f"No matching hook found in {event}")
    elif action == "clear":
        event = sys.argv[2] if len(sys.argv) > 2 else None
        clear_hooks(event)
        print(f"Cleared hooks" + (f" for {event}" if event else ""))
    else:
        print(f"Unknown action: {action}")
        print("Available actions: list, add, remove, clear")
        sys.exit(1)
