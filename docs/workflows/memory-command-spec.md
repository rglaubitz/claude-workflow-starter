# /memory Command Specification

> **Status:** 📋 PLANNED - This is a command specification, not fully implemented yet.
>
> **Purpose:** Documents the design for the /memory command to monitor the learning system's health and insights.

---

## Purpose
Provides a comprehensive snapshot of the learning system's health, recent learnings, and performance metrics. This is the single command for monitoring the continuous learning system.

## Usage
```
/memory              # Full learning system report
/memory --brief      # Summary only
/memory --patterns   # Focus on learned patterns
/memory --health     # System health details
```

## Output Format

The command generates a structured report showing:

### 1. System Status
- Overall health indicator (🟢 Healthy / 🟡 Warning / 🔴 Critical)
- Last update timestamp
- Processing queue status
- Active learning focus

### 2. Recent Learnings
- Patterns discovered in the past 7 days
- Preferences learned with confidence scores
- Team collaboration improvements
- Workflow optimizations

### 3. Team Performance
- Agent synergy score
- Average task completion time
- Success rate trends
- Collaboration effectiveness

### 4. Storage Health
- Database size and usage
- Pattern count by status
- Event queue depth
- Memory graph statistics

### 5. Next Actions
- Scheduled learning tasks
- Pending validations
- Upcoming consolidations

## Implementation

The command queries multiple data sources:
1. `learning_summary` view for metrics
2. `recent_learnings` view for discoveries
3. `learning_health` table for system status
4. `team_metrics` table for performance

## Example Output

```yaml
═══ Learning System Health Check ═══
Last Update: 2 minutes ago
Status: 🟢 Healthy

📚 Recent Learnings (Past 7 Days):
• Code Patterns: 42 identified, 38 applied
• Preferences: 15 learned, avg confidence: 87%
• Team Patterns: 23 collaboration improvements
• Workflows: 8 optimizations discovered

🎯 Active Learning Focus:
• Tracking: TypeScript error handling patterns
• Monitoring: Agent delegation effectiveness
• Analyzing: Git commit message patterns

👥 Team Performance:
• Agent Synergy: 8.7/10 (↑0.3 this week)
• Task Completion: 4.2min avg (↓18% faster)
• Success Rate: 94% (↑2%)
• Collaboration Score: 92/100

💾 Storage Health:
• SQLite: 2.3MB, 142 patterns
• Events Queue: 12 pending
• MCP Memory: 847 nodes (Phase 2)

🔄 Next Scheduled:
• Pattern consolidation in 15 min
• Preference update in 1 hour
• Weekly synthesis tomorrow 9am
```

## Error Handling

If the learning system is unavailable:
- Show last known status
- Indicate system is offline
- Provide troubleshooting steps
- Suggest recovery actions

## Integration Points

- Learning Orchestrator agent provides data
- Event processor maintains queue metrics
- Pattern validator reports quality scores
- Team metrics tracked automatically

## Success Metrics

- Query response time < 1 second
- Data freshness < 5 minutes
- Accurate health indicators
- Actionable insights provided

## Related Commands

- `/test-learning` - Test learning system
- `/clear-learning` - Reset learning data
- `/export-patterns` - Export learned patterns
- `/import-patterns` - Import pattern library

---

*The /memory command is your window into the continuous learning system's mind.*