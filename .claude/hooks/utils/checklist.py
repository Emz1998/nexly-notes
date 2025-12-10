"""Checklist parsing utilities."""

import re
from dataclasses import dataclass, field
from itertools import takewhile
from pathlib import Path
import sys
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_io import read_file

# from utils.validation import validate_task

PATTERNS = {
    "milestone": r"MS-(\d{3})",
    "completed_task": r"^- \[x\]\s(T\d{3}):.*$",
    "uncompleted_task": r"^- \[ \]\s(T\d{3}):.*$",
    "unchecked_item": r"^- \[ \]",
    "all_tasks": r"^- \[[x ]\]\s(T\d{3}):.*$",
    "task_with_status": r"^- \[(x| )\]\s(T\d{3}):.*$",
    "phase": r"^### Phase (\d+): (.+)$",
    "ms_header": r"#### \*\*MS-{:03d}:\*\*",
}


def _sequential(items: list[Any], pred: Callable, mode: str = "count") -> Any:
    """Get count or last item where predicate is True before first False."""
    taken = list(takewhile(pred, items))
    return len(taken) if mode == "count" else (taken[-1] if taken else None)


class SectionExtractor:
    """Extracts sections from checklist content."""

    def __init__(self, content: str):
        self._content = content

    def get_phase_section(self, phase_num: int) -> str | None:
        """Get content section for a specific phase."""
        phase_matches = list(
            re.finditer(PATTERNS["phase"], self._content, re.MULTILINE)
        )
        for i, match in enumerate(phase_matches):
            if int(match.group(1)) == phase_num:
                start = match.start()
                end = (
                    phase_matches[i + 1].start()
                    if i + 1 < len(phase_matches)
                    else len(self._content)
                )
                return self._content[start:end].strip()
        return None

    def get_milestone_section(self, milestone: str) -> str | None:
        """Get content section for a specific milestone."""
        match = re.search(PATTERNS["milestone"], milestone)
        if not match:
            return None
        ms_num = int(match.group(1))
        header = PATTERNS["ms_header"]
        start = re.search(header.format(ms_num), self._content)
        if not start:
            return None
        end = re.search(header.format(ms_num + 1), self._content)
        return self._content[
            start.start() : end.start() if end else len(self._content)
        ].strip()


class ChecklistValidator:
    """Validates checklist items using regex patterns."""

    @staticmethod
    def is_valid_milestone(milestone: str) -> bool:
        """Check if milestone matches MS-NNN format."""
        return bool(re.fullmatch(r"MS-\d{3}", milestone))

    @staticmethod
    def is_valid_task(task: str) -> bool:
        """Check if task matches TNNN format."""
        return bool(re.fullmatch(r"T\d{3}", task))

    @staticmethod
    def section_has_unchecked(section: str | None) -> bool:
        """Check if section contains unchecked items."""
        if not section:
            return False
        return bool(re.search(PATTERNS["unchecked_item"], section, re.MULTILINE))

    @staticmethod
    def section_has_completed(section: str | None) -> bool:
        """Check if section contains completed tasks."""
        if not section:
            return False
        return bool(re.search(PATTERNS["completed_task"], section, re.MULTILINE))


class ChecklistCounter:
    """Counts completed and total tasks, milestones, and phases."""

    def __init__(self, content: str):
        self._content = content
        self._extractor = SectionExtractor(content)

    @property
    def total_tasks(self) -> int:
        return len(re.findall(PATTERNS["all_tasks"], self._content, re.MULTILINE))

    @property
    def completed_tasks(self) -> int:
        return len(re.findall(PATTERNS["completed_task"], self._content, re.MULTILINE))

    @property
    def remaining_tasks(self) -> int:
        return self.total_tasks - self.completed_tasks

    @property
    def total_milestones(self) -> int:
        return len(set(re.findall(PATTERNS["milestone"], self._content)))

    @property
    def completed_milestones(self) -> int:
        count = 0
        for m in set(re.findall(PATTERNS["milestone"], self._content)):
            section = self._extractor.get_milestone_section(f"MS-{m}")
            if section and not re.search(
                PATTERNS["unchecked_item"], section, re.MULTILINE
            ):
                count += 1
        return count

    @property
    def remaining_milestones(self) -> int:
        return self.total_milestones - self.completed_milestones

    @property
    def total_phases(self) -> int:
        return len(re.findall(PATTERNS["phase"], self._content, re.MULTILINE))

    @property
    def completed_phases(self) -> int:
        count = 0
        for i in range(1, self.total_phases + 1):
            section = self._extractor.get_phase_section(i)
            if section and not re.search(
                PATTERNS["unchecked_item"], section, re.MULTILINE
            ):
                count += 1
            else:
                break
        return count

    @property
    def remaining_phases(self) -> int:
        return self.total_phases - self.completed_phases


