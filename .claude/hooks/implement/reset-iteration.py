#!/usr/bin/env python3
"""
Hook to reset iteration flag on stop event.
"""

import json
import sys
from pathlib import Path


def main():
    try:
        script_dir = Path(__file__).parent
        iteration_file = script_dir / "iteration.json"

        if not iteration_file.exists():
            sys.exit(0)

        with open(iteration_file, "r") as f:
            iteration_data = json.load(f)

        iteration_data["iterate"] = True

        with open(iteration_file, "w") as f:
            json.dump(iteration_data, f)

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
