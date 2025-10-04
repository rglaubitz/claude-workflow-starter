---
description: "Accept Review Board approval and proceed to Phase 4 (Implementation)"
allowed-tools: Bash, Read, Write
---

# Approve Review Board (Phase 3.5)

You are accepting **Review Board approval** and unlocking **Phase 4: Implementation**.

## Prerequisites Check

1. **Verify Review Board session completed**:
```python
cursor.execute("""
    SELECT overall_verdict, status FROM review_board_sessions
    ORDER BY created_at DESC LIMIT 1
""")
result = cursor.fetchone()

if not result:
    print("❌ No Review Board session found")
    print("Run: /start-review-board")
    exit()

if result[1] != 'completed':
    print("❌ Review Board session still in progress")
    exit()

if result[0] == 'REJECTED':
    print("❌ Review Board REJECTED the execution plan")
    print("Run: /address-review-concerns to revise the plan")
    exit()
```

2. **Display Review Board Summary**:
```python
# Get individual verdicts
cursor.execute("""
    SELECT executive_role, verdict, blockers_count, concerns_count, report_path
    FROM review_board_findings
    WHERE session_id = (SELECT id FROM review_board_sessions ORDER BY created_at DESC LIMIT 1)
    ORDER BY executive_role
""")

findings = cursor.fetchall()

print("📊 **REVIEW BOARD SUMMARY**\n")
for exec_role, verdict, blockers, concerns, report_path in findings:
    icon = "✅" if verdict == "APPROVED" else "⚠️" if verdict == "APPROVED_WITH_CONCERNS" else "❌"
    print(f"{icon} **{exec_role.upper()}**: {verdict}")
    if concerns > 0:
        print(f"   - Concerns: {concerns}")
    if blockers > 0:
        print(f"   - Blockers: {blockers}")
    print(f"   - Report: {report_path}\n")
```

## Your Task

1. **Accept the Review Board decision**:
```python
# Mark review board as accepted
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'review-board-approved',
        phase_number = 3.5,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

conn.commit()
```

2. **Inform the user**:
```
✅ **REVIEW BOARD APPROVED - IMPLEMENTATION UNLOCKED**

**C-Suite Sign-off:**
- CIO: [Verdict]
- CTO: [Verdict]
- COO: [Verdict]

**Overall Verdict:** [APPROVED / CONDITIONALLY_APPROVED]

**Concerns to address during implementation:**
[List any concerns from APPROVED_WITH_CONCERNS verdicts]

**Status:**
- All planning phases (Vision, Mission, Execution) validated
- C-suite executives signed off
- Phase 4 (Implementation): Now unlocked

**What happens in Phase 4?**
Phase 4 (Implementation) will:
- Execute all tasks from the approved Execution Plan
- Deploy specialized agents as assigned
- Track progress in real-time with TodoWrite
- Conduct code reviews as work completes
- Generate Implementation Report documenting all work

**Next Steps:**
1. Review any concerns from the board (if CONDITIONALLY_APPROVED)
2. When ready to begin building, run: `/start-implementation`
3. Check progress anytime with: `/phase-status`
4. View full workflow: `/workflow-dashboard`
```

## Important Notes

- If verdict was CONDITIONALLY_APPROVED, address concerns during implementation
- Implementation can now begin - this is the "green light"
- The Implementation phase will track against the approved Execution Plan
- All C-suite concerns are documented for reference during building
