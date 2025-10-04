---
description: "Initialize new project through conversational setup"
argument-hint: "<project-slug>"
allowed-tools: Bash, Write, Read
---

# Start Project: $ARGUMENTS

You are initiating a **conversational project setup** in the 5-Phase Workflow System.

## Your Task

### 1. Validate Project Slug

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

print(f"✅ Project slug validated: {project_slug}")
```

### 2. Load Brief Template as Schema

```python
from pathlib import Path

# Load the brief template to understand what we need to capture
template_path = Path.home() / ".claude/templates/phases/00-project-brief-template.md"
template = template_path.read_text()

# This template defines the structure for our conversation
# We'll fill it in section by section
print("📋 Brief template loaded as conversation schema")
```

### 3. Begin Conversational Setup

Tell the user:

```
🚀 **LET'S BUILD SOMETHING AWESOME: $ARGUMENTS**

I'm going to ask you some questions to understand what you're building.
We'll fill out a project brief together as we talk. It should take about 5-10 minutes.

Just talk naturally - this is a conversation, not a form.

Ready? Let's go!
```

### 4. Conversational Questions (Fill Template As We Go)

Ask these questions **one at a time**, filling in the template as you receive answers.

---

**Question 1: What are we building?**
```
🎯 **What are we building?**

Give me the full picture and then sum it up in one sentence.

Full description: (What is this project? What does it do?)
One-liner: (Elevator pitch version)
```

*Fills: `{WHAT_DESCRIPTION}`, `{ONE_LINER}`, `{PROJECT_TYPE}` (infer from description)*

---

**Question 2: Who's it for?**
```
👥 **Who is this for?**

Who are the primary users?
What do they need from this?
```

*Fills: `{TARGET_USERS}`, `{USER_NEEDS}`*

---

**Question 3: Why does it matter?**
```
💡 **Why does this matter?**

What problem are we solving?
What's the impact if we nail this?
```

*Fills: `{PROBLEM}`, `{IMPACT}`*

---

**Question 4: Must-have features**
```
✅ **What are the must-have features?**

If you could only build 3-5 things for v1, what would they be?
These are the non-negotiables.
```

*Fills: `{MUST_HAVE_FEATURES}` as a bulleted list*

---

**Question 5: Should-have and nice-to-have**
```
🎁 **What about should-haves and nice-to-haves?**

Should-have: Important but not critical for launch
Nice-to-have: Future enhancements, v2+

Just say "none" if you want to keep it minimal for now.
```

*Fills: `{SHOULD_HAVE_FEATURES}`, `{NICE_TO_HAVE_FEATURES}` as bulleted lists or "None specified"*

---

**Question 6: Constraints**
```
⚠️ **Any constraints I should know about?**

Timeline: When do you need this?
Budget: Any cost limitations?
Technical: Must use certain tech? Can't use certain tech?
Other: Any other limitations?

Just say "flexible" or "none" for any that don't apply.
```

*Fills: `{TIMELINE}`, `{BUDGET}`, `{TECHNICAL_CONSTRAINTS}`, `{OTHER_CONSTRAINTS}`*

---

**Question 7: Success definition**
```
🎯 **What does success look like?**

How will we know this project is a win?
What metrics or outcomes matter most?

(e.g., "Users complete tasks 50% faster", "Handle 1000 requests/sec", "10,000 active users")
```

*Fills: `{SUCCESS_CRITERIA}`, `{KEY_METRICS}`*

---

**Question 8: Inspiration and references**
```
✨ **Any inspiration or references?**

Similar projects you like? (what you like about them)
Technical docs/APIs to reference?
Design inspiration?

Or just say "no" if nothing comes to mind - totally fine!
```

*Fills: `{INSPIRATION}`, `{TECH_REFERENCES}`, `{DESIGN_INSPIRATION}` or "None specified"*

---

**Question 9: Anything else?**
```
💭 **Anything else I should know?**

