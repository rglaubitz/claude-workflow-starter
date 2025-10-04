# /build-agent Workflow Specification

> **Status:** 📋 PLANNED - This is a workflow specification, not an executable command yet.
>
> **Purpose:** Documents the design for a future /build-agent command that will orchestrate complete agent creation.

---

## Purpose
Orchestrates the complete agent creation pipeline, engaging multiple specialists to design, build, test, and deploy a production-ready agent.

## Usage
```
/build-agent <agent-name> <purpose>
/build-agent financial-analyst "Analyze P&L statements and generate insights"
/build-agent customer-bot "Handle customer inquiries via chat"
```

## Workflow Pipeline

### Phase 1: Design & Architecture (Parallel)
**Agents:** Agent Architecture Designer, Integration Specialist
- Create system blueprint
- Identify required integrations
- Define data flows
- Map communication patterns

### Phase 2: Infrastructure Setup (Sequential)
**Agents:** Memory System Engineer, MCP Bridge Engineer
- Design persistence layer
- Configure MCP servers if needed
- Setup knowledge schemas
- Prepare data pipelines

### Phase 3: Implementation (Parallel)
**Agents:** Task Manager (orchestrating multiple specialists)
- Implement core logic
- Build integration connectors
- Create memory systems
- Setup communication protocols

### Phase 4: Testing & Validation (Parallel)
**Agents:** Agent Testing Engineer, Code Review Expert
- Unit testing
- Integration testing
- Performance validation
- Security review
- Code quality analysis

### Phase 5: Documentation & Deployment
**Agents:** Documentation Expert, Integration Specialist
- Generate comprehensive docs
- Create deployment guide
- Setup monitoring
- Prepare handoff materials

## Workflow Execution

```python
def execute_build_agent(agent_name, purpose):
    # Phase 1: Parallel Design
    results = parallel_execute([
        Task("Design architecture",
             agent="agent-architecture-designer",
             params={"name": agent_name, "purpose": purpose}),
        Task("Plan integrations",
             agent="integration-specialist",
             params={"purpose": purpose})
    ])

    # Phase 2: Sequential Infrastructure
    memory_design = Task("Design memory system",
                        agent="memory-system-engineer",
                        params={"architecture": results['architecture']})

    # Phase 3: Parallel Implementation
    implementation = parallel_execute([
        Task("Build core agent", agent="task-manager"),
        Task("Create connectors", agent="integration-specialist"),
        Task("Implement memory", agent="memory-system-engineer")
    ])

    # Phase 4: Parallel Testing
    testing = parallel_execute([
        Task("Run tests", agent="agent-testing-engineer"),
        Task("Review code", agent="code-review-expert")
    ])

    # Phase 5: Documentation
    docs = Task("Generate documentation",
                agent="documentation-expert",
                params={"all_results": results})

    return compile_agent_package(results)
```

## Output Format

```yaml
Agent Created: [agent-name]
Status: ✅ Ready for Deployment

Architecture:
  - Type: [architecture-pattern]
  - Components: [list]
  - Integrations: [list]

Memory System:
  - Schema: [defined]
  - Persistence: [configured]

Testing Results:
  - Unit Tests: [pass/fail]
  - Integration: [pass/fail]
  - Performance: [metrics]

Documentation:
  - User Guide: ✓
  - API Reference: ✓
  - Deployment Guide: ✓

Next Steps:
  1. Review generated agent at: ~/.claude/agents/[agent-name].md
  2. Test with: /test-agent [agent-name]
  3. Deploy with: /deploy-agent [agent-name]
```

## Success Criteria

- All phases complete successfully
- Test coverage > 80%
- Documentation complete
- No critical issues from code review
- Performance benchmarks met

## Error Handling

If any phase fails:
1. Halt pipeline
2. Diagnostic mode activates
3. Debug team engages
4. Resolution proposed
5. Resume or restart options presented

## Related Commands

- `/test-agent` - Test an existing agent
- `/deploy-agent` - Deploy agent to production
- `/optimize-agent` - Optimize existing agent
- `/clone-agent` - Create variant of existing agent