#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Hook: switch-plan-mode

Purpose: Switch from --dangerously-skip-permissions mode to plan mode before using ExitPlanMode.
This will stop auto-approving plans and force switching to plan mode when presenting the plan.

Hook Behavior:
1. Detect when Claude is running with the --dangerously-skip-permissions flag active
2. Intercept when the ExitPlanMode tool is about to be used
3. Switch from auto-approval mode to interactive plan mode
4. This ensures that plans are not auto-approved and require user confirmation
5. The hook should activate specifically when ExitPlanMode is being called while in --dangerously-skip-permissions mode

Event Trigger: PreToolUse - ExitPlanMode
Action: Remove auto-approval behavior and switch to interactive plan mode
"""

import json
import sys
import os
import subprocess
from typing import Dict, Any, Optional


def check_dangerous_skip_permissions() -> bool:
    """
    Check if Claude is currently running with --dangerously-skip-permissions flag.
    This can be detected by checking the current process arguments or environment.
    """
    try:
        # Check current process command line arguments
        with open('/proc/self/cmdline', 'rb') as f:
            cmdline = f.read().decode('utf-8', errors='ignore')
            if '--dangerously-skip-permissions' in cmdline:
                return True
    except (FileNotFoundError, PermissionError):
        # /proc not available or not Linux, try alternative methods
        pass

    try:
        # Check parent process arguments (Claude Code process)
        ppid = os.getppid()
        with open(f'/proc/{ppid}/cmdline', 'rb') as f:
            cmdline = f.read().decode('utf-8', errors='ignore')
            if '--dangerously-skip-permissions' in cmdline:
                return True
    except (FileNotFoundError, PermissionError):
        pass

    # Check environment variables that might indicate dangerous skip mode
    if os.environ.get('CLAUDE_DANGEROUS_SKIP_PERMISSIONS'):
        return True

    # As a fallback, check if we can find claude process with the flag
    try:
        result = subprocess.run(
            ['pgrep', '-f', '--dangerously-skip-permissions'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return False


def validate_input(input_data: Dict[str, Any]) -> bool:
    """Validate the hook input data structure."""
    required_fields = ['hook_event_name', 'tool_name']

    for field in required_fields:
        if field not in input_data:
            return False

    return True


def create_plan_mode_switch_response() -> Dict[str, Any]:
    """
    Create the JSON response to switch from auto-approval to interactive plan mode.
    This asks the user to confirm the ExitPlanMode tool call instead of auto-approving it.
    """
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": "Switched from auto-approval mode to interactive plan mode. Please review the plan before proceeding."
        },
        "suppressOutput": False
    }


def main():
    """Main hook execution function."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate input structure
    if not validate_input(input_data):
        print("Error: Invalid input structure", file=sys.stderr)
        sys.exit(1)

    # Extract relevant data
    hook_event_name = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only proceed if this is a PreToolUse event for ExitPlanMode
    if hook_event_name != "PreToolUse" or tool_name != "ExitPlanMode":
        # Not our target event, allow normal processing
        sys.exit(0)

    # Check if dangerous skip permissions mode is active
    if not check_dangerous_skip_permissions():
        # Not in dangerous skip mode, allow normal processing
        sys.exit(0)

    # We are in dangerous skip mode and ExitPlanMode is being called
    # Switch to interactive plan mode
    response = create_plan_mode_switch_response()

    # Output the JSON response to switch modes
    print(json.dumps(response, indent=2))

    # Exit successfully to apply the mode switch
    sys.exit(0)


if __name__ == "__main__":
    main()