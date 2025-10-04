---
description: "Begin Phase 3.5 (Review Board) - C-suite executive review"
allowed-tools: Task, Bash, Write, Read
---

# Phase 3.5: Start Review Board

You are initiating **Phase 3.5: Review Board** - C-suite executive evaluation.

## Prerequisites Check

1. **Verify Execution Plan is user-approved**:
```python
cursor.execute("""
    SELECT status FROM deliverables
    WHERE phase_number = 3 AND phase_name = 'execution-plan'
""")
result = cursor.fetchone()

if not result or result[0] != 'approved':
    print("❌ Cannot start Review Board - Execution Plan must be approved first")
    print("Run: /approve-execution-plan")
    exit()
```

## Your Task

Coordinate the Review Board session:

1. **Use the review board coordinator**:
```bash
python3 ~/.claude/scripts/review-board-coordinator.py <project-slug>
```

This script will:
- Create review session directory
- Deploy 3 C-suite executive agents
- Generate individual review reports
- Compile overall verdict

2. **The 3 C-suite Executives**:

   **🔍 CIO (Chief Information Officer)**
   - Agent: `CIO`
   - Reviews: Research quality, dependencies, documentation, examples
   - Report: `review-board/session-TIMESTAMP/cio-review.md`
   - Checklist: `templates/review-board/checklists/cio-checklist.md`

   **🔍 CTO (Chief Technology Officer)**
   - Agent: `CTO`
   - Reviews: Technical architecture, code standards, APIs, feasibility
   - Report: `review-board/session-TIMESTAMP/cto-review.md`
   - Checklist: `templates/review-board/checklists/cto-checklist.md`

   **🔍 COO (Chief Operations Officer)**
   - Agent: `COO`
   - Reviews: Operations, goals, UX/UI, beauty, execution capacity
   - Report: `review-board/session-TIMESTAMP/coo-review.md`
   - Checklist: `templates/review-board/checklists/coo-checklist.md`

3. **Each executive evaluates**:
   - Vision alignment
   - Mission completeness
   - Execution plan feasibility
   - Technical soundness
   - Operational viability

4. **Each executive delivers verdict**:
   - ✅ **APPROVED**: No blocking issues
   - ⚠️ **APPROVED_WITH_CONCERNS**: Concerns noted but can proceed
   - ❌ **REJECTED**: Must address issues before implementation

## Overall Board Verdict

**Board APPROVES if:**
- All 3 executives: APPROVED ✅✅✅
- Or: 2 APPROVED + 1 APPROVED_WITH_CONCERNS ✅✅⚠️

**Board CONDITIONALLY APPROVES if:**
- 1 APPROVED + 2 APPROVED_WITH_CONCERNS ✅⚠️⚠️
- 3 APPROVED_WITH_CONCERNS ⚠️⚠️⚠️

**Board REJECTS if:**
- Any executive: REJECTED ❌

## When Complete

The coordinator will display:
```
📊 **REVIEW BOARD SESSION COMPLETE**

**Verdicts:**
- CIO: [APPROVED/APPROVED_WITH_CONCERNS/REJECTED]
- CTO: [APPROVED/APPROVED_WITH_CONCERNS/REJECTED]
- COO: [APPROVED/APPROVED_WITH_CONCERNS/REJECTED]

**Overall Decision:** [APPROVED/CONDITIONALLY_APPROVED/REJECTED]

**Reports Location:**
projects/<project-slug>/review-board/session-TIMESTAMP/

**Next Steps:**
- If APPROVED: Run `/approve-review-board` to proceed to Phase 4
- If REJECTED: Run `/address-review-concerns` to revise execution plan
```

## Database Updates

```python
import uuid
from datetime import datetime

session_id = str(uuid.uuid4())
session_number = get_next_session_number()

# Create review session
cursor.execute("""
    INSERT INTO review_board_sessions (id, session_number, status, created_at)
    VALUES (?, ?, 'in-progress', CURRENT_TIMESTAMP)
""", (session_id, session_number))

# Record each executive's finding
for executive in ['CIO', 'CTO', 'COO']:
    cursor.execute("""
        INSERT INTO review_board_findings
        (id, session_id, executive_role, agent_name, verdict, report_path,
         blockers_count, concerns_count, recommendations_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (finding_id, session_id, executive.lower(), executive,
          verdict, report_path, blockers, concerns, recommendations))

# Update session with overall verdict
cursor.execute("""
    UPDATE review_board_sessions
    SET status = 'completed',
        overall_verdict = ?,
        completed_at = CURRENT_TIMESTAMP
    WHERE id = ?
""", (overall_verdict, session_id))

# Update workflow state
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'review-board-complete',
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))
```

## Important

- The Review Board has **veto power** - unanimous concerns = rejection
- Each executive's report is thorough and actionable
- If rejected, specific feedback guides revisions
- This is the final gate before expensive implementation work begins