Any other context, background, or important info?
Or just say "that's it!" if we've covered everything.
```

*Fills: `{ADDITIONAL_CONTEXT}` or "N/A"*

---

### 5. Generate and Save Brief

After collecting all answers, tell the user:

```
🎨 **AWESOME! I've got everything I need.**

Creating your project brief now...
```

Then fill in the template and save:

```python
from pathlib import Path
from datetime import datetime

project_slug = "$ARGUMENTS"
project_name = project_slug.replace('-', ' ').title()

# Read template
template_path = Path.home() / ".claude/templates/phases/00-project-brief-template.md"
template = template_path.read_text()

# Fill in template with user's answers from the conversation
brief_content = template.format(
    PROJECT_NAME=project_name,
    DATE=datetime.now().strftime('%Y-%m-%d'),
    PROJECT_SLUG=project_slug,
    PROJECT_TYPE="[inferred from description - e.g., Web App, API, CLI Tool, etc.]",
    WHAT_DESCRIPTION="[from question 1 - full description]",
    ONE_LINER="[from question 1 - one sentence]",
    TARGET_USERS="[from question 2 - who it's for]",
    USER_NEEDS="[from question 2 - what they need]",
    PROBLEM="[from question 3 - problem]",
    IMPACT="[from question 3 - impact]",
    MUST_HAVE_FEATURES="[from question 4 - as bulleted list]",
    SHOULD_HAVE_FEATURES="[from question 5 - should-haves or 'None specified']",
    NICE_TO_HAVE_FEATURES="[from question 5 - nice-to-haves or 'None specified']",
    TIMELINE="[from question 6]",
    BUDGET="[from question 6]",
    TECHNICAL_CONSTRAINTS="[from question 6]",
    OTHER_CONSTRAINTS="[from question 6 or 'None']",
    SUCCESS_CRITERIA="[from question 7 - success definition]",
    KEY_METRICS="[from question 7 - metrics or 'To be defined']",
    INSPIRATION="[from question 8 - similar projects or 'None specified']",
    TECH_REFERENCES="[from question 8 - technical docs or 'None specified']",
    DESIGN_INSPIRATION="[from question 8 - design examples or 'None specified']",
    ADDITIONAL_CONTEXT="[from question 9 or 'N/A']"
)

# Create project directory
project_dir = Path.home() / ".claude/projects" / project_slug
project_dir.mkdir(parents=True, exist_ok=True)

# Write brief
brief_path = project_dir / "00-project-brief.md"
brief_path.write_text(brief_content)

print(f"✅ Project brief created: {brief_path}")
```

### 6. Initialize Project Infrastructure

```bash
echo "🔧 Setting up project infrastructure..."
python3 ~/.claude/scripts/init-project-database.py "$ARGUMENTS"
```

Create supporting directories:

```bash
PROJECT_DIR="$HOME/.claude/projects/$ARGUMENTS"

# Create supporting directories
mkdir -p "$PROJECT_DIR/research"
mkdir -p "$PROJECT_DIR/examples"
mkdir -p "$PROJECT_DIR/review"
mkdir -p "$PROJECT_DIR/agent-notes"
mkdir -p "$PROJECT_DIR/review-board"

# Create placeholder READMEs
cat > "$PROJECT_DIR/research/README.md" <<EOF
# Research & Findings

This directory contains technical research, dependency analysis, and architectural decisions.

Created during Phase 2 (Mission).
EOF

cat > "$PROJECT_DIR/examples/README.md" <<EOF
# Code Examples & References

This directory contains code samples, UI examples, and reference implementations.

Created during Phase 2 (Mission).
EOF

cat > "$PROJECT_DIR/review/README.md" <<EOF
# Review & Approval Tracking

This directory contains user review notes and approval checkpoints.

Updated throughout all phases.
EOF

cat > "$PROJECT_DIR/agent-notes/README.md" <<EOF
# Agent Communications

This directory contains agent collaboration logs, handoffs, and decision records.

Updated during Phase 4 (Implementation).
EOF

