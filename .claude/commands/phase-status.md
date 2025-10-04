---
description: "Show current phase status and progress (project-specific)"
argument-hint: "[project-slug]"
allowed-tools: Bash, Read
---

# Phase Status: $ARGUMENTS

You are displaying the **current phase status** for a project in the 5-Phase Workflow System.

## Your Task

1. **Determine project slug**:
```python
import os
from pathlib import Path
import sqlite3

# Get project slug from argument or detect from current directory
project_slug = "$ARGUMENTS"

if not project_slug:
    # Try to detect from current directory
    cwd = Path.cwd()
    projects_dir = Path.home() / ".claude" / "projects"

    if str(cwd).startswith(str(projects_dir)):
        project_slug = cwd.relative_to(projects_dir).parts[0]
    else:
        print("❌ No project slug provided and not in a project directory")
        print("Usage: /phase-status <project-slug>")
        print("\nAvailable projects:")
        for proj in projects_dir.iterdir():
            if proj.is_dir() and (proj / "workflow.db").exists():
                print(f"  - {proj.name}")
        exit(1)

# Verify project exists
project_dir = Path.home() / ".claude" / "projects" / project_slug
db_path = project_dir / "workflow.db"

if not db_path.exists():
    print(f"❌ Project not found: {project_slug}")
    print(f"Database not found at: {db_path}")
    print("\nRun: /start-project \"{project_slug}\"")
    exit(1)
```

2. **Query workflow status**:
```python
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get workflow info
cursor.execute("""
    SELECT id, project_name, current_phase, phase_number, created_at, updated_at
    FROM workflow
    LIMIT 1
""")

workflow = cursor.fetchone()
if not workflow:
    print(f"❌ Workflow not initialized for {project_slug}")
    conn.close()
    exit(1)

wf_id, project_name, current_phase, phase_num, created_at, updated_at = workflow
```

3. **Display phase status**:
```python
from datetime import datetime

print()
print("═" * 70)
print(f"  PROJECT: {project_name}")
print(f"  CURRENT PHASE: {current_phase.upper()}")
print("═" * 70)
print()

# Phase progression with status
phases = [
    (0, "brief-uploaded", "Project Brief", "00-project-brief.md"),
    (1, "vision", "Vision - Define What & Why", "01-vision.md"),
    (2, "mission", "Mission - Research How", "02-mission.md"),
    (3, "execution-plan", "Execution Planning", "03-execution-plan.md"),
    (3.5, "review-board", "Review Board (C-suite)", "review-board/session-*/"),
    (4, "implementation", "Implementation - Build It", "04-implementation-report.md"),
    (5, "test-plan", "Testing - Validate & Verify", "05-test-plan.md")
]

print("📋 **PHASE PROGRESSION:**\n")

for phase_number, phase_key, phase_name, deliverable in phases:
    # Determine status
    if phase_num > phase_number:
        status = "✅ Complete"
    elif phase_num == phase_number:
        if 'approved' in current_phase or 'complete' in current_phase:
            status = "✅ Complete"
        elif 'in-progress' in current_phase:
            status = "🔄 In Progress"
        else:
            status = "⏳ Ready"
    else:
        status = "🔒 Locked"

    # Check if deliverable exists
    cursor.execute("""
        SELECT status, approved_at FROM deliverables
        WHERE phase_number = ? AND phase_name = ?
    """, (int(phase_number), phase_key.replace('-in-progress', '').replace('-approved', '')))

    result = cursor.fetchone()
    if result:
        deliv_status, approved_at = result
        if deliv_status == 'approved':
            status = f"✅ Approved {approved_at[:10] if approved_at else ''}"
        elif deliv_status == 'in-progress':
            status = "🔄 In Progress"
        elif deliv_status == 'draft':
            status = "📝 Draft"

    marker = "→" if phase_num == phase_number else " "
    print(f"  {marker} Phase {phase_number}: {phase_name:<40} {status}")
```

