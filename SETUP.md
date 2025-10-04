# Installation Guide

Complete step-by-step guide to installing the Claude 5-Phase Workflow Starter.

## Prerequisites

### Required

- **Python 3.8+**: For running automation scripts
- **SQLite3**: For project databases
- **Claude Code**: The Claude CLI tool

### Optional

- **Node.js 18+**: For MCP servers (memory, knowledge persistence)
- **Git**: For version control
- **uvx**: For Python MCP servers (auto-installed by pipx)

## Installation Methods

### Method 1: Automated Installation (Recommended)

The easiest way to install is using the automated setup script:

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-workflow-starter.git
cd claude-workflow-starter

# Run the installer
./scripts/setup.sh
```

The installer will:
1. Check prerequisites
2. Backup existing `~/.claude/` (if present)
3. Create directory structure
4. Install all components
5. Set up configuration
6. Initialize databases
7. Validate installation

**Installation takes ~1-2 minutes.**

### Method 2: Manual Installation

If you prefer manual control:

```bash
# 1. Create directory structure
mkdir -p ~/.claude/{agents,commands,templates/phases,scripts,config,constitution,docs/workflows,plugins,data,projects,logs,backups}

# 2. Copy configuration files
cp CLAUDE.md PREFERENCES.md TOOL-SELECTION.md WORKFLOW.md version.json ~/.claude/

# 3. Copy agents (32 files)
cp agents/*.md ~/.claude/agents/

# 4. Copy commands (20 files)
cp commands/*.md ~/.claude/commands/

# 5. Copy templates
cp templates/phases/*.md ~/.claude/templates/phases/

# 6. Copy scripts
cp scripts/*.py scripts/*.sh ~/.claude/scripts/
chmod +x ~/.claude/scripts/*.sh

# 7. Copy constitution
cp -r constitution/* ~/.claude/constitution/

# 8. Copy documentation
cp -r docs/workflows/* ~/.claude/docs/workflows/

# 9. Set up configuration
cp config/.mcp.json.example ~/.claude/.mcp.json
cp config/settings.json.example ~/.claude/settings.json

# 10. Create shared knowledge database
sqlite3 ~/.claude/data/shared-knowledge.db "CREATE TABLE IF NOT EXISTS memo (id INTEGER PRIMARY KEY AUTOINCREMENT, insight TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);"
```

## Post-Installation Configuration

### 1. MCP Servers (Optional but Recommended)

MCP servers provide memory persistence and knowledge sharing across sessions.

**Install Node.js** (if not already installed):
```bash
# macOS
brew install node

# Linux
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Configure MCP servers** in `~/.claude/.mcp.json`:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "description": "Persistent memory with knowledge graph"
    },
    "sqlite-knowledge": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "~/.claude/data/shared-knowledge.db"],
      "description": "Shared knowledge base"
    }
  }
}
```

**Test MCP servers**:
```bash
# In Claude Code
/mcp-status
```

### 2. Claude Code Configuration

Ensure Claude Code can find the configuration:

```bash
# Check that files exist
ls -la ~/.claude/CLAUDE.md
ls -la ~/.claude/agents/
ls -la ~/.claude/commands/
```

### 3. Validate Installation

Run the health check:

```bash
~/.claude/scripts/health-check-v2.sh
```

Expected output:
```
✓ Configuration files present
✓ 32 agents installed
✓ 20 commands installed
✓ 6 phase templates installed
✓ Scripts executable
✓ Databases initialized
```

## Troubleshooting

### Issue: Permission Denied

```bash
chmod +x ~/.claude/scripts/*.sh
chmod +x ~/.claude/scripts/*.py
```

### Issue: Python Module Not Found

The scripts use only standard library modules. If you get import errors:

```bash
python3 --version  # Ensure 3.8+
```

### Issue: SQLite Not Found

```bash
# macOS
brew install sqlite

# Linux
sudo apt-get install sqlite3
```

### Issue: MCP Servers Not Working

1. Check Node.js installation:
   ```bash
   node --version  # Should be 18+
   ```

2. Check MCP configuration:
   ```bash
   cat ~/.claude/.mcp.json
   ```

3. Test manually:
   ```bash
   npx -y @modelcontextprotocol/server-memory
   ```

### Issue: Commands Not Found

Claude Code needs to be restarted after installation:

```bash
# Exit Claude Code and restart
# Then check:
/phase-status
```

If commands still don't work, verify:
```bash
ls ~/.claude/commands/*.md | wc -l  # Should show 20+
```

## Upgrading

To upgrade to a newer version:

```bash
# Backup your current installation
cp -r ~/.claude ~/.claude-backup-$(date +%Y%m%d)

# Pull latest changes
cd claude-workflow-starter
git pull

# Re-run installer
./scripts/setup.sh
```

The installer preserves:
- Project data (`~/.claude/projects/`)
- Logs (`~/.claude/logs/`)
- Backups (`~/.claude/backups/`)
- Custom settings

## Uninstallation

To completely remove the system:

```bash
# Backup first (optional)
cp -r ~/.claude ~/.claude-backup-final

# Remove installation
rm -rf ~/.claude

# Or keep projects and remove only the system:
cd ~/.claude
rm -rf agents/ commands/ templates/ scripts/ constitution/ docs/
rm CLAUDE.md PREFERENCES.md TOOL-SELECTION.md WORKFLOW.md version.json
```

## Backup Strategy

The system includes automatic backup scripts:

```bash
# Manual backup
~/.claude/scripts/backup-daily.sh

# Restore from backup
~/.claude/scripts/restore.sh <backup-path>
```

Backups include:
- Configuration files
- Project data
- Databases
- Custom settings

## Next Steps

After installation:

1. **Read the documentation**:
   - `~/.claude/WORKFLOW.md` - Workflow overview
   - `~/.claude/CLAUDE.md` - Configuration reference
   - `ARCHITECTURE.md` - System design

2. **Explore the components**:
   ```bash
   ls ~/.claude/agents/       # 32 specialists
   ls ~/.claude/commands/     # 20 slash commands
   ls ~/.claude/templates/    # Phase templates
   ```

3. **Create your first project**:
   ```bash
   mkdir -p ~/.claude/projects/my-first-project
   cp ~/.claude/templates/phases/00-project-brief-template.md \
      ~/.claude/projects/my-first-project/00-project-brief.md

   # Fill out the brief, then in Claude Code:
   /start-project my-first-project
   ```

4. **Join the community**:
   - Report issues on GitHub
   - Share your projects
   - Contribute improvements

## System Requirements

**Minimum:**
- macOS 10.15+ or Linux
- 2GB RAM
- 500MB disk space
- Python 3.8+
- SQLite3

**Recommended:**
- macOS 12+ or Ubuntu 20.04+
- 8GB RAM
- 1GB disk space
- Python 3.10+
- Node.js 18+
- Git

## Support

- **Documentation**: See the `docs/` directory
- **Issues**: GitHub Issues
- **Community**: GitHub Discussions

---

**Installation complete! Ready to build. 🚀**
