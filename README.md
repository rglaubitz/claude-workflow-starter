# Claude 5-Phase Workflow Starter

> **The workflow infrastructure for Claude Code projects**

Transform your Claude Code experience with a structured 5-phase workflow and C-suite Review Board. This system provides the templates, commands, and scripts to orchestrate professional-grade projects from concept to deployment.

> **Looking for specialist agents?** See [claude-agents](https://github.com/rglaubitz/claude-agents) - 42+ agents to import as needed
>
> **Architecture details:** See [ARCHITECTURE.md](./ARCHITECTURE.md)

## 🎯 What You Get

- **5-Phase Workflow System**: Vision → Mission → Execution Planning → Review Board → Implementation → Testing
- **3 C-Suite Agents**: CIO, CTO, and COO (Review Board executives)
- **42+ Specialist Agents**: Import from [claude-agents](https://github.com/rglaubitz/claude-agents) library as needed
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

### Specialist Agents (Import from Library)

**42+ specialist agents** are available in the [claude-agents](https://github.com/rglaubitz/claude-agents) library. During Phase 3 (Execution Planning), you'll identify which agents your project needs and import them.

**Agent Categories:**
- **Orchestration (4):** task-manager, project-task-planner, prd-expert, agent-architecture-designer
- **Development (6):** database-architect, graph-database-specialist, ai-ml-engineer, frontend-developer, backend-developer, devops-engineer
- **Quality (4):** security-auditor, performance-engineer, accessibility-specialist, qa-engineer
- **Research (17):** research-manager, deep-researcher, documentation-expert, + 14 specialists ⭐
- **Review (4):** code-review-expert, database-reviewer, frontend-reviewer, backend-reviewer
- **Support (7):** api-architect, ui-ux-designer, data-pipeline-engineer, knowledge-graph-engineer, sql-specialist, integration-specialist, mcp-bridge-engineer

**You don't need all 42** - import only what your project requires.

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
