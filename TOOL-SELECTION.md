# Tool Selection Guide

Quick decision trees for choosing the right tool for the task.

## Team-First Delegation (ALWAYS CHECK FIRST)

```text
Can a specialist agent handle this better?
├── YES → Complex task requiring expertise?
│   ├── Code review needed → **Task with code-review-expert**
│   ├── Documentation needed → **Task with documentation-expert**
│   ├── Architecture design → **Task with agent-architecture-designer**
│   ├── Testing required → **Task with agent-testing-engineer**
│   ├── Integration work → **Task with integration-specialist**
│   ├── Memory system → **Task with memory-system-engineer**
│   ├── MCP configuration → **Task with mcp-bridge-engineer**
│   ├── PRD creation → **Task with prd-expert**
│   ├── Task breakdown → **Task with project-task-planner**
│   ├── Research needed → **Task with research-manager**
│   └── Orchestration → **Task with task-manager**
└── NO → Continue with direct tool selection below
```

## Code Operations Decision Tree

```text
Need to work with code?
├── YES → Understanding/Analyzing code?
│   ├── YES → Need semantic understanding (symbols, relationships)?
│   │   ├── YES → **USE GREP** with semantic patterns
│   │   └── NO → Simple text search?
│   │       ├── YES → **USE GREP**
│   │       └── NO → **USE READ**
│   └── NO → Modifying code?
│       ├── YES → Refactoring entire functions/classes?
│       │   ├── YES → **USE EDIT/MULTIEDIT** for refactoring
│       │   └── NO → Multiple edits in one file?
│       │       ├── YES → **USE MULTIEDIT**
│       │       └── NO → Small edit?
│       │           ├── YES → **USE EDIT**
│       │           └── NO → Creating new file? → **USE WRITE**
│       └── NO → **USE READ**
└── NO → See other categories below
```

## File Operations Decision Tree

```text
Working with files/directories?
├── Finding files?
│   ├── By name pattern → **USE GLOB**
│   ├── By content → **USE GREP**
│   └── By symbol → **USE GREP** with symbol patterns
├── Reading files?
│   ├── Code file → **USE READ** then analyze
│   ├── Config/data → **USE READ**
│   ├── Jupyter notebook → **USE READ** (handles .ipynb)
│   └── Multiple files → **USE TASK** (with specialist agent)
└── Managing files?
    ├── Create → **USE WRITE**
    ├── Delete → **USE BASH** (rm)
    ├── Move/Rename → **USE BASH** (mv)
    └── Backup → **USE BASH** (backup scripts)
```

## External Resources

```text
Need external information?
├── Documentation?
│   ├── Library docs → **USE WEBFETCH** or **WEBSEARCH**
│   ├── GitHub operations → **USE BASH** (gh CLI)
│   └── General web → **USE WEBSEARCH**
├── API/Web interaction?
│   ├── Browser automation → **USE BASH** with browser tools
│   ├── JavaScript execution → **USE mcp__ide__executeCode** (for Python/Jupyter)
│   ├── Simple fetch → **USE WEBFETCH**
│   └── GitHub API → **USE BASH** (gh api)
└── Current information?
    ├── News/recent → **USE WEBSEARCH**
    └── Specific site → **USE WEBFETCH**
```

## System Operations

```text
System task?
├── Commands/Scripts?
│   ├── Git operations → **USE BASH** (git commands)
│   ├── Package management → **USE BASH** (npm, pip, etc.)
│   ├── Database queries → **USE BASH** (sqlite3 ~/.claude/data/shared-knowledge.db)
│   └── System health → **USE /memory** command
├── Memory/Knowledge?
│   ├── Project-specific → **USE BASH** (sqlite3 for storage)
│   ├── Global knowledge → **USE BASH** (sqlite3 shared-knowledge.db)
│   ├── View learning health → **USE /memory**
│   └── Store patterns → **USE BASH** (sqlite3)
├── Task Management?
│   ├── Track todos → **USE TODOWRITE**
│   ├── Delegate work → **USE TASK** (with agent)
│   └── Complex workflow → **USE TASK** (with task-manager)
└── Notebook Operations?
    └── Edit cells → **USE NOTEBOOKEDIT**
```

## Available Commands

### Workflow Commands

- `/memory` - Show learning system health and recent learnings
- `/build-agent <name> <purpose>` - Create new agent with full pipeline
- `/review-all [path]` - Comprehensive parallel code review
- `/integrate <service>` - Service integration workflow
- `/debug [issue]` - Multi-angle debugging approach

## Performance Guidelines

### Fast Operations (< 1 second)

- Glob (file patterns)
- Grep (text search)
- Read (single file)
- Edit (small changes)
- TodoWrite (task tracking)
- Bash (simple commands)

### Medium Operations (1-5 seconds)

- Serena (symbol operations)
- WebFetch (single page)
- MultiEdit (batch edits)
- Memory operations (openmemory)
- Database queries (SQLite)

### Slow Operations (> 5 seconds)

- Task (agent spawning)
- WebSearch (multiple results)
- Browserbase (full automation)
- Playwright (JavaScript execution)
- Learning pipeline (batch processing every 30 min)

