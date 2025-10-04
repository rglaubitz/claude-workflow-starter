#!/bin/bash

# Claude Global Health Check Script v2.0
# Enhanced version with comprehensive monitoring
# Part of Phase 3: Automation & Scheduling

set -euo pipefail

# Configuration
LOG_DIR="$HOME/.claude/logs/health"
LOG_FILE="$LOG_DIR/health-check-$(date +%Y%m%d).log"
STATUS_FILE="$HOME/.claude/health/status.json"
ALERT_THRESHOLD=3  # Number of failures before alert
ERROR_COUNT_FILE="$HOME/.claude/health/error_count"

# Create directories if needed
mkdir -p "$LOG_DIR" "$(dirname "$STATUS_FILE")"

# Logging function
log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

# Initialize health status
HEALTH_STATUS="OK"
FAILED_CHECKS=()
WARNINGS=()

# Global variables for metrics
memory_percent=0
disk_usage=0

# Function to check MCP servers
check_mcp_servers() {
    log "INFO" "Checking MCP server connections..."
    
    # Check if claude command exists
    if ! command -v claude &> /dev/null; then
        log "ERROR" "Claude command not found"
        HEALTH_STATUS="CRITICAL"
        FAILED_CHECKS+=("Claude command not available")
        return 1
    fi
    
    # Get MCP status
    local mcp_output
    mcp_output=$(claude mcp list 2>&1 || true)
    
    # Check MCP configuration exists
    local mcp_config="$HOME/.config/claude/claude_desktop_config.json"
    if [ ! -f "$mcp_config" ]; then
        log "ERROR" "MCP configuration file missing: $mcp_config"
        HEALTH_STATUS="CRITICAL"
        FAILED_CHECKS+=("MCP configuration missing")
        return 1
    fi
    
    # Check specific servers from our config
    local expected_servers=("filesystem" "memory" "serena" "github" "playwright" "browserbase" "context7" "ide")
    local missing_servers=()
    
    for server in "${expected_servers[@]}"; do
        if ! grep -q "\"$server\"" "$mcp_config"; then
            missing_servers+=("$server")
        fi
    done
    
    if [ ${#missing_servers[@]} -gt 0 ]; then
        log "WARN" "Missing MCP servers: ${missing_servers[*]}"
        WARNINGS+=("MCP servers not configured: ${missing_servers[*]}")
    else
        log "INFO" "All expected MCP servers configured"
    fi
    
    # Count connected servers
    local connected_count=$(echo "$mcp_output" | grep -c "✓ Connected" || true)
    local expected_servers=7  # Adjust based on your setup
    
    if [ "$connected_count" -lt "$expected_servers" ]; then
        log "WARNING" "Only $connected_count/$expected_servers MCP servers connected"
        WARNINGS+=("MCP servers: $connected_count/$expected_servers connected")
    else
        log "INFO" "All $connected_count MCP servers connected"
    fi
}

# Function to check system resources
check_system_resources() {
    log "INFO" "Checking system resources..."
    
    # Check memory usage (macOS specific)
    local memory_info=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
    local pages_size=4096  # Page size in bytes
    local free_memory=$((memory_info * pages_size / 1024 / 1024))  # Convert to MB
    
    # Get total memory
    local total_memory=$(($(sysctl -n hw.memsize) / 1024 / 1024))
    local used_memory=$((total_memory - free_memory))
    memory_percent=$((used_memory * 100 / total_memory))
    
    if [ "$memory_percent" -gt 90 ]; then
        log "ERROR" "Memory usage critical: ${memory_percent}%"
        HEALTH_STATUS="CRITICAL"
        FAILED_CHECKS+=("Memory usage: ${memory_percent}%")
    elif [ "$memory_percent" -gt 80 ]; then
        log "WARNING" "Memory usage high: ${memory_percent}%"
        WARNINGS+=("Memory usage: ${memory_percent}%")
    else
        log "INFO" "Memory usage normal: ${memory_percent}%"
    fi
    
    # Check disk usage
    disk_usage=$(df -h "$HOME" | awk 'NR==2 {print int($5)}')
    if [ "$disk_usage" -gt 90 ]; then
        log "ERROR" "Disk usage critical: ${disk_usage}%"
        HEALTH_STATUS="CRITICAL"
        FAILED_CHECKS+=("Disk usage: ${disk_usage}%")
    elif [ "$disk_usage" -gt 80 ]; then
        log "WARNING" "Disk usage high: ${disk_usage}%"
        WARNINGS+=("Disk usage: ${disk_usage}%")
    else
        log "INFO" "Disk usage normal: ${disk_usage}%"
    fi
}

# Function to check Docker status
check_docker() {
    log "INFO" "Checking Docker status..."
    
    if command -v docker &> /dev/null; then
        if docker ps &> /dev/null; then
            local container_count=$(docker ps -q | wc -l | tr -d ' ')
            log "INFO" "Docker running with $container_count containers"
        else
            log "WARNING" "Docker daemon not running"
            WARNINGS+=("Docker daemon not running")
        fi
    else
        log "WARNING" "Docker not installed"
        WARNINGS+=("Docker not installed")
    fi
}

# Function to check critical files
check_critical_files() {
    log "INFO" "Checking critical files..."
    
    local critical_files=(
        "$HOME/.claude/settings.local.json"
        "$HOME/.claude/scripts/backup-now.sh"
        "$HOME/.claude/commands/help.md"
    )
    
    for file in "${critical_files[@]}"; do
        if [ ! -f "$file" ]; then
            log "WARNING" "Critical file missing: $file"
            WARNINGS+=("Missing file: $(basename "$file")")
        fi
    done
}

# Function to check backup freshness
check_backups() {
    log "INFO" "Checking backup freshness..."
    
    local backup_dir="$HOME/.claude/backups"
    if [ -d "$backup_dir" ]; then
        # Find most recent backup
        local latest_backup=$(find "$backup_dir" -name "*.tar.gz" -type f -exec stat -f "%m %N" {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
        
        if [ -n "$latest_backup" ]; then
            local backup_age=$(( ($(date +%s) - $(stat -f %m "$latest_backup")) / 3600 ))
            if [ "$backup_age" -gt 48 ]; then
                log "WARNING" "Last backup is $backup_age hours old"
                WARNINGS+=("Backup age: ${backup_age}h")
            else
                log "INFO" "Last backup is $backup_age hours old"
            fi
        else
            log "WARNING" "No backups found"
            WARNINGS+=("No backups found")
        fi
    fi
}

# Function to update error count
update_error_count() {
    local current_count=0
    if [ -f "$ERROR_COUNT_FILE" ]; then
        current_count=$(cat "$ERROR_COUNT_FILE")
    fi
    
    if [ "$HEALTH_STATUS" = "CRITICAL" ]; then
        current_count=$((current_count + 1))
        echo "$current_count" > "$ERROR_COUNT_FILE"
        
        if [ "$current_count" -ge "$ALERT_THRESHOLD" ]; then
            log "CRITICAL" "Error threshold reached: $current_count consecutive failures"
            # Trigger alert (will be handled by notification script)
            if [ -x "$HOME/.claude/scripts/send-notification.sh" ]; then
                "$HOME/.claude/scripts/send-notification.sh" "CRITICAL" "Health check failed $current_count times"
            fi
        fi
    else
        # Reset counter on success
        echo "0" > "$ERROR_COUNT_FILE"
    fi
}

# Function to generate status JSON
generate_status_json() {
    cat > "$STATUS_FILE" <<EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "$HEALTH_STATUS",
  "failed_checks": [$(printf '"%s",' "${FAILED_CHECKS[@]}" | sed 's/,$//')]",
  "warnings": [$(printf '"%s",' "${WARNINGS[@]}" | sed 's/,$//')]",
  "metrics": {
    "memory_usage": "$memory_percent",
    "disk_usage": "$disk_usage"
  }
}
EOF
}

# Main execution
main() {
    log "INFO" "Starting health check..."
    
    # Run all checks
    check_mcp_servers
    check_system_resources
    check_docker
    check_critical_files
    check_backups
    
    # Determine overall status
    if [ ${#FAILED_CHECKS[@]} -gt 0 ]; then
        HEALTH_STATUS="CRITICAL"
        log "CRITICAL" "Health check failed with ${#FAILED_CHECKS[@]} critical issues"
    elif [ ${#WARNINGS[@]} -gt 0 ]; then
        HEALTH_STATUS="WARNING"
        log "WARNING" "Health check completed with ${#WARNINGS[@]} warnings"
    else
        HEALTH_STATUS="OK"
        log "INFO" "Health check completed successfully"
    fi
    
    # Update error count
    update_error_count
    
    # Generate status file
    generate_status_json
    
    # Output summary
    echo "=== Health Check Summary ==="
    echo "Status: $HEALTH_STATUS"
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
    if [ ${#FAILED_CHECKS[@]} -gt 0 ]; then
        echo "Critical Issues:"
        printf '  - %s\n' "${FAILED_CHECKS[@]}"
    fi
    if [ ${#WARNINGS[@]} -gt 0 ]; then
        echo "Warnings:"
        printf '  - %s\n' "${WARNINGS[@]}"
    fi
    
    # Exit with appropriate code
    if [ "$HEALTH_STATUS" = "CRITICAL" ]; then
        exit 1
    elif [ "$HEALTH_STATUS" = "WARNING" ]; then
        exit 0  # Warnings don't fail the health check
    else
        exit 0
    fi
}

# Run main function
main "$@"