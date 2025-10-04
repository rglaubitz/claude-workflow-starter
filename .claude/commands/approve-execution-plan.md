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

2. **Create Phase 3→4 Handoff Artifact**:

Prepare structured handoff package for execution-director:

```python
import json
import uuid
from pathlib import Path
from datetime import datetime

# Determine project directory
project_dir = Path.home() / ".claude" / "projects" / project_slug

# Read execution plan for team details
execution_plan_path = project_dir / "03-execution-plan.md"
execution_plan = execution_plan_path.read_text()

# Create handoff package artifact
handoff_package = {
    'handoff_id': str(uuid.uuid4()),
    'timestamp': datetime.now().isoformat(),
    'phase_from': 3,
    'phase_to': 4,
    'transition': 'Planning → Execution',
    'handoff_from': 'task-manager (Strategic Planning)',
    'handoff_to': 'execution-director (Tactical Execution)',
    'execution_plan_path': str(execution_plan_path),
    'agent_teams': {
        'Foundation': ['database-architect', 'devops-engineer'],
        'Backend': ['backend-developer', 'api-architect', 'sql-specialist'],
        'Frontend': ['frontend-developer', 'ui-ux-designer'],
        'Research': ['research-manager', 'documentation-expert', 'specialists'],
        'Quality': ['qa-engineer', 'code-review-expert', 'security-auditor', 'performance-engineer'],
        'Integration': ['integration-specialist', 'mcp-bridge-engineer'],
        'Orchestration': ['execution-director', 'delivery-coordinator', 'quality-enforcer', 'blocker-resolver', 'progress-tracker']
    },
    'dependencies': {
        'technical': 'All dependencies documented in research/dependencies.md',
        'information': 'Research and docs from Phase 2 (Mission)',
        'resource': 'Agent teams identified with capacity limits',
        'team': '7 teams with defined roles and coordination protocols'
    },
    'quality_gates': {
        'task_level': 'Code review, unit tests, linting',
        'feature_level': 'Integration tests, feature review',
        'epic_level': 'E2E tests, epic validation',
        'phase_level': 'Complete validation before Phase 5'
    },
    'communication_infrastructure': {
        'real_time': 'TodoWrite for task broadcasting',
        'persistent': 'SQLite workflow.db with 10 execution tables',
        'coordination': 'execution-coordinator.py for team management'
    },
    'review_board_approval': 'APPROVED (pending)',  # Will be updated by Review Board
    'execution_readiness': 'Verified and user-approved',
    'created_at': datetime.now().isoformat(),
    'created_by': 'approve-execution-plan command'
}

# Store artifact in project directory
handoff_path = project_dir / "handoff-package-phase-3-to-4.json"
handoff_path.write_text(json.dumps(handoff_package, indent=2))

print(f"✅ Phase 3→4 Handoff Package Created")
print(f"   Location: {handoff_path}")
print(f"   Handoff ID: {handoff_package['handoff_id']}")
print(f"   - 7 agent teams identified")
print(f"   - 4 dependency types mapped")
print(f"   - 4 quality gate levels defined")
print(f"   - Communication infrastructure specified")
print(f"   - Execution readiness verified")
print("")
```

3. **Update the database**:
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

4. **Inform the user**:
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
