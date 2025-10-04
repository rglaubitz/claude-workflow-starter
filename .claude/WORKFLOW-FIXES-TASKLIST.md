# Workflow System - Complete Task List to 100% Production Ready

**Analysis Date:** 2025-10-04
**Current Status:** 85% Production Ready
**Target:** 100% Production Ready
**Critical Gaps:** 3 (P0)
**Optimizations:** 7 (P1-P3)

---

## P0: CRITICAL FIXES (Must Complete Before Production)

### ✅ Task 1: Fix Phase 4 Agent Deployment
**File:** `/Users/richardglaubitz/Projects/claude-workflow-starter/.claude/commands/start-implementation.md`
**Priority:** P0 - BLOCKING
**Estimated Time:** 20 minutes

**Changes Required:**

**Line 38-40 - Replace:**
```markdown
3. **Deploy the task-manager orchestrator**:
   - Primary: `task-manager` (coordinates all implementation work)
   - The task-manager will deploy other agents based on Execution Plan assignments
```

**With:**
```markdown
3. **Deploy the execution-director field commander**:
   - Primary: `execution-director` (commands 7 agent teams during Phase 4)
   - Support: `delivery-coordinator`, `quality-enforcer`, `blocker-resolver`, `progress-tracker`
   - The execution-director orchestrates tactical implementation

   Use Task tool to deploy:
   ```python
   # Deploy field commander
   Task(
       agent="execution-director",
       prompt="Take command of Phase 4 implementation. Read execution plan, activate teams, coordinate execution.",
       context={'execution_plan': execution_plan_path, 'review_feedback': review_feedback_path}
   )
   ```
```

**Line 90-96 - Replace:**
```markdown
The `task-manager` will:
- Coordinate agent work
- Track progress in real-time
- Update Implementation Report
- Handle dependencies
- Escalate blockers
- Ensure quality gates are met
```

**With:**
```markdown
The `execution-director` will:
- Command 7 agent teams (Foundation, Backend, Frontend, Research, Quality, Integration, Orchestration)
- Deploy delivery-coordinator for team handoffs
- Deploy quality-enforcer for gate enforcement
- Deploy blocker-resolver for escalations
- Deploy progress-tracker for war room dashboard
- Make tactical decisions in real-time
- Coordinate all implementation work
```

**Line 156 - Replace:**
```markdown
- The task-manager is the orchestrator - let it coordinate
```

**With:**
```markdown
- The execution-director is the field commander - let it orchestrate
- Trust the execution support team (delivery-coordinator, quality-enforcer, blocker-resolver, progress-tracker)
```

**Verification:**
```bash
grep -n "task-manager" /Users/richardglaubitz/Projects/claude-workflow-starter/.claude/commands/start-implementation.md
# Should return ZERO matches after fix
```

---

### ✅ Task 2: Add Execution Coordinator Initialization
**File:** `/Users/richardglaubitz/Projects/claude-workflow-starter/.claude/commands/start-implementation.md`
**Priority:** P0 - BLOCKING
**Estimated Time:** 15 minutes

**Changes Required:**

**After line 40, INSERT:**
```markdown

4. **Initialize Phase 4 communication infrastructure**:
```bash
echo "🔧 Initializing execution team communication infrastructure..."

# Create 10 SQLite tables for Phase 4 coordination
python3 ~/.claude/scripts/execution-coordinator.py init "$PROJECT_SLUG"

# Verify infrastructure ready
echo ""
echo "📊 Verifying communication infrastructure..."
python3 ~/.claude/scripts/execution-coordinator.py health "$PROJECT_SLUG"

echo ""
echo "✅ Phase 4 infrastructure initialized:"
echo "   - agent_messages (inter-agent communication)"
echo "   - handoff_log (team handoffs)"
echo "   - quality_gates (gate enforcement)"
echo "   - sop_compliance (SOP tracking)"
echo "   - blockers (blocker resolution)"
echo "   - blocker_patterns (learning)"
echo "   - team_status (7 teams initialized)"
echo "   - review_deployments (review tracking)"
echo "   - team_sync_log (sync tracking)"
echo "   - tactical_decisions (execution-director decisions)"
```

5. **Load tasks from database**:
```

**Renumber subsequent steps** (current step 4 becomes step 6, etc.)

**Verification:**
```bash
# After fix, start-implementation should create tables
python3 ~/.claude/scripts/execution-coordinator.py health test-project
# Should show all 10 tables present
```

