---
description: "Approve Phase 3 (Execution Plan) and proceed to Review Board"
allowed-tools: Bash, Read, Write
---

# Approve Execution Plan (Phase 3)

You are approving **Phase 3: Execution Plan** and proceeding to **Phase 3.5: Review Board**.

## Your Task

1. **Confirm the Execution Plan exists**:
   - Check: `~/.claude/projects/<project-slug>/03-execution-plan.md`
   - If missing, tell user to run `/start-execution-planning` first

2. **Update the database**:
```python
import sqlite3
from datetime import datetime

db_path = f"~/.claude/projects/{project_slug}/workflow.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Mark Execution Plan deliverable as approved
cursor.execute("""
    UPDATE deliverables
    SET status = 'approved',
        approved_at = CURRENT_TIMESTAMP,
        approved_by = 'user'
    WHERE phase_number = 3 AND phase_name = 'execution-plan'
""")

# Update workflow state to ready for review board
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'execution-plan-approved-pending-review',
        phase_number = 3,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

conn.commit()
conn.close()
```

3. **Inform the user**:
```
✅ **Phase 3 (Execution Plan) APPROVED**

**Status:**
- Execution Plan: User-approved, pending C-suite review
- Phase 3.5 (Review Board): Ready to convene

**What happens next?**

The **Review Board** (3 C-suite executives) will now evaluate your execution plan:

🔍 **CIO (Chief Information Officer)**
- Validates research quality and completeness
- Reviews dependencies and reference materials
- Checks documentation and code examples

🔍 **CTO (Chief Technology Officer)**
- Validates technical architecture and approach
- Reviews code quality standards and API design
- Assesses technical feasibility and risks

🔍 **COO (Chief Operations Officer)**
- Validates operational capacity and resources
- Reviews goal achievement and timeline realism
- Assesses UX/UI quality and user adoption

**Possible Outcomes:**
1. ✅ **APPROVED** - All 3 executives approve → Proceed to Phase 4 (Implementation)
2. ⚠️ **APPROVED_WITH_CONCERNS** - Concerns noted but proceed
3. ❌ **REJECTED** - Return to Phase 3 for revisions

**Next Steps:**
1. When ready for review, run: `/start-review-board`
2. The board will generate 3 individual reports
3. You'll receive a consolidated verdict
```

## Important Notes

- User approval ≠ Executive approval (two separate gates)
- Review Board has **veto power** - implementation cannot begin without their approval
- If rejected, loop back to `/start-execution-planning` with board feedback
- All 3 executives must approve (or conditionally approve) for the board to pass
