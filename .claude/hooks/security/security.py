#!/usr/bin/env python3
"""
PreToolUse Hook: Security validation for dangerous commands and paths.

Blocks critical system-damaging operations using exit code 2.
"""
import sys
from pathlib import Path

# Add parent directory to import from utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json, log

# Risk levels
CRITICAL = 20
HIGH = 10
MEDIUM = 5
LOW = 1

# Critical paths that should never be modified
CRITICAL_PATHS = {
    "/etc/passwd",
    "/etc/shadow",
    "/boot/",
    "/sys/",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
}

# Critical commands that can damage the system
CRITICAL_COMMANDS = {
    "rm -rf /",      # Wipes root filesystem
    "rm -rf /*",     # Same effect
    "rm -rf /etc",   # Destroys system config
    "rm -rf /boot",  # Destroys bootloader
    "rm -rf /sys",   # Destroys system interface
    "dd if=/dev/zero of=/dev/",  # Overwrites devices
    "mkfs.ext",      # Formats filesystems
    "mkfs.xfs",
    "mkfs.btrfs",
    "> /dev/sd",     # Overwrites disk
    "> /dev/nvme",
    ":(){ :|:& };:", # Fork bomb
    "chmod -r 777 /", # Destroys permissions
}

# Safe directories (operations here are allowed)
SAFE_DIRECTORIES = {"/.claude/", "/src/", "/tests/"}


def is_safe_path(file_path: str) -> bool:
    """Check if path is within safe project directories."""
    return any(safe_dir in file_path for safe_dir in SAFE_DIRECTORIES)


def check_dangerous_path(file_path: str) -> str | None:
    """Return reason if path is dangerous, None otherwise."""
    if not file_path:
        return None

    # Skip safe project directories
    if is_safe_path(file_path):
        return None

    for pattern in CRITICAL_PATHS:
        if pattern in file_path:
            return f"Attempting to modify critical system file: {pattern}"

    return None


def check_dangerous_command(command: str) -> str | None:
    """Return reason if command is dangerous, None otherwise."""
    if not command:
        return None

    cmd_lower = command.lower()
    for pattern in CRITICAL_COMMANDS:
        if pattern.lower() in cmd_lower:
            return f"System-damaging command detected: {pattern}"

    return None


def validate_security(input_data: dict) -> None:
    """
    Validate tool input for security risks.

    Exits with code 2 if dangerous operation detected.
    Returns None if operation is safe.
    """
    if input_data is None:
        return

    try:
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Check file operations
        if tool_name in ("Write", "Edit", "MultiEdit"):
            file_path = tool_input.get("file_path", "")
            reason = check_dangerous_path(file_path)
            if reason:
                log(f"BLOCKED: {reason}")
                print(reason, file=sys.stderr)
                sys.exit(2)

        # Check bash commands
        elif tool_name == "Bash":
            command = tool_input.get("command", "")
            reason = check_dangerous_command(command)
            if reason:
                log(f"BLOCKED: {reason}")
                print(reason, file=sys.stderr)
                sys.exit(2)

    except Exception as e:
        log(f"Security hook error: {e}")
        # Fail-safe: allow on error


def main():
    """Standalone entry point for direct execution."""
    input_data = read_stdin_json()
    validate_security(input_data)
    sys.exit(0)


if __name__ == "__main__":
    main()
