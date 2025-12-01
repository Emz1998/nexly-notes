import json
import sys
from pathlib import Path


def get_plan_content():
    for file in Path(".claude/plans").glob("*.md"):
        if file.is_file():
            with open(file, "r") as f:
                content = f.read()
                return content
    return None
