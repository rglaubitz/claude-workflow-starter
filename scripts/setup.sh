#!/bin/bash
set -e

# Claude Workflow Starter - Installation Script
# Version: 3.1.0
# Description: Installs the 5-phase workflow system to ~/.claude/

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
INSTALL_DIR="$HOME/.claude"
BACKUP_DIR="$HOME/.claude-backup-$(date +%Y%m%d-%H%M%S)"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Claude 5-Phase Workflow Starter - Installation        ║${NC}"
echo -e "${BLUE}║                    Version 3.1.0                           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print success message
success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print error message
error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to print warning message
warning() {
    echo -e "${YELLOW}!${NC} $1"
}

# Function to print info message
info() {
    echo -e "${BLUE}→${NC} $1"
}

# 1. Validate Prerequisites
echo "Step 1: Checking prerequisites..."

# Check for Python 3
if ! command_exists python3; then
    error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
success "Python 3 found: $PYTHON_VERSION"

# Check for SQLite3
if ! command_exists sqlite3; then
    error "SQLite3 is not installed. Please install SQLite3."
    exit 1
fi
success "SQLite3 found"

# Check for git
if ! command_exists git; then
    warning "Git is not installed. Some features may not work."
else
    success "Git found"
fi

# Check for Node.js (needed for MCP servers)
if ! command_exists node; then
    warning "Node.js is not installed. MCP servers will not work without it."
else
    NODE_VERSION=$(node --version)
    success "Node.js found: $NODE_VERSION"
fi

echo ""

# 2. Backup existing installation
if [ -d "$INSTALL_DIR" ]; then
    echo "Step 2: Backing up existing installation..."
    info "Existing installation found at $INSTALL_DIR"
    info "Creating backup at $BACKUP_DIR"

    mkdir -p "$BACKUP_DIR"
    cp -r "$INSTALL_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true

    success "Backup created successfully"
    warning "Your existing installation has been backed up"
    echo ""

    # Ask user if they want to continue
    read -p "Continue with installation? This will overwrite configuration files. (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        info "Installation cancelled."
        exit 0
    fi
else
    echo "Step 2: No existing installation found. Proceeding with fresh install..."
fi

echo ""

# 3. Create directory structure
echo "Step 3: Creating directory structure..."

mkdir -p "$INSTALL_DIR"/{agents,commands,templates/phases,scripts,config,constitution,docs/workflows,plugins,data}
mkdir -p "$INSTALL_DIR"/{projects,logs,backups,file-history,shell-snapshots,statsig,todos,ide}

success "Directory structure created"
echo ""

# 4. Copy configuration files
echo "Step 4: Installing configuration files..."

cp "$REPO_ROOT/CLAUDE.md" "$INSTALL_DIR/" && success "CLAUDE.md installed"
cp "$REPO_ROOT/PREFERENCES.md" "$INSTALL_DIR/" && success "PREFERENCES.md installed"
cp "$REPO_ROOT/TOOL-SELECTION.md" "$INSTALL_DIR/" && success "TOOL-SELECTION.md installed"
cp "$REPO_ROOT/WORKFLOW.md" "$INSTALL_DIR/" && success "WORKFLOW.md installed"
cp "$REPO_ROOT/version.json" "$INSTALL_DIR/" && success "version.json installed"

echo ""

# 5. Copy agents
echo "Step 5: Installing 32 specialized agents..."