4. **Show current phase details**:
```python
print("\n" + "─" * 70)
print(f"📍 **CURRENT PHASE DETAILS:**\n")

phase_commands = {
    'brief-uploaded': {
        'description': 'User has uploaded project brief. Ready to begin Vision.',
        'next_command': '/start-vision',
        'next_action': 'Create Vision document (what and why)'
    },
    'vision-in-progress': {
        'description': 'Creating Vision document with prd-expert',
        'next_command': '/approve-vision',
        'next_action': 'Review and approve Vision document'
    },
    'vision-approved': {
        'description': 'Vision approved. Ready to begin Mission.',
        'next_command': '/start-mission',
        'next_action': 'Research technical approach and gather dependencies'
    },
    'mission-in-progress': {
        'description': 'Researching technical approach with research-manager',
        'next_command': '/approve-mission',
        'next_action': 'Review and approve Mission document'
    },
    'mission-approved': {
        'description': 'Mission approved. Ready to create Execution Plan.',
        'next_command': '/start-execution-planning',
        'next_action': 'Break down work into detailed tasks'
    },
    'execution-planning-in-progress': {
        'description': 'Creating Execution Plan with project-task-planner',
        'next_command': '/approve-execution-plan',
        'next_action': 'Review and approve Execution Plan'
    },
    'execution-plan-approved-pending-review': {
        'description': 'Execution Plan user-approved. Awaiting C-suite Review Board.',
        'next_command': '/start-review-board',
        'next_action': 'Convene Review Board (CIO, CTO, COO)'
    },
    'review-board-complete': {
        'description': 'Review Board has evaluated the plan.',
        'next_command': '/approve-review-board or /address-review-concerns',
        'next_action': 'Accept approval or address concerns'
    },
    'review-board-approved': {
        'description': 'C-suite approved. Ready to implement.',
        'next_command': '/start-implementation',
        'next_action': 'Begin building with task-manager orchestration'
    },
    'implementation-in-progress': {
        'description': 'Implementing tasks from approved Execution Plan',
        'next_command': '/complete-implementation',
        'next_action': 'Finish all tasks and mark implementation complete'
    },
    'implementation-complete': {
        'description': 'Implementation finished. Ready to test.',
        'next_command': '/start-testing',
        'next_action': 'Create test plan and validate requirements'
    },
    'testing-in-progress': {
        'description': 'Running comprehensive test suite',
        'next_command': '/approve-testing',
        'next_action': 'Approve tests and complete project'
    },
    'project-complete': {
        'description': '🎉 Project fully complete! All phases passed.',
        'next_command': 'N/A',
        'next_action': 'Deploy or start new project'
    }
}

phase_info = phase_commands.get(current_phase, {
    'description': current_phase,
    'next_command': 'Check /workflow-dashboard',
    'next_action': 'Consult workflow dashboard'
})

print(f"**Status:** {phase_info['description']}")
print(f"**Next Command:** {phase_info['next_command']}")
print(f"**Next Action:** {phase_info['next_action']}")
```

5. **Show deliverables status**:
```python
print("\n" + "─" * 70)
print("📄 **DELIVERABLES:**\n")

cursor.execute("""
    SELECT phase_number, phase_name, document_path, status, approved_at
    FROM deliverables
    ORDER BY phase_number
""")

deliverables = cursor.fetchall()

if deliverables:
    for phase_num, phase_name, doc_path, status, approved_at in deliverables:
        status_icon = {
            'draft': '📝',
            'in-progress': '🔄',
            'approved': '✅',
            'completed': '✅',
            'needs-revision': '⚠️'
        }.get(status, '❓')

        approval_date = f" ({approved_at[:10]})" if approved_at else ""
        print(f"  {status_icon} Phase {phase_num} ({phase_name}): {status.title()}{approval_date}")
        print(f"     {doc_path}")
else:
    print("  No deliverables created yet")
```

6. **Show task summary** (if Phase 4):
```python
if phase_num == 4 or 'implementation' in current_phase:
    print("\n" + "─" * 70)
    print("✅ **TASK SUMMARY:**\n")

    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending
        FROM tasks
        WHERE phase_number = 4
    """)

    total, completed, in_progress, pending = cursor.fetchone()

    if total and total > 0:
        pct_complete = int((completed / total) * 100)
        print(f"  Total Tasks: {total}")
        print(f"  ✅ Completed: {completed} ({pct_complete}%)")
        print(f"  🔄 In Progress: {in_progress}")
        print(f"  ⏳ Pending: {pending}")
    else:
        print("  No tasks defined yet")
```

7. **Show Review Board status** (if Phase 3.5):
```python
if phase_num == 3.5 or 'review' in current_phase:
    print("\n" + "─" * 70)
    print("🔍 **REVIEW BOARD STATUS:**\n")

    cursor.execute("""
        SELECT session_number, overall_verdict, status, created_at, completed_at
        FROM review_board_sessions
        ORDER BY created_at DESC LIMIT 1
    """)

    session = cursor.fetchone()
    if session:
        sess_num, verdict, status, created, completed = session
        print(f"  Session: #{sess_num}")
        print(f"  Status: {status}")
        if verdict:
            print(f"  Overall Verdict: {verdict}")

        # Get individual verdicts
        cursor.execute("""
            SELECT executive_role, verdict, blockers_count, concerns_count
            FROM review_board_findings
            WHERE session_id = (SELECT id FROM review_board_sessions ORDER BY created_at DESC LIMIT 1)
        """)

        findings = cursor.fetchall()
        if findings:
            print("\n  Executive Verdicts:")
            for exec_role, verdict, blockers, concerns in findings:
                icon = "✅" if verdict == "APPROVED" else "⚠️" if verdict == "APPROVED_WITH_CONCERNS" else "❌"
                print(f"    {icon} {exec_role.upper()}: {verdict}")
                if blockers > 0:
                    print(f"       Blockers: {blockers}")
                if concerns > 0:
                    print(f"       Concerns: {concerns}")
    else:
        print("  No Review Board session started yet")
```

8. **Footer**:
```python
print("\n" + "═" * 70)
print(f"Last Updated: {updated_at}")
print(f"Project Directory: ~/.claude/projects/{project_slug}/")
print(f"Database: ~/.claude/projects/{project_slug}/workflow.db")
print("═" * 70)
print()

conn.close()
```

## Important

- Shows real-time status from project-specific database
- Displays clear next steps and commands
- Tracks progress across all 6 phases (including Review Board)
- Can be run without arguments from within project directory
