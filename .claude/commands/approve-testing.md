---
description: "Approve Phase 5 (Testing) and complete the project"
allowed-tools: Bash, Read, Write
---

# Approve Testing (Phase 5) - PROJECT COMPLETE

You are approving **Phase 5: Testing** and marking the **entire project as COMPLETE**.

## Prerequisites Check

1. **Verify Test Plan exists and all tests pass**:
```python
import os

test_plan_path = f"~/.claude/projects/{project_slug}/05-test-plan.md"
if not os.path.exists(test_plan_path):
    print("❌ Test Plan not found")
    print("Run: /start-testing")
    exit()

# Read test plan and check for failures
with open(test_plan_path, 'r') as f:
    content = f.read()
    if 'Failed:' in content and not 'Failed: 0' in content:
        print("⚠️ Warning: Test failures detected in Test Plan")
        print("Ensure all tests pass before approving")
```

2. **Validate Vision goals achieved**:
```python
# Prompt user for final validation
print("""
🎯 **VISION GOALS VALIDATION**

Review the Vision document and confirm:
""")

cursor.execute("""
    SELECT document_path FROM deliverables
    WHERE phase_number = 1 AND phase_name = 'vision'
""")
vision_path = cursor.fetchone()[0]

print(f"Vision: {vision_path}")
print(f"Test Plan: {test_plan_path}")
print("\nVerify that all Vision success criteria are validated in the Test Plan.")
```

## Your Task

1. **Generate project completion summary**:
```python
# Get all phase completion data
cursor.execute("""
    SELECT
        phase_number,
        phase_name,
        status,
        approved_at,
        document_path
    FROM deliverables
    ORDER BY phase_number
""")

deliverables = cursor.fetchall()

# Get task statistics
cursor.execute("""
    SELECT
        COUNT(*) as total,
        COUNT(DISTINCT assigned_agent) as agents,
        MIN(created_at) as project_start,
        MAX(completed_at) as project_end
    FROM tasks
""")

total_tasks, total_agents, start_date, end_date = cursor.fetchone()

# Calculate project duration
from datetime import datetime
start = datetime.fromisoformat(start_date)
end = datetime.fromisoformat(end_date)
duration = (end - start).days

print(f"""
🎉 **PROJECT COMPLETION SUMMARY**

**Project:** {project_name}
**Duration:** {duration} days ({start_date} to {end_date})

**Phases Completed:**
""")

for phase_num, phase_name, status, approved_at, doc_path in deliverables:
    print(f"✅ Phase {phase_num} ({phase_name}): {status} - {approved_at}")
    print(f"   Document: {doc_path}")

print(f"""
**Execution Statistics:**
- Total Tasks Completed: {total_tasks}
- Specialized Agents Deployed: {total_agents}
- Review Board Sessions: [count from review_board_sessions]

**Deliverables:**
- Vision Document ✅
- Mission Document ✅
- Execution Plan ✅
- Implementation Report ✅
- Test Plan ✅
""")
```

2. **Update the database**:
```python
# Mark Testing deliverable as approved
cursor.execute("""
    UPDATE deliverables
    SET status = 'approved',
        approved_at = CURRENT_TIMESTAMP,
        approved_by = 'user'
    WHERE phase_number = 5 AND phase_name = 'test-plan'
""")

# Update workflow to COMPLETE
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'project-complete',
        phase_number = 5,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

conn.commit()
```

3. **Generate final project report**:
```python
# Create completion report
report_path = f"~/.claude/projects/{project_slug}/PROJECT-COMPLETE.md"

report_content = f"""
# Project Completion Report: {project_name}

**Status:** ✅ COMPLETE
**Completed:** {datetime.now().isoformat()}
**Duration:** {duration} days

## Executive Summary

[Summarize what was built, key achievements, and final outcomes]

## Phase Completion

- ✅ **Phase 0: Project Brief** - Problem defined, goals set
- ✅ **Phase 1: Vision** - Strategic direction established
- ✅ **Phase 2: Mission** - Technical approach defined
- ✅ **Phase 3: Execution Planning** - Detailed plan created
- ✅ **Phase 3.5: Review Board** - C-suite approval obtained
- ✅ **Phase 4: Implementation** - All tasks completed
- ✅ **Phase 5: Testing** - All tests passing

## Vision Goals Achievement

[For each Vision goal, show how it was achieved and validated]

## Final Metrics

- Tasks Completed: {total_tasks}
- Agents Deployed: {total_agents}
- Test Coverage: [X%]
- Performance: [Meets requirements]
- Security: [No vulnerabilities]

## Key Documents

- Vision: 01-vision.md
- Mission: 02-mission.md
- Execution Plan: 03-execution-plan.md
- Implementation Report: 04-implementation-report.md
- Test Plan: 05-test-plan.md

## Review Board Approval

[Summary of C-suite executive approvals]

## Next Steps (Post-Project)

- [ ] Deploy to production (if applicable)
- [ ] Monitor performance
- [ ] Gather user feedback
- [ ] Plan V2 features

---

**This project followed the 5-Phase Workflow System**
Managed by Claude Code with multi-agent deployment
"""

# Write completion report
with open(report_path, 'w') as f:
    f.write(report_content)
```

4. **Celebrate and inform user**:
```
🎉🎉🎉 **PROJECT COMPLETE** 🎉🎉🎉

**{project_name}** has successfully completed all 5 phases!

**What Was Accomplished:**
- ✅ Vision defined and goals set
- ✅ Technical research and planning completed
- ✅ Execution plan approved by C-suite Review Board
- ✅ Implementation completed with {total_tasks} tasks
- ✅ All tests passing and Vision goals validated

**Project Duration:** {duration} days
**Agents Deployed:** {total_agents} specialists
**Quality Gates Passed:** 6 (Vision, Mission, Execution, Review Board, Implementation, Testing)

**Final Deliverables:**
All project documents are in: `~/.claude/projects/{project_slug}/`

**Completion Report:**
`projects/{project_slug}/PROJECT-COMPLETE.md`

**Database:**
Project workflow data preserved at: `projects/{project_slug}/workflow.db`

**What's Next?**
- Review the completion report
- Deploy to production (if applicable)
- Start a new project with: `/start-project "Next Project"`
- View all projects: `/workflow-dashboard`

Thank you for using the 5-Phase Workflow System! 🚀
```

## Important Notes

- This is the final approval in the workflow
- The project is now officially complete
- All documents are preserved for future reference
- Database contains complete audit trail
- Ready for deployment or V2 planning
