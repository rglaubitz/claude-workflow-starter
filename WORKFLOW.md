# 6-Phase Project Workflow System
## Including C-Suite Review Board Quality Gate

## Overview

The 6-Phase Project Workflow System provides a structured approach to building projects in Claude Code. From user-created project brief through C-suite review to final testing, each phase has specific deliverables, assigned agents, and quality gates to ensure successful project completion.

**Philosophy:** Plan thoroughly before executing. Each phase builds on the previous, with explicit user approval required between phases. Phase 3.5 adds a C-suite Review Board quality gate before expensive implementation begins.

**Key Enhancements (v3.1.0):**
- **Explicit Approval Workflow**: No automatic phase transitions
- **Phase 0**: User-created project brief required before Phase 1
- **Phase 3.5**: C-suite Review Board (CIO, CTO, COO) quality gate
- **Project-Specific Databases**: Isolated SQLite database per project
- **Just-in-Time Documents**: Phase documents created only when phase starts
- **Loop-Back Mechanism**: Review Board can reject and return to Phase 3

---

## The 6 Phases

### Phase 0: Project Brief 📝
**User-Created Prerequisite (Before Phase 1)**

**Purpose:** Define the problem, requirements, and constraints before starting the workflow.

**Created By:** User (not Claude)

**Template Location:** `templates/phases/00-project-brief-template.md`

**Required Sections:**
1. **Problem Statement** - What problem are we solving? What's the impact?
2. **Goals & Success Metrics** - What does success look like? How will we measure it?
3. **Requirements** - Must-have, should-have, and nice-to-have features
4. **Constraints** - Budget, timeline, technical, resource limitations
5. **Reference Materials** - Links, examples, inspiration, existing solutions
6. **User Experience** - How should it feel? What's the user journey?
7. **Success Metrics** - KPIs, acceptance criteria, measurable outcomes
8. **Risks & Assumptions** - What could go wrong? What are we assuming?
9. **Stakeholders** - Who cares? Who will use it? Who approves it?
10. **Additional Context** - Anything else we should know?

**Deliverable:** Project brief document
- Location: `~/.claude/projects/<project-slug>/00-project-brief.md`
- Created manually by user following template
- Required before running `/start-project`

**Commands:** None (manual creation)

**Next Phase Unlocks When:** Project brief exists at designated location

---

### Phase 1: Vision 🎯
**Brainstorm → Key Concepts → "The Vision" Document**

**Purpose:** Define what we're building and why it matters.

**Primary Agents:**
- `prd-expert` - Creates the Vision document
- `agent-architecture-designer` - Defines system concepts

**Support Agents:**
- `research-manager` - Initial market/problem research

**Activities:**
1. Brainstorm the core idea
2. Define key concepts and terminology
3. Identify the problem statement
4. Establish success criteria
5. Define stakeholder requirements
6. Document constraints (budget, timeline, technical)
7. List must-have vs. nice-to-have features

**Deliverable:** "The Vision" document
- Location: `~/.claude/projects/<project-slug>/01-vision.md`
- Template: `templates/phases/01-vision-template.md`

**Commands:**
```bash
/start-vision        # Initiates Phase 1, creates Vision document
/approve-vision      # Approves Vision and unlocks Phase 2
```

**Completion Criteria:**
- [ ] Vision document created
- [ ] Problem statement clearly defined
- [ ] Success criteria measurable
- [ ] Stakeholders identified
- [ ] Document approved with `/approve-vision`

**Next Phase Unlocks When:** Vision approved via `/approve-vision` command

---

### Phase 2: Mission 🔬
**Research → Dependencies → Examples → "The Mission" Document**

**Purpose:** Determine how to build it and what we need.

**Primary Agents:**
- `research-manager` - Research technical approaches
- `documentation-expert` - Document findings
- `integration-specialist` - Identify dependencies

**Support Agents:**
- `mcp-bridge-engineer` - MCP server needs

**MCP Tools:**
- `exa` - AI-powered semantic search for examples
- `context7` - Documentation lookup
- `browserbase` - Web research automation

**Activities:**
1. Research technical approaches and best practices
2. Identify ALL dependencies (packages, services, APIs)
3. Gather code examples from similar projects
4. Document architecture decisions
5. Define technology stack
6. Create data models and flow diagrams
7. Document security considerations
8. Plan testing strategy
9. Identify integration points

