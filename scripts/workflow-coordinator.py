#!/usr/bin/env python3
"""
Workflow Coordinator - Orchestrates the 5-Phase Project Workflow

This script manages the lifecycle of projects through the 5 phases:
1. Vision (Brainstorm → Key Concepts → "The Vision")
2. Mission (Research → Dependencies → "The Mission")
3. Execution (Planning → Tasks → "The Execution")
4. Execute (Implementation)
5. Testing (Validation → Quality Gates)

Enhanced with:
- Project type detection integration
- Automatic phase detection from codebase state
- Phase-appropriate agent recommendations
- Project context awareness

Author: Claude Code
"""

import sqlite3
import os
import json
import uuid
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

# Configuration
CLAUDE_HOME = Path.home() / ".claude"
DB_PATH = CLAUDE_HOME / "data" / "workflow.db"
TEMPLATES_PATH = CLAUDE_HOME / "templates"
PROJECTS_PATH = CLAUDE_HOME / "projects"

# Phase definitions
PHASES = {
    1: {
        "name": "Vision",
        "description": "Brainstorm → Key Concepts → 'The Vision'",
        "primary_agents": ["prd-expert", "agent-architecture-designer"],
        "support_agents": ["research-manager"],
        "deliverable": "vision",
        "template": "vision-template.md"
    },
    2: {
        "name": "Mission",
        "description": "Research → Dependencies → 'The Mission'",
        "primary_agents": ["research-manager", "documentation-expert"],
        "support_agents": ["integration-specialist", "mcp-bridge-engineer"],
        "deliverable": "mission",
        "template": "mission-template.md"
    },
    3: {
        "name": "Execution Planning",
        "description": "Planning → Tasks → 'The Execution'",
        "primary_agents": ["project-task-planner", "task-manager"],
        "support_agents": ["agent-architecture-designer"],
        "deliverable": "execution",
        "template": "execution-template.md"
    },
    4: {
        "name": "Execute",
        "description": "Implementation",
        "primary_agents": ["task-manager"],
        "support_agents": "all",
        "deliverable": None,
        "template": None
    },
    5: {
        "name": "Testing",
        "description": "Validation → Quality Gates",
        "primary_agents": ["agent-testing-engineer"],
        "support_agents": ["code-review-expert"],
        "deliverable": "test-plan",
        "template": "test-plan-template.md"
    }
}


