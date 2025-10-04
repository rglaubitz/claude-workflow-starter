#!/usr/bin/env python3
"""
Execution Coordinator - Phase 4 Communication Infrastructure

Initializes SQLite schema for Phase 4 execution team communication,
handoff logging, quality gates, and SOP compliance tracking.

Used by: execution-director, delivery-coordinator, quality-enforcer, blocker-resolver, progress-tracker

Usage:
    python3 execution-coordinator.py init <project-name>
    python3 execution-coordinator.py health <project-name>
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime


def get_db_path(project_name):
    """Get path to project workflow database"""
    home = Path.home()
    db_path = home / ".claude" / "projects" / project_name / "workflow.db"
    return db_path


def init_execution_schema(db_path):
    """Initialize Phase 4 execution communication schema"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Agent Messages Table (Inter-agent communication)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            from_agent TEXT NOT NULL,
            to_agent TEXT NOT NULL,
            message_type TEXT NOT NULL,  -- 'task_assignment', 'status_update', 'handoff_notification', 'blocker_alert', 'clarification'
            content TEXT NOT NULL,
            task_id TEXT,
            priority TEXT,  -- 'P0', 'P1', 'P2'
            acknowledged BOOLEAN DEFAULT 0
        )
    """)

    # Handoff Log Table (Team handoffs)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS handoff_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            from_team TEXT NOT NULL,
            to_team TEXT NOT NULL,
            deliverable TEXT NOT NULL,
            handoff_package TEXT,  -- JSON: {deliverable, docs, tests, context, notes}
            status TEXT NOT NULL,  -- 'initiated', 'confirmed', 'complete', 'rejected'
            confirmed_by TEXT,
            confirmed_at DATETIME,
            notes TEXT
        )
    """)

    # Quality Gates Table (Gate enforcement tracking)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_gates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            gate_level TEXT NOT NULL,  -- 'task', 'feature', 'epic', 'phase'
            item_id TEXT NOT NULL,
            item_name TEXT NOT NULL,
            gate_status TEXT NOT NULL,  -- 'passed', 'failed'
            checks_run TEXT,  -- JSON: list of checks performed
            failed_checks TEXT,  -- JSON: list of failed checks (if failed)
            enforced_by TEXT DEFAULT 'quality-enforcer'
        )
    """)

    # SOP Compliance Table (Standard Operating Procedure tracking)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sop_compliance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            sop_name TEXT NOT NULL,  -- 'task_completion', 'team_handoff', 'quality_gate_enforcement', 'blocker_escalation', 'daily_sync'
            item_id TEXT NOT NULL,
            compliance_status TEXT NOT NULL,  -- 'compliant', 'violation', 'warning'
            violations TEXT,  -- JSON: list of violations (if non-compliant)
            agent TEXT,
            notes TEXT
        )
    """)

    # Blockers Table (Blocker tracking and resolution)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blockers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            blocker_id TEXT UNIQUE NOT NULL,
            blocker_type TEXT NOT NULL,  -- 'technical', 'information', 'resource', 'team_dependency'
            blocker_subtype TEXT,
            task_id TEXT,
            description TEXT NOT NULL,
            current_level TEXT NOT NULL,  -- 'L1', 'L2', 'L3', 'L4', 'L5'
            status TEXT NOT NULL,  -- 'active', 'resolved', 'escalated'
            on_critical_path BOOLEAN DEFAULT 0,
            resolution TEXT,
            resolved_at DATETIME
        )
    """)

    # Blocker Patterns Table (Learning from blockers)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocker_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blocker_type TEXT NOT NULL,
            blocker_subtype TEXT,
            blocker_signature TEXT NOT NULL,  -- Unique pattern identifier
            solution TEXT NOT NULL,
            solution_steps TEXT,
            resolution_level TEXT,  -- 'L1', 'L2', 'L3', 'L4'
            specialist_used TEXT,
            success_rate REAL DEFAULT 1.0,
            usage_count INTEGER DEFAULT 1,
            last_used DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Team Status Table (Real-time team tracking)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_status (
            team_name TEXT PRIMARY KEY,
            active_tasks INTEGER DEFAULT 0,
            queued_tasks INTEGER DEFAULT 0,
            capacity INTEGER DEFAULT 3,
            utilization_percent REAL DEFAULT 0,
            current_epic TEXT,
            blockers TEXT,  -- JSON: list of active blockers
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Review Deployments Table (Review agent deployment tracking)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS review_deployments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            reviewer_agent TEXT NOT NULL,
            item_id TEXT NOT NULL,
            item_type TEXT NOT NULL,  -- 'task', 'feature', 'epic'
            review_status TEXT NOT NULL,  -- 'requested', 'in_progress', 'complete'
            review_result TEXT,  -- 'approved', 'changes_requested', 'rejected'
            feedback TEXT
        )
    """)

    # Team Sync Log Table (Daily standups and syncs)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sync_date DATE NOT NULL,
            sync_type TEXT NOT NULL,  -- 'daily_standup', 'epic_kickoff', 'epic_retro'
            teams_involved TEXT NOT NULL,
            summary TEXT,  -- JSON: {team_status, cross_team_issues, blockers_summary}
            issues_identified TEXT,
            actions_taken TEXT
        )
    """)

    # Tactical Decisions Table (execution-director decisions)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tactical_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            decision_type TEXT NOT NULL,
            situation TEXT NOT NULL,
            decision_made TEXT NOT NULL,
            rationale TEXT,
            impact TEXT,
            outcome TEXT
        )
    """)

    # Initialize 7 agent teams in team_status
    teams = [
        ('Foundation', 3, 'database-architect, devops-engineer'),
        ('Backend', 5, 'backend-developer, api-architect, sql-specialist'),
        ('Frontend', 3, 'frontend-developer, ui-ux-designer'),
        ('Research', 5, 'research-manager, documentation-expert, specialists'),
        ('Quality', 10, 'qa-engineer, code-review-expert, security-auditor, performance-engineer'),
        ('Integration', 3, 'integration-specialist, mcp-bridge-engineer'),
        ('Orchestration', 999, 'execution-director, delivery-coordinator, quality-enforcer, blocker-resolver, progress-tracker')
    ]

    for team_name, capacity, members in teams:
        cursor.execute("""
            INSERT OR IGNORE INTO team_status (team_name, capacity, active_tasks, queued_tasks, utilization_percent)
            VALUES (?, ?, 0, 0, 0)
        """, (team_name, capacity))

    conn.commit()
    conn.close()

    print(f"✅ Execution communication schema initialized")
    print(f"📍 Database: {db_path}")
    print(f"\n📋 Tables created:")
    print(f"  - agent_messages (inter-agent communication)")
    print(f"  - handoff_log (team handoffs)")
    print(f"  - quality_gates (gate enforcement)")
    print(f"  - sop_compliance (SOP tracking)")
    print(f"  - blockers (blocker tracking)")
    print(f"  - blocker_patterns (learning)")
    print(f"  - team_status (7 teams initialized)")
    print(f"  - review_deployments (review tracking)")
    print(f"  - team_sync_log (sync tracking)")
    print(f"  - tactical_decisions (execution-director decisions)")