### Performance Metrics (From Load Testing)

- Event processing: 2,083 events/second
- Event generation: 70,379 events/second
- Circuit breaker threshold: 10% error rate
- Memory usage: < 50MB for 1000 events
- Database growth: < 1MB per 1000 events

## Common Patterns

### Pattern: "Delegate to specialist"

1. Identify task complexity
2. **TASK** with appropriate agent
3. Monitor progress with **TODOWRITE**

### Pattern: "Find and modify a function"

1. **GREP** to locate function
2. **READ** to understand context
3. **EDIT/MULTIEDIT** to modify
4. **GREP** to check usage

### Pattern: "Understand a codebase"

1. **GLOB** to find relevant files
2. **READ** multiple files for structure
3. **GREP** for specific elements
4. **BASH** (sqlite3) to store learnings

### Pattern: "Fix a bug"

1. **GREP** to find error locations
2. **READ** to understand code context
3. **EDIT** or **MULTIEDIT** to fix
4. **BASH** to run tests
5. **TASK** with code-review-expert for review

### Pattern: "Create new feature"

1. **TASK** with prd-expert for specification
2. **TASK** with project-task-planner for breakdown
3. **READ** and **GREP** to understand existing patterns
4. **WRITE** to create new files
5. **EDIT** to integrate with existing code

### Pattern: "Learning from work"

1. Automatic capture via hooks (post-edit, post-command)
2. Batch processing every 30 minutes
3. Pattern extraction (score > 21)
4. View with **/memory** command

### Pattern: "Database operations"

1. **BASH** with sqlite3 for queries
2. Store in `~/.claude/data/shared-knowledge.db`
3. Tables: learned_patterns, preferences, agent_performance

## Tool Capabilities Matrix

| Tool | Best For | Avoid For |
|------|----------|-----------|
| **IDE (mcp__ide__)** | VS Code diagnostics, Python execution | General code operations |
| **Grep** | Fast text search, patterns | Understanding code structure |
| **TodoWrite** | Task tracking, progress | Long-term storage |
| **Task** | Agent delegation, complex ops | Simple single-tool operations |
| **MultiEdit** | Multiple edits in one file | Cross-file changes |
| **NotebookEdit** | Jupyter notebook cells | Regular code files |
| **SQLite (via Bash)** | Persistent knowledge storage | Complex queries |
| **WebSearch** | Current information, research | Specific documentation |
| **WebFetch** | Single page content | Multiple pages |
| **Bash** | System commands, git, SQLite | Complex logic |

## MCP Servers

| Server | Purpose | Current Status |
|--------|---------|----------------|
| **sequential-thinking** | Structured problem solving | ✓ Connected |
| **memory** | Persistent knowledge graph | ✓ Connected |
| **sqlite-knowledge** | Shared database access | Not added (use `claude mcp add`) |
| **exa** | AI-powered semantic search | Not added (requires EXA_API_KEY) |
| **context7** | Documentation lookup | Not added (use `claude mcp add`) |
| **serena** | Semantic code understanding | Not added (use `claude mcp add`) |

**Note:** Server definitions are in `~/.claude/.mcp.json`. Add them with `claude mcp add` command.
**Check status:** `claude mcp list`

## Actually Available MCP Functions in This Session

| Function | Purpose |
|----------|---------|
| **mcp__ide__getDiagnostics** | Get VS Code diagnostics for files |
| **mcp__ide__executeCode** | Execute Python code in Jupyter kernel |

**Note:** The MCP servers in .mcp.json may not be active in Claude Code CLI. See MCP-ACCESS-PROTOCOL.md for how agents should reference these capabilities using standard tools.

## Database Schema

### Key Tables in ~/.claude/data/shared-knowledge.db

- `learned_patterns` - Patterns with score > 21
- `preferences` - User preferences
- `agent_performance` - Agent metrics
- `learning_events` - Captured events
- `agent_messages` - Inter-agent communication
- `tasks` - Task definitions and status

## Rules of Thumb

1. **Team-First** - Always consider delegation to specialist agents
2. **Read First** - Always understand before modifying
3. **Batch Operations** - Use MultiEdit for multiple changes in one file
4. **Check Before Modify** - Always read/understand before editing
5. **Prefer WebSearch/WebFetch** - Over direct MCP calls when available
6. **Memory for Patterns** - Store reusable knowledge with openmemory
7. **Track Progress** - Use TodoWrite for multi-step tasks
8. **Learning is Automatic** - Hooks capture all edits/commands

## Quick Reference

- **Code**: Read > Grep > Edit
- **Edits**: MultiEdit > Edit > Write
- **Files**: Glob > Bash
- **External**: WebSearch > WebFetch
- **Memory**: SQLite (via Bash) > File storage
- **Tasks**: Task (with agent) > TodoWrite > Manual
- **Complex**: Delegate to specialist > Research > Manual

---
*For agent details: `ls ~/.claude/agents/`*
*For preferences: `~/.claude/PREFERENCES.md`*
*For learning health: `/memory`*
