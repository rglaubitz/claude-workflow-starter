---
description: "Execute Review Board validation for project execution plan"
argument-hint: "<project-name> [--resubmit | --quick-check]"
allowed-tools: Bash
---

Execute the Review Board process for a project execution plan. The Review Board is a quality gate that validates Vision, Mission, and Execution documents before transitioning to Phase 4 (Implementation).

!python3 -c "
import sys
import subprocess
from pathlib import Path

# Get project name from args
if len(sys.argv) < 2:
    print('Usage: /review-board <project-name>')
    print()
    print('Flags:')
    print('  --resubmit      Full re-review after fixing blockers')
    print('  --quick-check   Re-run only specialists who had concerns')
    print()
    print('Example: /review-board \"Claude Code Performance Dashboard\"')
    sys.exit(1)

project_name = ' '.join(sys.argv[1:]).strip('\"')

# Remove flags from project name
flags = []
if '--resubmit' in project_name:
    flags.append('--resubmit')
    project_name = project_name.replace('--resubmit', '').strip()
if '--quick-check' in project_name:
    flags.append('--quick-check')
    project_name = project_name.replace('--quick-check', '').strip()

print()
print('╔════════════════════════════════════════════════════════════╗')
print('║           REVIEW BOARD - EXECUTION VALIDATION              ║')
print('╚════════════════════════════════════════════════════════════╝')
print()
print(f'Project: {project_name}')
if flags:
    print(f'Flags: {\" \".join(flags)}')
print()

# Run the coordinator
coordinator_path = Path.home() / '.claude/scripts/review-board-coordinator.py'

if not coordinator_path.exists():
    print('❌ Error: Review Board coordinator not found')
    print(f'   Expected: {coordinator_path}')
    sys.exit(1)

# Execute coordinator
cmd = ['python3', str(coordinator_path), project_name]
if flags:
    cmd.extend(flags)

result = subprocess.run(cmd, capture_output=False)
sys.exit(result.returncode)
"
