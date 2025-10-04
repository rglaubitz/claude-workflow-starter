---
description: "Begin Phase 2 (Mission) - Research and define technical approach"
allowed-tools: Task, Bash, Write, Read
---

# Phase 2: Start Mission

You are initiating **Phase 2: Mission** of the 5-phase workflow.

## Prerequisites Check

1. **Verify Phase 1 is approved**:
```python
cursor.execute("""
    SELECT status FROM deliverables
    WHERE phase_number = 1 AND phase_name = 'vision'
""")
result = cursor.fetchone()

if not result or result[0] != 'approved':
    print("❌ Cannot start Mission - Vision must be approved first")
    print("Run: /approve-vision")
    exit()
```

## Your Task

Create the Mission document by:

1. **Read the approved Vision** at `~/.claude/projects/<project-slug>/01-vision.md`
2. **Use the mission template** at `~/.claude/templates/phases/02-mission-template.md`
3. **Deploy the Research Division**:
   - **Strategic Lead**: `research-manager` (oversees quality, coordinates with CIO)
   - **Tactical Coordinator**: `research-coordinator` (routes to specialist teams)
   - **4 Specialist Teams (12 agents)**:

     **Documentation Team (3 agents)**:
     - `documentation-hunter`: Official docs (Anthropic, frameworks)
     - `api-documentation-specialist`: API specs, OpenAPI
     - `standards-researcher`: W3C, RFCs, technical standards

     **Code Examples Team (3 agents)**:
     - `github-examples-hunter`: 1.5k+ star repos with working examples
     - `pattern-implementation-analyst`: Extract patterns from code
     - `code-quality-validator`: Validate licenses and quality

     **Market Intelligence Team (3 agents)**:
     - `company-researcher`: Company and product analysis
     - `competitive-intelligence-analyst`: Alternative solutions
     - `technical-trend-analyst`: Industry trends and best practices

     **Deep Research Team (3 agents)**:
     - `deep-researcher`: Multi-source synthesis and analysis
     - `technical-validator`: Verify technical claims
     - `citation-manager`: Maintain references.md with proper citations

   - **Support**: Technology-specific agents as needed:
     - `frontend-developer` (if web/UI)
     - `backend-developer` (if API/services)
     - `database-architect` (if data-heavy)
     - `ai-ml-engineer` (if AI/ML features)

4. **Create supporting directories** (enforced folder structure):
```bash
mkdir -p ~/.claude/projects/<project-slug>/research/documentation/anthropic-docs
mkdir -p ~/.claude/projects/<project-slug>/research/documentation/framework-docs
mkdir -p ~/.claude/projects/<project-slug>/research/documentation/api-specs
mkdir -p ~/.claude/projects/<project-slug>/research/examples/implementation-patterns
mkdir -p ~/.claude/projects/<project-slug>/research/examples/best-practices
mkdir -p ~/.claude/projects/<project-slug>/research/architecture-decisions
mkdir -p ~/.claude/projects/<project-slug>/dependencies
```

5. **Research and document** (enforce quality standards):
   - **Source Quality Hierarchy**: Follow templates/research-quality-standards.md
     - Tier 1: Official Documentation (Anthropic, Claude, framework sites) - HIGHEST PRIORITY
     - Tier 2: Verified GitHub Repositories (1.5k+ stars minimum)
     - Tier 3: Authoritative Technical Sources (known experts, reputable blogs)
     - Tier 4: Official Package Registries (npm, PyPI, etc.)
   - **Research Outputs**:
     - Technical approaches aligned with Vision goals
     - All dependencies with versions and justifications
     - Code examples from 1.5k+ star repos demonstrating key patterns
     - Best practices from authoritative sources
     - Architecture decisions backed by research citations
   - **Quality Gate**: Research Division enforces standards, CIO validates during Review Board

6. **Create the Mission document** at:
   `~/.claude/projects/<project-slug>/02-mission.md`

## What Goes in the Mission Document

- **Technical Approach**: How will we build this?
- **Technology Stack**: What tools, frameworks, languages?
- **Dependencies**: Complete list with versions and purposes
- **Architecture Overview**: High-level system design
- **Data Model**: How will data be structured?
- **API Design**: If applicable, API contracts
- **Code Examples**: Reference implementations
- **Research Summary**: Key findings and decisions
- **Open Questions**: What still needs investigation?

## When Complete

Tell the user:
> "✅ **Phase 2 (Mission) Complete**
>
> Mission document created at: `projects/<project-slug>/02-mission.md`
>
> **Supporting Materials:**
> - Research: `projects/<project-slug>/research/`
> - Examples: `projects/<project-slug>/examples/`
> - Dependencies: `projects/<project-slug>/dependencies/`
>
> **Next Steps:**
> 1. Review the Mission document
> 2. Verify all dependencies are identified
> 3. Check that technical approach aligns with Vision
> 4. When satisfied, run: `/approve-mission`"

## Database Updates

```python
# Update phase status
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'mission-in-progress',
        phase_number = 2,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

# Create deliverable record
cursor.execute("""
    INSERT INTO deliverables (id, phase_number, phase_name, document_path, status)
    VALUES (?, 2, 'mission', ?, 'draft')
""", (deliverable_id, document_path))
```

## Important

- Do NOT proceed to Phase 3 without explicit user approval via `/approve-mission`
- Thorough research now saves time in implementation
- Use `/add-dependency` to track dependencies as you find them
- Gather real code examples, not just theory
