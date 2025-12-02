"""Unit tests for hooks utility modules."""

import pytest
import sys
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(HOOKS_DIR))


class TestCache:
    """Tests for utils/cache.py"""

    def test_set_and_get_cache(self, mock_cache):
        from utils import set_cache, get_cache

        set_cache("test_ns", "key1", "value1")
        assert get_cache("test_ns", "key1") == "value1"

    def test_get_nonexistent_returns_none(self, mock_cache):
        from utils import get_cache

        assert get_cache("nonexistent", "key") is None

    def test_namespace_isolation(self, mock_cache):
        from utils import set_cache, get_cache

        set_cache("ns1", "key", "value1")
        set_cache("ns2", "key", "value2")

        assert get_cache("ns1", "key") == "value1"
        assert get_cache("ns2", "key") == "value2"


class TestBaseMode:
    """Tests for utils/base_mode.py"""

    def test_mode_manager_activate(self, mock_cache):
        from utils import ModeManager

        mode = ModeManager("test")
        mode.activate("session-123", "Test message")

        assert mode.is_active() is True
        assert mode.get_session_id() == "session-123"

    def test_mode_manager_deactivate(self, mock_cache):
        from utils import ModeManager

        mode = ModeManager("test")
        mode.activate("session-123")
        mode.deactivate()

        assert mode.is_active() is False
        assert mode.get_session_id() == ""

    def test_mode_manager_extra_keys(self, mock_cache):
        from utils import ModeManager

        mode = ModeManager("test", ["extra1", "extra2"])
        mode.activate("session-123", extra1="val1", extra2="val2")

        assert mode.get("extra1") == "val1"
        assert mode.get("extra2") == "val2"

    def test_pre_instantiated_modes(self, mock_cache):
        from utils import plan_mode, research_mode, code_mode

        assert plan_mode.namespace == "plan_mode"
        assert research_mode.namespace == "research_mode"
        assert code_mode.namespace == "code_mode"


class TestAgentValidation:
    """Tests for utils/agent_validation.py"""

    def test_extract_agent_info(self, sample_task_input):
        from utils import extract_agent_info

        data = sample_task_input("test-engineer")
        tool_name, subagent = extract_agent_info(data)

        assert tool_name == "Task"
        assert subagent == "test-engineer"

    def test_is_task_call_true(self, sample_task_input):
        from utils import is_task_call

        data = sample_task_input("test-engineer")
        assert is_task_call(data) is True

    def test_is_task_call_false(self, sample_bash_input):
        from utils import is_task_call

        data = sample_bash_input("ls -la")
        assert is_task_call(data) is False

    def test_get_subagent_type_pretooluse(self, sample_task_input):
        from utils import get_subagent_type

        data = sample_task_input("test-engineer")
        assert get_subagent_type(data) == "test-engineer"

    def test_get_subagent_type_subagent_stop(self, sample_subagent_stop_input):
        from utils import get_subagent_type

        data = sample_subagent_stop_input("test-engineer")
        assert get_subagent_type(data) == "test-engineer"


class TestPrerequisites:
    """Tests for utils/prerequisites.py"""

    def test_is_tdd_commit_complete_false(self, mock_cache):
        from utils import is_tdd_commit_complete, set_cache

        set_cache("code_mode", "current_phase", "failing_test")
        assert is_tdd_commit_complete() is False

    def test_is_tdd_commit_complete_true(self, mock_cache):
        from utils import is_tdd_commit_complete, set_cache

        set_cache("code_mode", "current_phase", "commit")
        assert is_tdd_commit_complete() is True


class TestFrontmatter:
    """Tests for utils/frontmatter.py"""

    def test_parse_frontmatter_with_content(self):
        from utils import parse_frontmatter

        content = """---
title: Test
consulted_by: consulting-expert
---

Body content here.
"""
        result = parse_frontmatter(content)
        assert result["title"] == "Test"
        assert result["consulted_by"] == "consulting-expert"

    def test_parse_frontmatter_no_frontmatter(self):
        from utils import parse_frontmatter

        content = "Just plain content without frontmatter."
        result = parse_frontmatter(content)
        assert result == {}

    def test_has_consultation_marker(self, tmp_path):
        from utils import has_consultation_marker

        file_path = tmp_path / "test.md"
        file_path.write_text("""---
consulted_by: consulting-expert
---
Content
""")
        assert has_consultation_marker(file_path) is True

    def test_has_research_validation_marker(self, tmp_path):
        from utils import has_research_validation_marker

        file_path = tmp_path / "test.md"
        file_path.write_text("""---
validated_by: research-consultant
---
Content
""")
        assert has_research_validation_marker(file_path) is True
