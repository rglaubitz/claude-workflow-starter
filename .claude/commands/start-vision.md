---
description: "Begin Phase 1 (Vision) - Create the Vision document"
allowed-tools: Task, Bash, Write, Read
---

# Phase 1: Start Vision

You are initiating **Phase 1: Vision** of the 5-phase workflow.

## Your Task

Create the Vision document by:

1. **Read the project brief** at `~/.claude/projects/<project-slug>/00-project-brief.md`
2. **Use the vision template** at `~/.claude/templates/phases/01-vision-template.md`
3. **Deploy appropriate agents**:
   - Primary: `prd-expert` (overall vision)
   - Support: `agent-architecture-designer` (system design thinking)
   - Support: `ui-ux-designer` (user experience perspective)

4. **Create the Vision document** at:
   `~/.claude/projects/<project-slug>/01-vision.md`

## What Goes in the Vision Document

- **Problem Statement**: What problem are we solving?
- **Goals & Success Criteria**: What does success look like?
- **User Impact**: Who benefits and how?
- **Value Proposition**: Why build this?
- **Stakeholder Requirements**: What do stakeholders need?
- **High-level Constraints**: Budget, timeline, technical limitations
- **Vision Statement**: The inspiring "why" behind this project

## When Complete

Tell the user:
> "✅ **Phase 1 (Vision) Complete**
>
> Vision document created at: `projects/<project-slug>/01-vision.md`
>
> **Next Steps:**
> 1. Review the Vision document
> 2. Make any necessary edits
> 3. When satisfied, run: `/approve-vision`"

## Database Updates

Update the workflow database:
```python
# Update phase status
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'vision-in-progress',
        phase_number = 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

# Create deliverable record
cursor.execute("""
    INSERT INTO deliverables (id, phase_number, phase_name, document_path, status)
    VALUES (?, 1, 'vision', ?, 'draft')
""", (deliverable_id, document_path))
```

## Important

- Do NOT proceed to Phase 2 without explicit user approval via `/approve-vision`
- The Vision document is the foundation - take time to get it right
- Ensure all sections from the template are completed
