import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from scripts import inject_context


def main():
    # Context injection
    print("Injecting context...")
    inject_context()
    print("Context injected successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
