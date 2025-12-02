#!/usr/bin/env python3
"""Code Mode - Validate Subagent Stop (SubagentStop Handler).

Validates that subagents completed their required work before stopping:
1. failing_test: test-engineer must create tests in src/tests that fail
2. troubleshoot: troubleshooter must have addressed issues

After validation passes, advances to the next phase.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import code_mode, log

TDD_PHASES = ["failing_test", "passing_test", "refactor", "troubleshoot", "commit"]
VALIDATABLE_AGENTS = ["test-engineer", "troubleshooter"]
AGENT_PHASE_MAP = {
    "test-engineer": "failing_test",
    "troubleshooter": "troubleshoot",
}
TEST_DIR = Path("src/tests")


def check_tests_exist() -> bool:
    """Check if test files exist in src/tests directory."""
    if not TEST_DIR.exists():
        return False
    test_files = list(TEST_DIR.glob("**/*.test.*")) + list(TEST_DIR.glob("**/*.spec.*"))
    return len(test_files) > 0


def run_tests() -> tuple[bool, str]:
    """Run tests and check if they fail (for failing_test phase)."""
    try:
        result = subprocess.run(
            ["npm", "test"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=Path.cwd()
        )
        return result.returncode != 0, result.stderr or result.stdout
    except subprocess.TimeoutExpired:
        return False, "Test execution timed out"
    except FileNotFoundError:
        return False, "npm not found"
    except Exception as e:
        return False, str(e)


def advance_phase(current_phase: str) -> str:
    """Advance to the next TDD phase and return it."""
    try:
        current_idx = TDD_PHASES.index(current_phase)
        if current_idx < len(TDD_PHASES) - 1:
            next_phase = TDD_PHASES[current_idx + 1]
            code_mode.set("current_phase", next_phase)
            return next_phase
    except ValueError:
        pass
    return current_phase


def validate_subagent_stop(input_data: dict) -> None:
    """Validate subagent completed required work before stopping."""
    if not code_mode.is_active():
        return

    current_phase = code_mode.get("current_phase") or "failing_test"

    # Determine which agent is stopping based on current phase
    agent_type = None
    for agent, phase in AGENT_PHASE_MAP.items():
        if phase == current_phase:
            agent_type = agent
            break

    if not agent_type:
        return

    if agent_type == "test-engineer":
        if not check_tests_exist():
            log("test-engineer stop blocked: No test files found in src/tests")
            print(
                "Test files not created. Write tests in src/tests directory.\n"
                "Expected files: *.test.* or *.spec.* in src/tests/",
                file=sys.stderr
            )
            sys.exit(2)

        tests_fail, output = run_tests()
        if not tests_fail:
            log("test-engineer stop blocked: Tests are not failing")
            print(
                "Tests are not failing (Red phase requires failing tests).\n"
                "Write tests that fail before implementation exists.\n"
                f"Test output: {output[:500]}",
                file=sys.stderr
            )
            sys.exit(2)

        next_phase = advance_phase(current_phase)
        log(f"test-engineer completed. Advanced to: {next_phase}")
        print(f"Failing tests created. Advancing to phase: {next_phase}")
        return

    elif agent_type == "troubleshooter":
        next_phase = advance_phase(current_phase)
        log(f"troubleshooter completed. Advanced to: {next_phase}")
        print(f"Troubleshooting complete. Advancing to phase: {next_phase}")
        return


if __name__ == "__main__":
    import json
    input_data = json.load(sys.stdin)
    validate_subagent_stop(input_data)
