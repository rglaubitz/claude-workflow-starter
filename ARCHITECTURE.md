# System Architecture

Deep dive into the Claude 5-Phase Workflow System architecture, design decisions, and implementation details.

## Table of Contents

1. [Overview](#overview)
2. [Core Components](#core-components)
3. [Workflow Engine](#workflow-engine)
4. [Agent System](#agent-system)
5. [Review Board](#review-board)
6. [Database Architecture](#database-architecture)
7. [Command System](#command-system)
8. [Configuration Management](#configuration-management)
9. [Data Flow](#data-flow)
10. [Design Decisions](#design-decisions)

---

## Overview

The Claude 5-Phase Workflow System is a structured framework for building software projects with Claude Code. It provides:

- **Explicit approval gates** at each phase
- **Specialized agent delegation** for complex tasks
- **C-suite Review Board** quality gate before implementation
- **Project-specific databases** for workflow state
- **Template-driven documentation** at every phase
- **Automated coordination** between agents and phases

### Version

**Current Version**: 3.1.0
**Release Date**: 2025-10-01
**Status**: Production-ready

---

## Core Components

### 1. Configuration Layer

**Files:**
- `CLAUDE.md` - Main system configuration
- `PREFERENCES.md` - Coding standards and philosophy
- `TOOL-SELECTION.md` - Tool decision trees
- `WORKFLOW.md` - Workflow documentation
- `version.json` - Version tracking

**Purpose:**
Defines system behavior, agent roster, available commands, and coding standards. Claude Code reads these files to understand how to operate.

### 2. Agent Library (32 Specialists)

**Location:** `~/.claude/agents/`

**Structure:**
```
agents/
├── CIO.md              # Chief Information Officer
├── CTO.md              # Chief Technology Officer
├── COO.md              # Chief Operations Officer
├── task-manager.md     # Workflow orchestration
├── prd-expert.md       # Requirements specification
└── ... (27 more)
```

Each agent is defined as a markdown file containing:
- **Role description**: What the agent does
- **Responsibilities**: Specific tasks handled
- **Tools available**: Which tools the agent can use
- **Output format**: Expected deliverables
- **Invocation patterns**: When to use this agent

### 3. Command System (20 Slash Commands)

**Location:** `~/.claude/commands/`

Commands orchestrate workflow phases:

**Project Management:**
- `start-project.md` - Initialize new project
- `phase-status.md` - Show current status
- `workflow-dashboard.md` - Visual overview

**Phase Commands:**
- `start-vision.md` / `approve-vision.md`
- `start-mission.md` / `approve-mission.md`
- `start-execution-planning.md` / `approve-execution-plan.md`
- `start-review-board.md` / `approve-review-board.md`
- `start-implementation.md` / `complete-implementation.md`
- `start-testing.md` / `approve-testing.md`

**Review Board:**
- `review-board.md` - Execute Review Board
- `address-review-concerns.md` - Loop back to Phase 3

### 4. Template System

**Location:** `~/.claude/templates/phases/`

Six templates guide documentation:
- `00-project-brief-template.md` - User-created requirements
- `01-vision-template.md` - What and why
- `02-mission-template.md` - How to build it
- `03-execution-plan-template.md` - Detailed implementation plan
- `04-implementation-report-template.md` - Build progress
- `05-test-plan-template.md` - Validation and testing

### 5. Automation Scripts

**Location:** `~/.claude/scripts/`

**Core Scripts:**
- `workflow-coordinator.py` - Orchestrates phase transitions
- `review-board-coordinator.py` - Manages C-suite reviews
- `init-project-database.py` - Creates project databases
- `invoke-specialist-agent.py` - Delegates to agents
- `health-check-v2.sh` - System validation
- `backup-daily.sh` - Automated backups

### 6. Constitution System

**Location:** `~/.claude/constitution/`

Defines agent governance, quality standards, and ethical guidelines.

---

## Workflow Engine

### Phase State Machine

```
┌─────────────────────┐
│  Phase 0: Brief     │ (User-created)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Phase 1: Vision    │ (/start-vision → /approve-vision)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Phase 2: Mission   │ (/start-mission → /approve-mission)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Phase 3: Execution  │ (/start-execution-planning → /approve-execution-plan)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Phase 3.5: Review   │ (/start-review-board)
│       Board         │  ↓                    ↓
└──────────┬──────────┘  APPROVED    REJECTED → Loop back to Phase 3
           │              ↓
           ▼              ▼
┌─────────────────────┐
│ Phase 4: Implement  │ (/start-implementation → /complete-implementation)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Phase 5: Testing   │ (/start-testing → /approve-testing)
└─────────────────────┘
```

### Approval Gates

**Every phase requires explicit user approval before progression.**

**Why?**
- User maintains control
- Can review deliverables at each stage
- Prevents runaway automation
- Ensures understanding before proceeding

### Phase Progression Rules

1. **Sequential only**: Cannot skip phases
2. **Approval required**: Must approve before next phase
3. **Loop-back allowed**: Review Board can reject and send back to Phase 3
4. **State persistence**: All state stored in project database
5. **Idempotent commands**: Can re-run commands safely

---

## Agent System

### Agent Invocation Model

**Direct Invocation:**
```
User → Claude → Agent (via Task tool)
```

**Chained Invocation:**
```
User → Claude → Agent A → Agent B → Agent C → Results
```

**Parallel Invocation:**
```
User → Claude → [Agent A, Agent B, Agent C] → Results
```

### Agent Categories

**1. Executive Leadership (3 agents)**
- **CIO**: Research, dependencies, documentation quality
- **CTO**: Technical architecture, code standards, feasibility
- **COO**: Operations, UX, beauty, execution capacity

**2. Orchestration (4 agents)**
- Coordinate other agents
- Break down complex tasks
- Manage workflows

**3. Core Development (6 agents)**
- Build features
- Write code
- Implement architectures

**4. Quality Assurance (4 agents)**
- Test implementations
- Find vulnerabilities
- Ensure standards

**5. Code Review (4 agents)**
- Review code quality
- Validate designs
- Ensure best practices

**6. Specialized Support (7 agents)**
- Handle specific technical domains
- Provide expert guidance
- Integrate systems

**7. Research & Documentation (4 agents)**
- Gather information
- Document decisions
- Validate approaches

### Agent Communication

**Methods:**
1. **Shared Database**: `~/.claude/data/shared-knowledge.db`
2. **MCP Memory**: Persistent knowledge graph
3. **Project Files**: Write outputs to project directories
4. **Return Messages**: Pass data back through Tool results

---

## Review Board

### Architecture

The Review Board is a quality gate introduced in Phase 3.5, after Execution Planning but before Implementation.

**Purpose:**
Validate that the plan is:
- Well-researched (CIO)
- Technically sound (CTO)
- Operationally feasible (COO)

### Execution Flow

```python
# Pseudocode for Review Board execution

def execute_review_board(project_slug):
    # 1. Load execution plan
    plan = load_execution_plan(project_slug)

    # 2. Invoke C-suite in parallel
    cio_report = invoke_agent("CIO", plan)
    cto_report = invoke_agent("CTO", plan)
    coo_report = invoke_agent("COO", plan)

    # 3. Aggregate findings
    findings = aggregate_reports([cio_report, cto_report, coo_report])

    # 4. Determine verdict
    verdict = determine_verdict(findings)

    # 5. Store in database
    store_review_session(project_slug, findings, verdict)

    # 6. Return verdict
    return verdict  # APPROVED | APPROVED_WITH_CONCERNS | REJECTED
```

### Verdict Logic

**APPROVED**:
- All executives approve with no critical concerns
- Minor concerns noted but non-blocking
- Proceed to Phase 4

**APPROVED_WITH_CONCERNS**:
- Executives have concerns but approve proceeding
- Concerns documented for attention during implementation
- Proceed to Phase 4 with caution

**REJECTED**:
- One or more executives find critical issues
- Cannot proceed to implementation
- Loop back to Phase 3 for revision

### Database Schema

```sql
CREATE TABLE review_board_sessions (
    id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    session_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    overall_verdict TEXT NOT NULL,
    cio_verdict TEXT,
    cto_verdict TEXT,
    coo_verdict TEXT,
    FOREIGN KEY (workflow_id) REFERENCES workflow(id)
);

CREATE TABLE review_board_findings (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    executive TEXT NOT NULL,
    category TEXT NOT NULL,
    severity TEXT NOT NULL,
    finding TEXT NOT NULL,
    recommendation TEXT,
    FOREIGN KEY (session_id) REFERENCES review_board_sessions(id)
);
```

---

## Database Architecture

### Project-Specific Databases

**Location:** `~/.claude/projects/<slug>/workflow.db`

Each project gets its own isolated SQLite database.

**Why?**
- Project independence
- No cross-contamination
- Easy to backup/restore individual projects
- Simple to delete projects

### Schema

```sql
-- Main workflow state
CREATE TABLE workflow (
    id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_slug TEXT NOT NULL UNIQUE,
    current_phase TEXT NOT NULL,
    phase_number INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME
);

-- Phase deliverables
CREATE TABLE deliverables (
    id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    phase_number INTEGER NOT NULL,
    deliverable_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_at DATETIME,
    FOREIGN KEY (workflow_id) REFERENCES workflow(id)
);

-- Review Board sessions
CREATE TABLE review_board_sessions (
    id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    session_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    overall_verdict TEXT NOT NULL,
    cio_verdict TEXT,
    cto_verdict TEXT,
    coo_verdict TEXT,
    FOREIGN KEY (workflow_id) REFERENCES workflow(id)
);

-- Review Board findings
CREATE TABLE review_board_findings (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    executive TEXT NOT NULL,
    category TEXT NOT NULL,
    severity TEXT NOT NULL,
    finding TEXT NOT NULL,
    recommendation TEXT,
    FOREIGN KEY (session_id) REFERENCES review_board_sessions(id)
);

-- Task tracking (Phase 4)
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    task_name TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    assigned_agent TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (workflow_id) REFERENCES workflow(id)
);

-- Agent assignments
CREATE TABLE agent_assignments (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    result TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
```

### Shared Knowledge Database

**Location:** `~/.claude/data/shared-knowledge.db`

Persistent knowledge shared across all projects.

**Schema:**
```sql
CREATE TABLE memo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    insight TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Usage:**
- Cross-project learnings
- Agent communication
- Pattern recognition
- Best practices

---

## Command System

### Command Definition Format

Each command is a markdown file with YAML frontmatter:

```markdown
---
description: "Command description"
argument-hint: "<required-arg> [optional-arg]"
allowed-tools: Bash, Read, Write, Task
---

# Command Name: $ARGUMENTS

Your task description here...

1. Step 1
2. Step 2
3. Step 3
```

### Command Execution

```
User types: /start-vision

↓

Claude Code reads: ~/.claude/commands/start-vision.md

↓

Claude executes the instructions with tools

↓

Results returned to user
```

### Command Categories

**1. Project Management**
- Initialize projects
- Check status
- View dashboards

**2. Phase Commands**
- Start phases
- Approve phases
- Transition between phases

**3. Review Board**
- Convene executives
- Handle verdicts
- Address concerns

**4. Utility**
- Add dependencies
- Check health
- Run backups

---

## Configuration Management

### Configuration Hierarchy

```
1. Global Config (~/.claude/CLAUDE.md)
   ↓
2. Project Config (~/Projects/project/CLAUDE.md)
   ↓
3. User Preferences (~/.claude/PREFERENCES.md)
   ↓
4. MCP Configuration (~/.claude/.mcp.json)
   ↓
5. Settings (~/.claude/settings.json)
```

Later configurations can override earlier ones.

### MCP Profiles

**Profile System:**
- **minimal**: memory + sqlite-knowledge
- **research**: minimal + sequential-thinking + exa + context7
- **code-work**: minimal + sequential-thinking + serena
- **full**: All servers

**Switching:**
```bash
# Edit .mcp.json to include desired servers
# Restart Claude Code
```

---

## Data Flow

### Project Creation Flow

```
1. User creates project brief
   ↓
2. /start-project <slug>
   ↓
3. init-project-database.py creates workflow.db
   ↓
4. Project structure created
   ↓
5. Workflow state initialized
   ↓
6. Ready for Phase 1
```

### Phase Execution Flow

```
1. User runs /start-<phase>
   ↓
2. Command reads workflow state from database
   ↓
3. Validates prerequisites (previous phase approved)
   ↓
4. Invokes appropriate agents
   ↓
5. Agents produce deliverables
   ↓
6. Deliverables written to project directory
   ↓
7. Database updated with deliverable paths
   ↓
8. User reviews and approves
   ↓
9. /approve-<phase> updates workflow state
   ↓
10. Next phase unlocked
```

### Review Board Flow

```
1. /start-review-board
   ↓
2. Load execution plan from Phase 3
   ↓
3. Invoke CIO, CTO, COO in parallel (via review-board-coordinator.py)
   ↓
4. Each executive reviews plan independently
   ↓
5. Reports aggregated
   ↓
6. Verdict determined
   ↓
7. Findings stored in database
   ↓
8. User receives verdict
   ↓
9. If APPROVED → Proceed to Phase 4
   If REJECTED → /address-review-concerns loops back to Phase 3
```

---

## Design Decisions

### Why Project-Specific Databases?

**Before v3.0**: Single shared database for all projects
**After v3.0**: Isolated database per project

**Reasons:**
1. **Isolation**: Projects don't interfere with each other
2. **Simplicity**: Easy to understand one project's state
3. **Portability**: Can move/backup individual projects
4. **Performance**: Smaller databases = faster queries
5. **Cleanup**: Delete project = delete database

### Why C-Suite Review Board?

**Problem**: Teams were implementing plans that were:
- Under-researched
- Technically flawed
- Operationally infeasible

**Solution**: Add quality gate with specialized executives before implementation.

**Result**: Catch issues early, before expensive implementation phase.

### Why Explicit Approval Gates?

**Problem**: Automated workflows ran too far without user oversight.

**Solution**: Require user approval at every phase.

**Result**: User maintains control and understanding throughout.

### Why Markdown for Agents/Commands?

**Pros:**
- Human-readable
- Easy to edit
- Version-controllable
- No compilation needed
- Claude can parse directly

**Cons:**
- Less structured than JSON/YAML
- No schema validation

**Decision**: Readability and editability outweigh cons.

### Why 32 Agents?

**Coverage**: Sufficient to handle most software development scenarios:
- Planning: 4 agents
- Development: 6 agents
- QA: 4 agents
- Review: 4 agents
- Support: 7 agents
- Research: 4 agents
- Leadership: 3 agents

**Not too many**: System remains manageable.
**Not too few**: Sufficient specialization.

---

## Future Architecture Considerations

### Potential Enhancements

1. **Agent Skill Levels**: Novice, Intermediate, Expert versions
2. **Custom Agents**: User-defined specialists
3. **Phase Plugins**: Community-contributed phase definitions
4. **Multi-Project Workflows**: Dependencies between projects
5. **Real-Time Collaboration**: Multiple users on same project
6. **Agent Learning**: Pattern recognition and adaptation
7. **Visual Workflow Editor**: GUI for workflow customization

### Scalability

Current design scales to:
- **100+ projects** without performance issues
- **Thousands of tasks** per project
- **Gigabytes** of project data

Limitations:
- SQLite (single-writer) limits concurrent modifications
- File-based agents don't scale to 1000+ agents

---

## Conclusion

The Claude 5-Phase Workflow System provides a structured, scalable framework for building software projects with Claude Code. Its architecture emphasizes:

- **Clarity**: Easy to understand and modify
- **Control**: User approval at every step
- **Quality**: C-suite review before implementation
- **Extensibility**: Easy to add agents and commands
- **Simplicity**: Minimal dependencies, straightforward design

**Ready to build amazing things! 🚀**
