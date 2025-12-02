#!/usr/bin/env python3
"""Base class for mode state management.

Provides common functionality for activate/deactivate patterns
used across all mode modules (plan, research, explore, code, code_review).
"""

from typing import Any

from .cache import get_cache, set_cache


class ModeManager:
    """Base class for mode state management.

    Usage:
        plan_mode = ModeManager("plan")
        plan_mode.activate("session-123", "Planning Phase started")
        if plan_mode.is_active():
            session_id = plan_mode.get_session_id()
        plan_mode.deactivate()
    """

    def __init__(self, mode_name: str, extra_keys: list[str] = None):
        """Initialize mode manager.

        Args:
            mode_name: Base name without '_mode' suffix (e.g., "plan", "code")
            extra_keys: Additional cache keys beyond is_active and session_id
        """
        self.mode_name = mode_name
        self.namespace = f"{mode_name}_mode"
        self.cache_keys = ["is_active", "session_id"] + (extra_keys or [])

    def activate(self, session_id: str, message: str = None, **extra_cache) -> None:
        """Activate mode with common pattern.

        Args:
            session_id: Current session identifier
            message: Optional message to print on activation
            **extra_cache: Additional cache key-value pairs to set
        """
        set_cache(self.namespace, "is_active", True)
        set_cache(self.namespace, "session_id", session_id)
        for key, value in extra_cache.items():
            set_cache(self.namespace, key, value)
        if message:
            print(message)

    def deactivate(self) -> None:
        """Deactivate mode and clear all cache keys."""
        for key in self.cache_keys:
            if key == "is_active":
                set_cache(self.namespace, key, False)
            else:
                set_cache(self.namespace, key, "")

    def is_active(self) -> bool:
        """Check if mode is currently active."""
        return get_cache(self.namespace, "is_active") or False

    def get_session_id(self) -> str:
        """Get current session ID."""
        return get_cache(self.namespace, "session_id") or ""

    def get(self, key: str) -> Any:
        """Get arbitrary cache value for this mode."""
        return get_cache(self.namespace, key)

    def set(self, key: str, value: Any) -> None:
        """Set arbitrary cache value for this mode."""
        set_cache(self.namespace, key, value)


# Pre-instantiated mode managers for common use
plan_mode = ModeManager("plan")
research_mode = ModeManager("research")
explore_mode = ModeManager("explore")
code_mode = ModeManager("code", ["current_phase", "plan_file"])
code_review_mode = ModeManager("code_review")
