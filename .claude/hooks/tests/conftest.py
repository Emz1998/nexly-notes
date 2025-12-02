"""Pytest configuration and fixtures for hooks testing."""

import json
import pytest
import sys
from pathlib import Path

# Add hooks directory to path
HOOKS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(HOOKS_DIR))


@pytest.fixture
def mock_cache(tmp_path, monkeypatch):
    """Create isolated cache for testing."""
    cache_file = tmp_path / "cache.json"
    from utils import cache
    monkeypatch.setattr(cache, "CACHE_PATH", cache_file)
    return cache_file


@pytest.fixture
def sample_task_input():
    """Factory for creating Task tool input data."""
    def _create(subagent_type: str, **kwargs):
        return {
            "tool_name": "Task",
            "tool_input": {"subagent_type": subagent_type, **kwargs},
            "session_id": "test-session-123"
        }
    return _create


@pytest.fixture
def sample_bash_input():
    """Factory for creating Bash tool input data."""
    def _create(command: str):
        return {
            "tool_name": "Bash",
            "tool_input": {"command": command}
        }
    return _create


@pytest.fixture
def sample_write_input():
    """Factory for creating Write tool input data."""
    def _create(file_path: str):
        return {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path}
        }
    return _create


@pytest.fixture
def sample_subagent_stop_input():
    """Factory for creating SubagentStop event input data."""
    def _create(subagent_type: str):
        return {
            "subagent_type": subagent_type,
            "session_id": "test-session-123"
        }
    return _create


@pytest.fixture
def reset_cache(mock_cache):
    """Reset cache to empty state."""
    if mock_cache.exists():
        mock_cache.write_text("{}")
    yield
    if mock_cache.exists():
        mock_cache.unlink()
