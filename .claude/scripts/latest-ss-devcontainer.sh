#!/bin/bash

# Directories
MOUNTED_DIR="/workspace/screenshots"
PROJECT_DIR="/workspace/.claude/screenshots"
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

# Get timestamp of newest screenshot in mounted directory
newest_mounted_timestamp=$(find "$MOUNTED_DIR" -name "*.png" -type f -printf "%T@\n" 2>/dev/null | sort -rn | head -1)

if [ -z "$newest_mounted_timestamp" ]; then
    echo "No screenshots found in mounted directory."
    exit 0
fi

# Read reference timestamp from file
if [ -f "$TIMESTAMP_FILE" ]; then
    reference_timestamp=$(cat "$TIMESTAMP_FILE")
    # Strip fractional part for display
    display_timestamp=$(echo "$reference_timestamp" | cut -d'.' -f1)
    echo "Reference timestamp: $(date -d @$display_timestamp '+%Y-%m-%d %H:%M:%S')"

    # Check if newest screenshot is newer than reference
    if ! awk -v newest="$newest_mounted_timestamp" -v ref="$reference_timestamp" 'BEGIN { exit !(newest > ref) }'; then
        echo "No new screenshots to copy. Already up to date."
        exit 0
    fi

    echo "Finding screenshots newer than reference..."
    # Find ONLY screenshots newer than reference timestamp
    new_screenshots=()
    while IFS= read -r entry; do
        timestamp=$(echo "$entry" | cut -d' ' -f1)
        filepath=$(echo "$entry" | cut -d' ' -f2-)

        # Compare timestamps - only add if newer than reference
        if awk -v ts="$timestamp" -v ref="$reference_timestamp" 'BEGIN { exit !(ts > ref) }'; then
            new_screenshots+=("$filepath")
        fi
    done < <(find "$MOUNTED_DIR" -name "*.png" -type f -printf "%T@ %p\n" 2>/dev/null | sort -rn)
else
    # No reference timestamp - copy only 5 most recent screenshots
    echo "No reference timestamp found. Copying 5 most recent screenshots..."

    # Find 5 most recent screenshots
    mapfile -t new_screenshots < <(find "$MOUNTED_DIR" -name "*.png" -type f -printf "%T@ %p\n" 2>/dev/null | sort -rn | head -5 | cut -d' ' -f2-)
fi

# Check if any screenshots found
if [ ${#new_screenshots[@]} -eq 0 ]; then
    echo "No new screenshots to copy. Already up to date."
    exit 0
fi

echo "Found ${#new_screenshots[@]} new screenshot(s)"

# Remove old reference files before adding new ones
echo "Cleaning up old screenshots..."
old_files=$(find "$PROJECT_DIR" -name "latest*.png" -type f 2>/dev/null)
old_count=$(echo "$old_files" | grep -c "png" 2>/dev/null || echo 0)

if [ "$old_count" -gt 0 ]; then
    echo "$old_files" | while read -r file; do
        echo "  Deleting: $(basename "$file")"
    done
fi

rm -f "$PROJECT_DIR"/latest*.png
echo "Removed $old_count old screenshot(s)"
echo ""

# Use the newest timestamp we already found earlier
newest_timestamp="$newest_mounted_timestamp"

# Copy screenshots with sequential numbering
echo "Creating new screenshot files..."
counter=1
newest_file=""

for screenshot in "${new_screenshots[@]}"; do
    # Format counter with leading zeros
    file_num=$(printf "%03d" $counter)
    dest_file="$PROJECT_DIR/latest-$file_num.png"

    # Copy with preserved timestamps
    cp -p "$screenshot" "$dest_file"
    echo "  [$counter] $(basename "$screenshot") -> latest-$file_num.png"

    newest_file="$dest_file"
    ((counter++))
done

# Save the timestamp of the newest screenshot for next run
if [ -n "$newest_file" ]; then
    echo ""
    echo "Total screenshots copied: ${#new_screenshots[@]}"

    echo "$newest_timestamp" > "$TIMESTAMP_FILE"
    # Strip fractional part for display
    display_newest=$(echo "$newest_timestamp" | cut -d'.' -f1)
    echo "Updated reference timestamp: $(date -d @$display_newest '+%Y-%m-%d %H:%M:%S')"
fi