#!/usr/bin/env python3
"""
Claude Code Hook: Session Context Manager
Manages session context for slash commands, particularly /implement with phase tracking.

This hook triggers on PreToolUse for SlashCommand events and creates/updates
session context files that track command execution, phases, and tasks.
"""

import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple


# Phase definitions for /implement command
IMPLEMENT_PHASES = ['E', 'P', 'I', 'C']
PHASE_NAMES = {
    'E': 'Explore',
    'P': 'Plan',
    'I': 'Implement',
    'C': 'Commit'
}

# Default tasks for each phase of /implement
DEFAULT_IMPLEMENT_TASKS = {
    'E': [
        {'id': 'T001-E', 'content': 'Explore existing codebase patterns', 'status': 'pending'},
        {'id': 'T002-E', 'content': 'Identify relevant components and dependencies', 'status': 'pending'},
        {'id': 'T003-E', 'content': 'Review related documentation and specs', 'status': 'pending'},
    ],
    'P': [
        {'id': 'T001-P', 'content': 'Create implementation plan', 'status': 'pending'},
        {'id': 'T002-P', 'content': 'Define acceptance criteria', 'status': 'pending'},
        {'id': 'T003-P', 'content': 'Identify potential risks and mitigations', 'status': 'pending'},
    ],
    'I': [
        {'id': 'T001-I', 'content': 'Implement core functionality', 'status': 'pending'},
        {'id': 'T002-I', 'content': 'Write tests (TDD approach)', 'status': 'pending'},
        {'id': 'T003-I', 'content': 'Refactor and clean up code', 'status': 'pending'},
    ],
    'C': [
        {'id': 'T001-C', 'content': 'Run all tests and verify passing', 'status': 'pending'},
        {'id': 'T002-C', 'content': 'Review changes and prepare commit', 'status': 'pending'},
        {'id': 'T003-C', 'content': 'Create commit with descriptive message', 'status': 'pending'},
    ],
}


def get_next_session_number(sessions_dir: Path) -> int:
    """Scan existing session directories and return the next sequential number."""
    max_num = 0

    if sessions_dir.exists():
        for entry in sessions_dir.iterdir():
            if entry.is_dir():
                # Pattern: NN-description_sessionid
                match = re.match(r'^(\d+)-', entry.name)
                if match:
                    max_num = max(max_num, int(match.group(1)))

    return max_num + 1


def sanitize_description(feature: str) -> str:
    """Convert feature description to directory-safe name.

    Examples:
        'Login Form' -> 'login-form'
        'User Authentication System' -> 'user-authentication-system'
    """
    # Convert to lowercase
    sanitized = feature.lower()

    # Replace spaces and special chars with hyphens
    sanitized = re.sub(r'[^a-z0-9]+', '-', sanitized)

    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')

    # Limit to 30 characters
    if len(sanitized) > 30:
        sanitized = sanitized[:30].rstrip('-')

    return sanitized or 'unnamed'


def parse_command_args(prompt: str) -> Tuple[str, str]:
    """Extract feature and functionality from /implement command arguments.

    Handles formats like:
        /implement "login form" "basic authentication"
        /implement login-form basic-auth
        /implement Build a login form that handles authentication
    """
    # Remove the command prefix
    args = prompt.strip()
    if args.startswith('/implement'):
        args = args[10:].strip()

    # Try to extract quoted strings first
    quoted = re.findall(r'"([^"]+)"', args)
    if len(quoted) >= 2:
        return quoted[0], quoted[1]
    elif len(quoted) == 1:
        return quoted[0], ''

    # Fall back to first word as feature
    words = args.split()
    if words:
        return words[0], ' '.join(words[1:]) if len(words) > 1 else ''

    return 'feature', ''


