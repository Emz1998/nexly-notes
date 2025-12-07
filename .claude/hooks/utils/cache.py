import json
from pathlib import Path
from typing import Any

CACHE_PATH = Path(".claude/hooks/cache.json")


def load_cache():
    try:
        cache = json.loads(CACHE_PATH.read_text())
        return cache
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def write_cache(cache: dict) -> None:
    CACHE_PATH.write_text(json.dumps(cache, indent=2))


def get_cache(key: str):
    """Get value from shared cache. Returns None if not found."""
    if not key:
        raise ValueError("Cache key is required")
    try:
        cache = load_cache()
        return cache.get(key)
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def set_cache(key: str, value: Any) -> None:
    """Set value in shared cache with namespace isolation."""
    try:
        cache = json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}
    except json.JSONDecodeError:
        cache = {}

    if not key:
        print("Cache key is required")
        return
    if key not in cache:
        print(f"Cache key {key} not found")
        return

    cache[key] = value

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2))


def append_to_cache_list(key: str, value: Any) -> None:
    try:
        cache = load_cache()
        if type(cache[key]) is not list:
            raise ValueError(f"Cache key {key} is not a list")
        cache[key].append(value)
        CACHE_PATH.write_text(json.dumps(cache, indent=2))
    except Exception as e:
        print(f"Error appending to cache list: {e}")
        cache = {}
