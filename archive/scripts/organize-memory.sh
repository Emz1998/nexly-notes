#!/bin/bash

# Memory Organization Script for NEXLY RN Project
# Moves tmp session files to organized memory structure

set -e  # Exit on any error

# Configuration
# Get current worktree root
WORKTREE_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
CLAUDE_DIR="$WORKTREE_ROOT/.claude"
MEMORY_DIR="$CLAUDE_DIR/memory"
TMP_DIR="$WORKTREE_ROOT/tmp"

# Date calculations
TODAY=$(date +%m-%d-%Y)
YESTERDAY=$(date -d "1 day ago" +%m-%d-%Y)
DAY_BEFORE_YESTERDAY=$(date -d "2 days ago" +%m-%d-%Y)

# Logging
LOG_FILE="$CLAUDE_DIR/logs/memory-organization.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Backup function
create_backup() {
    local backup_dir="$CLAUDE_DIR/backups/memory-backup-$(date +%Y%m%d-%H%M%S)"
    log "Creating backup at $backup_dir"
    mkdir -p "$backup_dir"

    if [[ -d "$MEMORY_DIR" ]]; then
        cp -r "$MEMORY_DIR" "$backup_dir/"
    fi

    if [[ -d "$TMP_DIR" ]]; then
        cp -r "$TMP_DIR" "$backup_dir/"
    fi

    log "Backup created successfully"
    echo "$backup_dir"
}

# Create memory structure
create_memory_structure() {
    log "Creating memory folder structure"

    # Create base structure
    mkdir -p "$MEMORY_DIR/archive"
    mkdir -p "$MEMORY_DIR/sessions_today"
    mkdir -p "$MEMORY_DIR/sessions_yesterday"

    log "Memory structure created"
}

# Move session folder as-is (no modifications)
move_session() {
    local source_session="$1"
    local destination="$2"
    local session_name="$(basename "$source_session")"

    if [[ ! -d "$source_session" ]]; then
        log "Warning: Session folder $source_session does not exist"
        return 1
    fi

    log "Moving session $session_name to $destination"

    # Create destination and copy entire session folder, then remove source
    mkdir -p "$destination"

    # Use cp -r followed by rm -rf to avoid WSL2 permission issues
    if cp -r "$source_session" "$destination/"; then
        rm -rf "$source_session"
        log "Session $session_name moved successfully"
    else
        log "Error: Failed to copy session $session_name"
        return 1
    fi
}

# Organize current tmp files
organize_current_tmp() {
    log "Organizing current tmp files based on age"

    # Create destination folders
    local sessions_today="$MEMORY_DIR/sessions_today"
    local sessions_yesterday="$MEMORY_DIR/sessions_yesterday"
    mkdir -p "$sessions_today"
    mkdir -p "$sessions_yesterday"

    # Get date references for comparison
    local today_date=$(date +%Y-%m-%d)
    local yesterday_date=$(date -d "1 day ago" +%Y-%m-%d)

    # Process session folders from /tmp
    if [[ -d "$TMP_DIR" ]]; then
        for session_folder in "$TMP_DIR"/session_*; do
            if [[ -d "$session_folder" ]]; then
                # Check folder creation/modification date
                local folder_timestamp=$(stat -c %Y "$session_folder" 2>/dev/null)
                local folder_date=$(date -d "@$folder_timestamp" +%Y-%m-%d 2>/dev/null)

                # Determine destination based on age
                if [[ "$folder_date" == "$today_date" ]]; then
                    move_session "$session_folder" "$sessions_today"
                    log "Moved session $(basename "$session_folder") to sessions_today (created: $folder_date)"
                elif [[ "$folder_date" == "$yesterday_date" ]]; then
                    move_session "$session_folder" "$sessions_yesterday"
                    log "Moved session $(basename "$session_folder") to sessions_yesterday (created: $folder_date)"
                else
                    # Older sessions go directly to archive
                    local formatted_date=$(date -d "@$folder_timestamp" +%m-%d-%Y 2>/dev/null)
                    local archive_dir="$MEMORY_DIR/archive/sessions_$formatted_date"
                    mkdir -p "$archive_dir"
                    move_session "$session_folder" "$archive_dir"
                    log "Moved session $(basename "$session_folder") to archive/sessions_$formatted_date (created: $folder_date)"
                fi
            fi
        done
    fi

    log "Session organization completed based on age"
}


# Main execution
main() {
    log "Starting memory organization script"

    # Create backup
    local backup_location=$(create_backup)

    # Create structure
    create_memory_structure

    # Organize current files
    organize_current_tmp

    # Show results
    log "Memory organization completed successfully"
    log "Backup saved at: $backup_location"

    echo "
Memory organization completed!

Structure created:
- $MEMORY_DIR/sessions_today/ (today's sessions)
- $MEMORY_DIR/sessions_yesterday/ (yesterday's sessions)
- $MEMORY_DIR/archive/ (older sessions by date)

Sessions organized by age:
- Today's sessions → sessions_today/
- Yesterday's sessions → sessions_yesterday/
- Older sessions → archive/sessions_[mm-dd-yyyy]/

Backup saved at: $backup_location
Log file: $LOG_FILE
"
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [--help]"
        echo "  Organizes session folders from tmp/ to memory/ based on their age"
        echo "  - Today's sessions go to memory/sessions_today/"
        echo "  - Yesterday's sessions go to memory/sessions_yesterday/"
        echo "  - Older sessions go to memory/archive/sessions_[mm-dd-yyyy]/"
        echo "  --help    Show this help"
        ;;
    *)
        main
        ;;
esac