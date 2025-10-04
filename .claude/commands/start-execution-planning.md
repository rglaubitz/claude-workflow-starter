---
description: "Begin Phase 3 (Execution Planning) - Create detailed implementation plan"
allowed-tools: Task, Bash, Write, Read
---

# Phase 3: Start Execution Planning

You are initiating **Phase 3: Execution Planning** of the 5-phase workflow.

## Prerequisites Check

1. **Verify Phase 2 is approved**:
```python
cursor.execute("""
    SELECT status FROM deliverables
    WHERE phase_number = 2 AND phase_name = 'mission'
""")
result = cursor.fetchone()

if not result or result[0] != 'approved':
    print("❌ Cannot start Execution Planning - Mission must be approved first")
    print("Run: /approve-mission")
    exit()
```

## Your Task

Create the Execution Plan by:

1. **Read approved documents**:
   - Vision: `~/.claude/projects/<project-slug>/01-vision.md`
   - Mission: `~/.claude/projects/<project-slug>/02-mission.md`
   - Research: `~/.claude/projects/<project-slug>/research/`

2. **Use the execution template** at `~/.claude/templates/phases/03-execution-plan-template.md`

3. **Deploy appropriate agents**:
   - Primary: `project-task-planner` (break down work)
   - Primary: `task-manager` (agent assignments, scheduling)
   - Support: `database-architect` (if data work needed)
   - Support: `api-architect` (if API design needed)
   - Support: `ui-ux-designer` (if UI work needed)

4. **Create detailed execution plan**:
   - Break Mission into specific, measurable tasks
   - Map dependencies between tasks
   - Assign specialized agents to each task
   - Create realistic timeline (include buffer time)
   - Define quality gates and review checkpoints
   - Identify risks and mitigation strategies

5. **Create the Execution Plan** at:
   `~/.claude/projects/<project-slug>/03-execution-plan.md`

## What Goes in the Execution Plan

### Task Breakdown
- **Granular tasks**: Each task 0.5-2 days max
- **Clear deliverables**: What "done" looks like for each task
- **Dependencies**: What must finish before what can start
- **Agent assignments**: Which specialist handles each task

### Timeline
- **Sprints/Milestones**: Break work into manageable chunks
- **Critical path**: Identify longest dependent chain
- **Buffer time**: Add 20-30% for unknowns
- **Parallel work**: Maximize concurrent tasks

### Quality Gates
- **Code review checkpoints**: When reviews happen
- **Testing milestones**: Unit, integration, E2E
- **Review Board**: Prepares for Phase 3.5 review

### Resource Allocation
- **Agent capacity**: Don't overload any single agent
- **Skill requirements**: Match expertise to complexity
- **Bus factor**: Ensure knowledge sharing

## When Complete

Tell the user:
> "✅ **Phase 3 (Execution Planning) Complete**
>
> Execution Plan created at: `projects/<project-slug>/03-execution-plan.md`
>
> **Plan Summary:**
> - Total Tasks: [X]
> - Estimated Duration: [X weeks]
> - Agents Assigned: [X specialists]
> - Critical Path: [X days]
>
> **Next Steps:**
> 1. Review the Execution Plan thoroughly
> 2. Verify timeline is realistic
> 3. Check agent assignments make sense
> 4. When satisfied, run: `/approve-execution-plan`
>
> ⚠️ **Note:** After approval, the plan goes to the **Review Board** (3 C-suite executives) for final validation before implementation begins."

## Database Updates

```python
# Update phase status
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'execution-planning-in-progress',
        phase_number = 3,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

# Create deliverable record
cursor.execute("""
    INSERT INTO deliverables (id, phase_number, phase_name, document_path, status)
    VALUES (?, 3, 'execution-plan', ?, 'draft')
""", (deliverable_id, document_path))

# Insert all tasks into tasks table
for task in tasks:
    cursor.execute("""
        INSERT INTO tasks (id, phase_number, description, assigned_agent, status, dependencies)
        VALUES (?, ?, ?, ?, 'pending', ?)
    """, (task_id, task.phase, task.description, task.agent, task.dependencies))
```

## Important

- Do NOT proceed to Review Board without explicit user approval via `/approve-execution-plan`
- Realistic estimates are crucial - optimistic timelines fail
- Every task needs a clear owner and deliverable
- The Review Board (CIO, CTO, COO) will scrutinize this plan
