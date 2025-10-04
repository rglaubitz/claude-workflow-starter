# Agent Constitution Integration Guide v1.0

## Quick Start

The Agent Constitution system is now active! Here's how to use it.

## For Manual Agent Launches

### Python Integration

```python
import sys
sys.path.append(str(Path.home() / '.claude/scripts'))
from agent_launcher_simple import launch_with_constitution, complete_session

# 1. Prepare task with constitution
enhanced_prompt, session_id = launch_with_constitution(
    agent_type="security-auditor",
    task="Review the dashboard code for security vulnerabilities"
)

# 2. Launch agent (using Task tool or any method)
result = Task(
    subagent_type="security-auditor",
    prompt=enhanced_prompt
)

# 3. Check compliance
import subprocess
subprocess.run([
    "python3",
    str(Path.home() / ".claude/scripts/check-compliance-simple.py"),
    session_id
], input=result.output.encode())

# 4. Mark session complete
complete_session(session_id, status='completed')
```

### Bash Integration

```bash
# 1. Launch with constitution
SESSION_ID=$(python3 ~/.claude/scripts/agent-launcher-simple.py \
    security-auditor \
    "Review code for vulnerabilities" \
    | grep "Session ID:" | awk '{print $3}')

# 2. Agent runs and returns output...
AGENT_OUTPUT="Constitution v1.0 acknowledged. Found 3 issues..."

# 3. Check compliance
echo "$AGENT_OUTPUT" | python3 ~/.claude/scripts/check-compliance-simple.py $SESSION_ID

# 4. Check status
constitution-status.sh
```

## For Review Board Integration

Add this to `review-board-orchestrator.py`:

```python
import sys
from pathlib import Path
sys.path.append(str(Path.home() / '.claude/scripts'))
from agent_launcher_simple import launch_with_constitution, complete_session

def prepare_review(project_name):
    # ... existing setup code ...

    # For each agent config:
    for config in setup['launch_configs']:
        # Wrap with constitution
        enhanced_prompt, session_id = launch_with_constitution(
            agent_type=config['agent'],
            task=config['description']
        )

        # Update config
        config['prompt'] = enhanced_prompt
        config['session_id'] = session_id

    return setup
```

## Monitoring Compliance

### Check Overall Status

```bash
constitution-status.sh
```

Shows:
- Total sessions last 7 days
- Acknowledgment rate
- Violations
- Compliance by agent type

### Check Specific Session

```bash
python3 ~/.claude/scripts/check-compliance-simple.py <session-id>
```

### View Alerts

```bash
tail -f ~/.claude/logs/constitution-alerts.log
```

## What Gets Tracked

**agent_sessions table:**
- session_id
- agent_type
- launched_at
- acknowledged (boolean)
- task_summary

**violations table:**
- violation_type ('no_acknowledgment', etc.)
- severity ('critical', 'warning', 'info')
- details
- detected_at

## Expected Agent Behavior

Agents MUST include this phrase in their first response:

```
Constitution v1.0 acknowledged
```

Then proceed with the task following all rules from the constitution.

## Troubleshooting

### Agent didn't acknowledge

**Symptom:** Alert logged, `acknowledged = 0` in database

**Fix:** Check if agent saw the constitution in its prompt. The launcher should prepend it automatically.

### Database locked errors

**Symptom:** SQLite database locked message

**Fix:** Only one process should write at a time. Add retry logic or use `PRAGMA journal_mode=WAL` for better concurrency.

### Status command shows 0 sessions

**Symptom:** Empty report

**Fix:** Agents haven't been launched with the new system yet. Start using `launch_with_constitution()` for all agent launches.

## Future Enhancements (Not Yet Implemented)

- Real-time concurrency violation detection
- Tool misuse tracking
- Auto-termination of non-compliant agents
- Email/Slack notifications
- Dashboard web interface

## Files Created

- `~/.claude/constitution/agent-constitution.md` - The constitution
- `~/.claude/data/constitution_compliance.db` - Tracking database
- `~/.claude/scripts/agent-launcher-simple.py` - Launcher
- `~/.claude/scripts/check-compliance-simple.py` - Compliance checker
- `~/.claude/scripts/constitution-status.sh` - Status report
- `~/.claude/logs/constitution-alerts.log` - Alert log

## Quick Commands

```bash
# Check status
constitution-status.sh

# Check specific session
check-compliance-simple.py <session-id>

# View alerts
tail ~/.claude/logs/constitution-alerts.log

# Query database
sqlite3 ~/.claude/data/constitution_compliance.db "SELECT * FROM agent_sessions LIMIT 5"
```

---

**The Agent Constitution is now enforced! All agents must acknowledge and follow the rules.**