cp "$REPO_ROOT"/agents/*.md "$INSTALL_DIR/agents/" && success "32 agents installed"

echo ""

# 6. Copy commands
echo "Step 6: Installing slash commands..."

cp "$REPO_ROOT"/commands/*.md "$INSTALL_DIR/commands/" && success "Slash commands installed"

echo ""

# 7. Copy templates
echo "Step 7: Installing phase templates..."

cp "$REPO_ROOT"/templates/phases/*.md "$INSTALL_DIR/templates/phases/" && success "Phase templates installed"

echo ""

# 8. Copy scripts
echo "Step 8: Installing automation scripts..."

cp "$REPO_ROOT"/scripts/*.py "$INSTALL_DIR/scripts/" 2>/dev/null || true
cp "$REPO_ROOT"/scripts/*.sh "$INSTALL_DIR/scripts/" 2>/dev/null || true
chmod +x "$INSTALL_DIR/scripts"/*.sh 2>/dev/null || true
chmod +x "$INSTALL_DIR/scripts"/*.py 2>/dev/null || true

success "Scripts installed and made executable"

echo ""

# 9. Copy constitution
echo "Step 9: Installing constitution system..."

cp -r "$REPO_ROOT"/constitution/* "$INSTALL_DIR/constitution/" 2>/dev/null || true

success "Constitution system installed"

echo ""

# 10. Copy documentation
echo "Step 10: Installing documentation..."

cp -r "$REPO_ROOT"/docs/workflows/* "$INSTALL_DIR/docs/workflows/" 2>/dev/null || true

success "Documentation installed"

echo ""

# 11. Set up configuration
echo "Step 11: Setting up configuration..."

if [ ! -f "$INSTALL_DIR/.mcp.json" ]; then
    if [ -f "$REPO_ROOT/config/.mcp.json.example" ]; then
        cp "$REPO_ROOT/config/.mcp.json.example" "$INSTALL_DIR/.mcp.json"
        success ".mcp.json created from example"
    fi
else
    warning ".mcp.json already exists (preserved)"
fi

if [ ! -f "$INSTALL_DIR/settings.json" ]; then
    if [ -f "$REPO_ROOT/config/settings.json.example" ]; then
        cp "$REPO_ROOT/config/settings.json.example" "$INSTALL_DIR/settings.json"
        success "settings.json created from example"
    fi
else
    warning "settings.json already exists (preserved)"
fi

echo ""

# 12. Create shared knowledge database
echo "Step 12: Creating shared knowledge database..."

if [ ! -f "$INSTALL_DIR/data/shared-knowledge.db" ]; then
    sqlite3 "$INSTALL_DIR/data/shared-knowledge.db" "CREATE TABLE IF NOT EXISTS memo (id INTEGER PRIMARY KEY AUTOINCREMENT, insight TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);" && success "Shared knowledge database created"
else
    warning "Shared knowledge database already exists (preserved)"
fi

echo ""

# 13. Set permissions
echo "Step 13: Setting permissions..."

chmod -R 755 "$INSTALL_DIR" 2>/dev/null || true
chmod 644 "$INSTALL_DIR"/*.md 2>/dev/null || true

success "Permissions set"

echo ""

# 14. Validation
echo "Step 14: Validating installation..."

# Count components
AGENT_COUNT=$(ls -1 "$INSTALL_DIR/agents"/*.md 2>/dev/null | wc -l)
COMMAND_COUNT=$(ls -1 "$INSTALL_DIR/commands"/*.md 2>/dev/null | wc -l)
TEMPLATE_COUNT=$(ls -1 "$INSTALL_DIR/templates/phases"/*.md 2>/dev/null | wc -l)

if [ "$AGENT_COUNT" -ge 30 ]; then
    success "$AGENT_COUNT agents installed"
else
    warning "Only $AGENT_COUNT agents found (expected 32+)"
fi

if [ "$COMMAND_COUNT" -ge 15 ]; then
    success "$COMMAND_COUNT commands installed"
else
    warning "Only $COMMAND_COUNT commands found (expected 20+)"
fi

if [ "$TEMPLATE_COUNT" -ge 6 ]; then
    success "$TEMPLATE_COUNT phase templates installed"
else
    warning "Only $TEMPLATE_COUNT templates found (expected 6)"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          Installation Complete! 🎉                         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo "Installation Summary:"
echo "  • Location: $INSTALL_DIR"
echo "  • Agents: $AGENT_COUNT specialists"
echo "  • Commands: $COMMAND_COUNT slash commands"
echo "  • Templates: $TEMPLATE_COUNT phase templates"
echo "  • Scripts: Workflow automation installed"
echo "  • Constitution: Agent governance installed"
echo ""

if [ -d "$BACKUP_DIR" ]; then
    echo "Backup Location: $BACKUP_DIR"
    echo ""
fi

echo "Next Steps:"
echo ""
echo "1. Configure MCP servers (optional):"
echo "   Edit ~/.claude/.mcp.json to add memory and sqlite-knowledge servers"
echo ""
echo "2. Create your first project:"
echo "   • Copy the project brief template:"
echo "     mkdir -p ~/.claude/projects/my-first-project"
echo "     cp ~/.claude/templates/phases/00-project-brief-template.md \\"
echo "        ~/.claude/projects/my-first-project/00-project-brief.md"
echo "   • Fill out the brief"
echo "   • Run: /start-project my-first-project"
echo ""
echo "3. Explore the system:"
echo "   • View available commands: ~/.claude/commands/"
echo "   • View agent roster: ~/.claude/agents/"
echo "   • Read documentation: ~/.claude/WORKFLOW.md"
echo ""
echo "4. Check system health:"
echo "   ~/.claude/scripts/health-check-v2.sh"
echo ""
echo "For detailed documentation, see:"
echo "  • Getting Started: $REPO_ROOT/docs/getting-started.md"
echo "  • Architecture: $REPO_ROOT/ARCHITECTURE.md"
echo ""
echo -e "${BLUE}Happy building with Claude Code! 🚀${NC}"
echo ""