class WorkflowCoordinator:
    """Manages project workflow state and phase transitions."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Ensure the workflow database exists."""
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Workflow database not found at {self.db_path}. "
                "Run database initialization first."
            )

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.Connection(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def create_project_structure(self, project_name: str, project_slug: str) -> Path:
        """
        Create the complete project folder structure with all templates.

        Args:
            project_name: Display name of the project
            project_slug: Slugified name for folder

        Returns:
            project_path: Path to the created project folder
        """
        import shutil

        # Create project folder
        project_path = PROJECTS_PATH / project_slug
        project_path.mkdir(parents=True, exist_ok=True)

        # Create subfolder structure
        (project_path / "research").mkdir(exist_ok=True)
        (project_path / "examples" / "code-samples").mkdir(parents=True, exist_ok=True)
        (project_path / "examples" / "reference-implementations").mkdir(parents=True, exist_ok=True)
        (project_path / "review").mkdir(exist_ok=True)
        (project_path / "agent-notes").mkdir(exist_ok=True)

        # Copy templates
        templates_to_copy = {
            "project-brief-template.md": "00-project-brief.md",
            "vision-template.md": "01-vision.md",
            "mission-template.md": "02-mission.md",
            "execution-template.md": "03-execution.md",
            "test-plan-template.md": "04-test-plan.md",
            "research-readme-template.md": "research/README.md",
            "technical-research-template.md": "research/technical-research.md",
            "architecture-decisions-template.md": "research/architecture-decisions.md",
            "dependencies-template.md": "research/dependencies.md",
            "references-template.md": "research/references.md",
            "examples-readme-template.md": "examples/README.md",
            "review-checklist-template.md": "review/review-checklist.md",
            "feedback-template.md": "review/feedback.md",
            "communication-log-template.md": "agent-notes/communication-log.md",
            "decisions-log-template.md": "agent-notes/decisions-log.md",
        }

        # Copy and populate templates
        for template_name, dest_path in templates_to_copy.items():
            src = TEMPLATES_PATH / template_name
            dst = project_path / dest_path

            if src.exists():
                shutil.copy(src, dst)

                # Replace placeholders
                content = dst.read_text()
                content = content.replace("[Project Name]", project_name)
                content = content.replace("[project-slug]", project_slug)
                content = content.replace("[Date]", datetime.now().strftime("%Y-%m-%d"))
                dst.write_text(content)

        return project_path

    def create_workflow(self, project_name: str, user_prompt: str = "") -> Tuple[str, Path]:
        """
        Create a new workflow for a project.

        Args:
            project_name: Name of the project
            user_prompt: Original user request/prompt

        Returns:
            (workflow_id, project_path): UUID of workflow and path to project folder
        """
        workflow_id = str(uuid.uuid4())
        project_slug = project_name.lower().replace(" ", "-").replace("_", "-")

        # Create project structure
        project_path = self.create_project_structure(project_name, project_slug)

        # Add user prompt to project brief if provided
        if user_prompt:
            brief_path = project_path / "00-project-brief.md"
            if brief_path.exists():
                content = brief_path.read_text()
                content = content.replace(
                    "<!-- The initial user prompt/request that started this project -->",
                    user_prompt
                )
                brief_path.write_text(content)

        # Create workflow in database
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO workflows (id, project_name, current_phase, phase_status)
                VALUES (?, ?, 1, 'in_progress')
            """, (workflow_id, project_name))
            conn.commit()

        return workflow_id, project_path

    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Get workflow details by ID."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM workflows WHERE id = ?",
                (workflow_id,)
            ).fetchone()

            if row:
                return dict(row)
        return None

    def get_workflow_by_project(self, project_name: str) -> Optional[Dict]:
        """Get workflow by project name."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM workflows WHERE project_name = ?",
                (project_name,)
            ).fetchone()

            if row:
                return dict(row)
        return None

    def list_workflows(self, status: Optional[str] = None) -> List[Dict]:
        """List all workflows, optionally filtered by status."""
        with self._get_connection() as conn:
            if status:
                rows = conn.execute(
                    "SELECT * FROM workflows WHERE phase_status = ? ORDER BY updated_at DESC",
                    (status,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM workflows ORDER BY updated_at DESC"
                ).fetchall()

            return [dict(row) for row in rows]

    def update_phase(self, workflow_id: str, new_phase: int, status: str = "in_progress"):
        """Update workflow to a new phase."""
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE workflows
                SET current_phase = ?, phase_status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_phase, status, workflow_id))
            conn.commit()

    def get_phase_info(self, phase_number: int) -> Dict:
        """Get information about a specific phase."""
        if phase_number not in PHASES:
            raise ValueError(f"Invalid phase number: {phase_number}")
        return PHASES[phase_number]

    def add_deliverable(
        self,
        workflow_id: str,
        phase: int,
        deliverable_type: str,
        content_path: str,
        status: str = "draft"
    ) -> str:
        """Add a phase deliverable."""
        deliverable_id = str(uuid.uuid4())

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO phase_deliverables
                (id, workflow_id, phase, deliverable_type, content_path, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (deliverable_id, workflow_id, phase, deliverable_type, content_path, status))
            conn.commit()

        return deliverable_id

    def get_deliverables(self, workflow_id: str, phase: Optional[int] = None) -> List[Dict]:
        """Get deliverables for a workflow, optionally filtered by phase."""
        with self._get_connection() as conn:
            if phase:
                rows = conn.execute("""
                    SELECT * FROM phase_deliverables
                    WHERE workflow_id = ? AND phase = ?
                    ORDER BY created_at DESC
                """, (workflow_id, phase)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT * FROM phase_deliverables
                    WHERE workflow_id = ?
                    ORDER BY phase, created_at DESC
                """, (workflow_id,)).fetchall()

            return [dict(row) for row in rows]

    def add_task(
        self,
        workflow_id: str,
        phase: int,
        task_description: str,
        assigned_agent: Optional[str] = None,
        dependencies: Optional[List[str]] = None
    ) -> str:
        """Add a task to a workflow phase."""
        task_id = str(uuid.uuid4())
        deps_json = json.dumps(dependencies) if dependencies else None

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO phase_tasks
                (id, workflow_id, phase, task_description, assigned_agent, dependencies)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (task_id, workflow_id, phase, task_description, assigned_agent, deps_json))
            conn.commit()

        return task_id

    def get_tasks(
        self,
        workflow_id: str,
        phase: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """Get tasks for a workflow."""
        with self._get_connection() as conn:
            query = "SELECT * FROM phase_tasks WHERE workflow_id = ?"
            params = [workflow_id]

            if phase:
                query += " AND phase = ?"
                params.append(phase)

            if status:
                query += " AND status = ?"
                params.append(status)

            query += " ORDER BY created_at"

            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    def update_task_status(self, task_id: str, status: str):
        """Update task status."""
        with self._get_connection() as conn:
            if status == "completed":
                conn.execute("""
                    UPDATE phase_tasks
                    SET status = ?, completed_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (status, task_id))
            else:
                conn.execute("""
                    UPDATE phase_tasks
                    SET status = ?
                    WHERE id = ?
                """, (status, task_id))
            conn.commit()

    def validate_phase_complete(self, workflow_id: str, phase: int) -> Tuple[bool, List[str]]:
        """
        Validate if a phase is complete and can transition.

        Returns:
            (is_complete, issues): Tuple of completion status and list of issues
        """
        issues = []

        # Check if deliverable exists
        deliverables = self.get_deliverables(workflow_id, phase)
        phase_info = self.get_phase_info(phase)

        if phase_info["deliverable"]:
            if not deliverables:
                issues.append(f"Missing {phase_info['deliverable']} document")
            else:
                approved = any(d["status"] == "approved" for d in deliverables)
                if not approved:
                    issues.append(f"{phase_info['deliverable']} document not approved")

        # Check if tasks are complete (for phases with tasks)
        if phase >= 3:
            tasks = self.get_tasks(workflow_id, phase)
            if tasks:
                incomplete = [t for t in tasks if t["status"] != "completed"]
                if incomplete:
                    issues.append(f"{len(incomplete)} tasks incomplete")

        return (len(issues) == 0, issues)

    def transition_phase(self, workflow_id: str) -> Tuple[bool, str]:
        """
        Transition to the next phase if current phase is complete.

        Returns:
            (success, message): Tuple of success status and message
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return (False, "Workflow not found")

        current_phase = workflow["current_phase"]

        if current_phase >= 5:
            return (False, "Already at final phase")

        # Validate current phase is complete
        is_complete, issues = self.validate_phase_complete(workflow_id, current_phase)

        if not is_complete:
            return (False, f"Cannot transition: {'; '.join(issues)}")

        # Move to next phase
        next_phase = current_phase + 1
        self.update_phase(workflow_id, next_phase)

        next_phase_info = self.get_phase_info(next_phase)
        return (True, f"Transitioned to Phase {next_phase}: {next_phase_info['name']}")

    # ========================================================================
    # PROJECT DETECTION AND CONTEXT INTEGRATION
    # ========================================================================

    def detect_project_type(self, project_path: Path) -> List[str]:
        """
        Detect project type based on files and structure.

        Returns:
            List of detected project types (e.g., ['python', 'flask', 'docker'])
        """
        project_types = []

        # Check for package managers and build tools
        if (project_path / "package.json").exists():
            project_types.append("javascript")
        if any((project_path / f).exists() for f in ["requirements.txt", "pyproject.toml", "setup.py"]):
            project_types.append("python")
        if (project_path / "go.mod").exists():
            project_types.append("go")
        if (project_path / "Cargo.toml").exists():
            project_types.append("rust")
        if any((project_path / f).exists() for f in ["pom.xml", "build.gradle"]):
            project_types.append("java")
        if (project_path / "Gemfile").exists():
            project_types.append("ruby")

        # Check for frameworks
        if any((project_path / f).exists() for f in ["next.config.js", "next.config.ts"]):
            project_types.append("nextjs")
        if (project_path / "vue.config.js").exists():
            project_types.append("vue")
        if (project_path / "manage.py").exists():
            project_types.append("django")

        # Check for infrastructure
        if any((project_path / f).exists() for f in ["Dockerfile", "docker-compose.yml"]):
            project_types.append("docker")
        if (project_path / ".github" / "workflows").exists():
            project_types.append("ci-cd")
        if (project_path / "terraform").exists() or (project_path / "main.tf").exists():
            project_types.append("terraform")

        # Check for database
        if (project_path / "migrations").exists() or (project_path / "alembic").exists():
            project_types.append("database")

        # Check for ML/AI
        if (project_path / "models").exists() or (project_path / "notebooks").exists():
            project_types.append("ml-ai")

        return project_types

    def detect_current_phase_from_state(self, project_path: Path) -> int:
        """
        Detect the appropriate workflow phase based on project state.

        Returns:
            Phase number (1-5)
        """
        # Count code files
        code_extensions = [".py", ".js", ".ts", ".go", ".java", ".rb"]
        code_files = []
        for ext in code_extensions:
            code_files.extend(project_path.glob(f"**/*{ext}"))

        code_file_count = len([f for f in code_files if f.is_file()])

        # Determine phase based on project maturity
        if code_file_count < 5:
            return 1  # Vision - New project
        elif (project_path / "tests").exists() is False and code_file_count < 20:
            return 2  # Mission - Early development, no tests yet
        elif (project_path / "tests").exists() and code_file_count < 50:
            return 3  # Execution Planning - Tests exist but still small
        elif code_file_count >= 50:
            return 4  # Execute - Active development
        else:
            return 2  # Default to Mission

    def get_recommended_agents_for_phase(
        self,
        phase: int,
        project_types: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """
        Get recommended agents for a specific phase and project type.

        Args:
            phase: Phase number (1-5)
            project_types: List of detected project types

        Returns:
            Dict with 'primary', 'support', and 'optional' agent lists
        """
        phase_info = self.get_phase_info(phase)

        recommended = {
            "primary": phase_info["primary_agents"],
            "support": phase_info["support_agents"] if phase_info["support_agents"] != "all" else [],
            "optional": []
        }

        # Add project-type-specific agents
        if project_types:
            type_specific = self._get_type_specific_agents(project_types)
            recommended["optional"] = type_specific

        # Phase 4 (Execute) includes all relevant agents
        if phase == 4 and project_types:
            all_agents = set(recommended["primary"])
            all_agents.update(self._get_type_specific_agents(project_types))
            all_agents.update(["security-auditor", "code-review-expert", "performance-engineer"])
            recommended["support"] = list(all_agents - set(recommended["primary"]))

        return recommended

    def _get_type_specific_agents(self, project_types: List[str]) -> List[str]:
        """Get agents specific to project types."""
        agents: Set[str] = set()

        type_agent_map = {
            "javascript": ["frontend-developer", "frontend-reviewer"],
            "react": ["frontend-developer", "ui-ux-designer", "accessibility-specialist"],
            "nextjs": ["frontend-developer", "ui-ux-designer"],
            "vue": ["frontend-developer", "ui-ux-designer"],
            "python": ["backend-developer", "backend-reviewer"],
            "django": ["backend-developer", "api-architect", "database-architect"],
            "flask": ["backend-developer", "api-architect"],
            "go": ["backend-developer", "backend-reviewer"],
            "java": ["backend-developer", "backend-reviewer"],
            "ruby": ["backend-developer", "backend-reviewer"],
            "rust": ["backend-developer", "performance-engineer"],
            "database": ["database-architect", "database-reviewer", "sql-specialist"],
            "ml-ai": ["ai-ml-engineer", "data-pipeline-engineer"],
            "docker": ["devops-engineer", "integration-specialist"],
            "ci-cd": ["devops-engineer"],
            "terraform": ["devops-engineer"],
        }

        for ptype in project_types:
            if ptype in type_agent_map:
                agents.update(type_agent_map[ptype])

        return list(agents)

    def load_project_context(self) -> Optional[Dict]:
        """
        Load project context from session-init.sh output.

        Returns:
            Project context dict or None if not available
        """
        context_file = CLAUDE_HOME / "data" / "project-context.json"
        if context_file.exists():
            try:
                with open(context_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def sync_workflow_from_context(self, workflow_id: str) -> Tuple[bool, str]:
        """
        Sync workflow phase based on detected project context.

        Returns:
            (success, message): Tuple indicating sync result
        """
        context = self.load_project_context()
        if not context:
            return (False, "No project context available")

        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return (False, "Workflow not found")

        # Parse workflow phase from context
        workflow_phase_str = context.get("workflow_phase", "")
        if "Phase 1" in workflow_phase_str:
            detected_phase = 1
        elif "Phase 2" in workflow_phase_str:
            detected_phase = 2
        elif "Phase 3" in workflow_phase_str:
            detected_phase = 3
        elif "Phase 4" in workflow_phase_str:
            detected_phase = 4
        elif "Phase 5" in workflow_phase_str:
            detected_phase = 5
        else:
            return (False, f"Could not parse phase from: {workflow_phase_str}")

        current_phase = workflow["current_phase"]

        if detected_phase != current_phase:
            self.update_phase(workflow_id, detected_phase, "in_progress")
            return (True, f"Synced workflow from Phase {current_phase} to Phase {detected_phase}")

        return (True, f"Workflow already at detected phase {current_phase}")


def main():
    """CLI interface for workflow coordinator."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: workflow-coordinator.py <command> [args]")
        print("Commands:")
        print("  create <project_name>        - Create new workflow")
        print("  list                         - List all workflows")
        print("  status <workflow_id>         - Show workflow status")
        print("  transition <workflow_id>     - Move to next phase")
        print("  detect <project_path>        - Detect project type and phase")
        print("  agents <phase> [types...]    - Show recommended agents")
        print("  sync <workflow_id>           - Sync workflow from project context")
        sys.exit(1)

    coordinator = WorkflowCoordinator()
    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("Usage: workflow-coordinator.py create <project_name>")
            sys.exit(1)

        project_name = sys.argv[2]
        workflow_id = coordinator.create_workflow(project_name)
        print(f"Created workflow: {workflow_id}")
        print(f"Project: {project_name}")
        print("Phase 1: Vision - IN PROGRESS")

    elif command == "list":
        workflows = coordinator.list_workflows()
        if not workflows:
            print("No workflows found")
        else:
            for wf in workflows:
                phase_info = coordinator.get_phase_info(wf["current_phase"])
                print(f"{wf['id'][:8]}... - {wf['project_name']} - "
                      f"Phase {wf['current_phase']}: {phase_info['name']} - {wf['phase_status']}")

    elif command == "status":
        if len(sys.argv) < 3:
            print("Usage: workflow-coordinator.py status <workflow_id>")
            sys.exit(1)

        workflow_id = sys.argv[2]
        workflow = coordinator.get_workflow(workflow_id)

        if not workflow:
            print(f"Workflow not found: {workflow_id}")
            sys.exit(1)

        phase_info = coordinator.get_phase_info(workflow["current_phase"])
        print(f"Project: {workflow['project_name']}")
        print(f"Current Phase: {workflow['current_phase']} - {phase_info['name']}")
        print(f"Status: {workflow['phase_status']}")
        print(f"Started: {workflow['started_at']}")
        print(f"Updated: {workflow['updated_at']}")

        # Show deliverables
        deliverables = coordinator.get_deliverables(workflow_id)
        if deliverables:
            print("\nDeliverables:")
            for d in deliverables:
                print(f"  Phase {d['phase']}: {d['deliverable_type']} - {d['status']}")

        # Show tasks
        tasks = coordinator.get_tasks(workflow_id)
        if tasks:
            print("\nTasks:")
            for t in tasks:
                print(f"  Phase {t['phase']}: {t['task_description']} - {t['status']}")

    elif command == "transition":
        if len(sys.argv) < 3:
            print("Usage: workflow-coordinator.py transition <workflow_id>")
            sys.exit(1)

        workflow_id = sys.argv[2]
        success, message = coordinator.transition_phase(workflow_id)

        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
            sys.exit(1)

    elif command == "detect":
        if len(sys.argv) < 3:
            print("Usage: workflow-coordinator.py detect <project_path>")
            sys.exit(1)

        project_path = Path(sys.argv[2])
        if not project_path.exists():
            print(f"✗ Path not found: {project_path}")
            sys.exit(1)

        # Detect project type
        project_types = coordinator.detect_project_type(project_path)
        print(f"Detected project types: {', '.join(project_types) if project_types else 'unknown'}")

        # Detect current phase
        detected_phase = coordinator.detect_current_phase_from_state(project_path)
        phase_info = coordinator.get_phase_info(detected_phase)
        print(f"Detected workflow phase: Phase {detected_phase} - {phase_info['name']}")

        # Show recommended agents
        recommended = coordinator.get_recommended_agents_for_phase(detected_phase, project_types)
        print(f"\nRecommended agents:")
        print(f"  Primary: {', '.join(recommended['primary'])}")
        if recommended['support']:
            print(f"  Support: {', '.join(recommended['support'])}")
        if recommended['optional']:
            print(f"  Optional: {', '.join(recommended['optional'])}")

    elif command == "agents":
        if len(sys.argv) < 3:
            print("Usage: workflow-coordinator.py agents <phase> [project_types...]")
            print("Example: workflow-coordinator.py agents 4 python django docker")
            sys.exit(1)

        try:
            phase = int(sys.argv[2])
        except ValueError:
            print(f"✗ Invalid phase number: {sys.argv[2]}")
            sys.exit(1)

        project_types = sys.argv[3:] if len(sys.argv) > 3 else None

        # Get recommendations
        recommended = coordinator.get_recommended_agents_for_phase(phase, project_types)
        phase_info = coordinator.get_phase_info(phase)

        print(f"Phase {phase}: {phase_info['name']}")
        print(f"Description: {phase_info['description']}")
        print(f"\nRecommended agents:")
        print(f"  Primary: {', '.join(recommended['primary'])}")
        if recommended['support']:
            print(f"  Support: {', '.join(recommended['support'])}")
        if recommended['optional']:
            print(f"  Optional: {', '.join(recommended['optional'])}")

    elif command == "sync":
        if len(sys.argv) < 3:
            print("Usage: workflow-coordinator.py sync <workflow_id>")
            sys.exit(1)

        workflow_id = sys.argv[2]
        success, message = coordinator.sync_workflow_from_context(workflow_id)

        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        print("Run without arguments to see available commands")
        sys.exit(1)


if __name__ == "__main__":
    main()