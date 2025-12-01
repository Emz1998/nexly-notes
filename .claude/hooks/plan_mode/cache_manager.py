import json


def load_cache(key: str) -> bool | None:
    try:
        with open(".claude/hooks/plan_mode/cache.json") as f:
            cache = json.load(f)
            return cache.get(key, None)
    except (json.JSONDecodeError, FileNotFoundError):
        return False


def set_cache(key: str, value: bool) -> None:
    try:
        with open(".claude/hooks/plan_mode/cache.json", "r+") as f:
            cache = json.load(f)
            cache[key] = value
            f.seek(0)
            json.dump(cache, f)
            f.truncate()
    except (json.JSONDecodeError, FileNotFoundError):
        pass
