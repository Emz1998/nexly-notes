"""Tests for security validation hooks."""

import pytest
import sys
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(HOOKS_DIR))


class TestSecurityValidation:
    """Tests for security/security.py"""

    def test_check_dangerous_command_rm_rf_root(self):
        from security.security import check_dangerous_command

        result = check_dangerous_command("rm -rf /")
        assert result is not None
        assert "System-damaging" in result

    def test_check_dangerous_command_rm_rf_etc(self):
        from security.security import check_dangerous_command

        result = check_dangerous_command("rm -rf /etc")
        assert result is not None

    def test_check_dangerous_command_fork_bomb(self):
        from security.security import check_dangerous_command

        result = check_dangerous_command(":(){ :|:& };:")
        assert result is not None

    def test_check_dangerous_command_safe(self):
        from security.security import check_dangerous_command

        result = check_dangerous_command("npm install")
        assert result is None

    def test_check_dangerous_path_etc_passwd(self):
        from security.security import check_dangerous_path

        result = check_dangerous_path("/etc/passwd")
        assert result is not None
        assert "critical system file" in result

    def test_check_dangerous_path_ssh_key(self):
        from security.security import check_dangerous_path

        result = check_dangerous_path("/home/user/.ssh/id_rsa")
        assert result is not None

    def test_is_safe_path_src(self):
        from security.security import is_safe_path

        assert is_safe_path("/project/src/file.ts") is True

    def test_is_safe_path_claude(self):
        from security.security import is_safe_path

        assert is_safe_path("/.claude/hooks/test.py") is True

    def test_check_dangerous_path_safe_src(self):
        from security.security import check_dangerous_path

        result = check_dangerous_path("/project/src/config.ts")
        assert result is None
