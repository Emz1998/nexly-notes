#!/bin/bash

# Memory Archive Script for NEXLY RN Project
# Analyzes and reorganizes files in the memory folder structure

set -e  # Exit on any error

# Configuration
WORKTREE_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
CLAUDE_DIR="$WORKTREE_ROOT/.claude"
MEMORY_DIR="$CLAUDE_DIR/memory"

# Operation mode
DRY_RUN=false

# Date references
TODAY=$(date +%Y-%m-%d)
TODAY_FORMATTED=$(date +%m-%d-%Y)
YESTERDAY=$(date -d "1 day ago" +%Y-%m-%d)
YESTERDAY_FORMATTED=$(date -d "1 day ago" +%m-%d-%Y)

# Logging
LOG_FILE="$CLAUDE_DIR/logs/memory-archive.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Statistics
SESSIONS_MOVED=0
SESSIONS_CHECKED=0

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Backup function
create_backup() {
    if [[ "$DRY_RUN" == "true" ]]; then
        log "[DRY-RUN] Would create backup"
        return
    fi

    local backup_dir="$CLAUDE_DIR/backups/archive-backup-$(date +%Y%m%d-%H%M%S)"
    log "Creating backup at $backup_dir"
    mkdir -p "$backup_dir"

    if [[ -d "$MEMORY_DIR" ]]; then
        cp -r "$MEMORY_DIR" "$backup_dir/"
    fi

    log "Backup created successfully"
    echo "$backup_dir"
}

# Get session date from folder
get_session_date() {
    local session_path="$1"
    local timestamp=$(stat -c %Y "$session_path" 2>/dev/null)

    if [[ -n "$timestamp" ]]; then
        date -d "@$timestamp" +%Y-%m-%d
    else
        echo ""
    fi
}

# Check and move session if needed
check_and_move_session() {
    local session_path="$1"
    local current_location="$2"
    local session_name=$(basename "$session_path")

    SESSIONS_CHECKED=$((SESSIONS_CHECKED + 1))

    # Get the session's actual date
    local session_date=$(get_session_date "$session_path")

    if [[ -z "$session_date" ]]; then
        log "Warning: Could not determine date for $session_name"
        return
    fi

    # Determine where it should be
    local target_location=""
    if [[ "$session_date" == "$TODAY" ]]; then
        target_location="sessions_today"
    elif [[ "$session_date" == "$YESTERDAY" ]]; then
        target_location="sessions_yesterday"
    else
        # Older sessions should be in archive
        local formatted_date=$(date -d "$session_date" +%m-%d-%Y 2>/dev/null)
        target_location="archive/sessions_$formatted_date"
    fi

    # Check if it needs to be moved
    if [[ "$current_location" != "$target_location" ]]; then
        local dest_dir="$MEMORY_DIR/$target_location"

        if [[ "$DRY_RUN" == "true" ]]; then
            log "[DRY-RUN] Would move $session_name from $current_location to $target_location"
        else
            mkdir -p "$dest_dir"
            mv "$session_path" "$dest_dir/"
            log "Moved $session_name from $current_location to $target_location"
        fi

        SESSIONS_MOVED=$((SESSIONS_MOVED + 1))
    else
        log "Session $session_name is correctly located in $current_location"
    fi
}

# Process sessions_today folder
process_sessions_today() {
    local sessions_today_dir="$MEMORY_DIR/sessions_today"

    if [[ ! -d "$sessions_today_dir" ]]; then
        log "No sessions_today folder found"
        return
    fi

    log "Processing sessions_today folder..."

    for session_folder in "$sessions_today_dir"/session_*; do
        if [[ -d "$session_folder" ]]; then
            check_and_move_session "$session_folder" "sessions_today"
        fi
    done
}

