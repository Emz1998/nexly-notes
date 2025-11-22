#!/usr/bin/env python3
"""
Claude Code Hook: Task Log Stop Hook
Logs incomplete tasks as "Cancelled" when session ends.

This hook fires on Stop event and checks if there are incomplete tasks
from the most recent TodoWrite operation. If found, logs them as Cancelled.
"""

import json
import sys
import os
import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def extract_agent_name(transcript_path: str) -> str:
    """Extract agent name from transcript or session context."""
    try:
        if os.path.exists(transcript_path):
            with open(transcript_path, 'r', encoding='utf-8') as f:
                # Read the last few lines to find agent context
                lines = f.readlines()
                for line in reversed(lines[-50:]):  # Check last 50 lines
                    try:
                        data = json.loads(line.strip())
                        if 'role' in data and data['role'] == 'assistant':
                            # Look for agent mentions in content
                            content = data.get('content', '')
                            # Check for subagent patterns
                            if 'subagent' in content.lower() or '@' in content:
                                agent_patterns = [
                                    r'@([a-zA-Z-]+(?:-[a-zA-Z]+)*)',
                                    r'subagent:\s*([a-zA-Z-]+(?:-[a-zA-Z]+)*)',
                                    r'agent:\s*([a-zA-Z-]+(?:-[a-zA-Z]+)*)',
                                    r'using\s+([a-zA-Z-]+(?:-[a-zA-Z]+)*)\s+agent'
                                ]
                                for pattern in agent_patterns:
                                    match = re.search(pattern, content, re.IGNORECASE)
                                    if match:
                                        return match.group(1).lower()
                    except (json.JSONDecodeError, KeyError):
                        continue
    except Exception:
        pass

    return "main-agent"

def extract_user_prompt(transcript_path: str) -> str:
    """Extract the most recent user prompt from transcript."""
    try:
        if os.path.exists(transcript_path):
            with open(transcript_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Look for the most recent user message
                for line in reversed(lines):
                    try:
                        data = json.loads(line.strip())
                        if 'role' in data and data['role'] == 'user':
                            content = data.get('content', '')
                            if content:
                                # Clean up and truncate
                                content = content.strip()
                                # Remove system-reminder tags if present
                                if '<system-reminder>' in content:
                                    # Extract just the user's actual prompt
                                    parts = content.split('<system-reminder>')
                                    content = parts[0].strip()

                                # Truncate to reasonable length
                                if len(content) > 150:
                                    content = content[:147] + "..."

                                return content if content else "No prompt found"
                    except (json.JSONDecodeError, KeyError):
                        continue
    except Exception:
        pass

    return "No prompt found"

def find_last_todo_list(transcript_path: str) -> Tuple[List[str], bool]:
    """
    Find the most recent TodoWrite tool call and extract tasks.
    Returns (tasks, has_incomplete) tuple.
    """
    try:
        if os.path.exists(transcript_path):
            with open(transcript_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                # Look for the most recent tool use with TodoWrite
                for line in reversed(lines):
                    try:
                        data = json.loads(line.strip())

                        # Check if this is a tool use message
                        if 'role' in data and data['role'] == 'assistant':
                            content = data.get('content', [])

                            # Content might be a list of content blocks
                            if isinstance(content, list):
                                for block in content:
                                    if isinstance(block, dict) and block.get('type') == 'tool_use':
                                        if block.get('name') == 'TodoWrite':
                                            tool_input = block.get('input', {})
                                            todos = tool_input.get('todos', [])

                                            if todos:
                                                tasks = []
                                                has_incomplete = False

                                                for todo in todos:
                                                    if isinstance(todo, dict):
                                                        task = todo.get('content', todo.get('description', 'Unknown task'))
                                                        status = todo.get('status', 'pending').lower()

                                                        tasks.append(task)

                                                        if status != 'completed':
                                                            has_incomplete = True

                                                return tasks, has_incomplete
                    except (json.JSONDecodeError, KeyError):
                        continue
    except Exception:
        pass

    return [], False

def format_tasks(tasks: List[str]) -> str:
    """Format all tasks as vertical list."""
    if not tasks:
        return "  None"

    # Format as vertical list
    formatted = []
    for task in tasks:
        formatted.append(f"  - {task}")

    return "\n".join(formatted)

def format_log_entry(timestamp: str, agent_name: str, user_prompt: str, tasks: List[str]) -> str:
    """Format log entry in vertical structure."""
    entry_parts = [
        timestamp,
        "",  # Empty line after timestamp
        f"Prompt: {user_prompt}",
        "Tasks:",
        format_tasks(tasks),
        f"Owned by: {agent_name}",
        "Status: Cancelled",
        "",  # Empty line before separator
        "---"
    ]

    return "\n".join(entry_parts)

def ensure_log_file(log_path: str) -> None:
    """Ensure the log file exists with header."""
    if not os.path.exists(log_path):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("# Task Log\n")
            f.write("# Vertical format for better readability with long todo lists\n")
            f.write("#" + "="*70 + "\n\n")

def append_log_entry(log_path: str, entry: str) -> None:
    """Append an entry to the log file."""
    try:
        ensure_log_file(log_path)

        # Check if we need to add date header
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # Read existing content
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if today's date header exists
        date_header = f"## {today}"
        if date_header not in content:
            # Add date header
            with open(log_path, 'a', encoding='utf-8') as f:
                if not content.endswith('\n\n'):
                    f.write('\n')
                f.write(f"\n{date_header}\n\n")

        # Append the entry
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(entry + '\n')

    except Exception as e:
        print(f"Error writing to log: {e}", file=sys.stderr)

def main():
    """Main hook execution function."""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract relevant data
    hook_event = input_data.get("hook_event_name", "")
    cwd = input_data.get("cwd", "")
    transcript_path = input_data.get("transcript_path", "")
    stop_hook_active = input_data.get("stop_hook_active", False)

    # Only process Stop events
    if hook_event != "Stop":
        sys.exit(0)

    # Avoid infinite loops - don't process if stop hook already active
    if stop_hook_active:
        sys.exit(0)

    # Check if there are incomplete tasks
    tasks, has_incomplete = find_last_todo_list(transcript_path)

    # Only log if there are incomplete tasks
    if not has_incomplete or not tasks:
        sys.exit(0)

    # Extract agent name and user prompt
    agent_name = extract_agent_name(transcript_path)
    user_prompt = extract_user_prompt(transcript_path)

    # Format the data
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    # Create the log entry
    log_entry = format_log_entry(timestamp, agent_name, user_prompt, tasks)

    # Write to log file
    log_path = os.path.join(cwd, ".claude", "logs", "TASKS.log")
    append_log_entry(log_path, log_entry)

    # Success - suppress output
    print(json.dumps({"suppressOutput": True}))
    sys.exit(0)

if __name__ == "__main__":
    main()
