"""Integration tests for mode modules."""

import pytest
import sys
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(HOOKS_DIR))


class TestPlanMode:
    """Tests for plan_mode module"""

    def test_activate_sets_cache(self, mock_cache):
        from plan_mode import activate_plan_mode
        from utils import plan_mode

        activate_plan_mode({"session_id": "test-123"})

        assert plan_mode.is_active() is True
        assert plan_mode.get_session_id() == "test-123"

    def test_deactivate_clears_cache(self, mock_cache):
        from plan_mode import activate_plan_mode
        from plan_mode.deactivate import deactivate
        from utils import plan_mode

        activate_plan_mode({"session_id": "test-123"})

        # deactivate calls sys.exit, so we catch it
        with pytest.raises(SystemExit) as exc_info:
            deactivate()

        assert exc_info.value.code == 0
        assert plan_mode.is_active() is False


class TestResearchMode:
    """Tests for research_mode module"""

    def test_activate_sets_cache(self, mock_cache):
        from research_mode import activate_research_mode
        from utils import research_mode

        activate_research_mode({"session_id": "test-123"})

        assert research_mode.is_active() is True
        assert research_mode.get_session_id() == "test-123"

    def test_deactivate_clears_cache(self, mock_cache):
        from research_mode import activate_research_mode
        from research_mode.deactivate import deactivate
        from utils import research_mode

        activate_research_mode({"session_id": "test-123"})
        deactivate()

        assert research_mode.is_active() is False


class TestExploreMode:
    """Tests for explore_mode module"""

    def test_activate_sets_cache(self, mock_cache):
        from explore_mode import activate_explore_mode
        from utils import explore_mode

        activate_explore_mode({"session_id": "test-123"})

        assert explore_mode.is_active() is True
        assert explore_mode.get_session_id() == "test-123"

    def test_deactivate_clears_cache(self, mock_cache):
        from explore_mode import activate_explore_mode
        from explore_mode.deactivate import deactivate
        from utils import explore_mode

        activate_explore_mode({"session_id": "test-123"})
        deactivate()

        assert explore_mode.is_active() is False


class TestCodeMode:
    """Tests for code_mode module"""

    def test_activate_requires_plan_file(self, mock_cache):
        from code_mode import activate_code_mode

        # Should fail without plan file
        with pytest.raises(SystemExit) as exc_info:
            activate_code_mode({"session_id": "test-123"})

        assert exc_info.value.code == 2

    def test_phase_constants(self):
        from code_mode.activate import TDD_PHASES

        assert "failing_test" in TDD_PHASES
        assert "passing_test" in TDD_PHASES
        assert "commit" in TDD_PHASES


class TestCodeReviewMode:
    """Tests for code_review_mode module"""

    def test_activate_sets_cache_when_committed(self, mock_cache, monkeypatch):
        from code_review_mode import activate_code_review_mode
        from utils import code_review_mode

        # Mock is_code_committed to return True
        monkeypatch.setattr(
            "code_review_mode.activate.is_code_committed",
            lambda: (True, "")
        )

        with pytest.raises(SystemExit) as exc_info:
            activate_code_review_mode({"session_id": "test-123"})

        assert exc_info.value.code == 0
        assert code_review_mode.is_active() is True

    def test_deactivate_clears_cache(self, mock_cache, monkeypatch):
        from code_review_mode.deactivate import deactivate_code_review_mode
        from utils import code_review_mode, set_cache

        # Set up active state
        set_cache("code_review_mode", "is_active", True)
        set_cache("code_review_mode", "session_id", "test-123")

        with pytest.raises(SystemExit) as exc_info:
            deactivate_code_review_mode()

        assert exc_info.value.code == 0
        assert code_review_mode.is_active() is False
