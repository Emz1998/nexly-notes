import json
from pathlib import Path

CACHE_PATH = Path(".claude/hooks/cache.json")


def get_cache(namespace: str, key: str):
    """Get value from shared cache. Returns None if not found."""
    try:
        cache = json.loads(CACHE_PATH.read_text())
        return cache.get(namespace, {}).get(key)
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def set_cache(namespace: str, key: str, value) -> None:
    """Set value in shared cache with namespace isolation."""
    try:
        cache = json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}
    except json.JSONDecodeError:
        cache = {}

    if namespace not in cache:
        cache[namespace] = {}
    cache[namespace][key] = value

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2))
