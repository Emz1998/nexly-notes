#!/usr/bin/env python3
"""YAML frontmatter parsing utilities for markdown files."""

import re
from pathlib import Path
from typing import Optional

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content. Returns empty dict if none."""
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split("\n"):
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def get_file_frontmatter(file_path: Path) -> dict:
    """Get frontmatter from a markdown file."""
    try:
        content = file_path.read_text()
        return parse_frontmatter(content)
    except (FileNotFoundError, IOError):
        return {}


def has_consultation_marker(file_path: Path) -> bool:
    """Check if plan file has been consulted by consulting-expert."""
    frontmatter = get_file_frontmatter(file_path)
    consulted_by = frontmatter.get("consulted_by", "")
    return "consulting-expert" in consulted_by.lower()


def has_research_validation_marker(file_path: Path) -> bool:
    """Check if research file has been validated by research-consultant."""
    frontmatter = get_file_frontmatter(file_path)
    validated_by = frontmatter.get("validated_by", "")
    return "research-consultant" in validated_by.lower()


def add_frontmatter(file_path: Path, key: str, value: str) -> bool:
    """Add or update a frontmatter field in a markdown file."""
    try:
        content = file_path.read_text()
        match = FRONTMATTER_PATTERN.match(content)

        if match:
            # Update existing frontmatter
            fm_content = match.group(1)
            body = content[match.end():]

            # Check if key exists
            lines = fm_content.split("\n")
            updated = False
            for i, line in enumerate(lines):
                if line.strip().startswith(f"{key}:"):
                    lines[i] = f"{key}: {value}"
                    updated = True
                    break

            if not updated:
                lines.append(f"{key}: {value}")

            new_content = f"---\n{chr(10).join(lines)}\n---\n{body}"
        else:
            # Add new frontmatter
            new_content = f"---\n{key}: {value}\n---\n\n{content}"

        file_path.write_text(new_content)
        return True
    except (FileNotFoundError, IOError):
        return False
