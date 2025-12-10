import json
import sys
from pathlib import Path

STATUS_FILE = Path(__file__).parent.parent.parent.parent / "project" / "status.json"

VERSION_STRUCTURE: dict[str, list[str]] = {
    "specs": [
        "business-plan.md",
        "tech-specs.md",
        "ux.md",
        "prd.md",
    ],
    "release-plan": [
        "roadmap.md",
        "release-plan.md",
    ],
}


def get_status() -> dict:
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text())
    return {}


def get_next_milestone_number() -> int:
    status = get_status()
    return status.get("total_milestones", 0) + 1


def init_dir(dir_path: str) -> Path:
    path = Path(dir_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    return path


def init_version_dir(base_path: str, version: str = "v0.1.0") -> Path:
    version_path = Path(base_path) / version
    print(version_path)
    for dir_name, files in VERSION_STRUCTURE.items():
        dir_path = version_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)

        for file_name in files:
            file_path = dir_path / file_name
            if not file_path.exists():
                file_path.touch()

    # Create first milestone
    milestone_num = get_next_milestone_number()
    init_milestone_dir(str(version_path), f"MS-{milestone_num:03d}", "Foundation")

    return version_path


def init_milestone_dir(
    version_path: str, milestone_id: str, milestone_name: str
) -> Path:
    milestone_dir = (
        Path(version_path) / "milestones" / f"{milestone_id}_{milestone_name}"
    )

    subdirs = ["reports", "plan", "decisions"]
    files = {
        "": ["status.md", "completion-checklist.md"],
        "plan": ["plan-overview.md", "tasks.md"],
    }

    for subdir in subdirs:
        (milestone_dir / subdir).mkdir(parents=True, exist_ok=True)

    for subdir, file_list in files.items():
        target_dir = milestone_dir / subdir if subdir else milestone_dir
        for file_name in file_list:
            file_path = target_dir / file_name
            if not file_path.exists():
                file_path.touch()

    return milestone_dir


def main():
    project_path = Path("project")
    init_version_dir(project_path, "v0.1.0")


if __name__ == "__main__":
    main()
