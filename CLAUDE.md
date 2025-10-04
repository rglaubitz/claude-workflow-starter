# CLAUDE.md - Global Claude Code Configuration

## System Overview (v3.0 - Workflow Restructure)
Streamlined Claude Code with explicit approval workflow, C-suite Review Board, and project-specific databases. Major restructure completed 2025-10-01. Full docs: `~/.claude/README.md`

## Available Tools (Priority Order)

### Code Operations
1. **Read/Write/Edit** - Direct file operations
2. **Grep/Glob** - Fast pattern/file search
3. **MultiEdit** - Multiple edits in one file
4. **NotebookEdit** - Jupyter notebook operations

### External Resources
- **WebSearch/WebFetch** - Current information and documentation
- **Bash** - Git operations via `gh` CLI

### System Management
- **Bash** - System commands, SQLite database, git operations
- **TodoWrite** - Task tracking and progress
- **Task** - Delegate to specialist agents

## Commands

### Default Claude Code Commands
- `/help` - Show available commands
- `/clear` - Clear conversation history
- `/compact` - Summarize when context full
- `/agents` - Configure sub-agents
- `/hooks` - Setup pre/post-edit hooks

### Project Workflow Commands (5-Phase System with C-Suite Review Board) ✅ ACTIVE

#### Project Management
- `/start-project <slug>` - Initialize new project (requires project brief)
- `/phase-status [slug]` - Show current phase status and next steps
- `/workflow-dashboard [slug]` - Visual overview of all phases and projects
- `/add-dependency <project> <dep>` - Track Phase 2 dependencies

#### Phase 1: Vision
- `/start-vision` - Create Vision document (what and why)
- `/approve-vision` - Approve Vision and unlock Phase 2

#### Phase 2: Mission
- `/start-mission` - Research technical approach and dependencies
- `/approve-mission` - Approve Mission and unlock Phase 3

#### Phase 3: Execution Planning
- `/start-execution-planning` - Create detailed implementation plan
- `/approve-execution-plan` - Approve plan and proceed to Review Board

#### Phase 3.5: Review Board (C-Suite)
- `/start-review-board` - Convene CIO, CTO, COO for evaluation
- `/approve-review-board` - Accept approval and proceed to implementation
- `/address-review-concerns` - Loop back to revise execution plan

#### Phase 4: Implementation
- `/start-implementation` - Begin building with task-manager orchestration
- `/complete-implementation` - Mark implementation complete and unlock testing

#### Phase 5: Testing
- `/start-testing` - Create and execute comprehensive test plan
- `/approve-testing` - Approve tests and complete project

### Workflow Commands (Planned) 📋 SPECS ONLY
These are documented workflow specifications in `~/.claude/docs/workflows/`. Not yet executable:
- `/build-agent` - Full agent creation pipeline (spec available)
- `/review-all` - Comprehensive parallel review (spec available)
- `/integrate` - Complete integration workflow (spec available)
- `/debug` - Multi-angle debugging approach (spec available)
- `/memory` - Learning system health check (spec available)

## 5-Phase Project Workflow (with C-Suite Review Board)

### Overview
Every Claude Code project follows a structured workflow from idea to deployment with explicit approval gates. Each phase requires user approval before progressing. Phase 3.5 adds a C-suite Review Board quality gate before implementation begins.

### Phase 0: Project Brief (User-Created)
**Purpose:** Define the problem and requirements
**Created By:** User (before starting workflow)
**Template:** `templates/phases/00-project-brief-template.md`
**Requirements:**
- Problem statement and impact
- Goals and success metrics
- Must-have/should-have/nice-to-have features
- Constraints (budget, timeline, technical)
- Reference materials and inspiration
**Command:** None (manual creation required)

### Phase 1: Vision (Brainstorm → Concept → Document)
**Purpose:** Define what we're building and why
**Primary Agents:** prd-expert, agent-architecture-designer
**Deliverable:** `01-vision.md`
**Activities:**
- Analyze project brief
- Define core concepts and value proposition
- Identify problem statement and success criteria
- Define stakeholder requirements
**Commands:** `/start-vision` → `/approve-vision`

### Phase 2: Mission (Research → Dependencies → Technical Plan)
**Purpose:** Determine how to build it
**Primary Agents:** research-manager, documentation-expert
**Deliverable:** `02-mission.md`
**Activities:**
- Research technical approaches and best practices
- Identify ALL dependencies (packages, APIs, services, tools)
- Gather code examples and documentation
- Define architecture and technology stack
**Commands:** `/start-mission` → `/approve-mission`

### Phase 3: Execution Planning (Tasks → Roles → Schedule)
**Purpose:** Plan the implementation in detail
**Primary Agents:** project-task-planner, task-manager
**Deliverable:** `03-execution-plan.md`
**Activities:**
- Break work into detailed, measurable tasks
- Assign specialized agents to each task
- Create realistic timeline with dependencies
- Define quality gates and review checkpoints
**Commands:** `/start-execution-planning` → `/approve-execution-plan`