---

### ✅ Task 3: Verify MCP Inheritance for Deployed Agents
**File:** TESTING REQUIRED (then document in ARCHITECTURE.md)
**Priority:** P0 - BLOCKING
**Estimated Time:** 30 minutes

**Test Procedure:**

1. **Create test project:**
```bash
# In Claude Code
/start-project "mcp-inheritance-test"
# Answer questions briefly
```

2. **Trigger agent deployment with WebSearch:**
```bash
/start-mission
# This deploys research-manager which has tools: WebSearch, WebFetch
```

3. **Observe agent behavior:**
- Watch for WebSearch calls in agent output
- Check if Exa MCP server is hit
- Look for semantic search results vs. generic search

4. **Expected outcomes:**

**Scenario A: MCP IS inherited** ✅
- Agent successfully uses WebSearch
- Exa semantic search works
- **ACTION:** Document in ARCHITECTURE.md: "Agents deployed via Task tool inherit parent MCP servers"

**Scenario B: MCP NOT inherited** ❌
- Agent fails or falls back to basic search
- No Exa semantic search
- **ACTION:** Add profile activation to phase commands

**If Scenario B, add to start-mission.md (after line 2):**
```markdown
## MCP Profile Activation

Before deploying research agents, activate research-pro profile:

```bash
# Activate research profile for Phase 2
echo "🔬 Activating research-pro profile (Exa, Firecrawl, Context7, mcpdocsearch)..."
cp ~/.claude/config/profiles/research-pro.json ~/.claude/.mcp.json
echo "✅ Research profile active - agents now have access to advanced search MCP servers"
```
```

**Verification:**
```bash
# Document finding
echo "MCP Inheritance: [CONFIRMED/NOT_CONFIRMED]" >> ~/.claude/ARCHITECTURE.md
```

---

## P1: QUALITY IMPROVEMENTS (Should Complete)

### ✅ Task 4: Add Auto Profile Switching
**Files:** `start-mission.md`, `start-implementation.md`, `start-testing.md`
**Priority:** P1
**Estimated Time:** 25 minutes

**Changes:**

**start-mission.md - Add after line 7:**
```markdown

## Phase 2 MCP Profile

This phase requires advanced research capabilities. Automatically activating research-pro profile.

```bash
echo "🔬 Activating research-pro profile for Phase 2..."
echo "   - Exa (semantic search)"
echo "   - Firecrawl (web scraping)"
echo "   - Context7 (documentation lookup)"
echo "   - mcpdocsearch (doc search)"
echo "   - chrome-devtools (browser automation)"

cp ~/.claude/config/profiles/research-pro.json ~/.claude/.mcp.json

echo "✅ Research profile activated"
```
```

**start-implementation.md - Add after initialization (new step after Task 2 fix):**
```markdown

**Activate code-work profile for Phase 4:**
```bash
echo "💻 Activating code-work profile for Phase 4..."
echo "   - Serena (semantic code analysis)"
echo "   - Sequential thinking (deep reasoning)"

cp ~/.claude/config/profiles/code-work.json ~/.claude/.mcp.json

echo "✅ Code-work profile activated"
```
```

**start-testing.md - Add early:**
```markdown

## Phase 5 MCP Profile

```bash
echo "🧪 Keeping code-work profile for Phase 5 (test analysis)..."
# Already active from Phase 4, no change needed
# Could switch to minimal for speed if preferred
```
```

---

### ✅ Task 5: Add LLM-as-Judge Scoring to Review Board
**Files:** `CIO.md`, `CTO.md`, `COO.md`
**Priority:** P1
**Estimated Time:** 30 minutes

**Add to each C-suite agent after their checklist sections:**

