import subprocess
from pathlib import Path


def get_git_status(cwd: Path = None) -> list[str]:
    """Get raw git status lines."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "-uall"],
            capture_output=True,
            text=True,
            cwd=cwd or Path.cwd(),
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        return []


def get_modified_files(cwd: Path = None) -> list[str]:
    """Get list of modified file paths (cleaned)."""
    return [fp[3:] for fp in get_git_status(cwd) if len(fp) > 3]
