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


def is_file_committed(file_path: str, cwd: Path = None) -> bool:
    """Check if a file has been committed (not in modified/untracked list)."""
    try:
        # Check if file exists in git index (has been committed at some point)
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", file_path],
            capture_output=True,
            text=True,
            cwd=cwd or Path.cwd(),
        )
        if result.returncode != 0:
            return False
        # Check if file has uncommitted changes
        modified = get_modified_files(cwd)
        return file_path not in modified
    except Exception:
        return False