### Phase 3.5: Review Board (C-Suite Approval Gate) **NEW**
**Purpose:** Executive validation before expensive implementation
**Executives:** CIO (intelligence), CTO (technical), COO (operational)
**Deliverable:** 3 individual review reports + overall verdict
**What's Reviewed:**
- CIO: Research quality, dependencies, documentation, examples
- CTO: Technical architecture, code standards, APIs, feasibility
- COO: Operations, goals, UX/UI, beauty, execution capacity
**Possible Verdicts:**
- ✅ APPROVED: Proceed to Phase 4
- ⚠️ APPROVED_WITH_CONCERNS: Proceed with noted concerns
- ❌ REJECTED: Loop back to Phase 3 for revision
**Commands:** `/start-review-board` → `/approve-review-board` OR `/address-review-concerns`

### Phase 4: Implementation (Build It)
**Purpose:** Execute the approved plan
**Primary Agent:** task-manager (orchestrator)
**Deliverable:** `04-implementation-report.md`
**Activities:**
- Execute all tasks from Execution Plan
- Deploy specialized agents as assigned
- Track real-time progress with TodoWrite
- Code review as work completes
- Handle blockers and adapt
**Commands:** `/start-implementation` → `/complete-implementation`

### Phase 5: Testing (Validation → Quality Gates)
**Purpose:** Validate implementation meets requirements
**Primary Agent:** agent-testing-engineer, qa-engineer
**Deliverable:** `05-test-plan.md`
**Activities:**
- Create comprehensive test plan
- Execute tests (unit, integration, E2E, performance, security)
- Bug fixing and iteration
- Validate against original Vision goals
**Commands:** `/start-testing` → `/approve-testing`
**Completion:** Project fully complete after approval

### Workflow Data Storage
- **Database:** `~/.claude/projects/<slug>/workflow.db` (project-specific, isolated)
- **Documents:** `~/.claude/projects/<slug>/`
- **Templates:** `~/.claude/templates/phases/`
- **Review Board:** `~/.claude/agents/CIO.md`, `CTO.md`, `COO.md`
- **Coordinator:** `~/.claude/scripts/review-board-coordinator.py`

## Agent Roster (32 Specialists)

### Executive Leadership (3 C-suite) **NEW**
- **CIO**: Chief Information Officer - Reviews intelligence, research quality, dependencies, documentation
- **CTO**: Chief Technology Officer - Reviews technical architecture, code quality, APIs, feasibility
- **COO**: Chief Operations Officer - Reviews operations, goal achievement, UX/UI, beauty, execution capacity

### Orchestration & Planning (4 agents)
- **task-manager**: Director of execution, workflow orchestration
- **project-task-planner**: Task breakdown, dependency mapping
- **prd-expert**: PRD creation, requirements specification
- **agent-architecture-designer**: Multi-agent system design

### Core Development (6 agents)
- **database-architect**: Schema design, database optimization
- **graph-database-specialist**: Neo4j, Cypher, GraphRAG systems
- **ai-ml-engineer**: RAG pipelines, embeddings, vector databases
- **frontend-developer**: React, Next.js, modern web apps
- **backend-developer**: APIs, services, business logic
- **devops-engineer**: CI/CD, deployment, infrastructure

### Quality Assurance (4 agents)
- **security-auditor**: Vulnerability scanning, penetration testing
- **performance-engineer**: Optimization, load testing, profiling
- **accessibility-specialist**: WCAG compliance, a11y testing
- **qa-engineer**: Test strategy, quality gates orchestration

### Code Review & Validation (4 agents)
- **code-review-expert**: Parallel code review, deep analysis
- **database-reviewer**: Database design validation
- **frontend-reviewer**: Frontend code quality validation
- **backend-reviewer**: Backend code quality validation

### Specialized Support (7 agents)
- **api-architect**: REST/GraphQL design, API contracts
- **ui-ux-designer**: Design systems, user experience
- **data-pipeline-engineer**: ETL, data processing pipelines
- **knowledge-graph-engineer**: GraphRAG ontologies, entity extraction
- **sql-specialist**: Query optimization, indexing strategies
- **integration-specialist**: API/service integration
- **mcp-bridge-engineer**: MCP server integration

### Research & Documentation (4 agents)
- **research-manager**: Technical research, documentation gathering
- **documentation-expert**: Technical writing, documentation structure
- **agent-testing-engineer**: Agent behavior validation
- **memory-system-engineer**: Knowledge persistence, data storage

## Coding Standards

### Python (Primary Language)
- **Style**: PEP8, black formatter, type hints always
- **Structure**: Max 500 lines/file, modular design
- **Testing**: Pytest in `/tests`, always include edge cases
- **Docs**: Google-style docstrings, `# Reason:` for non-obvious code
- **Validation**: Pydantic for data, python-dotenv for env vars

### Preferences
- **Philosophy**: Simplicity > complexity, practical > theoretical
- **Security**: Pass/GPG for secrets, no overcomplicated systems
- **Communication**: Casual, direct, explain purpose clearly
- **Workflows**: Verify before modify, backup before dangerous ops

