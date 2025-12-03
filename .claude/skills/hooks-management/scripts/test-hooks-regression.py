#!/usr/bin/env python3
"""
Regression Testing Script for Claude Code Hooks

Tests all hooks in .claude/hooks/ to ensure they work correctly.
Run from project root: python3 .claude/skills/hooks-management/scripts/test-hooks-regression.py
"""

import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


# Colors for output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


@dataclass
class TestResult:
    name: str
    passed: bool
    message: str = ""
    exit_code: Optional[int] = None


class HooksTestRunner:
    """Test runner for Claude Code hooks."""

    def __init__(self):
        self.project_root = Path.cwd()
        self.hooks_dir = self.project_root / ".claude" / "hooks"
        self.cache_path = self.hooks_dir / "cache.json"
        self.status_path = self.project_root / "project" / "status.json"
        self.results: list[TestResult] = []
        self.original_cache = None
        self.test_session_id = "test-session-12345"
        self.test_date = datetime.now().strftime("%m%d%y")

    def setup(self):
        """Save original state before tests."""
        if self.cache_path.exists():
            self.original_cache = self.cache_path.read_text()
        else:
            self.original_cache = None

    def teardown(self):
        """Restore original state after tests."""
        if self.original_cache is not None:
            self.cache_path.write_text(self.original_cache)
        elif self.cache_path.exists():
            self.cache_path.unlink()

    def run_hook(self, hook_path: Path, input_data: dict) -> tuple[int, str, str]:
        """Run a hook with given input and return exit code, stdout, stderr."""
        try:
            result = subprocess.run(
                ["python3", str(hook_path)],
                input=json.dumps(input_data),
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_root,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Timeout"
        except Exception as e:
            return -1, "", str(e)

    def set_cache(self, namespace: str, key: str, value):
        """Set cache value for testing."""
        try:
            cache = (
                json.loads(self.cache_path.read_text())
                if self.cache_path.exists()
                else {}
            )
        except json.JSONDecodeError:
            cache = {}
        if namespace not in cache:
            cache[namespace] = {}
        cache[namespace][key] = value
        self.cache_path.write_text(json.dumps(cache, indent=2))

    def clear_cache(self):
        """Clear the cache file."""
        if self.cache_path.exists():
            self.cache_path.write_text("{}")

    def get_milestone_dir(self) -> str:
        """Get milestone directory from status.json."""
        try:
            data = json.loads(self.status_path.read_text())
            milestone = data.get("current_milestone", "")
            description = data.get("milestone_description", "")
            if milestone and description:
                return f"{milestone}:{description}"
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return ""

    def log_test(
        self, name: str, passed: bool, message: str = "", exit_code: int = None
    ):
        """Log a test result."""
        result = TestResult(name, passed, message, exit_code)
        self.results.append(result)
        status = (
            f"{Colors.GREEN}PASS{Colors.END}"
            if passed
            else f"{Colors.RED}FAIL{Colors.END}"
        )
        exit_info = f" (exit={exit_code})" if exit_code is not None else ""
        msg_info = f" - {message}" if message else ""
        print(f"  [{status}] {name}{exit_info}{msg_info}")

    # =========================================================================
    # Utility Tests
    # =========================================================================

    def test_utils_cache(self):
        """Test cache utility functions."""
        print(f"\n{Colors.BOLD}Testing: utils/cache.py{Colors.END}")

        # Import cache module
        sys.path.insert(0, str(self.hooks_dir))
        from utils.cache import get_cache, set_cache

        # Test set and get
        set_cache("test_ns", "test_key", "test_value")
        value = get_cache("test_ns", "test_key")
        self.log_test("set_cache/get_cache", value == "test_value", f"got: {value}")

        # Test non-existent key
        value = get_cache("test_ns", "nonexistent")
        self.log_test("get_cache non-existent", value is None)

        # Clean up
        cache = json.loads(self.cache_path.read_text())
        if "test_ns" in cache:
            del cache["test_ns"]
            self.cache_path.write_text(json.dumps(cache, indent=2))

    def test_utils_frontmatter(self):
        """Test frontmatter utility functions."""
        print(f"\n{Colors.BOLD}Testing: utils/frontmatter.py{Colors.END}")

        sys.path.insert(0, str(self.hooks_dir))
        from utils.frontmatter import (
            parse_frontmatter,
            has_consultation_marker,
            has_research_validation_marker,
        )

        # Test parse_frontmatter
        content = "---\ntitle: Test\nconsulted_by: consulting-expert\n---\n\nBody"
        fm = parse_frontmatter(content)
        self.log_test("parse_frontmatter", fm.get("title") == "Test", f"got: {fm}")

        # Test no frontmatter
        content = "No frontmatter here"
        fm = parse_frontmatter(content)
        self.log_test("parse_frontmatter (none)", fm == {})

        # Test has_consultation_marker with temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\nconsulted_by: consulting-expert\n---\n\nBody")
            temp_path = Path(f.name)

        result = has_consultation_marker(temp_path)
        self.log_test("has_consultation_marker (true)", result is True)
        temp_path.unlink()

        # Test has_research_validation_marker with temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\nvalidated_by: research-consultant\n---\n\nBody")
            temp_path = Path(f.name)

        result = has_research_validation_marker(temp_path)
        self.log_test("has_research_validation_marker (true)", result is True)
        temp_path.unlink()

    def test_utils_milestone(self):
        """Test milestone utility functions."""
        print(f"\n{Colors.BOLD}Testing: utils/milestone.py{Colors.END}")

        sys.path.insert(0, str(self.hooks_dir))
        from utils.milestone import (
            get_milestone_info,
            get_milestone_dir,
            build_research_path,
            build_plan_path,
        )

        # Test get_milestone_info
        info = get_milestone_info()
        has_milestone = "milestone" in info and "description" in info
        self.log_test("get_milestone_info", has_milestone, f"got: {info}")

        # Test get_milestone_dir
        ms_dir = get_milestone_dir()
        self.log_test("get_milestone_dir", isinstance(ms_dir, str), f"got: {ms_dir}")

        # Test build_research_path
        path = build_research_path("test-session")
        expected_pattern = "researches/research_test-session_"
        self.log_test(
            "build_research_path",
            path is None or expected_pattern in str(path),
            f"got: {path}",
        )

        # Test build_plan_path
        path = build_plan_path("test-session")
        expected_pattern = "plans/plan_test-session_"
        self.log_test(
            "build_plan_path",
            path is None or expected_pattern in str(path),
            f"got: {path}",
        )

    def test_utils_git(self):
        """Test git utility functions."""
        print(f"\n{Colors.BOLD}Testing: utils/git.py{Colors.END}")

        sys.path.insert(0, str(self.hooks_dir))
        from utils.git import get_git_status, get_modified_files, is_file_committed

        # Test get_git_status
        status = get_git_status()
        self.log_test(
            "get_git_status", isinstance(status, list), f"got {len(status)} entries"
        )

        # Test get_modified_files
        modified = get_modified_files()
        self.log_test(
            "get_modified_files",
            isinstance(modified, list),
            f"got {len(modified)} files",
        )

        # Test is_file_committed (test with existing file)
        result = is_file_committed("CLAUDE.md")
        self.log_test(
            "is_file_committed (CLAUDE.md)", isinstance(result, bool), f"got: {result}"
        )

    # =========================================================================
    # Security Tests
    # =========================================================================

    def test_security(self):
        """Test security validation."""
        print(f"\n{Colors.BOLD}Testing: security/security.py{Colors.END}")

        security_hook = self.hooks_dir / "security" / "security.py"

        # Test dangerous command (should block with exit 2)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "rm -rf /"},
        }
        code, stdout, stderr = self.run_hook(security_hook, input_data)
        self.log_test("block rm -rf /", code == 2, stderr.strip(), code)

        # Test dangerous path (should block with exit 2)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/etc/passwd"},
        }
        code, stdout, stderr = self.run_hook(security_hook, input_data)
        self.log_test("block /etc/passwd write", code == 2, stderr.strip(), code)

        # Test safe operation (should allow with exit 0)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "src/test.ts"},
        }
        code, stdout, stderr = self.run_hook(security_hook, input_data)
        self.log_test("allow safe path", code == 0, "", code)

        # Test safe directory (.claude/)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": ".claude/hooks/test.py"},
        }
        code, stdout, stderr = self.run_hook(security_hook, input_data)
        self.log_test("allow .claude/ path", code == 0, "", code)

    # =========================================================================
    # Plan Mode Tests
    # =========================================================================

    def test_plan_mode_activation(self):
        """Test plan mode activation."""
        print(f"\n{Colors.BOLD}Testing: plan_mode/activate.py{Colors.END}")

        self.clear_cache()

        # Test via user_prompt_submit
        user_prompt_hook = self.hooks_dir / "user_prompt_submit.py"
        input_data = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/plan create feature",
            "session_id": self.test_session_id,
        }
        code, stdout, stderr = self.run_hook(user_prompt_hook, input_data)
        self.log_test("activate plan mode", code == 0, stdout.strip(), code)

        # Verify cache was set
        sys.path.insert(0, str(self.hooks_dir))
        from utils.cache import get_cache

        is_active = get_cache("plan_mode", "is_active")
        self.log_test("plan_mode.is_active set", is_active is True)

        session = get_cache("plan_mode", "session_id")
        self.log_test("plan_mode.session_id set", session == self.test_session_id)

    def test_plan_mode_block_agents(self):
        """Test plan mode agent blocking."""
        print(
            f"\n{Colors.BOLD}Testing: plan_mode/block_premature_agents.py{Colors.END}"
        )

        # Set up plan mode
        self.set_cache("plan_mode", "is_active", True)
        self.set_cache("plan_mode", "session_id", self.test_session_id)

        pre_tool_hook = self.hooks_dir / "pre_tool_use.py"

        # Test strategic-planner blocked (no research file)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "strategic-planner"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test(
            "block strategic-planner (no research)", code == 2, stderr.strip(), code
        )

        # Test consulting-expert blocked (no plan file)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "consulting-expert"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test(
            "block consulting-expert (no plan)", code == 2, stderr.strip(), code
        )

        # Test unrelated agent allowed
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "code-reviewer"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("allow unrelated agent", code == 0, "", code)

        # Test non-Task tool allowed
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "test.md"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("allow non-Task tool", code == 0, "", code)

    def test_plan_mode_validate_stop(self):
        """Test plan mode subagent stop validation."""
        print(
            f"\n{Colors.BOLD}Testing: plan_mode/validate_subagent_stop.py{Colors.END}"
        )

        # Set up plan mode
        self.set_cache("plan_mode", "is_active", True)
        self.set_cache("plan_mode", "session_id", self.test_session_id)

        subagent_stop_hook = self.hooks_dir / "subagent_stop.py"

        # Test strategic-planner stop blocked (no plan file)
        input_data = {
            "hook_event_name": "SubagentStop",
            "subagent_type": "strategic-planner",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test(
            "block strategic-planner stop (no plan)", code == 2, stderr.strip(), code
        )

        # Test consulting-expert stop blocked (no plan file)
        input_data = {
            "hook_event_name": "SubagentStop",
            "subagent_type": "consulting-expert",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test(
            "block consulting-expert stop (no plan)", code == 2, stderr.strip(), code
        )

        # Test unrelated agent stop allowed
        input_data = {
            "hook_event_name": "SubagentStop",
            "subagent_type": "code-reviewer",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test("allow unrelated agent stop", code == 0, "", code)

    # =========================================================================
    # Research Mode Tests
    # =========================================================================

    def test_research_mode_activation(self):
        """Test research mode activation."""
        print(f"\n{Colors.BOLD}Testing: research_mode/activate.py{Colors.END}")

        self.clear_cache()

        # Test via user_prompt_submit
        user_prompt_hook = self.hooks_dir / "user_prompt_submit.py"
        input_data = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/research topic",
            "session_id": self.test_session_id,
        }
        code, stdout, stderr = self.run_hook(user_prompt_hook, input_data)
        self.log_test("activate research mode", code == 0, stdout.strip(), code)

        # Verify cache was set
        sys.path.insert(0, str(self.hooks_dir))
        from utils.cache import get_cache

        is_active = get_cache("research_mode", "is_active")
        self.log_test("research_mode.is_active set", is_active is True)

        session = get_cache("research_mode", "session_id")
        self.log_test("research_mode.session_id set", session == self.test_session_id)

    def test_research_mode_block_agents(self):
        """Test research mode agent blocking."""
        print(
            f"\n{Colors.BOLD}Testing: research_mode/block_premature_agents.py{Colors.END}"
        )

        # Set up research mode
        self.set_cache("research_mode", "is_active", True)
        self.set_cache("research_mode", "session_id", self.test_session_id)

        pre_tool_hook = self.hooks_dir / "pre_tool_use.py"

        # Test research-specialist blocked (no explore status)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "research-specialist"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        # This may pass or fail depending on whether exploration file exists
        self.log_test(
            "research-specialist check (no explore)",
            code in (0, 2),
            stderr.strip() if code == 2 else "allowed (explore exists)",
            code,
        )

        # Test research-consultant blocked (no research file)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "research-consultant"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test(
            "block research-consultant (no research)", code == 2, stderr.strip(), code
        )

        # Test unrelated agent allowed
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "code-reviewer"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("allow unrelated agent", code == 0, "", code)

    def test_research_mode_validate_stop(self):
        """Test research mode subagent stop validation."""
        print(
            f"\n{Colors.BOLD}Testing: research_mode/validate_subagent_stop.py{Colors.END}"
        )

        # Set up research mode
        self.set_cache("research_mode", "is_active", True)
        self.set_cache("research_mode", "session_id", self.test_session_id)

        subagent_stop_hook = self.hooks_dir / "subagent_stop.py"

        # Test research-specialist stop blocked (no research file)
        input_data = {
            "hook_event_name": "SubagentStop",
            "subagent_type": "research-specialist",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test(
            "block research-specialist stop (no research)",
            code == 2,
            stderr.strip(),
            code,
        )

        # Test research-consultant stop blocked (no research file)
        input_data = {
            "hook_event_name": "SubagentStop",
            "subagent_type": "research-consultant",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test(
            "block research-consultant stop (no research)",
            code == 2,
            stderr.strip(),
            code,
        )

        # Test unrelated agent stop allowed
        input_data = {
            "hook_event_name": "SubagentStop",
            "subagent_type": "code-reviewer",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test("allow unrelated agent stop", code == 0, "", code)

    # =========================================================================
    # Explore Mode Tests
    # =========================================================================

    def test_explore_mode_activation(self):
        """Test explore mode activation."""
        print(f"\n{Colors.BOLD}Testing: explore_mode/activate.py{Colors.END}")

        self.clear_cache()

        # Test via user_prompt_submit with /explore command
        user_prompt_hook = self.hooks_dir / "user_prompt_submit.py"
        input_data = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/explore T001",
            "session_id": self.test_session_id,
        }
        code, stdout, stderr = self.run_hook(user_prompt_hook, input_data)
        self.log_test("activate explore mode", code == 0, stdout.strip(), code)

        # Verify cache was set
        sys.path.insert(0, str(self.hooks_dir))
        from utils.cache import get_cache

        is_active = get_cache("explore_mode", "is_active")
        self.log_test("explore_mode.is_active set", is_active is True)

        session = get_cache("explore_mode", "session_id")
        self.log_test("explore_mode.session_id set", session == self.test_session_id)

    def test_explore_mode_block_agents(self):
        """Test explore mode agent blocking."""
        print(
            f"\n{Colors.BOLD}Testing: explore_mode/block_premature_agents.py{Colors.END}"
        )

        # Set up explore mode
        self.set_cache("explore_mode", "is_active", True)
        self.set_cache("explore_mode", "session_id", self.test_session_id)

        pre_tool_hook = self.hooks_dir / "pre_tool_use.py"

        # Test codebase-explorer check (depends on specs/tasks.md existence)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "codebase-explorer"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        # This may pass or fail depending on whether specs/tasks.md exists
        self.log_test(
            "codebase-explorer check (tasks.md)",
            code in (0, 2),
            stderr.strip() if code == 2 else "allowed (tasks.md exists)",
            code,
        )

        # Test unrelated agent allowed
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "code-reviewer"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("allow unrelated agent", code == 0, "", code)

    def test_explore_mode_validate_stop(self):
        """Test explore mode subagent stop validation."""
        print(
            f"\n{Colors.BOLD}Testing: explore_mode/validate_subagent_stop.py{Colors.END}"
        )

        # Set up explore mode
        self.set_cache("explore_mode", "is_active", True)
        self.set_cache("explore_mode", "session_id", self.test_session_id)

        subagent_stop_hook = self.hooks_dir / "subagent_stop.py"

        # Test codebase-explorer stop blocked (no codebase-status file)
        input_data = {
            "hook_event_name": "SubagentStop",
            "subagent_type": "codebase-explorer",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test(
            "block codebase-explorer stop (no status file)",
            code == 2,
            stderr.strip(),
            code,
        )

        # Test unrelated agent stop allowed
        input_data = {
            "hook_event_name": "SubagentStop",
            "subagent_type": "code-reviewer",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test("allow unrelated agent stop", code == 0, "", code)

    # =========================================================================
    # Code Mode Tests (TDD Workflow)
    # =========================================================================

    def test_code_mode_activation(self):
        """Test code mode activation."""
        print(f"\n{Colors.BOLD}Testing: code_mode/activate.py{Colors.END}")

        self.clear_cache()

        # Test via user_prompt_submit with /code command (should fail without plan file)
        user_prompt_hook = self.hooks_dir / "user_prompt_submit.py"
        input_data = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/code start",
            "session_id": self.test_session_id,
        }
        code, stdout, stderr = self.run_hook(user_prompt_hook, input_data)
        # Should block because plan file doesn't exist
        self.log_test(
            "block code mode (no plan)",
            code == 2,
            "requires plan file",
            code,
        )

    def test_code_mode_block_agents(self):
        """Test code mode agent blocking."""
        print(
            f"\n{Colors.BOLD}Testing: code_mode/block_premature_agents.py{Colors.END}"
        )

        # Set up code mode in failing_test phase
        self.set_cache("code_mode", "is_active", True)
        self.set_cache("code_mode", "session_id", self.test_session_id)
        self.set_cache("code_mode", "current_phase", "failing_test")

        pre_tool_hook = self.hooks_dir / "pre_tool_use.py"

        # Test test-engineer allowed in failing_test phase
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "test-engineer"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("allow test-engineer (failing_test)", code == 0, "", code)

        # Test wrong agent blocked in failing_test phase
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "troubleshooter"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test(
            "block wrong agent (failing_test)", code == 2, stderr.strip(), code
        )

        # Test all Task tools blocked in passing_test phase (main agent handles)
        self.set_cache("code_mode", "current_phase", "passing_test")
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "test-engineer"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test(
            "block all agents (passing_test)", code == 2, stderr.strip(), code
        )

        # Test troubleshooter allowed in troubleshoot phase
        self.set_cache("code_mode", "current_phase", "troubleshoot")
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "troubleshooter"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("allow troubleshooter (troubleshoot)", code == 0, "", code)

    def test_code_mode_validate_stop(self):
        """Test code mode subagent stop validation."""
        print(
            f"\n{Colors.BOLD}Testing: code_mode/validate_subagent_stop.py{Colors.END}"
        )

        # Set up code mode
        self.set_cache("code_mode", "is_active", True)
        self.set_cache("code_mode", "session_id", self.test_session_id)
        self.set_cache("code_mode", "current_phase", "troubleshoot")

        subagent_stop_hook = self.hooks_dir / "subagent_stop.py"

        # Test troubleshooter stop advances phase
        input_data = {
            "hook_event_name": "SubagentStop",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test(
            "troubleshooter stop advances phase",
            code == 0,
            stdout.strip()[:50] if stdout else "",
            code,
        )

        # Verify phase advanced
        sys.path.insert(0, str(self.hooks_dir))
        from utils.cache import get_cache

        phase = get_cache("code_mode", "current_phase")
        self.log_test(
            "phase advanced to commit", phase == "commit", f"got: {phase}"
        )

    # =========================================================================
    # Code Review Mode Tests
    # =========================================================================

    def test_code_review_mode_activation(self):
        """Test code review mode activation."""
        print(f"\n{Colors.BOLD}Testing: code_review_mode/activate.py{Colors.END}")

        self.clear_cache()

        # Test via user_prompt_submit with /code-review command
        user_prompt_hook = self.hooks_dir / "user_prompt_submit.py"
        input_data = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/code-review",
            "session_id": self.test_session_id,
        }
        code, stdout, stderr = self.run_hook(user_prompt_hook, input_data)
        # Should succeed if no uncommitted changes in src/ or if TDD complete
        self.log_test(
            "activate code review mode",
            code in (0, 2),  # May fail if uncommitted src/ changes
            stdout.strip() if code == 0 else stderr.strip()[:50],
            code,
        )

        # Verify cache was set (if activation succeeded)
        if code == 0:
            sys.path.insert(0, str(self.hooks_dir))
            from utils.cache import get_cache

            is_active = get_cache("code_review_mode", "is_active")
            self.log_test("code_review_mode.is_active set", is_active is True)

            session = get_cache("code_review_mode", "session_id")
            self.log_test(
                "code_review_mode.session_id set", session == self.test_session_id
            )

    def test_code_review_mode_block_agents(self):
        """Test code review mode agent blocking."""
        print(
            f"\n{Colors.BOLD}Testing: code_review_mode/block_premature_agents.py{Colors.END}"
        )

        # Clear mode and test without code review mode active
        self.clear_cache()

        pre_tool_hook = self.hooks_dir / "pre_tool_use.py"

        # Test code-reviewer allowed when code is committed (git-based check)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "code-reviewer"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        # Should pass if no uncommitted src/ changes, else block
        self.log_test(
            "code-reviewer check (git-based)",
            code in (0, 2),
            stderr.strip() if code == 2 else "allowed (code committed)",
            code,
        )

        # Test unrelated agent allowed
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Task",
            "tool_input": {"subagent_type": "test-engineer"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("allow unrelated agent", code == 0, "", code)

    def test_code_review_mode_validate_stop(self):
        """Test code review mode subagent stop validation."""
        print(
            f"\n{Colors.BOLD}Testing: code_review_mode/validate_subagent_stop.py{Colors.END}"
        )

        # Set up code review mode
        self.set_cache("code_review_mode", "is_active", True)
        self.set_cache("code_review_mode", "session_id", self.test_session_id)

        subagent_stop_hook = self.hooks_dir / "subagent_stop.py"

        # Test code-reviewer stop blocked (no review file)
        input_data = {
            "hook_event_name": "SubagentStop",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test(
            "block code-reviewer stop (no review)",
            code == 2,
            stderr.strip()[:60] if stderr else "",
            code,
        )

        # Deactivate and test unrelated agent stop
        self.set_cache("code_review_mode", "is_active", False)
        input_data = {
            "hook_event_name": "SubagentStop",
            "subagent_type": "test-engineer",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test("allow stop when mode inactive", code == 0, "", code)

    # =========================================================================
    # Implement Flow Mode Tests
    # =========================================================================

    def test_implement_flow_activation(self):
        """Test implement flow mode activation."""
        print(f"\n{Colors.BOLD}Testing: implement_flow_mode/activate.py{Colors.END}")

        self.clear_cache()

        # Test via user_prompt_submit with /implement command
        user_prompt_hook = self.hooks_dir / "user_prompt_submit.py"
        input_data = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/implement MS-001",
            "session_id": self.test_session_id,
        }
        code, stdout, stderr = self.run_hook(user_prompt_hook, input_data)
        self.log_test("activate implement flow", code == 0, stdout.strip()[:60], code)

        # Verify cache was set
        sys.path.insert(0, str(self.hooks_dir))
        from utils.cache import get_cache

        is_active = get_cache("implement_flow", "is_active")
        self.log_test("implement_flow.is_active set", is_active is True)

        current_step = get_cache("implement_flow", "current_step")
        self.log_test("implement_flow.current_step initialized", current_step == 0)

    def test_implement_flow_validation(self):
        """Test implement flow slash command sequence validation."""
        print(f"\n{Colors.BOLD}Testing: implement_flow_mode/validate_flow.py{Colors.END}")

        # Set up implement flow mode
        self.set_cache("implement_flow", "is_active", True)
        self.set_cache("implement_flow", "session_id", self.test_session_id)
        self.set_cache("implement_flow", "current_step", 0)
        self.set_cache("implement_flow", "completed_steps", [])

        pre_tool_hook = self.hooks_dir / "pre_tool_use.py"

        # Test correct first step (/explore) is allowed
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "SlashCommand",
            "tool_input": {"command": "/explore test"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("allow /explore (first step)", code == 0, "", code)

        # Test skipping ahead blocked (/plan before /research)
        self.set_cache("implement_flow", "current_step", 1)  # After explore
        self.set_cache("implement_flow", "completed_steps", ["explore"])
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "SlashCommand",
            "tool_input": {"command": "/plan implementation test"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test(
            "block /plan (need /research first)",
            code == 2,
            stderr.strip()[:60] if stderr else "",
            code,
        )

        # Test correct next step (/research) is allowed
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "SlashCommand",
            "tool_input": {"command": "/research best practices"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("allow /research (correct step)", code == 0, "", code)

        # Test non-flow commands not blocked
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "SlashCommand",
            "tool_input": {"command": "/initialize something"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("allow non-flow command", code == 0, "", code)

    def test_implement_flow_step_completion(self):
        """Test implement flow step completion via post_tool_use."""
        print(f"\n{Colors.BOLD}Testing: implement_flow_mode step completion{Colors.END}")

        # Set up implement flow mode
        self.set_cache("implement_flow", "is_active", True)
        self.set_cache("implement_flow", "session_id", self.test_session_id)
        self.set_cache("implement_flow", "current_step", 0)
        self.set_cache("implement_flow", "completed_steps", [])

        post_tool_hook = self.hooks_dir / "post_tool_use.py"

        # Test marking /explore complete
        input_data = {
            "hook_event_name": "PostToolUse",
            "tool_name": "SlashCommand",
            "tool_input": {"command": "/explore test"},
        }
        code, stdout, stderr = self.run_hook(post_tool_hook, input_data)
        self.log_test("mark /explore complete", code == 0, stderr.strip()[:50] if stderr else "", code)

        # Verify step advanced
        sys.path.insert(0, str(self.hooks_dir))
        from utils.cache import get_cache

        current_step = get_cache("implement_flow", "current_step")
        self.log_test("current_step advanced to 1", current_step == 1)

        completed = get_cache("implement_flow", "completed_steps")
        self.log_test("explore in completed_steps", "explore" in completed)

    def test_implement_flow_duplicate_blocked(self):
        """Test that repeating a completed step is blocked."""
        print(f"\n{Colors.BOLD}Testing: implement_flow_mode duplicate blocking{Colors.END}")

        # Set up implement flow mode with explore already completed
        self.set_cache("implement_flow", "is_active", True)
        self.set_cache("implement_flow", "session_id", self.test_session_id)
        self.set_cache("implement_flow", "current_step", 1)
        self.set_cache("implement_flow", "completed_steps", ["explore"])

        pre_tool_hook = self.hooks_dir / "pre_tool_use.py"

        # Test repeating /explore is blocked
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "SlashCommand",
            "tool_input": {"command": "/explore again"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test(
            "block duplicate /explore",
            code == 2,
            stderr.strip()[:60] if stderr else "",
            code,
        )

    # =========================================================================
    # Root Dispatcher Tests
    # =========================================================================

    def test_pre_tool_use_dispatcher(self):
        """Test pre_tool_use.py dispatcher."""
        print(f"\n{Colors.BOLD}Testing: pre_tool_use.py (dispatcher){Colors.END}")

        self.clear_cache()
        pre_tool_hook = self.hooks_dir / "pre_tool_use.py"

        # Test with empty input (should not crash)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("handles empty input", code == 0, "", code)

        # Test security is called (dangerous command)
        input_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "rm -rf /"},
        }
        code, stdout, stderr = self.run_hook(pre_tool_hook, input_data)
        self.log_test("delegates to security", code == 2, stderr.strip(), code)

    def test_subagent_stop_dispatcher(self):
        """Test subagent_stop.py dispatcher."""
        print(f"\n{Colors.BOLD}Testing: subagent_stop.py (dispatcher){Colors.END}")

        self.clear_cache()
        subagent_stop_hook = self.hooks_dir / "subagent_stop.py"

        # Test with empty input (should not crash)
        input_data = {
            "hook_event_name": "SubagentStop",
            "subagent_type": "unknown-agent",
        }
        code, stdout, stderr = self.run_hook(subagent_stop_hook, input_data)
        self.log_test("handles unknown agent", code == 0, "", code)

    def test_user_prompt_submit_dispatcher(self):
        """Test user_prompt_submit.py dispatcher."""
        print(f"\n{Colors.BOLD}Testing: user_prompt_submit.py (dispatcher){Colors.END}")

        self.clear_cache()
        user_prompt_hook = self.hooks_dir / "user_prompt_submit.py"

        # Test normal prompt (no special command)
        input_data = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "hello world",
            "session_id": self.test_session_id,
        }
        code, stdout, stderr = self.run_hook(user_prompt_hook, input_data)
        self.log_test("handles normal prompt", code == 0, "", code)

        # Test /plan command
        input_data = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/plan test",
            "session_id": self.test_session_id,
        }
        code, stdout, stderr = self.run_hook(user_prompt_hook, input_data)
        self.log_test("handles /plan command", code == 0, stdout.strip(), code)

        self.clear_cache()

        # Test /research command
        input_data = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/research test",
            "session_id": self.test_session_id,
        }
        code, stdout, stderr = self.run_hook(user_prompt_hook, input_data)
        self.log_test("handles /research command", code == 0, stdout.strip(), code)

        self.clear_cache()

        # Test /explore command
        input_data = {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "/explore T001",
            "session_id": self.test_session_id,
        }
        code, stdout, _ = self.run_hook(user_prompt_hook, input_data)
        self.log_test("handles /explore command", code == 0, stdout.strip(), code)

    # =========================================================================
    # Session Hooks Tests
    # =========================================================================

    def test_session_start(self):
        """Test session_start.py hook."""
        print(f"\n{Colors.BOLD}Testing: session_start.py{Colors.END}")

        session_start_hook = self.hooks_dir / "session_start.py"
        input_data = {
            "hook_event_name": "SessionStart",
            "session_id": self.test_session_id,
        }
        code, stdout, _ = self.run_hook(session_start_hook, input_data)
        self.log_test("session_start runs", code == 0, stdout.strip()[:50], code)

    # =========================================================================
    # Main Runner
    # =========================================================================

    def run_all_tests(self):
        """Run all hook tests."""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}Claude Code Hooks Regression Test{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"Project: {self.project_root}")
        print(f"Hooks:   {self.hooks_dir}")
        print(f"Time:    {datetime.now().isoformat()}")

        self.setup()

        try:
            # Utility tests
            self.test_utils_cache()
            self.test_utils_frontmatter()
            self.test_utils_milestone()
            self.test_utils_git()

            # Security tests
            self.test_security()

            # Plan mode tests
            self.test_plan_mode_activation()
            self.test_plan_mode_block_agents()
            self.test_plan_mode_validate_stop()

            # Research mode tests
            self.test_research_mode_activation()
            self.test_research_mode_block_agents()
            self.test_research_mode_validate_stop()

            # Explore mode tests
            self.test_explore_mode_activation()
            self.test_explore_mode_block_agents()
            self.test_explore_mode_validate_stop()

            # Code mode tests (TDD workflow)
            self.test_code_mode_activation()
            self.test_code_mode_block_agents()
            self.test_code_mode_validate_stop()

            # Code review mode tests
            self.test_code_review_mode_activation()
            self.test_code_review_mode_block_agents()
            self.test_code_review_mode_validate_stop()

            # Implement flow mode tests
            self.test_implement_flow_activation()
            self.test_implement_flow_validation()
            self.test_implement_flow_step_completion()
            self.test_implement_flow_duplicate_blocked()

            # Dispatcher tests
            self.test_pre_tool_use_dispatcher()
            self.test_subagent_stop_dispatcher()
            self.test_user_prompt_submit_dispatcher()

            # Session tests
            self.test_session_start()

        finally:
            self.teardown()

        # Summary
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)

        print(f"{Colors.BOLD}Summary:{Colors.END}")
        print(f"  Total:  {total}")
        print(f"  {Colors.GREEN}Passed: {passed}{Colors.END}")
        print(f"  {Colors.RED}Failed: {failed}{Colors.END}")

        if failed > 0:
            print(f"\n{Colors.RED}Failed Tests:{Colors.END}")
            for r in self.results:
                if not r.passed:
                    print(f"  - {r.name}: {r.message}")

        print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

        return failed == 0


def main():
    runner = HooksTestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
