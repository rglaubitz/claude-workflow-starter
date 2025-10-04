---
description: Track project dependency (Phase 2)
argument-hint: <project-name> <dependency-name> [type] [version]
allowed-tools: Bash, Edit, Read
---

Add dependency to project: **$1** → **$2** ($3 $4)

!python3 -c "
import sys
sys.path.append('$HOME/.claude/scripts')
from workflow_coordinator import WorkflowCoordinator

coordinator = WorkflowCoordinator()
project_name = '$1'
dep_name = '$2'
dep_type = '$3' if '$3' else 'unknown'
dep_version = '$4' if '$4' else 'latest'

# Get workflow
workflow = coordinator.get_workflow_by_project(project_name)
if not workflow:
    print('❌ Workflow not found: ' + project_name)
    sys.exit(1)

# Add as task in Phase 2
task_description = f'Install dependency: {dep_name} ({dep_type} {dep_version})'
coordinator.add_task(
    workflow_id=workflow['id'],
    phase=2,
    task_description=task_description,
    assigned_agent='integration-specialist'
)

print(f'✓ Added dependency: {dep_name}')
print(f'  Type: {dep_type}')
print(f'  Version: {dep_version}')
print(f'  Assigned: integration-specialist')
print()

# Update Mission document if it exists
deliverables = coordinator.get_deliverables(workflow['id'], phase=2)
if deliverables:
    import os
    mission_doc = None
    for d in deliverables:
        if d['deliverable_type'] == 'mission':
            mission_doc = d['content_path']
            break

    if mission_doc and os.path.exists(mission_doc):
        with open(mission_doc, 'r') as f:
            content = f.read()

        # Find dependencies table and add entry
        dep_line = f'| {dep_name} | {dep_type} | {dep_version} | | |\\n'

        if '### Core Dependencies' in content:
            # Add after the header row
            parts = content.split('### Core Dependencies')
            if len(parts) > 1:
                table_start = parts[1].find('|', parts[1].find('|') + 1)
                # Find end of first table row (header separator)
                header_end = parts[1].find('\\n', table_start)
                if header_end > 0:
                    # Insert after header
                    parts[1] = parts[1][:header_end+1] + dep_line + parts[1][header_end+1:]
                    content = '### Core Dependencies'.join(parts)

                    with open(mission_doc, 'w') as f:
                        f.write(content)

                    print(f'✓ Updated Mission document: {mission_doc}')

print()
print('Run /phase-status to see all dependencies')
"