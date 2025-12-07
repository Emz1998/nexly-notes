import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import read_stdin_json, get_cache, set_cache


def main():
    print(get_cache("current_subagent"))


if __name__ == "__main__":
    main()