cat > "$PROJECT_DIR/review-board/README.md" <<EOF
# Review Board Sessions

This directory contains C-suite executive review sessions (Phase 3.5).

Each session creates a timestamped subdirectory with individual executive reports.
EOF

echo "✅ Project structure created"
```

### 7. Initialize Workflow Database

```python
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

project_slug = "$ARGUMENTS"
project_name = project_slug.replace('-', ' ').title()
project_dir = Path.home() / ".claude/projects" / project_slug
db_path = project_dir / "workflow.db"

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

workflow_id = str(uuid.uuid4())

cursor.execute("""
    INSERT INTO workflow (id, project_name, project_slug, current_phase, phase_number, created_at)
    VALUES (?, ?, ?, 'brief-complete', 0, CURRENT_TIMESTAMP)
""", (workflow_id, project_name, project_slug))

conn.commit()
conn.close()

print(f"✅ Workflow initialized with ID: {workflow_id}")
```

### 8. Display Success Message and Brief Preview

```
🎉 **PROJECT INITIALIZED: {PROJECT_NAME}**

**Location:** ~/.claude/projects/$ARGUMENTS/

**Project Structure Created:**
├── 00-project-brief.md ✅ (Created from our conversation)
├── research/ (Phase 2)
├── examples/ (Phase 2)
├── review/ (All phases)
├── agent-notes/ (Phase 4)
└── review-board/ (Phase 3.5)

**Your Project Brief:**

I've created a structured brief from our conversation. Here's what we captured:

📌 **What:** [one-liner from brief]
👥 **Who:** [target users]
🎯 **Success:** [success criteria]
✅ **Must-Haves:** [list top 3 must-haves]

**Review Your Brief:**
Open: `~/.claude/projects/$ARGUMENTS/00-project-brief.md`

Feel free to edit, add details, or refine anything before moving to Vision.

---

**The 5-Phase Journey:**
✅ **Phase 0: Brief Complete** ← You are here
⏳ **Phase 1: Vision** - Strategic synthesis (THE HOW, THE WHY, THE BOOM)
⏳ **Phase 2: Mission** - Research & technical approach
⏳ **Phase 3: Execution Plan** - Detailed implementation roadmap
⏳ **Phase 3.5: Review Board** - C-suite approval gate
⏳ **Phase 4: Implementation** - Build it
⏳ **Phase 5: Testing** - Validate it

---

**Next Steps:**

1. 📖 **Review the brief:** `~/.claude/projects/$ARGUMENTS/00-project-brief.md`
2. ✏️ **Edit if needed:** Add more details or refine anything
3. 🚀 **When ready:** `/start-vision` to create the strategic vision

**The Vision phase is where I take this brief and create:**
- Strategic approach (the HOW)
- Innovation & differentiation (the unique angle)
- Explosive outcome vision (what success looks like)
- Key architectural decisions (with trade-offs)

**Ready?** Run `/start-vision` when you're good with the brief!

---
**The conversational setup is complete. Time to create the strategic vision.**
```

## Important Notes

### Conversation Guidelines

1. **Keep it natural**: Ask one question at a time, wait for response
2. **Be flexible**: If they give you everything in one answer, great! Don't re-ask
3. **Infer intelligently**: If they mention "React app", infer PROJECT_TYPE as "Web App"
4. **Allow brevity**: If they say "no constraints", that's fine - write "None specified"
5. **Fill as you go**: Build up the brief progressively during conversation
6. **Show progress**: After key sections, summarize what you've captured so far

### Template Mapping

The brief template is your **schema** - it defines what to capture.
Map conversation answers to template placeholders.

### Quality Over Quantity

- A brief can be minimal and still be great
- Focus on clarity over completeness
- Let them add "none" or "flexible" where appropriate
- The brief is a foundation, not a dissertation

### The Handoff to Vision

The brief you create becomes the **source of truth** for Phase 1.
Vision will reference it, not duplicate it.
This is the context document that drives strategic synthesis.
