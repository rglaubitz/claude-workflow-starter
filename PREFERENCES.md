# Claude Code Preferences

## Autonomous Agent Deployment (ENABLED)

**Permission Level**: Full autonomous deployment authorized

- Deploy agents without asking when working on multi-agent projects
- Always maximize parallel agent deployment when possible
- Use TodoWrite to track progress but don't wait for approval
- Continue through to completion unless blocked by errors

**API Configuration**:
- API Key: Set via environment variable `ANTHROPIC_API_KEY`
- Model: claude-sonnet-4-5 (default)
- Timeout: 300s per agent (5 minutes)
- Parallel Limit: 5 agents per wave (hardware limit)

**Deployment Strategy**:
- Batch deploy independent tasks in parallel waves
- Use git worktrees for isolation (prevents Cursor crashes)
- Monitor background agents with BashOutput tool
- Retry failed agents once with simplified prompts

**Execution Mode**: When user says "continue" or "finish tasks" or "deploy intelligently", deploy all remaining agents in parallel waves without asking for permission between waves. Report progress as you go.