# Process sessions_yesterday folder
process_sessions_yesterday() {
    local sessions_yesterday_dir="$MEMORY_DIR/sessions_yesterday"

    if [[ ! -d "$sessions_yesterday_dir" ]]; then
        log "No sessions_yesterday folder found"
        return
    fi

    log "Processing sessions_yesterday folder..."

    for session_folder in "$sessions_yesterday_dir"/session_*; do
        if [[ -d "$session_folder" ]]; then
            check_and_move_session "$session_folder" "sessions_yesterday"
        fi
    done
}

# Process archive folders
process_archive() {
    local archive_dir="$MEMORY_DIR/archive"

    if [[ ! -d "$archive_dir" ]]; then
        log "No archive folder found"
        return
    fi

    log "Processing archive folders..."

    # Check each archive subfolder
    for archive_folder in "$archive_dir"/sessions_*; do
        if [[ -d "$archive_folder" ]]; then
            local folder_name=$(basename "$archive_folder")

            # Extract the date from folder name (sessions_mm-dd-yyyy)
            local folder_date_string=$(echo "$folder_name" | sed 's/sessions_//')

            # Process each session in this archive folder
            for session_folder in "$archive_folder"/session_*; do
                if [[ -d "$session_folder" ]]; then
                    # Use the archive folder name as the current location
                    check_and_move_session "$session_folder" "archive/$folder_name"
                fi
            done
        fi
    done
}

# Clean up empty directories
cleanup_empty_dirs() {
    if [[ "$DRY_RUN" == "true" ]]; then
        log "[DRY-RUN] Would clean up empty directories"
        return
    fi

    log "Cleaning up empty directories..."

    # Clean empty archive folders
    if [[ -d "$MEMORY_DIR/archive" ]]; then
        find "$MEMORY_DIR/archive" -type d -empty -delete 2>/dev/null || true
    fi

    # Don't delete sessions_today or sessions_yesterday even if empty
    # They should remain as part of the structure
}

# Main execution
main() {
    log "Starting memory archive analysis"

    if [[ "$DRY_RUN" == "true" ]]; then
        log "Running in DRY-RUN mode - no changes will be made"
    else
        # Create backup
        local backup_location=$(create_backup)
    fi

    # Check if memory directory exists
    if [[ ! -d "$MEMORY_DIR" ]]; then
        log "Error: Memory directory does not exist at $MEMORY_DIR"
        log "Run organize-memory.sh first to create the structure"
        exit 1
    fi

    # Process each folder
    process_sessions_today
    process_sessions_yesterday
    process_archive

    # Clean up empty directories
    cleanup_empty_dirs

    # Report results
    log "Archive analysis completed"
    log "Sessions checked: $SESSIONS_CHECKED"
    log "Sessions moved: $SESSIONS_MOVED"

    echo "
Memory archive analysis completed!

Sessions checked: $SESSIONS_CHECKED
Sessions moved: $SESSIONS_MOVED

Current structure:
- $MEMORY_DIR/sessions_today/ (today's sessions)
- $MEMORY_DIR/sessions_yesterday/ (yesterday's sessions)
- $MEMORY_DIR/archive/sessions_[mm-dd-yyyy]/ (older sessions)
"

    if [[ "$DRY_RUN" == "false" ]] && [[ -n "${backup_location:-}" ]]; then
        echo "Backup saved at: $backup_location"
    fi

    echo "Log file: $LOG_FILE"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo "
This was a DRY RUN - no changes were made.
Run without --dry-run to apply changes."
    fi
}

# Handle command line arguments
case "${1:-}" in
    --dry-run)
        DRY_RUN=true
        main
        ;;
    --help|-h)
        echo "Usage: $0 [--dry-run|--help]"
        echo "  Analyzes and reorganizes sessions in memory folder based on their age"
        echo ""
        echo "Options:"
        echo "  --dry-run  Preview changes without making them"
        echo "  --help     Show this help"
        echo ""
        echo "This script ensures sessions are in the correct folders:"
        echo "  - Today's sessions should be in sessions_today/"
        echo "  - Yesterday's sessions should be in sessions_yesterday/"
        echo "  - Older sessions should be in archive/sessions_[mm-dd-yyyy]/"
        ;;
    *)
        main
        ;;
esac