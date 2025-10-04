---
description: "Address Review Board concerns and revise Execution Plan"
allowed-tools: Bash, Read, Write
---

# Address Review Board Concerns

You are addressing **Review Board feedback** and returning to **Phase 3: Execution Planning** for revision.

## Prerequisites Check

1. **Verify Review Board rejection or concerns**:
```python
cursor.execute("""
    SELECT overall_verdict, status FROM review_board_sessions
    ORDER BY created_at DESC LIMIT 1
""")
result = cursor.fetchone()

if not result:
    print("❌ No Review Board session found")
    print("Run: /start-review-board first")
    exit()

if result[0] == 'APPROVED' and result[1] == 'completed':
    print("✅ Review Board approved - no concerns to address")
    print("Run: /approve-review-board to proceed to implementation")
    exit()
```

## Your Task

1. **Display all concerns and blockers**:
```python
cursor.execute("""
    SELECT
        executive_role,
        verdict,
        report_path,
        blockers_count,
        concerns_count,
        recommendations_count
    FROM review_board_findings
    WHERE session_id = (SELECT id FROM review_board_sessions ORDER BY created_at DESC LIMIT 1)
    ORDER BY
        CASE verdict
            WHEN 'REJECTED' THEN 1
            WHEN 'APPROVED_WITH_CONCERNS' THEN 2
            ELSE 3
        END,
        executive_role
""")

findings = cursor.fetchall()

print("🔍 **REVIEW BOARD FEEDBACK**\n")
print("=" * 60)

for exec_role, verdict, report_path, blockers, concerns, recommendations in findings:
    if verdict == 'REJECTED' or concerns > 0 or blockers > 0:
        icon = "❌" if verdict == "REJECTED" else "⚠️"
        print(f"\n{icon} **{exec_role.upper()}** - {verdict}")
        print(f"   Report: {report_path}")

        if blockers > 0:
            print(f"\n   🚫 **BLOCKERS ({blockers}):**")
            print(f"   - Read {report_path} for details")

        if concerns > 0:
            print(f"\n   ⚠️ **CONCERNS ({concerns}):**")
            print(f"   - Read {report_path} for details")

        if recommendations > 0:
            print(f"\n   💡 **RECOMMENDATIONS ({recommendations}):**")
            print(f"   - Read {report_path} for details")

print("\n" + "=" * 60)
```

2. **Guide revision process**:
```
📋 **REVISION WORKFLOW**

**Step 1: Review All Executive Reports**

Read each report carefully:
- CIO Report: [path]
- CTO Report: [path]
- COO Report: [path]

**Step 2: Identify Changes Needed**

For each BLOCKER:
- [ ] [Blocker from CIO]: [Required change]
- [ ] [Blocker from CTO]: [Required change]
- [ ] [Blocker from COO]: [Required change]

For each CONCERN:
- [ ] [Concern from CIO]: [Recommended change]
- [ ] [Concern from CTO]: [Recommended change]
- [ ] [Concern from COO]: [Recommended change]

**Step 3: Determine Scope of Revision**

Choose your path:

**Option A: Minor revisions** (can edit Execution Plan directly)
- Fix specific issues identified
- Update timelines, resources, or approaches
- Manually edit: `projects/<project-slug>/03-execution-plan.md`

**Option B: Major revisions** (need to re-run execution planning)
- Significant architectural changes
- Different technical approach required
- Run: `/start-execution-planning` to regenerate

**Option C: Research gaps** (need to revisit Mission)
- Missing dependencies identified
- Insufficient research/examples
- Run: `/start-mission` to gather more information

**Step 4: Re-submit to Review Board**

After making revisions:
1. Run: `/start-review-board` to convene a new session
2. Executives will re-evaluate with previous feedback in mind
3. New session will reference prior concerns
```

## Database Updates

```python
# Update workflow state to revision mode
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'execution-plan-revision',
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

# Optionally mark execution plan as 'needs-revision'
cursor.execute("""
    UPDATE deliverables
    SET status = 'needs-revision'
    WHERE phase_number = 3 AND phase_name = 'execution-plan'
""")

conn.commit()
```

## Loop-back Architecture

```
Phase 3 (Execution Planning)
         ↓
    [User Approves]
         ↓
Phase 3.5 (Review Board)
         ↓
    [C-Suite Review]
         ↓
    ┌─────────────┐
    │  Approved?  │
    └─────────────┘
         │
    ┌────┴────┐
   Yes       No
    │         │
    ↓         ↓
Phase 4   [Address Concerns]
          ↓
     [Back to Phase 3] ← LOOP
```

## Important Notes

- The Review Board loop can happen multiple times
- Each revision session gets a new session ID
- Previous session feedback is preserved and referenced
- This loop prevents expensive implementation rework
- Address blockers first, concerns second, recommendations third
