#!/bin/bash

# Get the project root directory (2 levels up from this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Directories
MOUNTED_DIR="$PROJECT_ROOT/screenshots"
PROJECT_DIR="$PROJECT_ROOT/.claude/screenshots"
TIMESTAMP_FILE="$PROJECT_DIR/.latest-timestamp"

# Create project directory if it doesn't exist
mkdir -p "$PROJECT_DIR"

# Check if mounted directory exists
if [ ! -d "$MOUNTED_DIR" ]; then
    echo "Mounted directory not found. Container may need to be rebuilt."
    echo "Run: docker-compose up --build"
    exit 1
fi

echo "Using mounted screenshots directory"

# Get all PNG files using ls (works better with Windows mounts)
shopt -s nullglob
screenshots_array=("$MOUNTED_DIR"/*.png)
shopt -u nullglob

if [ ${#screenshots_array[@]} -eq 0 ]; then
    echo "No screenshots found in mounted directory."
    exit 0
fi

# Get timestamps and sort files
declare -A file_timestamps
newest_timestamp=0

for file in "${screenshots_array[@]}"; do
    timestamp=$(stat -c "%Y" "$file" 2>/dev/null)
    if [ -n "$timestamp" ]; then
        file_timestamps["$file"]="$timestamp"
        if (( timestamp > newest_timestamp )); then
            newest_timestamp=$timestamp
        fi
    fi
done

# Read reference timestamp from file
if [ -f "$TIMESTAMP_FILE" ]; then
    reference_timestamp=$(cat "$TIMESTAMP_FILE")
    # Strip fractional part for both display and comparison (bash doesn't support floating point in (( )))
    reference_timestamp=$(echo "$reference_timestamp" | cut -d'.' -f1)
    echo "Reference timestamp: $(date -d @$reference_timestamp '+%Y-%m-%d %H:%M:%S')"

    # Check if newest screenshot is newer than reference
    if (( newest_timestamp <= reference_timestamp )); then
        echo "No new screenshots to copy. Already up to date."
        exit 0
    fi

    echo "Finding screenshots newer than reference..."
    # Find ONLY screenshots newer than reference timestamp
    new_screenshots=()
    for file in "${!file_timestamps[@]}"; do
        timestamp="${file_timestamps[$file]}"
        if (( timestamp > reference_timestamp )); then
            new_screenshots+=("$file")
        fi
    done

    # Sort by timestamp (newest first) and take only the latest
    IFS=$'\n' new_screenshots=($(
        for file in "${new_screenshots[@]}"; do
            echo "${file_timestamps[$file]} $file"
        done | sort -rn | head -1 | cut -d' ' -f2-
    ))
    unset IFS
else
    # No reference timestamp - copy only the latest screenshot
    echo "No reference timestamp found. Copying latest screenshot..."

    # Sort all screenshots by timestamp and take the top 1
    IFS=$'\n' sorted_files=($(
        for file in "${!file_timestamps[@]}"; do
            echo "${file_timestamps[$file]} $file"
        done | sort -rn | head -1 | cut -d' ' -f2-
    ))
    unset IFS

    new_screenshots=("${sorted_files[@]}")
fi

# Check if any screenshots found
if [ ${#new_screenshots[@]} -eq 0 ]; then
    echo "No new screenshots to copy. Already up to date."
    exit 0
fi

echo "Found new screenshot"

# Remove old screenshot if it exists
if [ -f "$PROJECT_DIR/latest.png" ]; then
    echo "Removing old screenshot..."
    rm -f "$PROJECT_DIR/latest.png"
fi

# Copy the latest screenshot
echo "Copying latest screenshot..."
screenshot="${new_screenshots[0]}"
dest_file="$PROJECT_DIR/latest.png"

# Copy with preserved timestamps
cp -p "$screenshot" "$dest_file"
echo "  $(basename "$screenshot") -> latest.png"

# Save the timestamp of the screenshot for next run
echo ""
echo "$newest_timestamp" > "$TIMESTAMP_FILE"
echo "Updated reference timestamp: $(date -d @$newest_timestamp '+%Y-%m-%d %H:%M:%S')"
