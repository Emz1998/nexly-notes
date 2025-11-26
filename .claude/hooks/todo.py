#!/usr/bin/env python3
"""
Claude Code Hook: Phase-Aware Task Manager
Manages TodoWrite integration with session context for phase-based task tracking.

This hook triggers on PreToolUse for TodoWrite events and:
1. Reads session context to determine current phase
2. Filters tasks to only show current phase tasks
3. Detects phase completion and auto-advances to next phase
4. Updates TodoWrite input with phase-specific tasks
"""

import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import tempfile
import shutil


# Phase definitions
PHASE_ORDER = ['E', 'P', 'I', 'C']
PHASE_NAMES = {
    'E': 'Explore',
    'P': 'Plan',
    'I': 'Implement',
    'C': 'Commit'
}


def find_session_context(sessions_dir: Path, session_id: str) -> Optional[Path]:
    """Find the session context file for the given session_id."""
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


def load_session_context(context_path: Path) -> Optional[Dict]:
    """Load and parse the session context JSON file."""
    try:
        with open(context_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading context: {e}", file=sys.stderr)
        return None


def save_session_context(context_path: Path, context: Dict) -> bool:
    """Atomically save the session context to file."""
    try:
        # Update the updated_at timestamp
        context['updated_at'] = datetime.now().isoformat()

        # Write to temp file first, then move (atomic operation)
        fd, temp_path = tempfile.mkstemp(suffix='.json', dir=context_path.parent)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(context, f, indent=2)
            shutil.move(temp_path, context_path)
            return True
        except Exception:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise
    except Exception as e:
        print(f"Error saving context: {e}", file=sys.stderr)
        return False


def get_phase_tasks(context: Dict, phase: str) -> List[Dict]:
    """Get tasks for a specific phase from the context."""
    tasks = context.get('tasks', {})
    return tasks.get(phase, [])


def extract_task_id(content: str) -> Optional[str]:
    """Extract task ID from task content string.

    Examples:
        'T001-E: Review patterns' -> 'T001-E'
        'T002-P: Create plan' -> 'T002-P'
    """
    match = re.match(r'^(T\d+-[A-Z])', content)
    return match.group(1) if match else None


def check_phase_complete(tool_input_todos: List[Dict], phase_tasks: List[Dict]) -> bool:
    """Check if all tasks in the current phase are completed.

    Args:
        tool_input_todos: The todos from TodoWrite tool input (current status)
        phase_tasks: The phase tasks from session context

    Returns:
        True if all phase tasks are marked as 'completed'
    """
    if not phase_tasks:
        return True  # No tasks means phase is complete

    # Build a status map from the tool input
    status_map = {}
    for todo in tool_input_todos:
        content = todo.get('content', '')
        task_id = extract_task_id(content)
        if task_id:
            status_map[task_id] = todo.get('status', 'pending')

    # Check if all phase tasks are completed
    for task in phase_tasks:
        task_id = task.get('id', '')
        status = status_map.get(task_id, task.get('status', 'pending'))
        if status != 'completed':
            return False

    return True


def advance_phase(current_phase: str) -> Optional[str]:
    """Return the next phase in sequence, or None if at the end."""
    try:
        current_index = PHASE_ORDER.index(current_phase)
        if current_index < len(PHASE_ORDER) - 1:
            return PHASE_ORDER[current_index + 1]
    except ValueError:
        pass
    return None


def update_context_phase(context: Dict, new_phase: str) -> Dict:
    """Update the context with a new phase."""
    now = datetime.now().isoformat()
    old_phase = context.get('phase')

    # Update current phase
    context['phase'] = new_phase

    # Update phase history
    phase_history = context.get('phase_history', [])

    # Mark previous phase as completed
    if phase_history and old_phase:
        for entry in reversed(phase_history):
            if entry.get('phase') == old_phase and entry.get('completed_at') is None:
                entry['completed_at'] = now
                break

    # Add new phase entry
    phase_history.append({
        'phase': new_phase,
        'started_at': now,
        'completed_at': None
    })
    context['phase_history'] = phase_history

    return context


def sync_task_status(context: Dict, tool_input_todos: List[Dict]) -> Dict:
    """Sync task status from TodoWrite input back to context."""
    # Build status map from tool input
    status_map = {}
    for todo in tool_input_todos:
        content = todo.get('content', '')
        task_id = extract_task_id(content)
        if task_id:
            status_map[task_id] = todo.get('status', 'pending')

    # Update task status in context
    tasks = context.get('tasks', {})
    for _, phase_tasks in tasks.items():
        for task in phase_tasks:
            task_id = task.get('id', '')
            if task_id in status_map:
                task['status'] = status_map[task_id]

    return context


def create_active_form(content: str) -> str:
    """Convert task content to active/present continuous form.

    Examples:
        'T001-E: Review patterns' -> 'T001-E: Reviewing patterns'
        'T002-P: Create plan' -> 'T002-P: Creating plan'
    """
    # Common verb transformations
    verb_transforms = {
        'Review': 'Reviewing',
        'Identify': 'Identifying',
        'Create': 'Creating',
        'Define': 'Defining',
        'Implement': 'Implementing',
        'Write': 'Writing',
        'Run': 'Running',
        'Prepare': 'Preparing',
        'Explore': 'Exploring',
        'Design': 'Designing',
        'Build': 'Building',
        'Test': 'Testing',
        'Refactor': 'Refactoring',
        'Clean': 'Cleaning',
        'Verify': 'Verifying',
    }

    result = content
    for verb, active in verb_transforms.items():
        # Match verb at start of task description (after ID:)
        pattern = rf'(T\d+-[A-Z]:\s*){verb}\b'
        result = re.sub(pattern, rf'\1{active}', result, flags=re.IGNORECASE)

    return result


def format_todos_for_phase(phase_tasks: List[Dict]) -> List[Dict]:
    """Format phase tasks for TodoWrite tool input."""
    todos = []
    for task in phase_tasks:
        task_id = task.get('id', '')
        content = task.get('content', '')
        status = task.get('status', 'pending')

        full_content = f"{task_id}: {content}" if task_id else content
        active_form = create_active_form(full_content)

        todos.append({
            'content': full_content,
            'activeForm': active_form,
            'status': status
        })

    return todos


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

    # Only process PreToolUse events for TodoWrite
    if hook_event != 'PreToolUse':
        sys.exit(0)

    if tool_name != 'TodoWrite':
        sys.exit(0)

    if not session_id:
        sys.exit(0)

    # Get project directory and sessions path
    project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', cwd))
    sessions_dir = project_dir / 'sessions'

    # Find session context
    context_path = find_session_context(sessions_dir, session_id)
    if not context_path:
        # No session context, pass through original TodoWrite
        sys.exit(0)

    # Load session context
    context = load_session_context(context_path)
    if not context:
        sys.exit(0)

    # Check if this is an /implement session with phase tracking
    command = context.get('command', '')
    current_phase = context.get('phase')

    if command != 'implement' or not current_phase:
        # Not an /implement session or no phase tracking, pass through
        sys.exit(0)

    # Get current TodoWrite input
    current_todos = tool_input.get('todos', [])

    # Sync task status from tool input to context
    context = sync_task_status(context, current_todos)

    # Get tasks for current phase
    phase_tasks = get_phase_tasks(context, current_phase)

    # Check if current phase is complete
    if check_phase_complete(current_todos, phase_tasks):
        # Try to advance to next phase
        next_phase = advance_phase(current_phase)

        if next_phase:
            # Advance to next phase
            context = update_context_phase(context, next_phase)
            current_phase = next_phase
            phase_tasks = get_phase_tasks(context, current_phase)

            print(f"Phase advanced: {PHASE_NAMES.get(current_phase, current_phase)}", file=sys.stderr)
        else:
            # All phases complete
            print("All phases complete!", file=sys.stderr)

    # Save updated context
    save_session_context(context_path, context)

    # Format tasks for TodoWrite
    formatted_todos = format_todos_for_phase(phase_tasks)

    # Only update if we have phase-specific tasks
    if formatted_todos:
        output = {
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'permissionDecision': 'allow',
                'updatedInput': {
                    'todos': formatted_todos
                }
            }
        }
        print(json.dumps(output))

    sys.exit(0)


if __name__ == "__main__":
    main()