**Deliverable:** "The Mission" document
- Location: `~/.claude/projects/<project-slug>/02-mission.md`
- Template: `templates/phases/02-mission-template.md`

**Key Sections:**
- Technical Approach
- Architecture Overview
- Technology Stack
- Dependencies & Procurement
- Reference Documentation
- Code Examples
- Implementation Strategy
- Security Considerations

**Commands:**
```bash
/start-mission                                         # Initiates Phase 2, creates Mission document
/add-dependency "<project>" <package> <type> <version> # Track Phase 2 dependencies
/approve-mission                                       # Approves Mission and unlocks Phase 3
```

**Completion Criteria:**
- [ ] Mission document created
- [ ] All dependencies identified and documented
- [ ] Architecture defined
- [ ] Code examples gathered
- [ ] Testing strategy outlined
- [ ] Document approved with `/approve-mission`

**Next Phase Unlocks When:** Mission approved via `/approve-mission` command

---

### Phase 3: Execution Planning 📋
**Planning → Tasks → Roles → "The Execution" Document**

**Purpose:** Create detailed implementation plan.

**Primary Agents:**
- `project-task-planner` - Break work into tasks
- `task-manager` - Assign roles and orchestrate

**Support Agents:**
- `agent-architecture-designer` - Validate architecture

**Activities:**
1. Break work into epics and tasks
2. Define task dependencies
3. Assign agents to specific tasks
4. Create timeline and milestones
5. Identify parallel execution opportunities
6. Define quality gates
7. Create dependency graph
8. Plan sprint/iteration structure
9. Define handoff protocols
10. Establish progress tracking

**Deliverable:** "The Execution Plan" document
- Location: `~/.claude/projects/<project-slug>/03-execution-plan.md`
- Template: `templates/phases/03-execution-plan-template.md`

**Key Sections:**
- Work Breakdown Structure
- Task List with Dependencies
- Agent Assignment Matrix
- Sprint/Milestone Plan
- Parallel Execution Opportunities
- Critical Path Analysis
- Quality Gates
- Communication & Coordination

**Commands:**
```bash
/start-execution-planning    # Initiates Phase 3, creates Execution Plan
/approve-execution-plan      # Approves plan and proceeds to Review Board (Phase 3.5)
```

**Completion Criteria:**
- [ ] Execution document created
- [ ] All tasks defined with estimates
- [ ] Agents assigned to tasks
- [ ] Dependencies mapped
- [ ] Timeline created
- [ ] Quality gates defined
- [ ] Document approved with `/approve-execution-plan`

**Next Phase Unlocks When:** Execution plan approved via `/approve-execution-plan`, then proceeds to Phase 3.5 (Review Board)

---

### Phase 3.5: Review Board 🔍
**C-Suite Executive Approval Gate (Quality Gate Before Implementation)**

**Purpose:** Executive validation before expensive implementation begins. Prevents costly rework by catching issues early.

**Primary Agents (3 C-suite Executives):**
- **CIO** (Chief Information Officer): Reviews intelligence, research quality, dependencies, documentation
- **CTO** (Chief Technology Officer): Reviews technical architecture, code approach, APIs, feasibility
- **COO** (Chief Operations Officer): Reviews operational capacity, goal achievement, UX/UI, beauty

**Activities:**
1. **CIO Review**: Validates mission research supports execution plan
   - Are all dependencies identified and documented?
   - Is research complete with examples and references?
   - Do we have the documentation we need?
   - Are UI/UX preferences captured?

2. **CTO Review**: Validates technical soundness of execution plan
   - Is the architecture feasible?
   - Are the APIs well-designed?
   - Is the code approach solid?
   - Can we actually build this?

3. **COO Review**: Validates plan achieves project goals
   - Does this accomplish the original goals?
   - Will users actually use it?
   - Is it beautiful and well-designed?
   - Do we have capacity to execute?

**Deliverables:**
- 3 individual executive review reports
- Consolidated verdict with recommendations
- Location: `~/.claude/projects/<project-slug>/review-board/session-<N>/`

