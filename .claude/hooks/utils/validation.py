"""Format validation utilities."""

import re

PATTERNS = {
    "milestone": r"MS-(\d{3})",
    "milestone_strict": r"^MS-\d{3}$",
    "task_strict": r"^T\d{3}$",
}


class InvalidFormatError(Exception):
    """Raised when format is invalid."""

    pass


def validate_format(value: str, pattern: str, entity_name: str, example: str) -> None:
    """Generic format validator."""
    if not re.match(pattern, value):
        raise InvalidFormatError(
            f"Invalid {entity_name} format: '{value}'. Expected: {example}"
        )


def validate_milestone(milestone: str) -> None:
    """Validate milestone format (MS-XXX)."""
    validate_format(
        milestone, PATTERNS["milestone_strict"], "milestone", "MS-XXX (e.g., MS-001)"
    )


def validate_task(task: str) -> None:
    """Validate task format (TXXX)."""
    validate_format(task, PATTERNS["task_strict"], "task", "TXXX (e.g., T001)")
