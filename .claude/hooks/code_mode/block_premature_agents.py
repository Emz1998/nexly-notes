#!/usr/bin/env python3
"""Code Mode - Block Premature Agents (PreToolUse Handler).

Enforces TDD workflow phase sequence:
1. failing_test: Requires test-engineer subagent
2. passing_test: Main agent implements code (no Task tool)
3. refactor: Main agent refactors (no Task tool)
4. troubleshoot: Requires troubleshooter subagent
5. commit: No agent required (direct commit)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import code_mode, is_task_call, extract_agent_info, block_agent, log

# TDD phase to required agent mapping
# None means main agent handles it (no Task tool needed)
PHASE_AGENT_MAP = {
    "failing_test": "test-engineer",
    "passing_test": None,
    "refactor": None,
    "troubleshoot": "troubleshooter",
    "commit": None,
}


def block_premature_agents(input_data: dict) -> None:
    """Block Task tool calls that violate TDD phase sequence."""
    if not is_task_call(input_data):
        return

    if not code_mode.is_active():
        return

    current_phase = code_mode.get("current_phase") or "failing_test"
    _, requested_agent = extract_agent_info(input_data)
    required_agent = PHASE_AGENT_MAP.get(current_phase)

    # If phase requires no agent, block all Task calls
    if required_agent is None:
        log(f"TDD Phase '{current_phase}': Main agent handles this phase. No subagent allowed.")
        print(
            f"BLOCKED: Phase '{current_phase}' is handled by the main agent.\n"
            f"Do not delegate to subagents during this phase.",
            file=sys.stderr
        )
        sys.exit(2)

    # If phase requires specific agent, enforce it
    if requested_agent != required_agent:
        log(f"TDD Phase '{current_phase}': Requires '{required_agent}', got '{requested_agent}'")
        print(
            f"BLOCKED: Phase '{current_phase}' requires '{required_agent}' subagent.\n"
            f"Requested: '{requested_agent}'.\n"
            f"Complete current phase with the correct subagent.",
            file=sys.stderr
        )
        sys.exit(2)

    # Allow the correct agent (implicit return)


if __name__ == "__main__":
    import json
    input_data = json.load(sys.stdin)
    block_premature_agents(input_data)
