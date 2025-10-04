# Claude 5-Phase Workflow Starter

> **The workflow infrastructure for Claude Code projects**

Transform your Claude Code experience with a structured 5-phase workflow and C-suite Review Board. This system provides the templates, commands, and scripts to orchestrate professional-grade projects from concept to deployment.

> **Looking for specialist agents?** See [claude-agents](https://github.com/rglaubitz/claude-agents) - 47 agents to import as needed
>
> **Architecture details:** See [ARCHITECTURE.md](./ARCHITECTURE.md)

## 🎯 What You Get

- **5-Phase Workflow System**: Vision → Mission → Execution Planning → Review Board → Implementation → Testing
- **3 C-Suite Agents**: CIO, CTO, and COO (Review Board executives)
- **47 Specialist Agents**: Import from [claude-agents](https://github.com/rglaubitz/claude-agents) library as needed
- **20 Slash Commands**: Full workflow orchestration at your fingertips
- **6 Phase Templates**: Professional documentation from day one
- **Automation Scripts**: Database initialization, health checks, workflow coordination
- **MCP Server Support**: Memory and knowledge persistence

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-workflow-starter.git
cd claude-workflow-starter

# Run the installation script
./scripts/setup.sh

# Create your first project
mkdir -p ~/.claude/projects/my-first-project
cp ~/.claude/templates/phases/00-project-brief-template.md \
   ~/.claude/projects/my-first-project/00-project-brief.md

# Fill out the project brief, then start the workflow
# In Claude Code:
/start-project my-first-project
```

That's it! You're ready to build with the full power of structured workflows.

## 📋 Features

### The 5-Phase Workflow

Every project follows a structured path with explicit approval gates:

**Phase 0: Project Brief** (User-Created)
- Define the problem and requirements
- Set goals and success metrics
- Identify constraints and inspiration

**Phase 1: Vision** (Brainstorm → Concept → Document)
- Define what you're building and why
- Identify stakeholder requirements
- Document core value proposition
- **Command**: `/start-vision` → `/approve-vision`

**Phase 2: Mission** (Research → Dependencies → Technical Plan)
- Research technical approaches
- Identify ALL dependencies
- Gather code examples and documentation
- Define architecture
- **Command**: `/start-mission` → `/approve-mission`

**Phase 3: Execution Planning** (Tasks → Roles → Schedule)
- Break work into detailed tasks
- Assign specialized agents
- Create realistic timeline
- Define quality gates
- **Command**: `/start-execution-planning` → `/approve-execution-plan`

**Phase 3.5: Review Board** (C-Suite Approval Gate) ⭐ **NEW**
- **CIO**: Reviews research quality, dependencies, documentation
- **CTO**: Reviews technical architecture, code standards, feasibility
- **COO**: Reviews operations, goals, UX/UI, execution capacity
- **Verdicts**: APPROVED / APPROVED_WITH_CONCERNS / REJECTED
- **Command**: `/start-review-board` → `/approve-review-board` OR `/address-review-concerns`

**Phase 4: Implementation** (Build It)
- Execute the approved plan
- Deploy specialized agents as assigned
- Track real-time progress
- Code review as work completes
- **Command**: `/start-implementation` → `/complete-implementation`

**Phase 5: Testing** (Validation → Quality Gates)
- Create comprehensive test plan
- Execute all tests
- Bug fixing and iteration
- Validate against Vision goals
- **Command**: `/start-testing` → `/approve-testing`

### C-Suite Review Board (Included)

**Executive Leadership (3 agents):**
- **CIO** - Intelligence, research quality, dependencies
- **CTO** - Technical architecture, code quality, APIs
- **COO** - Operations, goals, UX/UI, beauty

These 3 C-suite agents are included as they're integral to the Review Board (Phase 3.5) workflow.

### Phase 4 Execution Team (Included) ⭐ **NEW**

**The Professional Implementation Team (5 agents):**

Phase 4 uses a dedicated **Execution Team** with 5 specialists who take over from the Planning Team after Review Board approval. This mirrors professional software teams with field leadership, handoff coordination, quality enforcement, problem solving, and progress tracking.

**execution-director** - Field Commander
- Orchestrates all tactical execution during Phase 4
- Commands 7 agent teams (Foundation, Backend, Frontend, Research, Quality, Integration, Orchestration)
- Makes real-time tactical decisions (priority adjustment, resource reallocation)
- Receives formal handoff from task-manager at Phase 3→4 transition

**delivery-coordinator** - Handoff Manager
- Manages all team-to-team handoffs with 10-step protocol
- Validates handoff packages before confirming transfer
- Logs all communications to SQLite database
- Runs daily async standups to sync teams
- Identifies bottlenecks in coordination

**quality-enforcer** - Gate Keeper with Blocking Authority
- Enforces quality gates at 4 levels (task, feature, epic, phase)
- **Has absolute blocking authority** - work cannot progress if gates fail
- Deploys review agents (code-review-expert, security-auditor, etc.)
- Creates remediation tasks for failed checks
- Validates SOP compliance across all teams

**blocker-resolver** - 5-Level Escalation Problem Solver
- Rapid blocker resolution with escalation protocol
- L1 (agent 0-1h) → L2 (resolver 1-4h) → L3 (specialist 4-8h) → L4 (director 8+h) → L5 (critical path/plan revision)
- Pattern-based resolution system (learns from past blockers)
- Proactive blocker detection before critical path impact
- Deploys specialist agents at L3 (database-architect, devops-engineer, etc.)

**progress-tracker** - War Room Dashboard & Metrics
- Maintains real-time war room dashboard (updated hourly)
- Tracks 6 KPIs: tasks on-time %, gate pass rate, blocker resolution time, code review TAT, utilization %, handoff success rate
- Generates daily/weekly status reports
- Calculates buffer consumption and critical path health
- Alert system for timeline/quality risks

**Handoff Protocol:**

When Review Board approves the execution plan, task-manager orchestrates a formal handoff meeting:

**Attendees**: project-task-planner, task-manager → execution-director, delivery-coordinator, quality-enforcer

**9-Point Handoff Agenda**:
1. Execution plan walkthrough
2. Agent team assignments (all 7 teams confirmed)
3. Critical path review
4. Quality gate criteria
5. Communication protocol (TodoWrite + SQLite)
6. Blocker escalation paths (5-level)
7. Success criteria alignment
8. Formal handoff acceptance
9. Phase 4 kickoff authorization

**Communication Infrastructure:**

Initialize the Phase 4 SQLite communication schema:

```bash
python3 ~/.claude/scripts/execution-coordinator.py init <project-name>
```

This creates 10 tables:
- `agent_messages` - Inter-agent communication
- `handoff_log` - Team handoffs with confirmation
- `quality_gates` - Gate enforcement tracking
- `sop_compliance` - SOP violation tracking
- `blockers` - Blocker tracking and resolution
- `blocker_patterns` - Learning from resolutions
- `team_status` - 7 teams initialized with capacity
- `review_deployments` - Review agent tracking
- `team_sync_log` - Daily standups
- `tactical_decisions` - execution-director decisions

**Health Check:**
```bash
python3 ~/.claude/scripts/execution-coordinator.py health <project-name>
```

These 5 execution agents are included in the workflow-starter as they're integral to Phase 4 implementation.

### Specialist Agents (Import from Library)

**47 specialist agents** are available in the [claude-agents](https://github.com/rglaubitz/claude-agents) library. During Phase 3 (Execution Planning), you'll identify which agents your project needs and import them.

**Agent Categories:**
- **Orchestration (9) ⭐ EXPANDED:** Planning Team (task-manager, project-task-planner, prd-expert, agent-architecture-designer) + Execution Team (execution-director, delivery-coordinator, quality-enforcer, blocker-resolver, progress-tracker)
- **Development (6):** database-architect, graph-database-specialist, ai-ml-engineer, frontend-developer, backend-developer, devops-engineer
- **Quality (4):** security-auditor, performance-engineer, accessibility-specialist, qa-engineer
- **Research (17):** research-manager, deep-researcher, documentation-expert, + 14 specialists ⭐
- **Review (4):** code-review-expert, database-reviewer, frontend-reviewer, backend-reviewer
- **Support (7):** api-architect, ui-ux-designer, data-pipeline-engineer, knowledge-graph-engineer, sql-specialist, integration-specialist, mcp-bridge-engineer

**You don't need all 47** - import only what your project requires.

**Example:** Web app might need:
```bash
# From claude-agents library
cp ~/claude-agents/orchestration/task-manager.md ~/.claude/projects/my-app/agents/
cp ~/claude-agents/development/backend-developer.md ~/.claude/projects/my-app/agents/
cp ~/claude-agents/development/frontend-developer.md ~/.claude/projects/my-app/agents/
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for agent import strategies.

## 🛠️ Installation

See [SETUP.md](./SETUP.md) for detailed installation instructions.

**Requirements:**
- Python 3.8+
- SQLite3
- Node.js (for MCP servers)
- Git (optional but recommended)

**Installation:**

```bash
./scripts/setup.sh
```

The installer will:
- ✅ Validate prerequisites
- ✅ Backup existing ~/.claude (if present)
- ✅ Install all components
- ✅ Create directory structure
- ✅ Set up configuration
- ✅ Initialize databases
- ✅ Validate installation

## 📖 Documentation

- **[SETUP.md](./SETUP.md)**: Complete installation guide
- **[ARCHITECTURE.md](./ARCHITECTURE.md)**: System design and architecture
- **[WORKFLOW.md](./WORKFLOW.md)**: Detailed workflow documentation
- **[CLAUDE.md](./CLAUDE.md)**: Main configuration reference
- **[PREFERENCES.md](./PREFERENCES.md)**: Coding standards and philosophy

## 🎮 Usage

### Starting a New Project

1. **Create the project brief:**
   ```bash
   mkdir -p ~/.claude/projects/my-project
   cp ~/.claude/templates/phases/00-project-brief-template.md \
      ~/.claude/projects/my-project/00-project-brief.md
   ```

2. **Fill out the brief** with your project details

3. **Start the workflow** in Claude Code:
   ```
   /start-project my-project
   ```

4. **Follow the phases:**
   - `/start-vision` → Review → `/approve-vision`
   - `/start-mission` → Review → `/approve-mission`
   - `/start-execution-planning` → Review → `/approve-execution-plan`
   - `/start-review-board` → Review → `/approve-review-board`
   - `/start-implementation` → Build → `/complete-implementation`
   - `/start-testing` → Test → `/approve-testing`

### Key Commands

**Project Management:**
- `/start-project <slug>` - Initialize new project
- `/phase-status [slug]` - Show current phase status
- `/workflow-dashboard [slug]` - Visual overview of all phases

**Phase Commands:**
- `/start-vision`, `/approve-vision`
- `/start-mission`, `/approve-mission`
- `/start-execution-planning`, `/approve-execution-plan`
- `/start-review-board`, `/approve-review-board`
- `/start-implementation`, `/complete-implementation`
- `/start-testing`, `/approve-testing`

**Review Board:**
- `/review-board <project>` - Execute Review Board validation
- `/address-review-concerns` - Loop back to revise execution plan

## 🏗️ Project Structure

After installation, your `~/.claude/` directory will contain:

```
~/.claude/
├── CLAUDE.md              # Main configuration
├── PREFERENCES.md         # Coding standards
├── TOOL-SELECTION.md      # Tool decision trees
├── WORKFLOW.md            # Workflow documentation
├── version.json           # System version (v3.1.0)
│
├── agents/                # 32 specialized agents
│   ├── CIO.md, CTO.md, COO.md
│   └── ... (29 more agents)
│
├── commands/              # 20 slash commands
│   ├── start-project.md
│   ├── start-vision.md
│   └── ... (18 more commands)
│
├── templates/phases/      # 6 phase templates
│   ├── 00-project-brief-template.md
│   ├── 01-vision-template.md
│   ├── 02-mission-template.md
│   ├── 03-execution-plan-template.md
│   ├── 04-implementation-report-template.md
│   └── 05-test-plan-template.md
│
├── scripts/               # Automation scripts
│   ├── setup.sh
│   ├── workflow-coordinator.py
│   ├── review-board-coordinator.py
│   ├── execution-coordinator.py
│   └── init-project-database.py
│
├── constitution/          # Agent governance
├── config/                # Configuration files
├── docs/                  # Documentation
└── projects/              # Your projects live here
    └── my-project/
        ├── 00-project-brief.md
        ├── workflow.db
        ├── research/
        ├── examples/
        └── review-board/
```

## 🔧 Configuration

### MCP Servers

The system supports MCP servers for enhanced capabilities:

**Minimal Profile** (default):
- memory: Persistent knowledge graph
- sqlite-knowledge: Shared knowledge base

**Research Profile**:
- memory + sqlite-knowledge
- sequential-thinking: Deep reasoning
- exa: Web search
- context7: Documentation lookup

**Code-Work Profile**:
- memory + sqlite-knowledge
- sequential-thinking
- serena: Semantic code analysis

**Full Profile**:
- All servers enabled

Edit `~/.claude/.mcp.json` to configure.

### Settings

Edit `~/.claude/settings.json` to customize:
- Agent behavior
- Workflow preferences
- Output formatting
- Quality gates

## 🎯 Examples

See the `examples/` directory for complete project examples showing the full workflow in action.

## 🤝 Contributing

This is a starter template. Feel free to:
- Fork and customize for your needs
- Add your own agents
- Create custom commands
- Extend the workflow

## 📝 License

MIT License - see [LICENSE](./LICENSE) for details.

## 🙏 Acknowledgments

Built for Claude Code by the community.

## 📞 Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: See the `docs/` directory
- **Community**: Join discussions in GitHub Discussions

## 🚀 What's Next?

After installation:

1. **Read the workflow documentation**: `~/.claude/WORKFLOW.md`
2. **Explore the agent roster**: `~/.claude/agents/`
3. **Review the constitution**: `~/.claude/constitution/`
4. **Create your first project**: Follow the Quick Start above
5. **Join the community**: Share your experience

---

**Ready to build something amazing? Let's go! 🎉**
