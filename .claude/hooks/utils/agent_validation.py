#!/usr/bin/env python3
"""Agent validation utilities for PreToolUse and SubagentStop handlers.

Provides helper functions for extracting agent info, checking tool calls,
and blocking agents with standardized error output.
"""

import sys
from typing import Callable

from .output import log


def extract_agent_info(input_data: dict) -> tuple[str, str]:
    """Extract tool name and subagent type from input data.

    Args:
        input_data: Hook input dictionary

    Returns:
        Tuple of (tool_name, subagent_type)
    """
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    subagent_type = tool_input.get("subagent_type", "")
    return tool_name, subagent_type


def is_task_call(input_data: dict) -> bool:
    """Check if input represents a Task tool call.

    Args:
        input_data: Hook input dictionary

    Returns:
        True if this is a Task tool call
    """
    return input_data.get("tool_name") == "Task"


def get_subagent_type(input_data: dict) -> str:
    """Get subagent type from input data.

    Works for both PreToolUse (tool_input.subagent_type) and
    SubagentStop (subagent_type at root level).

    Args:
        input_data: Hook input dictionary

    Returns:
        Subagent type string or empty string
    """
    # SubagentStop has subagent_type at root level
    if "subagent_type" in input_data:
        return input_data.get("subagent_type", "")
    # PreToolUse has it in tool_input
    tool_input = input_data.get("tool_input", {})
    return tool_input.get("subagent_type", "")


def block_agent(reason: str) -> None:
    """Block agent with standardized error output and exit.

    Args:
        reason: Human-readable reason for blocking
    """
    log(reason)
    print(reason, file=sys.stderr)
    sys.exit(2)


def check_dependency(
    condition: bool,
    block_message: str
) -> None:
    """Check a dependency condition and block if not met.

    Args:
        condition: True if dependency is satisfied
        block_message: Message to show if blocking

    Raises:
        SystemExit with code 2 if condition is False
    """
    if not condition:
        block_agent(block_message)


def create_agent_guard(
    target_agents: list[str],
    mode_check: Callable[[], bool],
    session_getter: Callable[[], str],
    dependency_checks: dict[str, Callable[[str], tuple[bool, str]]]
) -> Callable[[dict], None]:
    """Factory for creating agent blocking validators.

    Args:
        target_agents: List of agent names to validate
        mode_check: Function that returns True if mode is active
        session_getter: Function that returns current session_id
        dependency_checks: Dict mapping agent name to validation function
            that takes session_id and returns (satisfied, block_message)

    Returns:
        Validator function that takes input_data
    """
    def validator(input_data: dict) -> None:
        # Only process Task tool calls
        if not is_task_call(input_data):
            return

        _, subagent = extract_agent_info(input_data)

        # Only validate target agents
        if subagent not in target_agents:
            return

        # Check if mode is active
        if not mode_check():
            return

        # Get session_id
        session_id = session_getter()
        if not session_id:
            block_agent(f"{subagent} call rejected. Session ID not found.")

        # Check dependencies for this agent
        if subagent in dependency_checks:
            satisfied, message = dependency_checks[subagent](session_id)
            if not satisfied:
                block_agent(message)

    return validator


def create_stop_validator(
    target_agents: list[str],
    mode_check: Callable[[], bool],
    session_getter: Callable[[], str],
    completion_checks: dict[str, Callable[[str], tuple[bool, str]]]
) -> Callable[[dict], None]:
    """Factory for creating subagent stop validators.

    Args:
        target_agents: List of agent names to validate
        mode_check: Function that returns True if mode is active
        session_getter: Function that returns current session_id
        completion_checks: Dict mapping agent name to validation function
            that takes session_id and returns (completed, block_message)

    Returns:
        Validator function that takes input_data
    """
    def validator(input_data: dict) -> None:
        # Check if mode is active
        if not mode_check():
            return

        # Get subagent type
        subagent = get_subagent_type(input_data)

        # Only validate target agents
        if subagent not in target_agents:
            return

        # Get session_id
        session_id = session_getter()
        if not session_id:
            return

        # Check completion for this agent
        if subagent in completion_checks:
            completed, message = completion_checks[subagent](session_id)
            if not completed:
                block_agent(message)

    return validator
