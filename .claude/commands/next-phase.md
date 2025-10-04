---
description: Transition to next project phase
argument-hint: [project-name]
allowed-tools: Bash, Write, Read
---

Transition project to next phase: **$ARGUMENTS**

Execute the phase transition by:
1. Validating current phase completion (quality gates)
2. Transitioning phase in database
3. Creating next phase deliverable document from template
4. Registering new deliverable
5. Showing next phase information and steps

!python3 -c "
import sys
from pathlib import Path

# Import module with hyphenated name
spec = __import__('importlib.util').util.spec_from_file_location(
    'workflow_coordinator',
    Path.home() / '.claude/scripts/workflow-coordinator.py'
)
module = __import__('importlib.util').util.module_from_spec(spec)
spec.loader.exec_module(module)
WorkflowCoordinator = module.WorkflowCoordinator

import shutil
from datetime import datetime

coordinator = WorkflowCoordinator()
identifier = '$ARGUMENTS'

# Get workflow
if identifier and len(identifier) == 36 and '-' in identifier:
    workflow = coordinator.get_workflow(identifier)
else:
    workflow = coordinator.get_workflow_by_project(identifier)

if not workflow:
    print('❌ Workflow not found: $ARGUMENTS')
    sys.exit(1)

current_phase = workflow['current_phase']
project_name = workflow['project_name']

# Validate current phase
is_complete, issues = coordinator.validate_phase_complete(workflow['id'], current_phase)

if not is_complete:
    print('❌ Cannot transition - Phase {} incomplete:'.format(current_phase))
    for issue in issues:
        print(f'   • {issue}')
    sys.exit(1)

# Transition
success, message = coordinator.transition_phase(workflow['id'])

if not success:
    print(f'❌ {message}')
    sys.exit(1)

next_phase = current_phase + 1
next_phase_info = coordinator.get_phase_info(next_phase)

print()
print('═══════════════════════════════════════════════════════════')
print(f'  ✓ TRANSITIONED TO PHASE {next_phase}: {next_phase_info[\"name\"].upper()}')
print('═══════════════════════════════════════════════════════════')
print()
print(f'Project: {project_name}')
print(f'Description: {next_phase_info[\"description\"]}')
print()
print('PRIMARY AGENTS:')
for agent in next_phase_info['primary_agents']:
    print(f'  • {agent}')
print()

if next_phase_info.get('support_agents') and next_phase_info['support_agents'] != 'all':
    print('SUPPORT AGENTS:')
    for agent in next_phase_info['support_agents']:
        print(f'  • {agent}')
    print()

# Create deliverable document if needed
if next_phase_info.get('deliverable'):
    project_slug = project_name.lower().replace(' ', '-')
    projects_base = str(Path.home() / '.claude/projects')
    project_dir = f'{projects_base}/{project_slug}'
    doc_path = f'{project_dir}/{next_phase:02d}-{next_phase_info[\"deliverable\"].title()}.md'

    # Copy template
    template_path = str(Path.home() / f'.claude/templates/{next_phase_info[\"template\"]}')
    Path(doc_path).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(template_path, doc_path)

    # Replace placeholders
    with open(doc_path, 'r') as f:
        content = f.read()

    content = content.replace('[Project Name]', project_name)
    content = content.replace('[Date]', datetime.now().strftime('%Y-%m-%d'))

    with open(doc_path, 'w') as f:
        f.write(content)

    # Register deliverable
    coordinator.add_deliverable(
        workflow_id=workflow['id'],
        phase=next_phase,
        deliverable_type=next_phase_info['deliverable'],
        content_path=doc_path,
        status='draft'
    )

    print(f'DELIVERABLE CREATED:')
    print(f'  {doc_path}')
    print()

print('NEXT STEPS:')
if next_phase == 2:
    print('  1. Research technical approach and dependencies')
    print('  2. Document architecture and design decisions')
    print('  3. Gather code examples and references')
    print('  4. Complete Mission document')
elif next_phase == 3:
    print('  1. Break down work into tasks')
    print('  2. Assign agents to tasks')
    print('  3. Create timeline and dependencies')
    print('  4. Complete Execution document')
elif next_phase == 4:
    print('  1. Review Execution plan')
    print('  2. Activate assigned agents')
    print('  3. Begin implementation')
    print('  4. Track progress')
elif next_phase == 5:
    print('  1. Create test plan')
    print('  2. Execute test suites')
    print('  3. Fix bugs and iterate')
    print('  4. Validate all requirements met')

print()
print('═══════════════════════════════════════════════════════════')
"