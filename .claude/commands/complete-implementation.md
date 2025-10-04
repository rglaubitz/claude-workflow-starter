---
description: "Complete Phase 4 (Implementation) and unlock Phase 5 (Testing)"
allowed-tools: Bash, Read, Write
---

# Complete Implementation (Phase 4)

You are marking **Phase 4: Implementation** as complete and unlocking **Phase 5: Testing**.

## Prerequisites Check

1. **Verify all tasks are completed**:
```python
cursor.execute("""
    SELECT COUNT(*) as total,
           SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
    FROM tasks
    WHERE phase_number = 4
""")

total, completed = cursor.fetchone()

if completed < total:
    remaining = total - completed
    print(f"❌ Cannot complete implementation - {remaining} tasks still pending")
    print("Complete all tasks first, or remove tasks that are no longer needed")
    exit()
```

2. **Verify Implementation Report exists**:
```python
import os

report_path = f"~/.claude/projects/{project_slug}/04-implementation-report.md"
if not os.path.exists(report_path):
    print("❌ Implementation Report not found")
    print(f"Create report at: {report_path}")
    exit()
```

## Your Task

1. **Display implementation summary**:
```python
# Get completion stats
cursor.execute("""
    SELECT
        COUNT(*) as total_tasks,
        COUNT(DISTINCT assigned_agent) as agents_deployed,
        MIN(created_at) as start_date,
        MAX(completed_at) as end_date
    FROM tasks
    WHERE phase_number = 4 AND status = 'completed'
""")

total_tasks, agents, start_date, end_date = cursor.fetchone()

# Calculate duration
from datetime import datetime
start = datetime.fromisoformat(start_date)
end = datetime.fromisoformat(end_date)
duration_days = (end - start).days

print(f"""
📊 **IMPLEMENTATION SUMMARY**

**Tasks:**
- Total Completed: {total_tasks}
- Agents Deployed: {agents}

**Timeline:**
- Started: {start_date}
- Completed: {end_date}
- Duration: {duration_days} days

**Deliverables:**
- Implementation Report: projects/{project_slug}/04-implementation-report.md
- Code Changes: [Count from git diff]
- Tests Written: [Count from test files]
""")
```

2. **Final quality check**:
```python
print("""
🔍 **FINAL QUALITY CHECKLIST**

Before completing, verify:
- [ ] All tasks from Execution Plan completed
- [ ] All code reviewed and approved
- [ ] Tests written for new functionality
- [ ] Documentation updated
- [ ] No critical bugs or issues
- [ ] Vision goals appear achievable
- [ ] Implementation Report is current and complete
""")
```

3. **Update the database**:
```python
# Mark Implementation deliverable as completed
cursor.execute("""
    UPDATE deliverables
    SET status = 'completed',
        approved_at = CURRENT_TIMESTAMP,
        approved_by = 'user'
    WHERE phase_number = 4 AND phase_name = 'implementation'
""")

# Update workflow state
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'implementation-complete',
        phase_number = 4,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

conn.commit()
```

4. **Inform the user**:
```
✅ **Phase 4 (Implementation) COMPLETE**

**Status:**
- All tasks completed: ✅
- Code reviewed: ✅
- Implementation Report: Finalized
- Phase 5 (Testing): Now unlocked

**What happens in Phase 5?**
Phase 5 (Testing) will:
- Validate all functionality works as designed
- Run comprehensive test suite
- Performance and security testing
- Bug fixing and iteration
- Validate against Vision requirements
- Generate final test report

**Testing Strategy:**
- Unit tests (individual functions/components)
- Integration tests (system interactions)
- End-to-end tests (full user workflows)
- Performance benchmarks
- Security audit
- Accessibility validation (if web)

**Next Steps:**
1. Review the Implementation Report one final time
2. Ensure the codebase is ready for testing
3. When ready to begin testing, run: `/start-testing`
4. Check status anytime with: `/phase-status`
5. View full workflow: `/workflow-dashboard`
```

## Important Notes

- Implementation completion does NOT mean project is done
- Testing phase will likely find bugs that need fixing
- Be prepared for iteration between testing and bug fixes
- The Test Plan will validate against the original Vision goals
- Final project approval happens after Phase 5, not here
