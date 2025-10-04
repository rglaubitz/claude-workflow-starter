---
description: "Begin Phase 4 (Implementation) - Execute the approved plan"
allowed-tools: Task, Bash, Write, Read, TodoWrite
---

# Phase 4: Start Implementation

You are initiating **Phase 4: Implementation** - the execution phase.

## Prerequisites Check

1. **Verify Review Board approval**:
```python
cursor.execute("""
    SELECT overall_verdict FROM review_board_sessions
    ORDER BY created_at DESC LIMIT 1
""")
result = cursor.fetchone()

if not result or result[0] not in ['APPROVED', 'CONDITIONALLY_APPROVED']:
    print("❌ Cannot start Implementation - Review Board approval required")
    print("Run: /start-review-board")
    exit()
```

## Your Task

Begin implementation by:

1. **Read approved plan documents**:
   - Vision: `~/.claude/projects/<project-slug>/01-vision.md`
   - Mission: `~/.claude/projects/<project-slug>/02-mission.md`
   - Execution Plan: `~/.claude/projects/<project-slug>/03-execution-plan.md`
   - Review Board feedback: `~/.claude/projects/<project-slug>/review-board/session-*/`

2. **Use implementation template** at `~/.claude/templates/phases/04-implementation-report-template.md`

3. **Deploy the task-manager orchestrator**:
   - Primary: `task-manager` (coordinates all implementation work)
   - The task-manager will deploy other agents based on Execution Plan assignments

4. **Load tasks from database**:
```python
cursor.execute("""
    SELECT id, description, assigned_agent, dependencies, status
    FROM tasks
    WHERE phase_number = 4
    ORDER BY id
""")

tasks = cursor.fetchall()

# Initialize TodoWrite with all tasks
todo_items = []
for task_id, description, agent, deps, status in tasks:
    todo_items.append({
        'content': description,
        'status': status if status else 'pending',
        'activeForm': description.replace('Implement', 'Implementing')
                                 .replace('Create', 'Creating')
                                 .replace('Build', 'Building')
    })
```

5. **Create Implementation Report** at:
   `~/.claude/projects/<project-slug>/04-implementation-report.md`

6. **Begin task execution**:
   - Work through tasks in dependency order
   - Use TodoWrite to track real-time progress
   - Update Implementation Report as work completes
   - Conduct code reviews for completed work
   - Handle blockers and adapt as needed

## Implementation Workflow

```
For each task:
1. Mark as 'in_progress' in TodoWrite and database
2. Deploy assigned agent(s)
3. Execute the task
4. Code review (if code was written)
5. Mark as 'completed' in TodoWrite and database
6. Update Implementation Report
7. Proceed to next task
```

## When Tasks Are Running

The `task-manager` will:
- Coordinate agent work
- Track progress in real-time
- Update Implementation Report
- Handle dependencies
- Escalate blockers
- Ensure quality gates are met

User can monitor progress:
- `/phase-status` - Current task status
- `/workflow-dashboard` - Overall progress
- View: `projects/<project-slug>/04-implementation-report.md`

## When All Tasks Complete

Tell the user:
> "✅ **Phase 4 (Implementation) Complete**
>
> Implementation Report: `projects/<project-slug>/04-implementation-report.md`
>
> **Summary:**
> - Total Tasks Completed: [X]
> - Code Files Changed: [X]
> - Tests Written: [X]
> - Code Reviews Passed: [X]
>
> **Next Steps:**
> 1. Review the Implementation Report
> 2. Verify all requirements from Vision are met
> 3. Check that code quality is acceptable
> 4. When satisfied, run: `/complete-implementation`"

## Database Updates

```python
# Update phase status
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'implementation-in-progress',
        phase_number = 4,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

# Create deliverable record
cursor.execute("""
    INSERT INTO deliverables (id, phase_number, phase_name, document_path, status)
    VALUES (?, 4, 'implementation', ?, 'in-progress')
""", (deliverable_id, document_path))

# As tasks complete, update their status
cursor.execute("""
    UPDATE tasks
    SET status = 'completed',
        completed_at = CURRENT_TIMESTAMP
    WHERE id = ?
""", (task_id,))
```

## Important

- This is the longest phase - implementation takes time
- Use TodoWrite extensively for progress visibility
- Code review every significant change
- Update Implementation Report regularly (daily or per-task)
- Don't rush - quality over speed
- The task-manager is the orchestrator - let it coordinate
