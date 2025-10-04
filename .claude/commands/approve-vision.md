---
description: "Approve Phase 1 (Vision) and unlock Phase 2"
allowed-tools: Bash, Read, Write
---

# Approve Vision (Phase 1)

You are approving **Phase 1: Vision** and unlocking **Phase 2: Mission**.

## Your Task

1. **Confirm the Vision document exists**:
   - Check: `~/.claude/projects/<project-slug>/01-vision.md`
   - If missing, tell user to run `/start-vision` first

2. **Update the database**:
```python
import sqlite3
from datetime import datetime

db_path = f"~/.claude/projects/{project_slug}/workflow.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Mark Vision deliverable as approved
cursor.execute("""
    UPDATE deliverables
    SET status = 'approved',
        approved_at = CURRENT_TIMESTAMP,
        approved_by = 'user'
    WHERE phase_number = 1 AND phase_name = 'vision'
""")

# Update workflow state
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'vision-approved',
        phase_number = 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

conn.commit()
conn.close()
```

3. **Inform the user**:
```
✅ **Phase 1 (Vision) APPROVED**

**Status:**
- Vision document: Locked and approved
- Phase 2 (Mission): Now unlocked

**What happens in Phase 2?**
Phase 2 (Mission) will:
- Research technical approaches and best practices
- Identify all dependencies (packages, APIs, services)
- Gather code examples and reference documentation
- Define the technical "how" based on your Vision's "why"

**Next Steps:**
1. When ready to begin research, run: `/start-mission`
2. Check status anytime with: `/phase-status`
3. View full workflow: `/workflow-dashboard`
```

## Important Notes

- Once approved, the Vision document becomes **read-only** for the workflow
- Users can still manually edit if needed, but should re-approve if changes are significant
- Phase 2 cannot begin until this approval is recorded in the database
