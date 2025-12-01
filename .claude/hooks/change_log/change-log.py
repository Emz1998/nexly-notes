#!/usr/bin/env python3
"""
Claude Code Hook: Change Log Tracker
Automatically tracks file changes and logs them to .claude/logs/CHANGELOG.md

This hook monitors file creation, modification, and deletion events
and appends entries to the changelog in the proper format.
"""

import json
import sys
import os
import datetime
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

def extract_agent_name(transcript_path: str) -> str:
    """Extract agent name from transcript or session context."""
    try:
        if os.path.exists(transcript_path):
            with open(transcript_path, 'r', encoding='utf-8') as f:
                # Read the last few lines to find agent context
                lines = f.readlines()
                for line in reversed(lines[-20:]):  # Check last 20 lines
                    try:
                        data = json.loads(line.strip())
                        if 'role' in data and data['role'] == 'assistant':
                            # Look for agent mentions in content
                            content = data.get('content', '')
                            if 'subagent' in content.lower() or 'agent' in content.lower():
                                # Extract agent name patterns
                                agent_patterns = [
                                    r'@([a-zA-Z-]+(?:-[a-zA-Z]+)*)',
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


def determine_change_type(tool_name: str, file_path: str, tool_input: Dict) -> str:
    """Determine the type of change based on tool and context."""
    file_path_lower = file_path.lower()

    # Check if it's a new file creation
    if tool_name == "Write" and not os.path.exists(file_path):
        return "Added"

    # Check for specific file types and operations
    if tool_name in ["Edit", "MultiEdit"]:
        # Look for fix indicators in the operation
        old_string = tool_input.get("old_string", "").lower()
        new_string = tool_input.get("new_string", "").lower()

        if any(word in old_string or word in new_string for word in ["fix", "bug", "error", "issue"]):
            return "Fixed"
        elif any(word in old_string or word in new_string for word in ["security", "auth", "permission"]):
            return "Security"
        elif any(word in old_string or word in new_string for word in ["deprecat", "obsolete"]):
            return "Deprecated"
        else:
            return "Changed"

    if tool_name == "Write":
        return "Changed"

    # Handle file removals (theoretical, as most tools don't delete files)
    if "remove" in tool_name.lower() or "delete" in tool_name.lower():
        return "Removed"

    return "Changed"


def generate_description(tool_name: str, file_path: str, change_type: str) -> str:
    """Generate a meaningful description based on file path and change type."""
    path_obj = Path(file_path)
    file_name = path_obj.name
    parent_dir = path_obj.parent.name if path_obj.parent.name != "." else ""

    # Component/file type detection
    if file_path.endswith(('.tsx', '.ts', '.jsx', '.js')):
        if 'component' in file_name.lower():
            component_type = "component"
        elif 'hook' in file_name.lower():
            component_type = "hook"
        elif 'util' in file_name.lower() or 'helper' in file_name.lower():
            component_type = "utility"
        elif 'api' in file_name.lower():
            component_type = "API endpoint"
        elif 'test' in file_name.lower() or 'spec' in file_name.lower():
            component_type = "test"
        else:
            component_type = "module"
    elif file_path.endswith(('.py')):
        if 'test' in file_name.lower():
            component_type = "test script"
        elif '.claude/hooks/' in file_path:
            component_type = "hook script"
        elif '.claude/agents/' in file_path:
            component_type = "agent configuration"
        else:
            component_type = "Python script"
    elif file_path.endswith(('.md', '.mdx')):
        if 'readme' in file_name.lower():
            component_type = "documentation"
        elif '.claude/' in file_path:
            component_type = "configuration documentation"
        else:
            component_type = "documentation"
    elif file_path.endswith(('.json', '.yaml', '.yml')):
        if 'package' in file_name.lower():
            component_type = "package configuration"
        elif 'config' in file_name.lower() or 'settings' in file_name.lower():
            component_type = "configuration"
        else:
            component_type = "configuration file"
    elif file_path.endswith(('.css', '.scss', '.sass')):
        component_type = "stylesheet"
    else:
        component_type = "file"

    # Generate description based on change type
    if change_type == "Added":
        return f"Created {component_type}"
    elif change_type == "Changed":
        return f"Updated {component_type}"
    elif change_type == "Fixed":
        return f"Fixed issues in {component_type}"
    elif change_type == "Security":
        return f"Security update for {component_type}"
    elif change_type == "Deprecated":
        return f"Deprecated {component_type}"
    elif change_type == "Removed":
        return f"Removed {component_type}"
    else:
        return f"Modified {component_type}"


def read_existing_changelog(changelog_path: str) -> Tuple[str, str]:
    """Read existing changelog and return header and entries sections."""
    if not os.path.exists(changelog_path):
        # Create basic structure if file doesn't exist
        header = """# Changelog

## Format

```
TIME | TYPE | DESCRIPTION | FILE_PATH | AGENT
```

**Types:** Added, Changed, Deprecated, Removed, Fixed, Security

---

"""
        return header, ""

    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the first date section marker (### YYYY-MM-DD pattern)
        date_pattern = re.compile(r'^### \d{4}-\d{2}-\d{2}', re.MULTILINE)
        match = date_pattern.search(content)

        if match:
            # Split at the first date section
            header_end = match.start()
            header = content[:header_end]
            entries = content[header_end:]

            # Ensure header ends with ---\n if not already there
            if not header.rstrip().endswith('---'):
                header = header.rstrip() + "\n\n---\n\n"
        else:
            # No date sections yet, split at "---" marker
            if "---" in content:
                parts = content.split("---", 1)
                header = parts[0] + "---\n"
                entries = parts[1] if len(parts) > 1 else ""
            else:
                header = content + "\n---\n"
                entries = ""

        return header, entries
    except Exception as e:
        print(f"Error reading changelog: {e}", file=sys.stderr)
        return "", ""


def get_today_section_line(entries: str) -> Optional[int]:
    """Find the line number of today's date section in the entries."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    lines = entries.split('\n')

    for i, line in enumerate(lines):
        if line.strip() == f"### {today}":
            return i

    return None


def append_changelog_entry(changelog_path: str, entry: str) -> None:
    """Insert a new entry at the top of the changelog file (descending order)."""
    try:
        header, entries = read_existing_changelog(changelog_path)
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # Check if entry already exists (avoid duplicates)
        if entry.strip() in entries:
            return

        lines = entries.split('\n') if entries else []
        today_line = get_today_section_line(entries)

        if today_line is not None:
            # Today's section exists, insert entry right after the date header
            # Skip blank lines after the header
            insert_idx = today_line + 1
            while insert_idx < len(lines) and lines[insert_idx].strip() == "":
                insert_idx += 1
            lines.insert(insert_idx, f"- {entry}")
        else:
            # Create new section for today at the top
            # Find where to insert (skip initial blank lines)
            insert_idx = 0
            while insert_idx < len(lines) and lines[insert_idx].strip() == "":
                insert_idx += 1

            # Insert new date section at the top
            new_section = ["\n", f"### {today}", "", f"- {entry}"]
            for item in reversed(new_section):
                lines.insert(insert_idx, item)

        # Write back to file
        new_content = header + '\n'.join(lines)

        # Ensure parent directory exists
        os.makedirs(os.path.dirname(changelog_path), exist_ok=True)

        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    except Exception as e:
        print(f"Error appending to changelog: {e}", file=sys.stderr)


def should_track_file(file_path: str) -> bool:
    """Determine if a file should be tracked in the changelog."""
    # Skip tracking temporary files, logs, and certain paths
    skip_patterns = [
        r'\.tmp$', r'\.temp$', r'\.log$',
        r'/tmp/', r'/temp/', r'/.git/',
        r'/node_modules/', r'/.cache/',
        r'\.pyc$', r'__pycache__',
        r'\.DS_Store$', r'Thumbs\.db$'
    ]

    for pattern in skip_patterns:
        if re.search(pattern, file_path, re.IGNORECASE):
            return False

    return True

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
    cwd = input_data.get("cwd", "")
    transcript_path = input_data.get("transcript_path", "")

    # Only process PostToolUse events for file operations
    if hook_event != "PostToolUse":
        sys.exit(0)

    # Only track file modification tools
    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        sys.exit(0)

    # Get file path from tool input
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Skip files we don't want to track
    if not should_track_file(file_path):
        sys.exit(0)

    # Make file path relative to project root if possible
    if file_path.startswith(cwd):
        relative_path = os.path.relpath(file_path, cwd)
    else:
        relative_path = file_path

    # Extract agent information
    agent_name = extract_agent_name(transcript_path)

    # Determine change type and description
    change_type = determine_change_type(tool_name, file_path, tool_input)
    description = generate_description(tool_name, relative_path, change_type)

    # Create timestamp
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    # Format the entry
    entry = f"{timestamp} | {change_type} | {description} | `{relative_path}` | {agent_name}"

    # Append to changelog
    changelog_path = os.path.join(cwd, ".claude", "logs", "CHANGELOG.md")
    append_changelog_entry(changelog_path, entry)

    # Success - no output needed
    sys.exit(0)


if __name__ == "__main__":
    main()