#!/usr/bin/env python3
"""
Copy the latest screenshot from mounted directory to project directory.
Tracks previously processed screenshots via a timestamp file.
"""

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def main():
    # Get the project root directory (2 levels up from this script)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent

    # Directories
    mounted_dir = project_root / "screenshots"
    project_dir = project_root / ".claude" / "screenshots"
    timestamp_file = project_dir / ".latest-timestamp"

    # Create project directory if it doesn't exist
    project_dir.mkdir(parents=True, exist_ok=True)

    # Check if mounted directory exists
    if not mounted_dir.is_dir():
        print("Mounted directory not found. Container may need to be rebuilt.")
        print("Run: docker-compose up --build")
        sys.exit(1)

    print("Using mounted screenshots directory")

    # Get all PNG files
    screenshots = list(mounted_dir.glob("*.png"))

    if not screenshots:
        print("No screenshots found in mounted directory.")
        sys.exit(0)

    # Get timestamps for each file
    file_timestamps: dict[Path, float] = {}
    newest_timestamp = 0.0

    for file in screenshots:
        try:
            timestamp = file.stat().st_mtime
            file_timestamps[file] = timestamp
            if timestamp > newest_timestamp:
                newest_timestamp = timestamp
        except OSError:
            continue

    # Read reference timestamp from file
    reference_timestamp: float | None = None
    if timestamp_file.exists():
        try:
            content = timestamp_file.read_text().strip()
            reference_timestamp = float(content.split(".")[0])
            ref_date = datetime.fromtimestamp(reference_timestamp)
            print(f"Reference timestamp: {ref_date.strftime('%Y-%m-%d %H:%M:%S')}")
        except (ValueError, OSError):
            reference_timestamp = None

    if reference_timestamp is not None:
        # Check if newest screenshot is newer than reference
        if newest_timestamp <= reference_timestamp:
            print("No new screenshots to copy. Already up to date.")
            sys.exit(0)

        print("Finding screenshots newer than reference...")
        # Find ONLY screenshots newer than reference timestamp
        new_screenshots = [
            f for f, ts in file_timestamps.items() if ts > reference_timestamp
        ]
        # Sort by timestamp (newest first) and take only the latest
        new_screenshots.sort(key=lambda f: file_timestamps[f], reverse=True)
        new_screenshots = new_screenshots[:1]
    else:
        # No reference timestamp - copy only the latest screenshot
        print("No reference timestamp found. Copying latest screenshot...")
        sorted_files = sorted(
            file_timestamps.keys(), key=lambda f: file_timestamps[f], reverse=True
        )
        new_screenshots = sorted_files[:1]

    # Check if any screenshots found
    if not new_screenshots:
        print("No new screenshots to copy. Already up to date.")
        sys.exit(0)

    print("Found new screenshot")

    # Remove old screenshot if it exists
    dest_file = project_dir / "latest.png"
    if dest_file.exists():
        print("Removing old screenshot...")
        dest_file.unlink()

    # Copy the latest screenshot
    print("Copying latest screenshot...")
    screenshot = new_screenshots[0]

    # Copy with preserved timestamps
    shutil.copy2(screenshot, dest_file)
    print(f"  {screenshot.name} -> latest.png")

    # Save the timestamp of the screenshot for next run
    print()
    timestamp_file.write_text(str(int(newest_timestamp)))
    new_date = datetime.fromtimestamp(newest_timestamp)
    print(f"Updated reference timestamp: {new_date.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
