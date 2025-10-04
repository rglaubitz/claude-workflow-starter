---
description: "Approve Phase 2 (Mission) and unlock Phase 3"
allowed-tools: Bash, Read, Write
---

# Approve Mission (Phase 2)

You are approving **Phase 2: Mission** and unlocking **Phase 3: Execution Planning**.

## Your Task

1. **Confirm the Mission document exists**:
   - Check: `~/.claude/projects/<project-slug>/02-mission.md`
   - If missing, tell user to run `/start-mission` first

2. **Verify completeness**:
   - All dependencies identified with versions and justifications
   - Research materials present in proper folder structure
   - Code examples gathered from 1.5k+ star repos
   - Technical approach documented with citations

3. **Validate research quality** (Research-First Principle):
```bash
# Check folder structure exists
ls -la ~/.claude/projects/<project-slug>/research/documentation/anthropic-docs
ls -la ~/.claude/projects/<project-slug>/research/documentation/framework-docs
ls -la ~/.claude/projects/<project-slug>/research/examples/implementation-patterns

# Verify references.md exists and has citations
if [ -f ~/.claude/projects/<project-slug>/research/references.md ]; then
    echo "✅ references.md found"
    # Check for GitHub star counts in references
    grep -q "⭐" ~/.claude/projects/<project-slug>/research/references.md && echo "✅ GitHub repos have star counts"
    # Check for official docs
    grep -qi "anthropic\|claude" ~/.claude/projects/<project-slug>/research/references.md && echo "✅ Anthropic docs referenced"
else
    echo "⚠️  references.md missing - research quality cannot be validated"
fi
```

4. **Update the database**:
```python
import sqlite3
from datetime import datetime

db_path = f"~/.claude/projects/{project_slug}/workflow.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Mark Mission deliverable as approved
cursor.execute("""
    UPDATE deliverables
    SET status = 'approved',
        approved_at = CURRENT_TIMESTAMP,
        approved_by = 'user'
    WHERE phase_number = 2 AND phase_name = 'mission'
""")

# Update workflow state
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'mission-approved',
        phase_number = 2,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

conn.commit()
conn.close()
```

5. **Inform the user**:
```
✅ **Phase 2 (Mission) APPROVED**

**Status:**
- Mission document: Locked and approved
- Phase 3 (Execution Planning): Now unlocked

**What happens in Phase 3?**
Phase 3 (Execution Planning) will:
- Break the Mission into detailed, actionable tasks
- Assign specialized agents to each task
- Create a timeline with dependencies
- Define quality gates and review checkpoints
- Prepare for Review Board evaluation (Phase 3.5)

**Next Steps:**
1. When ready to create execution plan, run: `/start-execution-planning`
2. Check status anytime with: `/phase-status`
3. View full workflow: `/workflow-dashboard`
```

## Important Notes

- Once approved, the Mission document becomes the technical foundation
- All dependencies should be documented before execution planning
- Phase 3 will use this research to create realistic task estimates
