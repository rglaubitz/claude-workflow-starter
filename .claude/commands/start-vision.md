---
description: "Begin Phase 1 (Vision) - Create strategic vision document"
allowed-tools: Task, Bash, Write, Read
---

# Phase 1: Start Vision

You are initiating **Phase 1: Vision** - the strategic synthesis phase.

## Your Mission

Transform the project brief into a **strategic vision** that defines:
- **The HOW**: Technical architecture and approach
- **The Strategic WHY**: Innovation, differentiation, and value proposition
- **The EXPLOSIVE OUTCOME**: What success looks like when we nail this

## Task Overview

### 1. Read the Project Brief

```bash
# Determine project slug from current context
PROJECT_SLUG=$(python3 -c "
import sqlite3
from pathlib import Path

# Find the most recent project or use context
projects_dir = Path.home() / '.claude/projects'
projects = sorted(projects_dir.glob('*/workflow.db'), key=lambda p: p.stat().st_mtime, reverse=True)
if projects:
    print(projects[0].parent.name)
")

echo "📖 Reading project brief for: $PROJECT_SLUG"
cat "$HOME/.claude/projects/$PROJECT_SLUG/00-project-brief.md"
```

### 2. Deploy Strategic Agents

Use the **Task** tool to deploy specialist agents:

**Primary Agent: `prd-expert`**
- Task: "Create strategic vision document from project brief"
- Focus: Executive synthesis, value proposition, outcome vision
- Template: `~/.claude/templates/phases/01-vision-template.md`
- Brief: `~/.claude/projects/$PROJECT_SLUG/00-project-brief.md`

**Supporting Agent: `agent-architecture-designer`**
- Task: "Design technical architecture and system approach"
- Focus: HOW we'll solve this, key architectural decisions, trade-offs

**Supporting Agent: `ui-ux-designer`**
- Task: "Define user experience strategy and design approach"
- Focus: User impact, design innovation, UX differentiation

### 3. Create Vision Document

The vision document should be a **strategic synthesis**, NOT a duplication of the brief.

**What to Include:**

✅ **Executive Summary** (2-3 sentences)
- Synthesize the essence: WHAT, WHO, TRANSFORMATIVE OUTCOME

✅ **Strategic Solution Approach**
- Technical architecture (the HOW)
- Innovation & differentiation (what makes this unique)
- Why this approach wins (strategic justification)

✅ **The Explosive Outcome**
- Paint the success picture
- Specific user impacts
- Measurable metrics
- What changes in the world

✅ **Strategic Decisions**
- 3-5 key architectural/design decisions
- Rationale and trade-offs for each
- What we're NOT doing (scope boundaries)

✅ **Path Forward**
- Research requirements for Phase 2
- Documentation to gather
- Examples to find
- Dependencies to identify

**What NOT to Include:**

❌ Duplicated problem statements (reference the brief instead)
❌ Duplicated requirements lists (link to brief)
❌ Duplicated constraints (link to brief)
❌ Duplicated risk tables (link to brief)

**Use wiki-links to reference the brief:**
```markdown
See [[00-project-brief#core-requirements]] for detailed requirements.
```

### 4. Write the Vision Document

```python
from pathlib import Path
from datetime import datetime

project_slug = "$PROJECT_SLUG"
project_dir = Path.home() / ".claude/projects" / project_slug

# Read template
template_path = Path.home() / ".claude/templates/phases/01-vision-template.md"
template = template_path.read_text()

# Create vision document (agents will fill this out)
vision_path = project_dir / "01-vision.md"

# Template is already structured for strategic synthesis
# Agents should focus on:
# - Executive summary
# - Solution approach & innovation
# - Explosive outcome vision
# - Strategic decisions
# - Path forward to Phase 2

print(f"✅ Vision template prepared: {vision_path}")
```

### 5. Update Workflow Database

```python
import sqlite3
from pathlib import Path
from datetime import datetime
import uuid

project_slug = "$PROJECT_SLUG"
db_path = Path.home() / ".claude/projects" / project_slug / "workflow.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Update workflow phase
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'vision-in-progress',
        phase_number = 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

# Create deliverable record
deliverable_id = str(uuid.uuid4())
document_path = f"projects/{project_slug}/01-vision.md"

cursor.execute("""
    INSERT INTO deliverables (id, phase_number, phase_name, document_path, status, created_at)
    VALUES (?, 1, 'vision', ?, 'draft', CURRENT_TIMESTAMP)
""", (deliverable_id, document_path))

conn.commit()
conn.close()

print(f"✅ Workflow updated: Phase 1 (Vision) in progress")
```

### 6. Success Message

Tell the user:

```
✅ **PHASE 1 (VISION) - STRATEGIC SYNTHESIS COMPLETE**

**Vision document created:** `~/.claude/projects/$PROJECT_SLUG/01-vision.md`

**What I Created:**

🎯 **Executive Summary** - The essence of your project in 2-3 sentences
🏗️ **Strategic Solution Approach** - The HOW and the innovation
💥 **The Explosive Outcome** - What success looks like when we nail this
🧠 **Strategic Decisions** - Key architectural choices with trade-offs
🗺️ **Path Forward** - Research plan for Phase 2

**This is NOT the project brief repeated.**

This is strategic thinking:
- How we'll solve the problem (technical architecture)
- What makes our approach unique (innovation)
- Why this is the winning strategy (justification)
- The explosive outcome when we succeed (vision)

**Next Steps:**

1. 📖 **Review the vision:** Open `01-vision.md`
2. 💭 **Does it inspire you?** Does it capture the strategic approach?
3. ✅ **When ready, approve:** `/approve-vision`

**Questions to ask yourself:**
- Does the executive summary capture the transformative outcome?
- Is the strategic approach compelling and technically sound?
- Can you see the explosive outcome clearly?
- Are the key decisions justified?
- Are you EXCITED to build this?

---
**This is where AI adds value: Strategic synthesis, not data entry.**
```

## Important Notes

### Agent Instructions

When deploying agents, emphasize:

1. **prd-expert**: Focus on SYNTHESIS, not duplication
   - Don't copy the brief
   - Create strategic narrative
   - Paint the explosive outcome
   - Make it inspiring

2. **agent-architecture-designer**: Focus on the HOW
   - Technical approach
   - System design
   - Key architectural decisions
   - Trade-offs and justifications

3. **ui-ux-designer**: Focus on UX innovation
   - User experience strategy
   - Design differentiation
   - User impact vision

### Quality Standards

The vision should be:
- **Inspiring**: Makes the user excited to build this
- **Strategic**: Shows thoughtful approach to solving the problem
- **Clear**: Anyone can understand the approach and outcome
- **Actionable**: Sets up Phase 2 (Mission/Research) clearly
- **Concise**: No fluff, no duplication, pure strategic thinking

### DO NOT

- Copy/paste from the brief
- Create more tables and forms
- Duplicate problem statements
- List requirements again
- Make it bureaucratic

### DO

- Synthesize and elevate
- Define the strategic approach
- Show innovation and differentiation
- Paint the explosive outcome
- Inspire action
