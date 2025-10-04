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

3. **Deploy the execution-director field commander**:
   - Primary: `execution-director` (commands 7 agent teams during Phase 4)
   - Support: `delivery-coordinator`, `quality-enforcer`, `blocker-resolver`, `progress-tracker`
   - The execution-director orchestrates tactical implementation with real-time decision making

4. **Initialize Phase 4 communication infrastructure**:
```bash
echo "🔧 Initializing execution team communication infrastructure..."

# Create 10 SQLite tables for Phase 4 coordination
python3 ~/.claude/scripts/execution-coordinator.py init "$PROJECT_SLUG"

# Verify infrastructure ready
echo ""
echo "📊 Verifying communication infrastructure..."
python3 ~/.claude/scripts/execution-coordinator.py health "$PROJECT_SLUG"

echo ""
echo "✅ Phase 4 infrastructure initialized:"
echo "   - agent_messages (inter-agent communication)"
echo "   - handoff_log (team handoffs)"
echo "   - quality_gates (gate enforcement)"
echo "   - sop_compliance (SOP tracking)"
echo "   - blockers (blocker resolution)"
echo "   - blocker_patterns (learning)"
echo "   - team_status (7 teams initialized)"
echo "   - review_deployments (review tracking)"
echo "   - team_sync_log (sync tracking)"
echo "   - tactical_decisions (execution-director decisions)"
```

5. **Load tasks from database**:
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

6. **Create Implementation Report** at:
   `~/.claude/projects/<project-slug>/04-implementation-report.md`

7. **Begin task execution**:
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

The `execution-director` will:
- Command 7 agent teams (Foundation, Backend, Frontend, Research, Quality, Integration, Orchestration)
- Deploy delivery-coordinator for team handoffs
- Deploy quality-enforcer for gate enforcement with blocking authority
- Deploy blocker-resolver for 5-level escalation (L1→L5)
- Deploy progress-tracker for war room dashboard with 6 KPIs
- Make tactical decisions in real-time
- Coordinate all implementation work

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
- The execution-director is the field commander - let it orchestrate
- Trust the execution support team (delivery-coordinator, quality-enforcer, blocker-resolver, progress-tracker)
