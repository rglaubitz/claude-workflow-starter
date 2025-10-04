---
description: "Visual overview of all phases across projects"
argument-hint: "[project-slug]"
allowed-tools: Bash, Read
---

# Workflow Dashboard: $ARGUMENTS

You are displaying the **workflow dashboard** for the 5-Phase Workflow System.

## Your Task

```python
import os
from pathlib import Path
import sqlite3
from datetime import datetime

projects_dir = Path.home() / ".claude" / "projects"
project_slug = "$ARGUMENTS"

def get_all_projects():
    """Get list of all projects with workflow databases."""
    projects = []
    if projects_dir.exists():
        for proj_dir in projects_dir.iterdir():
            if proj_dir.is_dir() and (proj_dir / "workflow.db").exists():
                try:
                    conn = sqlite3.connect(str(proj_dir / "workflow.db"))
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT project_name, current_phase, phase_number, created_at
                        FROM workflow LIMIT 1
                    """)
                    result = cursor.fetchone()
                    conn.close()

                    if result:
                        projects.append({
                            'slug': proj_dir.name,
                            'name': result[0],
                            'phase': result[1],
                            'phase_num': result[2],
                            'created': result[3]
                        })
                except:
                    pass
    return projects


def display_project_dashboard(slug):
    """Display detailed dashboard for a single project."""
    db_path = projects_dir / slug / "workflow.db"

    if not db_path.exists():
        print(f"❌ Project not found: {slug}")
        return

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Get workflow info
    cursor.execute("""
        SELECT id, project_name, current_phase, phase_number, created_at, updated_at
        FROM workflow LIMIT 1
    """)
    result = cursor.fetchone()

    if not result:
        print(f"❌ Workflow not initialized: {slug}")
        conn.close()
        return

    wf_id, project_name, current_phase, phase_num, created_at, updated_at = result

    # Header
    print()
    print("╔" + "═" * 68 + "╗")
    print(f"║  WORKFLOW DASHBOARD: {project_name[:48]:<48} ║")
    print("╚" + "═" * 68 + "╝")
    print()

    # Phase progression
    phases = [
        (0, "BRIEF", "Project Brief Uploaded", "00-project-brief.md"),
        (1, "VISION", "Define What & Why", "01-vision.md"),
        (2, "MISSION", "Research How to Build", "02-mission.md"),
        (3, "EXECUTION", "Plan Implementation", "03-execution-plan.md"),
        (3.5, "REVIEW", "C-Suite Approval Gate", "review-board/"),
        (4, "IMPLEMENT", "Build the Project", "04-implementation-report.md"),
        (5, "TEST", "Validate & Verify", "05-test-plan.md")
    ]

    for phase_number, phase_name, phase_desc, deliverable in phases:
        # Determine status
        if phase_num > phase_number:
            marker = "█"
            status = "✓ COMPLETE"
        elif phase_num == phase_number:
            marker = "▓"
            status = "▶ IN PROGRESS"
        else:
            marker = "░"
            status = "○ PENDING"

        # Get deliverable status
        deliv_status = ""
        if phase_number != 0:  # Skip brief
            cursor.execute("""
                SELECT status, approved_at FROM deliverables
                WHERE phase_number = ?
            """, (int(phase_number),))

            deliv_result = cursor.fetchone()
            if deliv_result:
                d_status, d_approved = deliv_result
                if d_status == 'approved':
                    deliv_status = f" [✅ Approved]"
                elif d_status == 'in-progress':
                    deliv_status = f" [🔄 In Progress]"
                elif d_status == 'draft':
                    deliv_status = f" [📝 Draft]"

        # Get task status (Phase 4 only)
        task_status = ""
        if phase_number == 4:
            cursor.execute("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
                FROM tasks WHERE phase_number = 4
            """)
            total, completed = cursor.fetchone()
            if total and total > 0:
                task_status = f" [{completed}/{total} tasks]"

        # Review Board status (Phase 3.5)
        review_status = ""
        if phase_number == 3.5:
            cursor.execute("""
                SELECT overall_verdict, status FROM review_board_sessions
                ORDER BY created_at DESC LIMIT 1
            """)
            review_result = cursor.fetchone()
            if review_result:
                verdict, r_status = review_result
                if verdict == 'APPROVED':
                    review_status = " [✅ Approved]"
                elif verdict == 'CONDITIONALLY_APPROVED':
                    review_status = " [⚠️ Conditional]"
                elif verdict == 'REJECTED':
                    review_status = " [❌ Rejected]"
                elif r_status == 'in-progress':
                    review_status = " [🔄 In Review]"

        # Print phase line
        phase_label = f"Phase {phase_number}"
        print(f"{marker * 3} {phase_label:<12} {phase_name:<12} {status:<16}")
        print(f"    {phase_desc}{deliv_status}{task_status}{review_status}")
        print()

    # Timeline
    print("─" * 70)
    print("📅 **TIMELINE:**\n")

    created = datetime.fromisoformat(created_at)
    updated = datetime.fromisoformat(updated_at)
    elapsed = (updated - created).days

    print(f"  Started: {created_at[:10]}")
    print(f"  Updated: {updated_at[:10]}")
    print(f"  Elapsed: {elapsed} days")

    # Phase durations
    cursor.execute("""
        SELECT phase_number, phase_name, MIN(created_at) as started, MAX(approved_at) as completed
        FROM deliverables
        WHERE approved_at IS NOT NULL
        GROUP BY phase_number
        ORDER BY phase_number
    """)

    completed_phases = cursor.fetchall()
    if completed_phases:
        print("\n  Completed Phases:")
        for p_num, p_name, started, completed in completed_phases:
            start_dt = datetime.fromisoformat(started)
            complete_dt = datetime.fromisoformat(completed)
            duration = (complete_dt - start_dt).days
            print(f"    Phase {p_num} ({p_name}): {duration} days")

    # Statistics
    print("\n" + "─" * 70)
    print("📊 **STATISTICS:**\n")

    # Deliverables count
    cursor.execute("SELECT COUNT(*) FROM deliverables")
    total_deliverables = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM deliverables WHERE status = 'approved'")
    approved_deliverables = cursor.fetchone()[0]

    print(f"  Deliverables: {approved_deliverables}/{total_deliverables} approved")

    # Tasks count (if Phase 4)
    if phase_num >= 4:
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
            FROM tasks
        """)
        total_tasks, completed_tasks = cursor.fetchone()
        if total_tasks and total_tasks > 0:
            pct = int((completed_tasks / total_tasks) * 100)
            print(f"  Tasks: {completed_tasks}/{total_tasks} completed ({pct}%)")

    # Review Board sessions
    cursor.execute("SELECT COUNT(*) FROM review_board_sessions")
    review_sessions = cursor.fetchone()[0]
    if review_sessions > 0:
        print(f"  Review Board Sessions: {review_sessions}")

    # Next steps
    print("\n" + "─" * 70)
    print("🎯 **NEXT STEPS:**\n")

    phase_next_steps = {
        'brief-uploaded': '  Run: /start-vision',
        'vision-in-progress': '  Run: /approve-vision',
        'vision-approved': '  Run: /start-mission',
        'mission-in-progress': '  Run: /approve-mission',
        'mission-approved': '  Run: /start-execution-planning',
        'execution-planning-in-progress': '  Run: /approve-execution-plan',
        'execution-plan-approved-pending-review': '  Run: /start-review-board',
        'review-board-complete': '  Run: /approve-review-board or /address-review-concerns',
        'review-board-approved': '  Run: /start-implementation',
        'implementation-in-progress': '  Run: /complete-implementation',
        'implementation-complete': '  Run: /start-testing',
        'testing-in-progress': '  Run: /approve-testing',
        'project-complete': '  🎉 Project complete! Deploy or start new project.'
    }

    next_step = phase_next_steps.get(current_phase, '  Check /phase-status for details')
    print(next_step)

    # Footer
    print("\n" + "═" * 70)
    print(f"Project Directory: ~/.claude/projects/{slug}/")
    print(f"Database: ~/.claude/projects/{slug}/workflow.db")
    print("═" * 70)
    print()

    conn.close()


def display_all_projects_summary():
    """Display summary of all projects."""
    projects = get_all_projects()

    if not projects:
        print()
        print("═" * 70)
        print("  NO PROJECTS FOUND")
        print("═" * 70)
        print()
        print("Create a new project:")
        print("  1. Create project brief: ~/.claude/projects/<slug>/00-project-brief.md")
        print("  2. Run: /start-project \"<slug>\"")
        print()
        return

    print()
    print("╔" + "═" * 68 + "╗")
    print("║  ALL PROJECTS - WORKFLOW DASHBOARD" + " " * 33 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    # Sort by phase (active first), then by created date
    projects.sort(key=lambda p: (p['phase_num'] == 5, -p['phase_num'], p['created']), reverse=False)

    for proj in projects:
        # Phase status indicator
        if proj['phase_num'] == 5 and 'complete' in proj['phase']:
            status_icon = "✅"
        elif proj['phase_num'] >= 4:
            status_icon = "🔨"  # Building
        elif proj['phase_num'] >= 1:
            status_icon = "📋"  # Planning
        else:
            status_icon = "📝"  # Briefing

        # Phase name
        phase_names = {
            0: "Brief",
            1: "Vision",
            2: "Mission",
            3: "Execution",
            3.5: "Review",
            4: "Implementation",
            5: "Testing"
        }
        phase_name = phase_names.get(proj['phase_num'], "Unknown")

        print(f"{status_icon} {proj['name']:<30} │ Phase {proj['phase_num']}: {phase_name:<15}")
        print(f"   Slug: {proj['slug']:<28} │ Status: {proj['phase']}")
        print()

    print("─" * 70)
    print(f"Total Projects: {len(projects)}")
    print()
    print("**View project details:** /workflow-dashboard <project-slug>")
    print("**Check phase status:** /phase-status <project-slug>")
    print("═" * 70)
    print()


# Main execution
if project_slug:
    display_project_dashboard(project_slug)
else:
    display_all_projects_summary()
```

## Important

- Shows visual progress through all 6 phases (including Review Board)
- Displays deliverable status, task counts, and review verdicts
- Lists all projects when no argument provided
- Clear next steps for each phase
- Timeline tracking with phase durations
