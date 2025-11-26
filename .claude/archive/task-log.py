#!/usr/bin/env python3
"""
Claude Code Hook: Task Log Tracker
Automatically logs TodoList tool usage and task completions to .claude/logs/TASKS.log

This hook monitors TodoList tool operations and logs them in a structured format
for tracking task management activities across sessions.
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

def parse_todo_items(items: List[Dict]) -> Tuple[List[str], Dict[str, int]]:
    """Parse todo items and return all tasks with status counts."""
    all_tasks = []
    status_counts = {
        "pending": 0,
        "in_progress": 0,
        "completed": 0
    }

    for item in items:
        if isinstance(item, dict):
            status = item.get("status", "pending").lower()
            # Support both "content" and "description" field names
            description = item.get("content", item.get("description", "Unknown task"))

            # Count by status
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts["pending"] += 1  # Default to pending if unknown

            # Collect all tasks
            all_tasks.append(description)

    return all_tasks, status_counts

def format_status(status_counts: Dict[str, int]) -> str:
    """Determine overall status from task counts."""
    total = sum(status_counts.values())

    if total == 0:
        return "Cancelled"

    # If all tasks completed
    if status_counts["completed"] == total:
        return "Completed"

    # Any incomplete tasks = Cancelled (session interrupted/abandoned)
    return "Cancelled"

def format_tasks(tasks: List[str]) -> str:
    """Format all tasks as vertical list."""
    if not tasks:
        return "  None"

    # Format as vertical list
    formatted = []
    for task in tasks:
        formatted.append(f"  - {task}")

    return "\n".join(formatted)

def format_log_entry(timestamp: str, agent_name: str, user_prompt: str, status: str, tasks: List[str]) -> str:
    """Format log entry in vertical structure."""
    entry_parts = [
        timestamp,
        "",  # Empty line after timestamp
        f"Prompt: {user_prompt}",
        "Tasks:",
        format_tasks(tasks),
        f"Owned by: {agent_name}",
        f"Status: {status}",
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
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    tool_output = input_data.get("tool_output", {})
    cwd = input_data.get("cwd", "")
    transcript_path = input_data.get("transcript_path", "")

    # Only process PostToolUse events for TodoList/TodoWrite tools
    if hook_event != "PostToolUse":
        sys.exit(0)

    # Check if it's a TodoList-related tool
    if tool_name not in ["TodoWrite", "TodoList", "TodoUpdate", "TodoDelete"]:
        # Also check if tool_name contains "todo" (case insensitive)
        if "todo" not in tool_name.lower():
            sys.exit(0)

    # Extract agent name
    agent_name = extract_agent_name(transcript_path)

    # Extract user prompt as context
    context = extract_user_prompt(transcript_path)

    # Parse todo items from input or output
    items = []
    if tool_name == "TodoWrite" or tool_name == "TodoUpdate":
        # For write/update, items are in input (can be "todos" or "items")
        items = tool_input.get("todos", tool_input.get("items", []))
    elif tool_output:
        # For TodoList, items might be in output
        if isinstance(tool_output, dict):
            items = tool_output.get("items", [])
        elif isinstance(tool_output, list):
            items = tool_output

    # Parse tasks and get status
    all_tasks, status_counts = parse_todo_items(items)

    # Format the data
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    status = format_status(status_counts)

    # Create the log entry using vertical format
    log_entry = format_log_entry(timestamp, agent_name, context, status, all_tasks)

    # Write to log file
    log_path = os.path.join(cwd, ".claude", "logs", "TASKS.log")
    append_log_entry(log_path, log_entry)

    # Success - no output needed (suppress output to not interfere with tool)
    print(json.dumps({"suppressOutput": True}))
    sys.exit(0)

if __name__ == "__main__":
    main()