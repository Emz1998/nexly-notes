from utils import get_cache, load_cache, write_cache
from typing import Literal

ALL_PHASES = [
    "explore",
    "research",
    "research:consult",
    "plan",
    "plan:consult",
    "code",
    "tdd:failing-tests",
    "tdd:passing-tests",
    "tdd:refactor",
    "review:code",
    "commit",
]

ALL_SUBAGENTS = [
    "codebase-explorer",
    "research-specialist",
    "research-consultant",
    "strategic-planner",
    "plan-consultant",
    "test-engineer",
    "code-reviewer",
    "version-manager",
]


def track_phases(phase: str = ""):
    cache = load_cache()
    if phase not in cache["phases_completed"]:
        cache["phases_completed"].append(phase)
    write_cache(cache)


def track_subagents(subagent: str = ""):
    cache = load_cache()
    if subagent not in cache["subagents_triggered"]:
        cache["subagents_triggered"].append(subagent)
    write_cache(cache)


def validate_required_invocations(
    invocation_type: Literal["commands", "subagents"],
    required_invocations: list[str] = ALL_PHASES,
) -> bool:
    current_invocations_list = get_cache(f"{invocation_type}_triggered")
    is_all_requirements_met = all(
        invocation in required_invocations for invocation in current_invocations_list
    )

    if len(current_invocations_list) < len(required_invocations):
        return False

    if not is_all_requirements_met:
        return False

    return True


def validate_all_phases_triggered() -> bool:
    return validate_required_invocations("commands")


def validate_all_subagents_triggered() -> bool:
    return validate_required_invocations("subagents")