def check_health(db_path):
    """Check Phase 4 execution infrastructure health"""

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        print(f"\nRun: python3 execution-coordinator.py init <project-name>")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"📊 Phase 4 Execution Infrastructure Health Check")
    print(f"📍 Database: {db_path}\n")

    # Check table existence
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name IN ('agent_messages', 'handoff_log', 'quality_gates', 'sop_compliance',
                     'blockers', 'blocker_patterns', 'team_status', 'review_deployments',
                     'team_sync_log', 'tactical_decisions')
        ORDER BY name
    """)

    tables = cursor.fetchall()
    expected_tables = 10

    if len(tables) == expected_tables:
        print(f"✅ All {expected_tables} tables present")
    else:
        print(f"⚠️ Only {len(tables)} of {expected_tables} tables found")
        print(f"   Run init to create missing tables")

    # Show recent activity
    print(f"\n📈 Recent Activity (Last 24h):")

    cursor.execute("""
        SELECT COUNT(*) FROM agent_messages
        WHERE timestamp >= datetime('now', '-1 day')
    """)
    msg_count = cursor.fetchone()[0]
    print(f"  - Agent Messages: {msg_count}")

    cursor.execute("""
        SELECT COUNT(*) FROM handoff_log
        WHERE timestamp >= datetime('now', '-1 day')
    """)
    handoff_count = cursor.fetchone()[0]
    print(f"  - Team Handoffs: {handoff_count}")

    cursor.execute("""
        SELECT COUNT(*) FROM quality_gates
        WHERE timestamp >= datetime('now', '-1 day')
    """)
    gate_count = cursor.fetchone()[0]
    print(f"  - Quality Gates: {gate_count}")

    cursor.execute("""
        SELECT COUNT(*) FROM blockers
        WHERE status = 'active'
    """)
    active_blockers = cursor.fetchone()[0]
    print(f"  - Active Blockers: {active_blockers}")

    # Show team status
    print(f"\n🤝 Team Status:")
    cursor.execute("""
        SELECT team_name, active_tasks, queued_tasks, utilization_percent
        FROM team_status
        ORDER BY team_name
    """)

    for team_name, active, queued, util in cursor.fetchall():
        status = "✅" if util < 85 else "⚠️" if util < 95 else "❌"
        print(f"  {status} {team_name}: {active} active, {queued} queued ({util:.0f}% util)")

    # SOP Compliance
    print(f"\n✅ SOP Compliance (Last 7 Days):")
    cursor.execute("""
        SELECT sop_name,
               COUNT(*) as total,
               SUM(CASE WHEN compliance_status = 'compliant' THEN 1 ELSE 0 END) as compliant,
               ROUND(100.0 * SUM(CASE WHEN compliance_status = 'compliant' THEN 1 ELSE 0 END) / COUNT(*), 1) as rate
        FROM sop_compliance
        WHERE timestamp >= datetime('now', '-7 days')
        GROUP BY sop_name
    """)

    sop_results = cursor.fetchall()
    if sop_results:
        for sop_name, total, compliant, rate in sop_results:
            status = "✅" if rate >= 95 else "⚠️" if rate >= 85 else "❌"
            print(f"  {status} {sop_name}: {rate}% ({compliant}/{total})")
    else:
        print(f"  No SOP compliance data yet")

    conn.close()
    print(f"\n✅ Health check complete")


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 execution-coordinator.py init <project-name>")
        print("  python3 execution-coordinator.py health <project-name>")
        sys.exit(1)

    command = sys.argv[1]
    project_name = sys.argv[2]

    db_path = get_db_path(project_name)

    if command == "init":
        # Ensure project directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)
        init_execution_schema(db_path)

    elif command == "health":
        check_health(db_path)

    else:
        print(f"Unknown command: {command}")
        print("Valid commands: init, health")
        sys.exit(1)


if __name__ == "__main__":
    main()