**CIO.md - Add scoring rubric:**
```markdown

## Scoring Rubric (0-100)

Evaluate execution plan across 4 dimensions:

### 1. Research Quality (0-25 points)
- [ ] 25 pts: Comprehensive research from official sources, all frameworks documented
- [ ] 20 pts: Good research, minor gaps in documentation
- [ ] 15 pts: Adequate research, some official sources missing
- [ ] 10 pts: Minimal research, significant gaps
- [ ] 0 pts: Insufficient research to validate plan

**Score:** __/25

### 2. Dependencies Complete (0-25 points)
- [ ] 25 pts: All dependencies identified with versions, justifications, alternatives
- [ ] 20 pts: Most dependencies identified, minor gaps
- [ ] 15 pts: Core dependencies identified, some missing
- [ ] 10 pts: Significant dependency gaps
- [ ] 0 pts: Critical dependencies missing

**Score:** __/25

### 3. Documentation Coverage (0-25 points)
- [ ] 25 pts: Complete docs gathered (official, examples, API specs, best practices)
- [ ] 20 pts: Good coverage, minor gaps
- [ ] 15 pts: Adequate coverage, some areas lacking
- [ ] 10 pts: Minimal documentation
- [ ] 0 pts: Insufficient documentation to support implementation

**Score:** __/25

### 4. Source Authority (0-25 points)
- [ ] 25 pts: All sources Tier 1 (official docs) or Tier 2 (1.5k+ star repos)
- [ ] 20 pts: Mostly authoritative sources, few lower-tier
- [ ] 15 pts: Mix of authoritative and questionable sources
- [ ] 10 pts: Many low-authority sources
- [ ] 0 pts: Unverified or unreliable sources

**Score:** __/25

---

## Overall CIO Score

**Total:** __/100

**Verdict:**
- **APPROVED** (85-100): No blocking issues, proceed to implementation
- **APPROVED_WITH_CONCERNS** (70-84): Concerns noted but can proceed with mitigation
- **REJECTED** (<70): Must address gaps before implementation

**Final CIO Verdict:** [APPROVED | APPROVED_WITH_CONCERNS | REJECTED]
```

**Repeat similar rubrics for CTO.md and COO.md with their specific criteria.**

---

### ✅ Task 6: Implement Formal Handoff Artifacts
**File:** `approve-execution-plan.md`
**Priority:** P1
**Estimated Time:** 25 minutes

**Add before database update section:**
```markdown

## Create Phase 3→4 Handoff Artifact

Prepare structured handoff package for execution-director:

```python
import json
from datetime import datetime

# Read execution plan for details
execution_plan_path = project_dir / "03-execution-plan.md"
execution_plan = execution_plan_path.read_text()

# Create handoff package artifact
handoff_package = {
    'handoff_id': str(uuid.uuid4()),
    'timestamp': datetime.now().isoformat(),
    'phase_from': 3,
    'phase_to': 4,
    'execution_plan_path': str(execution_plan_path),
    'agent_teams': {
        'Foundation': ['database-architect', 'devops-engineer'],
        'Backend': ['backend-developer', 'api-architect', 'sql-specialist'],
        'Frontend': ['frontend-developer', 'ui-ux-designer'],
        'Research': ['research-manager', 'documentation-expert', 'specialists'],
        'Quality': ['qa-engineer', 'code-review-expert', 'security-auditor', 'performance-engineer'],
        'Integration': ['integration-specialist', 'mcp-bridge-engineer'],
        'Orchestration': ['execution-director', 'delivery-coordinator', 'quality-enforcer', 'blocker-resolver', 'progress-tracker']
    },
    'dependencies': {
        'technical': 'Listed in execution plan',
        'information': 'Research from Phase 2',
        'resource': 'Identified in execution plan',
        'team': '7 teams with capacity limits'
    },
    'quality_gates': {
        'task_level': 'Code review, unit tests, linting',
        'feature_level': 'Integration tests, feature review',
        'epic_level': 'E2E tests, epic validation',
        'phase_level': 'Complete validation before Phase 5'
    },
    'review_board_approval': 'APPROVED',  # From Review Board session
    'execution_readiness': 'Verified'
}

# Store artifact in project directory
handoff_path = project_dir / "handoff-package-phase-3-to-4.json"
handoff_path.write_text(json.dumps(handoff_package, indent=2))

print(f"✅ Handoff package created: {handoff_path}")
print(f"   - 7 agent teams identified")
print(f"   - 4 dependency types mapped")
print(f"   - 4 quality gate levels defined")
print(f"   - Review Board approval documented")
```
```

---

## P2: PERFORMANCE OPTIMIZATIONS (Nice to Have)

### ✅ Task 7: Add Context Compaction Strategy
**File:** `start-implementation.md`
**Priority:** P2
**Estimated Time:** 20 minutes

**Add to implementation workflow section:**
```markdown

## Context Management During Implementation

Long-running implementations require context management:

```python
# Track task completion count
completed_tasks = cursor.execute("""
    SELECT COUNT(*) FROM tasks WHERE status = 'completed'
""").fetchone()[0]

