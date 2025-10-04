# Slash Command Patterns & Best Practices

## Overview

This document defines the two primary patterns for creating Claude Code slash commands, based on Anthropic's official specification. All commands in this directory follow these patterns.

**Official Documentation:** https://docs.claude.com/en/docs/claude-code/slash-commands

---

## Pattern 1: Prompt-Based Commands (Claude Execution)

Commands that provide instructions for Claude to interpret and execute.

### When to Use
- Complex multi-step workflows requiring AI decision-making
- Tasks requiring context understanding and adaptation
- Workflows that benefit from Claude's reasoning capabilities
- Operations that involve multiple tool types (Task, Read, Write, etc.)

### Structure
```markdown
---
description: "Brief description of what the command does"
argument-hint: "[optional-arg] <required-arg>"
allowed-tools: Task, Bash, Write, Read
---

# Command Title: $ARGUMENTS

Detailed instructions for Claude to follow.

## Your Task

1. **Step one**: Do something
2. **Step two**: Do something else

```python
# Inline code examples that Claude should execute
```

## Important

- Additional guidance
- Edge cases to handle
```

### Examples
- `/start-vision` - Creates Vision document using prd-expert agent
- `/start-implementation` - Orchestrates implementation with task-manager
- `/phase-status` - Queries database and displays formatted status

### Key Requirements
- **Must include `allowed-tools`** for any tools Claude will use
- Use `$ARGUMENTS` or `$1`, `$2` for argument substitution
- Provide clear, actionable instructions
- Include error handling guidance
- Document expected outcomes

---

## Pattern 2: Direct Execution Commands (Shell Scripts)

Commands that execute bash/python code directly before returning context to Claude.

### When to Use
- Simple, deterministic operations
- Direct system commands
- File system checks
- Quick status queries
- Profile/configuration switches

### Structure
```markdown
---
description: "Brief description of what the command does"
argument-hint: "<required-arg> [optional-flag]"
allowed-tools: Bash
---

Brief explanation of what will happen.

!bash -c '
# Direct bash code execution
echo "Doing something..."
'
```

Or for Python:

```markdown
!python3 -c "
import sys
# Python code here
print('Result')
"
```

### Examples
- `/serena` - Checks if Serena MCP server is active
- `/mcp-status` - Shows current MCP server configuration
- `/review-board` - Executes review board coordinator script

### Key Requirements
- **Must include `allowed-tools: Bash`**
- Use `!` prefix for direct execution
- Keep logic simple and deterministic
- Output results directly (no AI interpretation needed)
- Handle errors within the script

---

## Frontmatter Fields

### Official Fields (Anthropic Spec)

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `description` | **Yes** | Brief description shown in command list | `"Initialize new project"` |
| `argument-hint` | No | Shows expected arguments in UI | `"<project-slug>"` |
| `allowed-tools` | **Yes*** | Tools this command can use | `Bash, Write, Read` |
| `model` | No | Specific model to use | `claude-3-5-haiku-20241022` |
| `disable-model-invocation` | No | Prevents automatic Claude invocation | `true` |

\* Required if command uses any tools

### Argument Syntax
- `$ARGUMENTS` - All arguments as single string
- `$1`, `$2`, `$3` - Individual positional arguments
- `[optional]` - Optional argument in hint
- `<required>` - Required argument in hint

### Custom Fields
**Do not use custom frontmatter fields.** Only the five official fields above are documented and guaranteed to work. Custom fields (like `gitignored`) are ignored and add clutter.

---

## Tool Permissions

### Available Tools
- `Task` - Launch specialized agents
- `Bash` - Execute shell commands
- `Write` - Create/overwrite files
- `Read` - Read file contents
- `Edit` - Edit existing files
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `TodoWrite` - Manage todo lists
- `WebSearch` - Search the web
- `WebFetch` - Fetch web content

### Tool Specification Format
```yaml
allowed-tools: Task, Bash, Write, Read
```

Multiple tools comma-separated, no special syntax needed.

### Bash Tool Wildcards
For bash commands, you can restrict specific commands:
```yaml
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git status:*)
```

---

## Common Patterns

### Pattern: Multi-Phase Workflow Commands
```markdown
---
description: "Begin Phase X - Create deliverable"
allowed-tools: Task, Bash, Write, Read
---

1. Prerequisites check (database query)
2. Deploy specialized agent(s)
3. Create deliverable document
4. Update workflow database
5. Inform user of next steps
```

Examples: `/start-vision`, `/start-mission`, `/start-execution-planning`

### Pattern: Approval Gate Commands
```markdown
---
description: "Approve Phase X and unlock Phase Y"
allowed-tools: Bash, Read, Write
---

1. Verify deliverable exists
2. Update database (mark approved)
3. Unlock next phase
4. Inform user what's next
```

Examples: `/approve-vision`, `/approve-mission`, `/approve-testing`

### Pattern: Status/Query Commands
```markdown
---
description: "Show current status"
argument-hint: "[project-slug]"
allowed-tools: Bash, Read
---

1. Detect or require project identifier
2. Query database for current state
3. Format and display results
4. Show next available actions
```

Examples: `/phase-status`, `/workflow-dashboard`

