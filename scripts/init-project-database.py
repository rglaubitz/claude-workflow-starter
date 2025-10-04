#!/usr/bin/env python3
"""
Project Database Initialization Script

Creates a fresh, isolated database for each project in the 5-phase workflow system.
Each project gets its own SQLite database to prevent cross-project contamination.

Usage:
    python3 init-project-database.py <project-slug>

Example:
    python3 init-project-database.py my-awesome-project
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

CLAUDE_HOME = Path.home() / ".claude"
PROJECTS_PATH = CLAUDE_HOME / "projects"


def create_project_database(project_slug: str) -> Path:
    """
    Create a fresh project-specific database with complete schema.

    Args:
        project_slug: URL-friendly project identifier

    Returns:
        Path to the created database
    """
    # Create project directory if it doesn't exist
    project_dir = PROJECTS_PATH / project_slug
    project_dir.mkdir(parents=True, exist_ok=True)

    db_path = project_dir / "workflow.db"

    # Remove old database if exists (fresh start)
    if db_path.exists():
        print(f"⚠️  Existing database found at {db_path}")
        response = input("Delete and recreate? (yes/no): ")
        if response.lower() != "yes":
            print("Aborted.")
            sys.exit(1)
        db_path.unlink()

    # Create new database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # Table 1: Workflow state
    cursor.execute("""
        CREATE TABLE workflow (
            id TEXT PRIMARY KEY,
            project_name TEXT NOT NULL,
            project_slug TEXT NOT NULL,
            current_phase TEXT NOT NULL DEFAULT 'brief-uploaded',
            phase_number INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table 2: Phase deliverables
    cursor.execute("""
        CREATE TABLE deliverables (
            id TEXT PRIMARY KEY,
            phase_number INTEGER NOT NULL,
            phase_name TEXT NOT NULL,
            document_path TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'draft',
            approved_at TIMESTAMP,
            approved_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table 3: Review Board sessions
    cursor.execute("""
        CREATE TABLE review_board_sessions (
            id TEXT PRIMARY KEY,
            session_number INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'in-progress',
            overall_verdict TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    """)

    # Table 4: Review Board findings (C-suite reviews)
    cursor.execute("""
        CREATE TABLE review_board_findings (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            executive_role TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            verdict TEXT NOT NULL,
            report_path TEXT NOT NULL,
            blockers_count INTEGER DEFAULT 0,
            concerns_count INTEGER DEFAULT 0,
            recommendations_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES review_board_sessions(id)
        )
    """)

    # Table 5: Tasks
    cursor.execute("""
        CREATE TABLE tasks (
            id TEXT PRIMARY KEY,
            phase_number INTEGER NOT NULL,
            description TEXT NOT NULL,
            assigned_agent TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            dependencies TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    """)

    # Table 6: Agent assignments
    cursor.execute("""
        CREATE TABLE agent_assignments (
            id TEXT PRIMARY KEY,
            phase_number INTEGER NOT NULL,
            agent_name TEXT NOT NULL,
            role TEXT NOT NULL,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Indexes for performance
    cursor.execute("CREATE INDEX idx_deliverables_phase ON deliverables(phase_number)")
    cursor.execute("CREATE INDEX idx_deliverables_status ON deliverables(status)")
    cursor.execute("CREATE INDEX idx_tasks_phase ON tasks(phase_number)")
    cursor.execute("CREATE INDEX idx_tasks_status ON tasks(status)")
    cursor.execute("CREATE INDEX idx_tasks_agent ON tasks(assigned_agent)")
    cursor.execute("CREATE INDEX idx_review_sessions_status ON review_board_sessions(status)")
    cursor.execute("CREATE INDEX idx_review_findings_session ON review_board_findings(session_id)")
    cursor.execute("CREATE INDEX idx_agent_assignments_phase ON agent_assignments(phase_number)")

    conn.commit()
    conn.close()

    return db_path


def verify_schema(db_path: Path):
    """Verify database schema is correct."""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    expected_tables = [
        'workflow',
        'deliverables',
        'review_board_sessions',
        'review_board_findings',
        'tasks',
        'agent_assignments'
    ]

    print("\n📊 Database Schema Verification:")
    print("-" * 50)

    for table in expected_tables:
        if table in tables:
            # Count columns
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"✅ {table}: {len(columns)} columns")
        else:
            print(f"❌ {table}: MISSING")

    # Get all indexes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = [row[0] for row in cursor.fetchall()]

    print(f"\n📑 Indexes Created: {len(indexes)}")

    conn.close()


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: init-project-database.py <project-slug>")
        print("\nExample:")
        print("  python3 init-project-database.py my-awesome-project")
        sys.exit(1)

    project_slug = sys.argv[1]

    # Validate slug (no spaces, all lowercase, hyphens ok)
    if ' ' in project_slug:
        print("❌ Error: Project slug cannot contain spaces")
        print("   Use hyphens instead: my-awesome-project")
        sys.exit(1)

    if project_slug != project_slug.lower():
        print("❌ Error: Project slug must be lowercase")
        sys.exit(1)

    print(f"\n🔧 Initializing project database for: {project_slug}")
    print("-" * 50)

    db_path = create_project_database(project_slug)

    print(f"\n✅ Database created: {db_path}")

    verify_schema(db_path)

    print("\n" + "=" * 50)
    print("🎉 Project database ready!")
    print("=" * 50)
    print(f"\nNext steps:")
    print(f"1. User fills out project brief:")
    print(f"   ~/.claude/projects/{project_slug}/00-project-brief.md")
    print(f"\n2. Run: /start-project \"{project_slug}\"")
    print(f"\n3. Begin Phase 1 (Vision)")


if __name__ == "__main__":
    main()