# Every 50 tasks, compact context
if completed_tasks > 0 and completed_tasks % 50 == 0:
    print(f"⚠️ {completed_tasks} tasks completed - context compaction recommended")
    print(f"")
    print(f"Run: /compact")
    print(f"")
    print(f"This will:")
    print(f"  - Summarize progress to date")
    print(f"  - Clear context window")
    print(f"  - Save summary to agent-notes/phase-4-summary-{datetime.now().strftime('%Y%m%d')}.md")
    print(f"  - Continue with fresh context")
```
```

---

### ✅ Task 8: Progressive Disclosure for Research
**File:** `research-manager.md`
**Priority:** P2
**Estimated Time:** 30 minutes

**Add to "Your Deliverables" section:**
```markdown

## Research Output Format

Follow progressive disclosure pattern (Anthropic best practice):

```python
# Instead of dumping full research report
# Return lightweight research reference:

research_output = {
    'research_id': f'research-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
    'summary': '2-3 sentence executive summary',
    'key_findings': [
        'Finding 1 (1 sentence)',
        'Finding 2 (1 sentence)',
        'Finding 3 (1 sentence)'
    ],
    'source_quality': 'Tier 1: Official Documentation',
    'confidence': 'High (95%)',
    'full_report_path': f'research/research-{timestamp}.md',
    'artifacts': {
        'documentation': 'research/documentation/',
        'examples': 'research/examples/',
        'citations': 'research/references.md'
    }
}

# Agents can request full report if needed:
# "Read full research report at: {full_report_path}"
```
```

---

### ✅ Task 9: Create Agent Validation Script
**File:** `scripts/validate-agents.sh` (NEW)
**Priority:** P2
**Estimated Time:** 45 minutes

**Create new file:**
```bash
#!/bin/bash
# Agent Validation Script
# Validates all agent files for correct YAML frontmatter and structure

set -e

CLAUDE_AGENTS="/Users/richardglaubitz/Projects/claude-agents"
ERRORS=0
WARNINGS=0
TOTAL=0

echo "🔍 Validating Claude Code Agents..."
echo ""

# Function to validate agent file
validate_agent() {
    local file="$1"
    local filename=$(basename "$file")
    TOTAL=$((TOTAL + 1))

    echo "Checking: $filename"

    # Check YAML frontmatter exists
    if ! grep -q "^---$" "$file"; then
        echo "  ❌ ERROR: Missing YAML frontmatter"
        ERRORS=$((ERRORS + 1))
        return
    fi

    # Extract frontmatter
    frontmatter=$(sed -n '/^---$/,/^---$/p' "$file" | head -n -1 | tail -n +2)

    # Check required field: name
    if ! echo "$frontmatter" | grep -q "^name:"; then
        echo "  ❌ ERROR: Missing required field: name"
        ERRORS=$((ERRORS + 1))
    fi

    # Check required field: description
    if ! echo "$frontmatter" | grep -q "^description:"; then
        echo "  ❌ ERROR: Missing required field: description"
        ERRORS=$((ERRORS + 1))
    fi

    # Check required field: tools
    if ! echo "$frontmatter" | grep -q "^tools:"; then
        echo "  ⚠️  WARNING: Missing optional field: tools (will inherit all)"
        WARNINGS=$((WARNINGS + 1))
    fi

    # Validate tool names if present
    if echo "$frontmatter" | grep -q "^tools:"; then
        tools=$(echo "$frontmatter" | grep "^tools:" | cut -d: -f2 | tr ',' '\n')

        valid_tools="Task TodoWrite Bash Read Write Edit MultiEdit Grep Glob WebSearch WebFetch NotebookEdit"

        for tool in $tools; do
            tool=$(echo "$tool" | xargs)  # Trim whitespace
            if [[ ! " $valid_tools " =~ " $tool " ]]; then
                echo "  ⚠️  WARNING: Unknown tool: $tool"
                WARNINGS=$((WARNINGS + 1))
            fi
        done
    fi

    echo "  ✅ Valid"
}

# Validate all agent files
for agent_file in "$CLAUDE_AGENTS"/**/*.md; do
    if [[ -f "$agent_file" && "$agent_file" != *"README.md" ]]; then
        validate_agent "$agent_file"
    fi
done

echo ""
echo "📊 Validation Summary"
echo "  Total agents: $TOTAL"
echo "  ✅ Passed: $((TOTAL - ERRORS))"
echo "  ❌ Errors: $ERRORS"
echo "  ⚠️  Warnings: $WARNINGS"

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "❌ VALIDATION FAILED - Fix errors before deployment"
    exit 1
else
    echo ""
    echo "✅ ALL AGENTS VALID"
    exit 0
fi
```