## Project Structure (v2.1)
```
~/.claude/           # Global config (persists across ALL projects)
├── README.md        # Comprehensive documentation
├── version.json     # Version tracking (v2.1.0)
├── agents/          # 30 specialized agents (production team)
├── automation/      # Webhooks only
├── backups/         # Automated daily/weekly/monthly
├── commands/        # Archived (custom commands in archived/)
├── docker/          # Docker compose files
├── learning/        # Pattern recognition pipeline
├── logs/            # System, webhook, agent logs
├── memory/          # Archived (content merged here)
├── plugins/         # Ready for MCP extensions
├── projects/        # → Symlink to ~/.cache/claude/projects
├── scripts/         # 21 utility scripts
└── archived/        # Old files for reference
```

## Key Principles & Power Questions

### Team-First Delegation Principle
**"Always look for opportunities to delegate to specialist agents."** Be proactive in identifying tasks that team members can handle better. Every complex task triggers consideration of which agent(s) could best handle it. Context-aware triggering means agents activate based on patterns, not keywords.

### Power Questions
1. **"Which agents could handle this better than me?"** - ALWAYS ASK FIRST
2. **"What tools or approaches did I miss?"** - THE GAME CHANGER
3. **"What would someone smarter than me do here?"** - Step outside current thinking
4. **"What's the 10x solution, not the 10% improvement?"** - Think bigger
5. **"What assumptions am I making that might be wrong?"** - Challenge constraints
6. **"How would I solve this if I had unlimited resources?"** - Think ideal first
7. **Patterns scoring 21+ only** (quality gate)
8. **Clear context between sessions** (`/clear`)

## Research-First Principle ⭐ CRITICAL

**Foundation:** High-quality results come from high-quality research. All decisions must be grounded in current, credible, well-documented sources.

### Research Quality Standards

**Source Hierarchy (highest to lowest priority):**
1. **Official Documentation** - Anthropic docs, Claude docs, framework official sites
2. **Verified GitHub Repositories** - Minimum 1.5k+ stars for alternatives/examples
3. **Technical Standards** - RFCs, W3C specs, academic papers from reputable institutions
4. **Verified Technical Sources** - Known technical blogs (Martin Fowler, etc.), conference talks
5. **Package Registries** - Official npm, PyPI, Maven with verified publishers

**Source Validation Requirements:**
- Documentation must be current (<2 years old OR explicitly verified as still valid)
- GitHub examples must demonstrate the pattern being researched
- All sources must include citations with URLs
- Breaking changes and deprecations must be noted

### Folder Organization Standard

**Every project must follow this structure:**
```
research/
├── documentation/     # Official docs, guides, best practices (saved/linked)
├── examples/          # Code samples from high-quality sources (saved/linked)
├── architecture-decisions/  # ADRs with research citations
└── references.md      # Index of all sources with quality ratings
```

### Research-Before-Action Protocol

**Before any agent executes a task:**
1. Check `research/documentation/` for official guidance
2. Review `research/examples/` for proven patterns
3. Validate approach against research findings
4. Reference sources in implementation decisions

**Quality Gate:** CIO validates research quality during Phase 3.5 Review Board before implementation begins.

## Critical Files
- **Team-First Principle**: See `~/.claude/README.md` for delegation approach
- **Context Triggering**: See `~/.claude/CONTEXT-AWARE-TRIGGERING.md` for patterns
- **Tool Selection**: See `~/.claude/TOOL-SELECTION.md` for decision trees
- **Preferences**: Full details in `~/.claude/PREFERENCES.md`
- **System Docs**: Comprehensive guide in `~/.claude/README.md`

## Quick Actions
```bash
# System health
~/.claude/scripts/health-check-v2.sh

# Create backup
~/.claude/scripts/backup-daily.sh backup

# List agents
python3 ~/.claude/scripts/agent-runner.py list

# View recent webhooks
tail -f ~/.claude/logs/webhooks/*.log
```

## MCP Servers (Profile System)

**Profile-based configuration** - Switch between server sets based on task needs:

### Available Profiles
- **minimal** (default): memory, sqlite-knowledge - Clean context for general tasks
- **research**: + sequential-thinking, exa, context7 - Documentation & web research
- **code-work**: + sequential-thinking, serena - Deep semantic code analysis
- **full**: All servers - Complex multi-faceted tasks

### Profile Management Commands
- `/mcp-status` - Show active servers & available profiles
- `/mcp-profile <name>` - Switch to a profile (requires restart)
- `/serena` - Check/activate Serena (code-work profile)
- `/context7` - Check/activate Context7 (research profile)
- `/exa` - Check/activate Exa (research profile)
- `/think` - Check/activate sequential-thinking

### Profiles Location
`~/.claude/profiles/*.json` - Profile definitions
`<project>/.mcp.json` - Current active profile

**Quick check:** `claude mcp list`
**VS Code integration:** mcp__ide__ functions available

---
*Token-optimized for Claude Code. Full documentation: `~/.claude/README.md`*