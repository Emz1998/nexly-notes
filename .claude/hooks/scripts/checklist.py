import re
from pathlib import Path
from typing import Callable
import sys
import json

sys.path.insert(0, str(Path(__file__).parent.parent))


DEFAULT_CHECKLIST_FILE = "specs/tasks.md"
DEFAULT_SUCCESS_CRITERIA_FILE = "specs/success-criteria.md"


def extract_milestone_section(
    milestone: str, file_path: str = DEFAULT_CHECKLIST_FILE
) -> str | None:
    # Extract the full section content for a given milestone.
    match = re.search(r"MS-(\d{3})", milestone)
    if match is None:
        return None

    current_milestone_number = int(match.group(1))
    next_milestone_number = current_milestone_number + 1

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    current_pattern = rf"MS-{current_milestone_number:03d}"
    next_pattern = rf"MS-{next_milestone_number:03d}"

    # Find the start of current milestone section
    current_match = re.search(rf"#### \*\*{current_pattern}:\*\*", content)
    if current_match is None:
        return None

    start_idx = current_match.start()

    # Find the start of next milestone section (or use end of file)
    next_match = re.search(rf"#### \*\*{next_pattern}:\*\*", content)
    end_idx = next_match.start() if next_match else len(content)
    return content[start_idx:end_idx].strip()


def is_checklist_completed(content: str) -> bool:
    # Returns True if there are NO unchecked tasks
    unchecked_regex = r"^- \[ \]"
    return re.search(unchecked_regex, content, re.MULTILINE) is None


def are_tasks_checked_off(
    milestone: str,
    extractor: Callable[[str], str | None] = extract_milestone_section,
) -> bool:
    content = extractor(milestone)
    return is_checklist_completed(content) if content else False


def are_success_criteria_checked_off(
    file_path: str = DEFAULT_SUCCESS_CRITERIA_FILE,
) -> bool:
    content = Path(file_path).read_text(encoding="utf-8")
    return is_checklist_completed(content) if content else False


def validate_checklist():
    if not are_tasks_checked_off("MS-001") or not are_success_criteria_checked_off():
        reason = {
            "decision": "block",
            "reason": "Tasks and success criteria are not completed.",
        }
        print(json.dumps(reason), file=sys.stderr)
        sys.exit(2)

    print(json.dumps({"continue": True}))
    print("Tasks and success criteria are completed.")
    sys.exit(0)


if __name__ == "__main__":
    validate_checklist()