def find_existing_session(sessions_dir: Path, session_id: str) -> Optional[Path]:
    """Find an existing session context file for the given session_id."""
    if not sessions_dir.exists():
        return None

    # Search for directory containing the session_id (first 8 chars)
    short_id = session_id[:8] if len(session_id) >= 8 else session_id

    for entry in sessions_dir.iterdir():
        if entry.is_dir() and short_id in entry.name:
            context_path = entry / 'context.json'
            if context_path.exists():
                return context_path

    return None


def create_session_context(
    sessions_dir: Path,
    session_id: str,
    command: str,
    feature: str,
    functionality: str
) -> Path:
    """Create a new session directory and context.json file."""

    # Get next session number
    session_number = get_next_session_number(sessions_dir)

    # Create directory name
    sanitized_feature = sanitize_description(feature)
    short_id = session_id[:8] if len(session_id) >= 8 else session_id
    dir_name = f"{session_number:02d}-{sanitized_feature}_{short_id}"

    # Create session directory
    session_dir = sessions_dir / dir_name
    session_dir.mkdir(parents=True, exist_ok=True)

    # Build context data
    now = datetime.now().isoformat()

    context = {
        'session_id': session_id,
        'session_number': session_number,
        'command': command,
        'feature': feature,
        'functionality': functionality,
        'phase': 'E' if command == 'implement' else None,
        'started_at': now,
        'updated_at': now,
        'phase_history': [],
        'tasks': {}
    }

    # Add phase-specific data for /implement
    if command == 'implement':
        context['phase_history'] = [
            {'phase': 'E', 'started_at': now, 'completed_at': None}
        ]
        # Deep copy the default tasks
        context['tasks'] = {
            phase: [task.copy() for task in tasks]
            for phase, tasks in DEFAULT_IMPLEMENT_TASKS.items()
        }

    # Write context file
    context_path = session_dir / 'context.json'
    with open(context_path, 'w', encoding='utf-8') as f:
        json.dump(context, f, indent=2)

    return context_path


def extract_command_name(tool_input: Dict) -> Optional[str]:
    """Extract the command name from SlashCommand tool input."""
    # Try different possible field names
    command = tool_input.get('command', '')
    if command:
        # Remove leading slash if present
        return command.lstrip('/')

    # Try 'skill' field (for Skill tool)
    skill = tool_input.get('skill', '')
    if skill:
        return skill

    return None


def main():
    """Main hook execution function."""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block on error

    # Extract relevant data
    hook_event = input_data.get('hook_event_name', '')
    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})
    session_id = input_data.get('session_id', '')
    cwd = input_data.get('cwd', os.getcwd())

    # Only process PreToolUse events for SlashCommand
    if hook_event != 'PreToolUse':
        sys.exit(0)

    if tool_name not in ['SlashCommand', 'Skill']:
        sys.exit(0)

    # Get command name
    command = extract_command_name(tool_input)
    if not command:
        sys.exit(0)

    # Get project directory
    project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', cwd))
    sessions_dir = project_dir / 'sessions'

    # Check for existing session context
    existing_context = find_existing_session(sessions_dir, session_id)

    if existing_context:
        # Session already exists, just log and continue
        print(f"Session context exists: {existing_context}", file=sys.stderr)
        sys.exit(0)

    # Parse command arguments for /implement
    feature = ''
    functionality = ''

    # Try to get the full prompt to parse arguments
    prompt = tool_input.get('command', '') or tool_input.get('arguments', '')
    if command == 'implement' and prompt:
        feature, functionality = parse_command_args(prompt)
    elif command == 'implement':
        # Use arguments field if available
        args = tool_input.get('arguments', '')
        if args:
            feature, functionality = parse_command_args(args)
        else:
            feature = 'feature'
            functionality = ''

    # Create session context
    try:
        context_path = create_session_context(
            sessions_dir=sessions_dir,
            session_id=session_id,
            command=command,
            feature=feature or command,
            functionality=functionality
        )
        print(f"Created session context: {context_path}", file=sys.stderr)
    except Exception as e:
        print(f"Error creating session context: {e}", file=sys.stderr)

    # Exit successfully without blocking
    sys.exit(0)


if __name__ == "__main__":
    main()
