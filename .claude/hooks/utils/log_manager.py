from datetime import datetime

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


from utils import get_cache


DEFAULT_LOG_FILE = str(Path(".claude/logs/VIOLATIONS.log"))


def load_log_file(file_path: str = DEFAULT_LOG_FILE) -> str:
    # Read a file and return its content
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")


def write_log_file(data: dict, file_path: str = DEFAULT_LOG_FILE) -> None:
    content = data.get("content")
    source_file = data.get("source_file")
    # Write content to a file
    session_id = get_cache("session_id")
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {content} | {session_id} | {source_file}\n"
            )
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