**Possible Verdicts:**
- ✅ **APPROVED**: All executives approve, proceed to Phase 4 (Implementation)
- ⚠️ **APPROVED_WITH_CONCERNS**: Proceed with noted concerns to address during implementation
- ❌ **REJECTED**: Significant issues found, loop back to Phase 3 for revision

**Commands:**
```bash
/start-review-board          # Convene CIO, CTO, COO for evaluation
/approve-review-board        # Accept approval and proceed to Phase 4
/address-review-concerns     # Accept rejection and loop back to Phase 3
```

**Loop-Back Mechanism:**
- If verdict is **REJECTED** and user runs `/address-review-concerns`:
  - Returns to Phase 3 (Execution Planning)
  - Execution plan must be revised based on feedback
  - Must re-approve execution plan
  - Must convene new Review Board session
- Loop continues until **APPROVED** or **APPROVED_WITH_CONCERNS**

**Completion Criteria:**
- [ ] All 3 executives have submitted reviews
- [ ] Consolidated verdict issued
- [ ] User has reviewed findings
- [ ] User has run `/approve-review-board` (if approved) OR `/address-review-concerns` (if rejected)

**Next Phase Unlocks When:**
- Review Board verdict is **APPROVED** or **APPROVED_WITH_CONCERNS**
- User runs `/approve-review-board` command

---

### Phase 4: Execute ⚡
**Implementation**

**Purpose:** Build the project according to the plan.

**Primary Agent:**
- `task-manager` - Orchestrates entire execution

**All Agents Available:**
- Deploy based on task assignments from Execution document
- Agents work in parallel when possible
- Automatic handoffs between agents

**Specialist Team Assignments by Project Type:**

*Database Projects:*
- `database-architect` - Schema design, optimization
- `sql-specialist` - Query optimization, indexing
- `database-reviewer` - Schema validation
- `performance-engineer` - Database tuning
- `security-auditor` - Access control validation

*GraphRAG/Neo4j Projects:*
- `graph-database-specialist` - Neo4j, Cypher queries
- `ai-ml-engineer` - RAG pipelines, embeddings
- `knowledge-graph-engineer` - Ontology design, entity extraction
- `data-pipeline-engineer` - Graph ingestion pipelines
- `performance-engineer` - Query optimization

*Website Projects:*
- `frontend-developer` - React, Next.js implementation
- `ui-ux-designer` - Design systems, user flows
- `frontend-reviewer` - Code quality validation
- `accessibility-specialist` - WCAG compliance
- `performance-engineer` - Core Web Vitals optimization

*Application Projects:*
- `backend-developer` - API, services, business logic
- `api-architect` - REST/GraphQL design
- `backend-reviewer` - Code quality validation
- `devops-engineer` - Deployment, infrastructure
- `security-auditor` - Security validation

*Cross-Project Support:*
- `code-review-expert` - Reviews all code changes
- `integration-specialist` - API/service integration
- `documentation-expert` - Maintains documentation
- `qa-engineer` - Quality orchestration

**Activities:**
1. Review Execution plan
2. Set up development environment
3. Implement tasks according to plan
4. Track progress in TodoWrite
5. Handle blockers and adapt
6. Code review for each change
7. Update documentation
8. Monitor quality metrics
9. Regular status updates
10. Coordinate agent handoffs

**Deliverable:** Implementation Report
- Location: `~/.claude/projects/<project-slug>/04-implementation-report.md`
- Template: `templates/phases/04-implementation-report-template.md`
- Documents: task progress, code changes, reviews, quality metrics, decisions, challenges

**Commands:**
```bash
/start-implementation        # Initiates Phase 4, begins building
/complete-implementation     # Marks implementation complete and unlocks Phase 5
```

**Progress Tracking:**
- Use TodoWrite for task status
- Update task status in workflow database
- Regular check-ins with task-manager
- Update implementation report continuously

**Completion Criteria:**
- [ ] All tasks from Execution plan completed
- [ ] All code reviewed and approved
- [ ] Documentation updated
- [ ] No critical bugs
- [ ] Implementation report complete
- [ ] Ready for testing
- [ ] User runs `/complete-implementation`

**Next Phase Unlocks When:** Implementation complete via `/complete-implementation` command

---

### Phase 5: Testing ✅
**Validation → Quality Gates → Test Report**

**Purpose:** Ensure quality and validate against requirements.

