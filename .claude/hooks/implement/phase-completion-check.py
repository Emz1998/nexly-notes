#!/usr/bin/env python3
"""
Phase Completion Validation Hook - PostToolUse

Exit Codes:
  0 = Requirements met
  2 = Incomplete (blocks with message)
"""

import json
import subprocess
import sys
from pathlib import Path

WORKFLOW_STATE_FILE = Path(__file__).parent / "state.json"
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SESSION_DIR = PROJECT_ROOT / "session"

DOCUMENTATION_REQUIREMENTS = {
    "explore": "codebase-status.md",
    "research": "research-report.md",
    "research_review": "research-report-feedback.md",
    "plan": "implementation-plan.md",
    "plan_consult": "implementation-plan-feedback.md",
}

CODING_PHASES = ("failing_test", "passing_test", "refactor")
CODE_EXTENSIONS = (".py", ".js", ".ts", ".tsx", ".jsx", ".css", ".html")


def read_state() -> dict:
    try:
        with open(WORKFLOW_STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"active": False, "phase": "explore"}


def get_git_status() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        return []


def has_code_changes() -> bool:
    """Check for code changes (includes untracked files)."""
    status_lines = get_git_status()
    for line in status_lines:
        if len(line) < 3:
            continue
        file_path = line[3:].strip()
        if any(file_path.endswith(ext) for ext in CODE_EXTENSIONS):
            return True
    return False


def has_uncommitted_changes() -> bool:
    return len(get_git_status()) > 0


def validate_phase_completion(phase: str) -> tuple[bool, str]:
    # Documentation phases
    if phase in DOCUMENTATION_REQUIREMENTS:
        required_file = SESSION_DIR / DOCUMENTATION_REQUIREMENTS[phase]
        if not required_file.exists():
            return False, (
                f"Phase '{phase}' requires: {DOCUMENTATION_REQUIREMENTS[phase]}\n"
                f"Expected at: session/{DOCUMENTATION_REQUIREMENTS[phase]}\n"
                f"Complete this deliverable before advancing."
            )

    # Coding phases
    elif phase in CODING_PHASES:
        if not has_code_changes():
            return False, (
                f"Phase '{phase}' requires code changes.\n"
                f"No modified/new code files detected in git status.\n"
                f"Implement required code changes before advancing."
            )

    # Commit phase
    elif phase == "commit":
        if has_uncommitted_changes():
            return False, (
                "Commit phase requires all changes to be committed.\n"
                "Uncommitted changes detected. Create a commit before completing."
            )

    return True, ""


def main():
    hook_input = json.load(sys.stdin)

    state = read_state()
    if not state.get("active", False):
        sys.exit(0)

    current_phase = state.get("phase", "explore")
    is_complete, message = validate_phase_completion(current_phase)

    if not is_complete:
        print(message, file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