class ProjectStatus:
    """Computes project status using SectionExtractor, ChecklistValidator, and ChecklistCounter."""

    def __init__(self, content: str):
        self._content = content
        self._extractor = SectionExtractor(content)
        self._validator = ChecklistValidator()
        self._counter = ChecklistCounter(content)
        self._version: str = ""
        self._project_name: str = ""

    # Project info (manual setters)
    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        self._version = value

    @property
    def project_name(self) -> str:
        return self._project_name

    @project_name.setter
    def project_name(self, value: str) -> None:
        self._project_name = value

    @property
    def project_status(self) -> str:
        if self._counter.completed_tasks == self._counter.total_tasks:
            return "completed"
        if self._counter.completed_tasks > 0:
            return "in_progress"
        return "not_started"

    # Phase (computed from counter)
    @property
    def total_phases(self) -> int:
        return self._counter.total_phases

    @property
    def phases_completed(self) -> int:
        return self._counter.completed_phases

    @property
    def phases_remaining(self) -> int:
        return self._counter.remaining_phases

    @property
    def current_phase_num(self) -> int:
        return self._counter.completed_phases + 1

    @property
    def current_phase(self) -> str:
        matches = re.findall(PATTERNS["phase"], self._content, re.MULTILINE)
        for num, name in matches:
            if int(num) == self.current_phase_num:
                return name.strip()
        return f"Phase {self.current_phase_num}"

    def current_phase_status(self, phase_num: int = 1) -> str:
        section = self._extractor.get_phase_section(phase_num)
        if not section:
            return "not_started"
        if not self._validator.section_has_unchecked(section):
            return "completed"
        if self._validator.section_has_completed(section):
            return "in_progress"
        return "not_started"

    # Milestone (computed from counter)
    @property
    def total_milestones(self) -> int:
        return self._counter.total_milestones

    @property
    def milestones_completed(self) -> int:
        return self._counter.completed_milestones

    @property
    def milestones_remaining(self) -> int:
        return self._counter.remaining_milestones

    @property
    def current_milestone(self) -> str:
        milestones = sorted(set(re.findall(PATTERNS["milestone"], self._content)))
        for m in milestones:
            ms = f"MS-{m}"
            section = self._extractor.get_milestone_section(ms)
            if section and self._validator.section_has_unchecked(section):
                return ms
        return f"MS-{milestones[-1]}" if milestones else "MS-001"

    @property
    def current_milestone_status(self) -> str:
        section = self._extractor.get_milestone_section(self.current_milestone)
        if not section:
            return "not_started"
        if not self._validator.section_has_unchecked(section):
            return "completed"
        if self._validator.section_has_completed(section):
            return "in_progress"
        return "not_started"

    # Task (computed from counter)
    @property
    def total_tasks(self) -> int:
        return self._counter.total_tasks

    @property
    def tasks_completed(self) -> int:
        return self._counter.completed_tasks

    @property
    def tasks_remaining(self) -> int:
        return self._counter.remaining_tasks

    @property
    def current_task(self) -> str:
        uncompleted = re.findall(
            PATTERNS["uncompleted_task"], self._content, re.MULTILINE
        )
        return uncompleted[0] if uncompleted else ""

    @property
    def current_task_status(self) -> str:
        if not self.current_task:
            return "completed"
        return "not_started"