**Make executable:**
```bash
chmod +x /Users/richardglaubitz/Projects/claude-workflow-starter/scripts/validate-agents.sh
```

---

## P3: FUTURE ENHANCEMENTS (Lower Priority)

### ✅ Task 10: Tighten Tool Permissions
**Files:** Multiple agent files
**Priority:** P3
**Estimated Time:** 60 minutes

**Agents to Review:**

1. **documentation-expert.md** - Remove Bash
   - Current: `tools: Read, Write, Edit, MultiEdit, Bash, WebFetch, Grep`
   - Proposed: `tools: Read, Write, Edit, MultiEdit, WebFetch, Grep`

2. **code-review-expert.md** - Remove WebFetch
   - Check current tools, remove if present

3. **ui-ux-designer.md** - Remove Bash
   - Check current tools, remove if not needed for design work

4. **citation-manager.md** - Restrict to core
   - Current: `tools: Read, Write, Edit, WebFetch`
   - Keep as-is (already minimal) ✅

---

## COMPLETION CHECKLIST

### P0 Critical (Must Complete)
- [ ] Task 1: Fix Phase 4 agent deployment (task-manager → execution-director)
- [ ] Task 2: Add execution-coordinator.py initialization to start-implementation
- [ ] Task 3: Verify MCP inheritance, document findings

### P1 Quality (Should Complete)
- [ ] Task 4: Add auto profile switching (research-pro, code-work)
- [ ] Task 5: Add LLM-as-judge scoring to C-suite agents
- [ ] Task 6: Implement formal handoff artifacts

### P2 Performance (Nice to Have)
- [ ] Task 7: Add context compaction strategy
- [ ] Task 8: Progressive disclosure for research
- [ ] Task 9: Create agent validation script

### P3 Future (Lower Priority)
- [ ] Task 10: Tighten tool permissions

---

## POST-FIX VERIFICATION

After completing P0 tasks, run end-to-end test:

```bash
# Create test project
/start-project "workflow-validation-test"

# Answer brief questions
# Quick answers: "Simple TODO app", "Developers", "Learn workflow"

# Phase 1
/start-vision
# Review vision.md
/approve-vision

# Phase 2
/start-mission
# Verify: research-pro profile activated
# Verify: Research agents deploy and can WebSearch
# Review mission.md
/approve-mission

# Phase 3
/start-execution-planning
# Review execution plan
/approve-execution-plan

# Phase 3.5
/start-review-board
# Verify: C-suite scoring rubrics present
# Verify: Quantitative scores calculated
/approve-review-board

# Phase 4
/start-implementation
# Verify: execution-director deploys (NOT task-manager)
# Verify: execution-coordinator.py runs successfully
# Verify: 10 SQLite tables created
# Verify: Execution support team activates
# Let it run a few tasks
/complete-implementation

# Phase 5
/start-testing
/approve-testing

# SUCCESS: Full workflow completed!
```

---

## ESTIMATED TOTAL TIME

- **P0 (Critical):** 65 minutes
- **P1 (Quality):** 80 minutes
- **P2 (Performance):** 90 minutes
- **P3 (Future):** 60 minutes

**Total to 100%:** ~5 hours (P0+P1+P2+P3)
**Minimum viable (P0 only):** ~1 hour

---

## SUCCESS CRITERIA

System is 100% production ready when:

1. ✅ User can run all 5 phases end-to-end without errors
2. ✅ Correct agents deploy at each phase (execution-director in Phase 4)
3. ✅ Phase 4 SQLite infrastructure initializes automatically
4. ✅ MCP servers accessible to deployed agents (verified and documented)
5. ✅ Research agents find latest documentation (Node 22, not 18)
6. ✅ Review Board uses quantitative scoring (LLM-as-judge)
7. ✅ Phase transitions have formal handoff artifacts
8. ✅ System doesn't overwhelm (team capacity limits enforced)
9. ✅ All 49 agents validate successfully
10. ✅ Documentation matches implementation

---

**After completing this task list, the workflow system will be 100% production-ready for real-world projects.**