**Primary Agent:**
- `agent-testing-engineer` - Comprehensive testing
- `qa-engineer` - Quality orchestration and test strategy

**Quality Gate Specialists (6 validation layers):**
- `code-review-expert` - Final code review
- `security-auditor` - Security vulnerability scanning
- `performance-engineer` - Performance benchmarking and optimization
- `accessibility-specialist` - WCAG compliance validation
- `frontend-reviewer` - Frontend code quality (if applicable)
- `backend-reviewer` - Backend code quality (if applicable)
- `database-reviewer` - Database design validation (if applicable)

**Activities:**
1. Create comprehensive test plan
2. Execute unit tests
3. Execute integration tests
4. Execute system/E2E tests
5. Performance testing
6. Security testing
7. Accessibility testing (if applicable)
8. Bug fixing and iteration
9. Regression testing
10. Validate against Vision requirements
11. Final quality gate checks

**Deliverable:** Test Report & Test Plan
- Location: `~/.claude/projects/<project-slug>/05-test-plan.md`
- Template: `templates/phases/05-test-plan-template.md`

**Commands:**
```bash
/start-testing        # Initiates Phase 5, creates test plan
/approve-testing      # Approves tests and completes project
```

**Test Levels:**
- Unit Testing (target 80%+ coverage)
- Integration Testing
- System/E2E Testing
- Performance Testing
- Security Testing
- Regression Testing

**Completion Criteria:**
- [ ] Test plan created and executed
- [ ] All test suites passing (unit, integration, E2E)
- [ ] Code coverage meets target (80%+)
- [ ] Zero critical bugs
- [ ] Code review approved (code-review-expert)
- [ ] Security audit passed (security-auditor)
- [ ] Performance benchmarks met (performance-engineer)
- [ ] Accessibility compliance verified (accessibility-specialist - if web project)
- [ ] All specialist reviews approved
- [ ] All Vision requirements validated
- [ ] User runs `/approve-testing`

**Project Complete When:** All quality gates passed and user runs `/approve-testing`

---

## Workflow Commands

All commands now require explicit user approval between phases. No automatic progression.

### Project Management Commands

**Initialize New Project**
```bash
/start-project "<project-slug>"
```
- Requires project brief at `~/.claude/projects/<slug>/00-project-brief.md`
- Creates project-specific database (`workflow.db`)
- Sets up project folder structure
- Initializes workflow state

**Check Status**
```bash
/phase-status [project-slug]
```
- Shows current phase and status
- Lists deliverables and their status
- Shows active tasks and assigned agents
- Highlights blockers
- Shows clear next steps

**View Dashboard**
```bash
/workflow-dashboard [project-slug]
```
- Visual overview of all 6 phases (including Review Board)
- Progress indicators and deliverable status
- Review Board verdicts
- Timeline information
- If no project specified, shows all projects

### Phase-Specific Commands

**Phase 1: Vision**
```bash
/start-vision              # Create Vision document
/approve-vision            # Approve and unlock Phase 2
```

**Phase 2: Mission**
```bash
/start-mission             # Create Mission document
/add-dependency <project> <dep> <type> <version>  # Track dependencies
/approve-mission           # Approve and unlock Phase 3
```

**Phase 3: Execution Planning**
```bash
/start-execution-planning  # Create Execution Plan
/approve-execution-plan    # Approve and proceed to Review Board
```

**Phase 3.5: Review Board**
```bash
/start-review-board        # Convene CIO, CTO, COO
/approve-review-board      # Accept approval, proceed to Phase 4
/address-review-concerns   # Accept rejection, return to Phase 3
```

**Phase 4: Implementation**
```bash
/start-implementation      # Begin building
/complete-implementation   # Mark complete, unlock Phase 5
```

**Phase 5: Testing**
```bash
/start-testing             # Create test plan
/approve-testing           # Approve tests, complete project
```

---

## Data Storage

### SQLite Database (Project-Specific)
**Location:** `~/.claude/projects/<project-slug>/workflow.db`

Each project has its own isolated database to prevent cross-project contamination.

**Tables:**
- `workflow` - Project state and current phase
- `deliverables` - Document tracking with approval status
- `review_board_sessions` - C-suite review tracking
- `review_board_findings` - Individual executive reviews
- `tasks` - Task assignments and status
- `agent_assignments` - Phase-specific agent assignments

