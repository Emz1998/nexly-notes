#!/usr/bin/env python3
"""Module: implement_flow_mode/validate_flow - Validate slash command flow sequence."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import set_cache, get_cache, log, block_response

NAMESPACE = "implement_flow"

# Define the expected flow sequence
FLOW_SEQUENCE = ["explore", "research", "plan", "code", "code-review", "commit"]


def _is_active() -> bool:
    """Check if implement flow mode is active."""
    return get_cache(NAMESPACE, "is_active") or False


def _get_current_step() -> int:
    """Get current step index in the flow."""
    return get_cache(NAMESPACE, "current_step") or 0


def _get_completed_steps() -> list:
    """Get list of completed steps."""
    return get_cache(NAMESPACE, "completed_steps") or []


def _advance_step(step_name: str) -> None:
    """Advance to the next step in the flow."""
    current = _get_current_step()
    completed = _get_completed_steps()

    completed.append(step_name)
    set_cache(NAMESPACE, "completed_steps", completed)
    set_cache(NAMESPACE, "current_step", current + 1)


def _extract_command_name(command: str) -> str:
    """Extract the base command name from a slash command.

    Examples:
        "/explore foo bar" -> "explore"
        "/code-review" -> "code-review"
        "/plan implementation xyz" -> "plan"
    """
    # Remove leading slash and get first word
    if command.startswith("/"):
        command = command[1:]
    return command.split()[0].lower() if command else ""


def validate_slash_command_flow(input_data: dict) -> None:
    """Validate that slash commands are called in the correct order.

    Called from PreToolUse when tool_name == "SlashCommand".

    Args:
        input_data: Hook input dictionary with tool_input.command
    """
    # Only validate when flow is active
    if not _is_active():
        return

    # Only process SlashCommand tool calls
    if input_data.get("tool_name") != "SlashCommand":
        return

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")
    command_name = _extract_command_name(command)

    # Skip if not a flow-related command
    if command_name not in FLOW_SEQUENCE:
        return

    current_step = _get_current_step()
    expected_step = FLOW_SEQUENCE[current_step] if current_step < len(FLOW_SEQUENCE) else None

    # Check if this command matches the expected step
    if command_name != expected_step:
        completed = _get_completed_steps()
        remaining = FLOW_SEQUENCE[current_step:]

        # Check if trying to skip ahead
        if command_name in remaining:
            skipped_steps = remaining[:remaining.index(command_name)]
            block_response(
                f"Flow sequence violation: Cannot call /{command_name} yet.\n"
                f"Complete these steps first: /{', /'.join(skipped_steps)}\n"
                f"Expected: /{expected_step}\n"
                f"Completed: {', '.join(completed) if completed else 'none'}"
            )

        # Check if command was already completed (going backwards)
        if command_name in completed:
            block_response(
                f"Flow sequence violation: /{command_name} was already completed.\n"
                f"Current expected step: /{expected_step}\n"
                f"Completed: {', '.join(completed)}"
            )

    # Command is valid - advance will happen in PostToolUse


def mark_step_complete(command_name: str) -> None:
    """Mark a flow step as complete after successful execution.

    Called from PostToolUse after SlashCommand completes.

    Args:
        command_name: The slash command that completed
    """
    if not _is_active():
        return

    # Normalize command name
    if command_name.startswith("/"):
        command_name = command_name[1:]
    command_name = command_name.split()[0].lower()

    if command_name not in FLOW_SEQUENCE:
        return

    current_step = _get_current_step()
    expected_step = FLOW_SEQUENCE[current_step] if current_step < len(FLOW_SEQUENCE) else None

    if command_name == expected_step:
        _advance_step(command_name)
        remaining = FLOW_SEQUENCE[current_step + 1:]
        if remaining:
            log(f"Flow step /{command_name} complete. Next: /{remaining[0]}")
        else:
            log(f"Flow step /{command_name} complete. Implement flow finished!")
            # Deactivate flow when complete
            from .deactivate import deactivate
            deactivate()
