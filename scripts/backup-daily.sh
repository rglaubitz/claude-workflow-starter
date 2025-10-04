#!/bin/bash
# Claude Daily Backup Script with Rotation
# Maintains 7 daily, 4 weekly, and 3 monthly backups

set -e

# Configuration
CLAUDE_HOME=~/.claude
BACKUP_ROOT=~/.claude/backups
DAILY_DIR="$BACKUP_ROOT/daily"
WEEKLY_DIR="$BACKUP_ROOT/weekly"
MONTHLY_DIR="$BACKUP_ROOT/monthly"
LOG_FILE="$BACKUP_ROOT/backup.log"

# Retention policy
DAILY_RETENTION=7
WEEKLY_RETENTION=4
MONTHLY_RETENTION=3

# Create directories if they don't exist
mkdir -p "$DAILY_DIR" "$WEEKLY_DIR" "$MONTHLY_DIR"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to create backup
create_backup() {
    local backup_type=$1
    local backup_dir=$2
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_name="claude-backup-$backup_type-$timestamp.tar.gz"
    local backup_path="$backup_dir/$backup_name"

    log "Creating $backup_type backup: $backup_name"

    # Create exclude file
    cat > /tmp/backup-exclude.txt << EOF
*.pyc
__pycache__
.git
.DS_Store
*.log
*.tmp
*.swp
backups/
EOF

    # Create backup archive
    tar -czf "$backup_path" \
        --exclude-from=/tmp/backup-exclude.txt \
        -C "$(dirname $CLAUDE_HOME)" \
        "$(basename $CLAUDE_HOME)"

    # Verify backup
    if tar -tzf "$backup_path" > /dev/null 2>&1; then
        local size=$(du -h "$backup_path" | cut -f1)
        log "✅ Backup created successfully: $backup_name ($size)"
        echo "$backup_path"
    else
        log "❌ Backup verification failed: $backup_name"
        rm -f "$backup_path"
        return 1
    fi

    rm -f /tmp/backup-exclude.txt
}

# Function to rotate backups
rotate_backups() {
    local dir=$1
    local retention=$2
    local backup_type=$3

    log "Rotating $backup_type backups (keeping last $retention)"

    # Get list of backups sorted by age (oldest first)
    local backups=($(ls -1t "$dir"/claude-backup-*.tar.gz 2>/dev/null | tail -r))
    local count=${#backups[@]}

    if [ $count -gt $retention ]; then
        local to_delete=$((count - retention))
        log "Deleting $to_delete old $backup_type backup(s)"

        for ((i=0; i<$to_delete; i++)); do
            local backup="${backups[$i]}"
            log "  Removing: $(basename "$backup")"
            rm -f "$backup"
        done
    fi
}

# Function to promote backup
promote_backup() {
    local source_path=$1
    local dest_dir=$2
    local backup_type=$3

    if [ -f "$source_path" ]; then
        local dest_name="$(basename "$source_path" | sed "s/daily/$backup_type/")"
        local dest_path="$dest_dir/$dest_name"

        cp "$source_path" "$dest_path"
        log "Promoted to $backup_type: $dest_name"
    fi
}

# Main backup process
main() {
    log "=== Starting Claude Daily Backup ==="

    # Create daily backup
    daily_backup=$(create_backup "daily" "$DAILY_DIR")

    if [ $? -eq 0 ]; then
        # Check if we should promote to weekly (Sunday)
        if [ $(date +%u) -eq 7 ]; then
            log "Sunday detected - promoting to weekly backup"
            promote_backup "$daily_backup" "$WEEKLY_DIR" "weekly"
            rotate_backups "$WEEKLY_DIR" "$WEEKLY_RETENTION" "weekly"
        fi

        # Check if we should promote to monthly (1st of month)
        if [ $(date +%d) -eq 01 ]; then
            log "First of month detected - promoting to monthly backup"
            promote_backup "$daily_backup" "$MONTHLY_DIR" "monthly"
            rotate_backups "$MONTHLY_DIR" "$MONTHLY_RETENTION" "monthly"
        fi

        # Rotate daily backups
        rotate_backups "$DAILY_DIR" "$DAILY_RETENTION" "daily"

        # Generate backup report
        generate_report

        log "✅ Backup process completed successfully"
    else
        log "❌ Backup process failed"
        exit 1
    fi
}

# Function to generate backup report
generate_report() {
    log "Generating backup report..."

    local report_file="$BACKUP_ROOT/backup-report.txt"

    cat > "$report_file" << EOF
Claude Backup Report
Generated: $(date)
====================

Daily Backups (Retention: $DAILY_RETENTION days):
$(ls -lh "$DAILY_DIR"/*.tar.gz 2>/dev/null | tail -n +1 || echo "  No daily backups found")

Weekly Backups (Retention: $WEEKLY_RETENTION weeks):
$(ls -lh "$WEEKLY_DIR"/*.tar.gz 2>/dev/null | tail -n +1 || echo "  No weekly backups found")

Monthly Backups (Retention: $MONTHLY_RETENTION months):
$(ls -lh "$MONTHLY_DIR"/*.tar.gz 2>/dev/null | tail -n +1 || echo "  No monthly backups found")

Total Backup Size: $(du -sh "$BACKUP_ROOT" | cut -f1)
====================
EOF

    log "Report saved to: $report_file"
}

# Function to restore backup
restore_backup() {
    local backup_path=$1
    local restore_dir=${2:-~/.claude-restored}

    if [ ! -f "$backup_path" ]; then
        log "❌ Backup file not found: $backup_path"
        exit 1
    fi

    log "Restoring backup: $backup_path"
    log "Restore directory: $restore_dir"

    # Create restore directory
    mkdir -p "$restore_dir"

    # Extract backup
    tar -xzf "$backup_path" -C "$restore_dir"

    if [ $? -eq 0 ]; then
        log "✅ Backup restored successfully to: $restore_dir"
        log "To activate restored backup, run:"
        log "  mv ~/.claude ~/.claude.old"
        log "  mv $restore_dir/.claude ~/.claude"
    else
        log "❌ Restore failed"
        exit 1
    fi
}

# Parse command line arguments
case "${1:-backup}" in
    backup)
        main
        ;;
    restore)
        if [ -z "$2" ]; then
            echo "Usage: $0 restore <backup-file> [restore-directory]"
            exit 1
        fi
        restore_backup "$2" "$3"
        ;;
    report)
        generate_report
        cat "$BACKUP_ROOT/backup-report.txt"
        ;;
    list)
        echo "=== Available Backups ==="
        echo
        echo "Daily:"
        ls -1t "$DAILY_DIR"/*.tar.gz 2>/dev/null | head -$DAILY_RETENTION || echo "  None"
        echo
        echo "Weekly:"
        ls -1t "$WEEKLY_DIR"/*.tar.gz 2>/dev/null | head -$WEEKLY_RETENTION || echo "  None"
        echo
        echo "Monthly:"
        ls -1t "$MONTHLY_DIR"/*.tar.gz 2>/dev/null | head -$MONTHLY_RETENTION || echo "  None"
        ;;
    *)
        echo "Usage: $0 [backup|restore|report|list]"
        echo "  backup  - Create a new backup (default)"
        echo "  restore - Restore from a backup file"
        echo "  report  - Generate and display backup report"
        echo "  list    - List available backups"
        exit 1
        ;;
esac