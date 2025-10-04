---
description: "Begin Phase 5 (Testing) - Validate implementation against requirements"
allowed-tools: Task, Bash, Write, Read
---

# Phase 5: Start Testing

You are initiating **Phase 5: Testing** - the validation phase.

## Phase 5 MCP Profile

```bash
echo "🧪 Keeping code-work profile for Phase 5 (test analysis)..."
# Already active from Phase 4, no change needed
# Could switch to minimal for speed if preferred
```

## Prerequisites Check

1. **Verify Implementation is complete**:
```python
cursor.execute("""
    SELECT status FROM deliverables
    WHERE phase_number = 4 AND phase_name = 'implementation'
""")
result = cursor.fetchone()

if not result or result[0] != 'completed':
    print("❌ Cannot start Testing - Implementation must be complete first")
    print("Run: /complete-implementation")
    exit()
```

## Your Task

Create comprehensive test plan and execute:

1. **Read completed work**:
   - Vision: `~/.claude/projects/<project-slug>/01-vision.md` (success criteria)
   - Mission: `~/.claude/projects/<project-slug>/02-mission.md` (technical specs)
   - Execution Plan: `~/.claude/projects/<project-slug>/03-execution-plan.md` (what was built)
   - Implementation Report: `~/.claude/projects/<project-slug>/04-implementation-report.md` (what was done)

2. **Use test plan template** at `~/.claude/templates/phases/05-test-plan-template.md`

3. **Deploy appropriate agents**:
   - Primary: `qa-engineer` (test strategy and orchestration)
   - Primary: `agent-testing-engineer` (agent behavior validation)
   - Support: `performance-engineer` (performance testing)
   - Support: `security-auditor` (security testing)
   - Support: `accessibility-specialist` (accessibility testing, if web)
   - Support: Technology-specific testers based on implementation

4. **Create Test Plan** at:
   `~/.claude/projects/<project-slug>/05-test-plan.md`

## What Goes in the Test Plan

### Test Strategy
- **Scope**: What will be tested and what won't
- **Approach**: Testing methodologies (unit, integration, E2E, etc.)
- **Environment**: Where tests will run
- **Tools**: Testing frameworks and tools

### Test Cases
- **Functional Tests**: Does it work as designed?
- **Integration Tests**: Do components work together?
- **End-to-End Tests**: Do full workflows complete?
- **Edge Cases**: Boundary conditions and error handling
- **Performance Tests**: Speed, load, scalability
- **Security Tests**: Vulnerabilities, auth, data protection
- **Accessibility Tests**: WCAG compliance (if applicable)

### Success Criteria (from Vision)
For each Vision goal:
- [ ] [Vision Goal 1]: [Test that validates it]
- [ ] [Vision Goal 2]: [Test that validates it]
- [ ] [Vision Goal 3]: [Test that validates it]

### Test Execution Plan
- Test execution order
- Dependencies between tests
- Pass/fail criteria
- Bug tracking and fixing workflow

## Testing Workflow

```
1. Create comprehensive test plan
2. Write automated tests (if not already done)
3. Execute test suite
4. Document results
5. For each failure:
   - Log bug
   - Fix bug
   - Re-test
   - Update Implementation Report
6. Repeat until all tests pass
7. Generate final test report
```

## Real-time Testing

As tests execute:
- Use TodoWrite to track test cases
- Mark pass/fail for each test category
- Update Test Plan with results
- Fix bugs as they're found
- Re-run tests after fixes

## When All Tests Pass

Tell the user:
> "✅ **Phase 5 (Testing) Complete - All Tests Passing**
>
> Test Plan: `projects/<project-slug>/05-test-plan.md`
>
> **Test Results:**
> - Total Test Cases: [X]
> - Passed: [X]
> - Failed: 0
> - Code Coverage: [X%]
> - Performance: [Meets/Exceeds requirements]
> - Security: [No vulnerabilities found]
>
> **Vision Goals Validated:**
> - [Goal 1]: ✅ Achieved
> - [Goal 2]: ✅ Achieved
> - [Goal 3]: ✅ Achieved
>
> **Next Steps:**
> 1. Review the Test Plan and results
> 2. Verify all Vision success criteria are met
> 3. When satisfied, run: `/approve-testing`"

## Database Updates

```python
# Update phase status
cursor.execute("""
    UPDATE workflow
    SET current_phase = 'testing-in-progress',
        phase_number = 5,
        updated_at = CURRENT_TIMESTAMP
    WHERE project_slug = ?
""", (project_slug,))

# Create deliverable record
cursor.execute("""
    INSERT INTO deliverables (id, phase_number, phase_name, document_path, status)
    VALUES (?, 5, 'test-plan', ?, 'in-progress')
""", (deliverable_id, document_path))
```

## Important

- Do NOT approve testing until ALL tests pass
- Bugs found = return to implementation to fix
- Testing validates against **Vision goals**, not just technical specs
- Performance and security are not optional
- Test Plan should be as thorough as the implementation
- This is the final quality gate before project completion