**Created via:** `python3 ~/.claude/scripts/init-project-database.py <slug>`

### Documents
**Location:** `~/.claude/projects/<project-slug>/`

**Structure:**
```
<project-slug>/
├── workflow.db                   # Project-specific database
├── 00-project-brief.md           # Phase 0 (user-created)
├── 01-vision.md                  # Phase 1
├── 02-mission.md                 # Phase 2
├── 03-execution-plan.md          # Phase 3
├── 04-implementation-report.md   # Phase 4 (NEW in v3.1.0)
├── 05-test-plan.md               # Phase 5
├── research/                     # Research findings
│   ├── README.md
│   ├── technical-research.md
│   ├── architecture-decisions.md
│   ├── dependencies.md
│   └── references.md
├── examples/                     # Code samples
│   ├── README.md
│   ├── code-samples/
│   └── reference-implementations/
├── review-board/                 # C-suite review (NEW in v3.1.0)
│   └── session-<N>/
│       ├── cio-review.md
│       ├── cto-review.md
│       ├── coo-review.md
│       └── consolidated-verdict.md
└── agent-notes/                  # Agent collaboration
    ├── communication-log.md
    └── decisions-log.md
```

### Templates
**Location:** `~/.claude/templates/`

**Reorganized Structure (v3.1.0):**
```
templates/
├── phases/                       # Phase deliverable templates
│   ├── 00-project-brief-template.md
│   ├── 01-vision-template.md
│   ├── 02-mission-template.md
│   ├── 03-execution-plan-template.md
│   ├── 04-implementation-report-template.md
│   └── 05-test-plan-template.md
├── supporting/                   # Research, examples, agent notes
│   ├── research/
│   ├── examples/
│   └── agent-notes/
└── review-board/                 # C-suite review checklists
    ├── checklists/
    │   ├── cio-checklist.md
    │   ├── cto-checklist.md
    │   └── coo-checklist.md
    └── reports/
```

---

## Workflow Coordinator

### Python Script
**Location:** `~/.claude/scripts/workflow-coordinator.py`

**Capabilities:**
- Create workflows
- Track phase state
- Manage deliverables
- Assign tasks
- Validate phase completion
- Transition between phases

**CLI Usage:**
```bash
# Create new workflow
python3 workflow-coordinator.py create "Project Name"

# List all workflows
python3 workflow-coordinator.py list

# Show workflow status
python3 workflow-coordinator.py status <workflow-id>

# Transition phase
python3 workflow-coordinator.py transition <workflow-id>
```

---

## Phase-Agent Mapping

### Phase 1: Vision
- **Primary:** prd-expert, agent-architecture-designer
- **Support:** research-manager

### Phase 2: Mission
- **Primary:** research-manager, documentation-expert
- **Support:** integration-specialist, mcp-bridge-engineer

### Phase 3: Execution Planning
- **Primary:** project-task-planner, task-manager
- **Support:** agent-architecture-designer

### Phase 4: Execute
- **Primary:** task-manager (orchestrator)
- **All:** Deployed based on task assignments

### Phase 5: Testing
- **Primary:** agent-testing-engineer
- **Support:** code-review-expert

---

## Quality Gates

### Phase 0 → Phase 1
- [ ] Project brief exists at `~/.claude/projects/<slug>/00-project-brief.md`
- [ ] All required sections completed
- [ ] User runs `/start-project "<slug>"`

### Phase 1 → Phase 2
- [ ] Vision document created
- [ ] Problem clearly defined
- [ ] Success criteria measurable
- [ ] User runs `/approve-vision`

### Phase 2 → Phase 3
- [ ] Mission document created
- [ ] All dependencies identified
- [ ] Architecture defined
- [ ] User runs `/approve-mission`

### Phase 3 → Phase 3.5 (Review Board)
- [ ] Execution plan created
- [ ] All tasks defined with agents assigned
- [ ] Timeline created
- [ ] User runs `/approve-execution-plan`

### Phase 3.5 → Phase 4 (or loop back to Phase 3)
- [ ] All 3 executives have submitted reviews
- [ ] Consolidated verdict issued
- [ ] If **APPROVED** or **APPROVED_WITH_CONCERNS**: User runs `/approve-review-board`
- [ ] If **REJECTED**: User runs `/address-review-concerns` (returns to Phase 3)

