---
description: "Initialize new project with 5-phase workflow (requires project brief)"
argument-hint: "<project-slug>"
allowed-tools: Bash, Write, Read
---

# Start Project: $ARGUMENTS

You are initializing a new project in the **5-Phase Workflow System**.

## Your Task

1. **Validate the project slug**:
```python
import re
project_slug = "$ARGUMENTS"

# Validate slug format (lowercase, hyphens only, no spaces)
if ' ' in project_slug:
    print("❌ Error: Project slug cannot contain spaces")
    print("   Use hyphens instead: my-awesome-project")
    exit(1)

if project_slug != project_slug.lower():
    print("❌ Error: Project slug must be lowercase")
    exit(1)

if not re.match(r'^[a-z0-9-]+$', project_slug):
    print("❌ Error: Project slug can only contain lowercase letters, numbers, and hyphens")
    exit(1)
```

2. **Check for project brief**:
```python
import os
from pathlib import Path

project_dir = Path.home() / ".claude" / "projects" / project_slug
brief_path = project_dir / "00-project-brief.md"

if not brief_path.exists():
    print(f"""
❌ **PROJECT BRIEF NOT FOUND**

Before starting a project, you must create a project brief.

**Steps:**
1. Create directory: mkdir -p {project_dir}
2. Copy template: cp ~/.claude/templates/phases/00-project-brief-template.md {brief_path}
3. Fill out all sections in the brief
4. Run this command again: /start-project "{project_slug}"

**What goes in the brief:**
- Problem statement
- Goals and success criteria
- Requirements (must-have, should-have, nice-to-have)
- Constraints (budget, timeline, technical)
- Reference materials and inspiration
- UX preferences
- Success metrics

See template for complete structure.
""")
    exit(1)

print(f"✅ Project brief found: {brief_path}")
```

3. **Initialize project-specific database**:
```bash
echo "🔧 Creating project-specific database..."
python3 ~/.claude/scripts/init-project-database.py "$ARGUMENTS"
```

This will:
- Create isolated database at `~/.claude/projects/$ARGUMENTS/workflow.db`
- Set up 6 tables (workflow, deliverables, review_board_sessions, review_board_findings, tasks, agent_assignments)
- Initialize workflow state

4. **Create project structure**:
```bash
PROJECT_DIR="$HOME/.claude/projects/$ARGUMENTS"

# Create supporting directories
mkdir -p "$PROJECT_DIR/research"
mkdir -p "$PROJECT_DIR/examples"
mkdir -p "$PROJECT_DIR/review"
mkdir -p "$PROJECT_DIR/agent-notes"
mkdir -p "$PROJECT_DIR/review-board"

# Create placeholder READMEs
echo "# Research & Findings

This directory contains technical research, dependency analysis, and architectural decisions.

Created during Phase 2 (Mission)." > "$PROJECT_DIR/research/README.md"

echo "# Code Examples & References

This directory contains code samples, UI examples, and reference implementations.

Created during Phase 2 (Mission)." > "$PROJECT_DIR/examples/README.md"

echo "# Review & Approval Tracking

This directory contains user review notes and approval checkpoints.

Updated throughout all phases." > "$PROJECT_DIR/review/README.md"

echo "# Agent Communications

This directory contains agent collaboration logs, handoffs, and decision records.

Updated during Phase 4 (Implementation)." > "$PROJECT_DIR/agent-notes/README.md"

echo "# Review Board Sessions

This directory contains C-suite executive review sessions (Phase 3.5).

Each session creates a timestamped subdirectory with individual executive reports." > "$PROJECT_DIR/review-board/README.md"

echo "✅ Project structure created"
```

5. **Initialize workflow in database**:
```python
import sqlite3
import uuid
from datetime import datetime

db_path = project_dir / "workflow.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

workflow_id = str(uuid.uuid4())

cursor.execute("""
    INSERT INTO workflow (id, project_name, project_slug, current_phase, phase_number, created_at)
    VALUES (?, ?, ?, 'brief-uploaded', 0, CURRENT_TIMESTAMP)
""", (workflow_id, project_slug.replace('-', ' ').title(), project_slug))

conn.commit()
conn.close()

print(f"✅ Workflow initialized with ID: {workflow_id}")
```

6. **Display success message**:
```
🎉 **PROJECT INITIALIZED SUCCESSFULLY**

**Project:** $ARGUMENTS
**Location:** ~/.claude/projects/$ARGUMENTS/
**Database:** ~/.claude/projects/$ARGUMENTS/workflow.db

**Project Structure:**
├── 00-project-brief.md ✅ (User-provided)
├── research/ (Phase 2)
├── examples/ (Phase 2)
├── review/ (All phases)
├── agent-notes/ (Phase 4)
└── review-board/ (Phase 3.5)

**5-Phase Workflow:**
- **Phase 1: Vision** - Define what and why
- **Phase 2: Mission** - Research how to build it
- **Phase 3: Execution Planning** - Create detailed plan
- **Phase 3.5: Review Board** - C-suite approval gate
- **Phase 4: Implementation** - Build it
- **Phase 5: Testing** - Validate and verify

**Current Status:**
✅ Phase 0: Project Brief uploaded
⏳ Phase 1: Ready to begin

**Next Steps:**
1. Review your project brief: ~/.claude/projects/$ARGUMENTS/00-project-brief.md
2. When ready to begin, run: `/start-vision`
3. Check project status: `/phase-status`
4. View workflow dashboard: `/workflow-dashboard`

**Commands Available:**
- `/phase-status` - Show current phase and progress
- `/workflow-dashboard` - Visual overview of all phases
- `/start-vision` - Begin Phase 1 (Vision)

---
**The 5-Phase Workflow System is now active for this project.**
```

## Important

- The project brief must exist before running this command
- Each project gets its own isolated database
- Project slug becomes the identifier for all future commands
- All phase documents will be created as phases progress
- Do NOT manually create phase documents - let the phase commands do it