### Pattern: Quick Check Commands
```markdown
---
description: "Check if feature/server is active"
allowed-tools: Bash
---

!bash -c '
if [ condition ]; then
    echo "✓ Active"
else
    echo "⚠️ Not active - run X to activate"
fi
'
```

Examples: `/serena`, `/mcp-status`, `/context7`

---

## Best Practices

### 1. Clear Descriptions
- ✅ `"Initialize new project with 5-phase workflow"`
- ❌ `"Start project"`

### 2. Helpful Argument Hints
- ✅ `"<project-slug>"` - Shows it's required
- ✅ `"[project-slug]"` - Shows it's optional
- ✅ `"<name> [--flag]"` - Shows required + optional

### 3. Minimal Tool Permissions
Only grant tools the command actually uses:
- ✅ `allowed-tools: Bash, Read` (if only reading and querying)
- ❌ `allowed-tools: Task, Bash, Write, Read, Edit, Glob, Grep, TodoWrite` (overly permissive)

### 4. Error Handling
Prompt-based commands should guide Claude on errors:
```python
if not file_exists:
    print("❌ Error: File not found")
    print("Run: /create-file first")
    exit(1)
```

### 5. User Communication
Always inform the user of:
- What was done
- What was created/changed
- What to do next
- Available commands

### 6. Consistent Formatting
- Use emoji for status: ✅ ❌ ⚠️ 🔄 📋 📊
- Use code blocks for output
- Use headers for sections
- Use bullets for lists

---

## Command Lifecycle

### Creating a New Command

1. **Choose pattern**: Prompt-based or Direct execution?
2. **Create file**: `/Users/richardglaubitz/.claude/commands/command-name.md`
3. **Add frontmatter**: At minimum: `description` and `allowed-tools`
4. **Write content**: Follow pattern template
5. **Test**: Run `/command-name` to verify
6. **Document**: Update this file if introducing new patterns

### File Naming
- Lowercase only
- Use hyphens for spaces: `start-vision.md`
- Descriptive but concise: `approve-testing.md`
- Verbs for actions: `start-`, `approve-`, `create-`

### Directory Location
- **Project commands**: `.claude/commands/` (project-specific)
- **Personal commands**: `~/.claude/commands/` (global across all projects)

Commands in `~/.claude/commands/` are available in all projects.

---

## Migration Notes

### v3.1.0 (2025-10-02)
- Added `allowed-tools` to all 17 workflow commands
- Removed non-functional `gitignored` custom field (not in Anthropic spec)
- Standardized frontmatter order: description → argument-hint → allowed-tools
- Verified all commands against Anthropic specification

### Removed Patterns
- ❌ `gitignored: true` - Not functional, not in spec, removed from all commands

---

## Troubleshooting

### "Permission denied" errors
- Check if `allowed-tools` includes required tool
- Verify tool name spelling (case-sensitive)

### Arguments not substituting
- Use `$ARGUMENTS` for all args, or `$1`, `$2` for individual
- Check argument-hint matches usage

### Command not appearing
- Verify file is in correct directory (`.claude/commands/` or `~/.claude/commands/`)
- Check filename ends with `.md`
- Ensure frontmatter is valid YAML (dashes, colons, quotes)

### Direct execution not working
- Must have `allowed-tools: Bash`
- Must prefix command with `!`
- Check bash/python syntax

---

## Command Inventory

### Workflow Phase Commands (17 total)
| Command | Pattern | Tools |
|---------|---------|-------|
| `/start-project` | Prompt | Bash, Write, Read |
| `/start-vision` | Prompt | Task, Bash, Write, Read |
| `/approve-vision` | Prompt | Bash, Read, Write |
| `/start-mission` | Prompt | Task, Bash, Write, Read |
| `/approve-mission` | Prompt | Bash, Read, Write |
| `/start-execution-planning` | Prompt | Task, Bash, Write, Read |
| `/approve-execution-plan` | Prompt | Bash, Read, Write |
| `/start-review-board` | Prompt | Task, Bash, Write, Read |
| `/approve-review-board` | Prompt | Bash, Read, Write |
| `/address-review-concerns` | Prompt | Bash, Read, Write |
| `/start-implementation` | Prompt | Task, Bash, Write, Read, TodoWrite |
| `/complete-implementation` | Prompt | Bash, Read, Write |
| `/start-testing` | Prompt | Task, Bash, Write, Read |
| `/approve-testing` | Prompt | Bash, Read, Write |
| `/phase-status` | Prompt | Bash, Read |
| `/workflow-dashboard` | Prompt | Bash, Read |
| `/review-board` | Direct | Bash |

### MCP & Utility Commands (8 total)
| Command | Pattern | Tools |
|---------|---------|-------|
| `/add-dependency` | Direct | Bash, Edit, Read |
| `/next-phase` | Direct | Bash, Write, Read |
| `/mcp-status` | Direct | Bash |
| `/mcp-profile` | Direct | Bash |
| `/serena` | Direct | Bash |
| `/context7` | Direct | Bash |
| `/exa` | Direct | Bash |
| `/think` | Direct | Bash |

**Total: 25 commands**

---

*Last updated: 2025-10-02*
*Spec version: v3.1.0*
*Anthropic docs: https://docs.claude.com/en/docs/claude-code/slash-commands*