### Phase 4 → Phase 5
- [ ] All execution tasks completed
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Implementation report complete
- [ ] No critical bugs
- [ ] User runs `/complete-implementation`

### Phase 5 → Complete
- [ ] Test plan executed
- [ ] All tests passing
- [ ] Coverage targets met
- [ ] Performance requirements met
- [ ] Security validated
- [ ] Vision requirements met
- [ ] User runs `/approve-testing`

---

## Best Practices

### Planning
- Spend adequate time in Phases 1-3
- Don't rush to implementation
- Thorough planning saves execution time
- Validate assumptions early

### Documentation
- Keep deliverable documents updated
- Link between phase documents using [[wiki-style]] links
- Use any markdown editor (VS Code, vim, or Obsidian)
- Version control in Git (everything in `~/.claude/`)

### Agent Coordination
- Let task-manager orchestrate Phase 4
- Trust agent specializations
- Clear handoff protocols
- Regular status updates

### Quality
- Don't skip quality gates
- Test throughout, not just Phase 5
- Code review everything
- Validate against Vision regularly

### Iteration
- Phases are not strictly linear
- Can return to earlier phases if needed
- Update documents as learnings emerge
- Adapt plan based on reality

---

## Troubleshooting

### "Cannot transition" error
- Run `/phase-status` to see blockers
- Ensure deliverable approved
- Complete all required tasks
- Check quality gate criteria

### Missing documents
- Check `~/.claude/projects/`
- Verify workflow created: `python3 ~/.claude/scripts/workflow-coordinator.py list`
- Manually copy from `~/.claude/templates/`
- Run `/start-project` to create complete structure

### Agent not activating
- Verify agent exists: `python3 ~/.claude/scripts/agent-runner.py list`
- Check phase-agent mapping above
- Task-manager handles orchestration in Phase 4

### Database errors
- Verify database: `ls -la ~/.claude/data/workflow.db`
- Reinitialize if needed: See database schema in workflow-coordinator.py

---

## Examples

### Starting a Feature Project
```bash
# Initialize
/start-project "User Authentication Feature"

# Phase 1: Vision
# Edit Vision document, define requirements
# Approve when ready

# Transition to Phase 2
/start-mission

# Phase 2: Mission
# Research OAuth libraries
/add-dependency "User Authentication Feature" "authlib" "python" "1.2.0"
# Complete Mission document

# Continue through phases...
```

### Checking Progress
```bash
# Quick status
/phase-status "User Authentication Feature"

# Full dashboard
/workflow-dashboard "User Authentication Feature"

# Database view
python3 ~/.claude/scripts/workflow-coordinator.py status <workflow-id>
```

---

## Integration with Learning System

The workflow system integrates with the learning pipeline:

- **Pattern Recognition:** Learns successful workflows
- **Agent Performance:** Tracks agent effectiveness per phase
- **Time Estimates:** Improves predictions over time
- **Blocker Patterns:** Identifies common issues
- **Best Practices:** Codifies what works

**Memory MCP stores:**
- Workflow definitions
- Phase requirements
- Agent assignments
- Quality gates
- Success patterns

---

## Version History

- **v3.1.0** (2025-10-01) - Workflow restructure with explicit approval gates
  - Added Phase 0 (Project Brief - user-created)
  - Added Phase 3.5 (Review Board - CIO, CTO, COO)
  - Created 14 phase-specific commands
  - Project-specific databases (isolated per project)
  - Template reorganization (phases/, supporting/, review-board/)
  - Added Phase 4 deliverable (implementation report)
  - Explicit approval workflow (no auto-progression)
  - Loop-back mechanism for rejected plans

- **v1.0** (2025-09-29) - Initial workflow implementation
  - All components operational
  - Templates created
  - Commands implemented
  - Documentation complete

---

## Related Documentation

- **CLAUDE.md** - Main configuration with workflow overview
- **CONTEXT-AWARE-TRIGGERING.md** - Agent activation patterns
- **agents/** - Individual agent capabilities
- **templates/** - Phase document templates

---

**The 5-Phase Workflow transforms Claude Code from a tool into a complete project delivery system.**