# /review-all Workflow Specification

> **Status:** 📋 PLANNED - This is a workflow specification, not an executable command yet.
>
> **Purpose:** Documents the design for a future /review-all command that orchestrates comprehensive parallel code review.

---

## Purpose
Triggers comprehensive parallel review by multiple specialists, providing multi-dimensional analysis of code, architecture, security, and documentation.

## Usage
```
/review-all                    # Review all changed files
/review-all <path>            # Review specific path
/review-all --focus security  # Emphasize security review
/review-all --pr 123          # Review pull request
```

## Parallel Review Streams

### Stream A: Code Quality
**Agent:** Code Review Expert
- Naming conventions
- Code organization
- DRY principle adherence
- SOLID principles
- Readability and maintainability
- Best practices compliance

### Stream B: Security Analysis
**Agent:** Code Review Expert (security focus)
- OWASP compliance
- Injection vulnerabilities
- Authentication issues
- Authorization flaws
- Data exposure risks
- Cryptographic weaknesses

### Stream C: Performance Review
**Agent:** Code Review Expert (performance focus)
- Algorithm efficiency
- Database query optimization
- Memory usage patterns
- Caching opportunities
- Bottleneck identification
- Scalability concerns

### Stream D: Testing Coverage
**Agent:** Agent Testing Engineer
- Test completeness
- Edge case coverage
- Test quality assessment
- Missing test scenarios
- Test performance
- Mock/stub appropriateness

### Stream E: Documentation Audit
**Agent:** Documentation Expert
- Code comment quality
- API documentation
- README completeness
- Inline documentation
- Example coverage
- Changelog updates

### Stream F: Architecture Review
**Agent:** Agent Architecture Designer
- Design pattern usage
- Architectural consistency
- Dependency management
- Modularity assessment
- Coupling analysis
- Extensibility evaluation

## Workflow Execution

```python
def execute_review_all(path=None, focus=None):
    # Launch all review streams in parallel
    review_streams = parallel_execute([
        Task("Code quality review",
             agent="code-review-expert",
             params={"focus": "quality", "path": path}),

        Task("Security analysis",
             agent="code-review-expert",
             params={"focus": "security", "path": path}),

        Task("Performance review",
             agent="code-review-expert",
             params={"focus": "performance", "path": path}),

        Task("Test coverage analysis",
             agent="agent-testing-engineer",
             params={"path": path}),

        Task("Documentation audit",
             agent="documentation-expert",
             params={"path": path}),

        Task("Architecture review",
             agent="agent-architecture-designer",
             params={"path": path})
    ])

    # Compile and prioritize findings
    results = compile_review_results(review_streams)

    # Generate action items
    action_items = prioritize_findings(results, focus)

    return format_review_report(results, action_items)
```

## Output Format

```markdown
# Comprehensive Review Report

## Executive Summary
- **Overall Health**: 🟢 Good / 🟡 Needs Attention / 🔴 Critical Issues
- **Items Reviewed**: [count]
- **Critical Issues**: [count]
- **Recommendations**: [count]

## Critical Issues (Must Fix)
🔴 **Security**: SQL injection vulnerability in user.py:45
🔴 **Performance**: O(n³) algorithm in data_processor.py:78
🔴 **Architecture**: Circular dependency between modules

## Major Issues (Should Fix)
🟡 **Code Quality**: Duplicate code in 3 locations
🟡 **Testing**: Missing tests for error conditions
🟡 **Documentation**: API endpoints undocumented

## Recommendations
1. **Immediate**: Address security vulnerabilities
2. **Short-term**: Improve test coverage to 80%
3. **Long-term**: Refactor for better modularity

## Detailed Findings

### Code Quality (Score: 7.5/10)
- ✅ Good naming conventions
- ✅ Consistent code style
- ⚠️ Some functions too complex
- ❌ Duplicate code detected

### Security (Score: 6.0/10)
- ✅ Authentication implemented
- ⚠️ Input validation incomplete
- ❌ SQL injection risk found

### Performance (Score: 8.0/10)
- ✅ Efficient database queries
- ✅ Good caching strategy
- ⚠️ One inefficient algorithm

### Testing (Coverage: 65%)
- ✅ Core functionality tested
- ⚠️ Edge cases missing
- ❌ No integration tests

### Documentation (Score: 7.0/10)
- ✅ README comprehensive
- ⚠️ Some functions undocumented
- ❌ API docs outdated

### Architecture (Score: 8.5/10)
- ✅ Good separation of concerns
- ✅ Modular design
- ⚠️ Minor coupling issues

## Action Items

### P0 - Critical (Do Now)
- [ ] Fix SQL injection in user.py
- [ ] Resolve circular dependency

### P1 - High (This Week)
- [ ] Add input validation
- [ ] Improve algorithm efficiency
- [ ] Add missing tests

### P2 - Medium (This Sprint)
- [ ] Remove code duplication
- [ ] Update API documentation
- [ ] Reduce coupling

## Next Steps
1. Run `/fix-critical` to auto-fix critical issues
2. Run `/improve-tests` to enhance test coverage
3. Run `/update-docs` to refresh documentation
```

## Review Customization

### Focus Areas
- `--focus security` - Emphasize security review
- `--focus performance` - Deep performance analysis
- `--focus architecture` - Architectural assessment
- `--focus quality` - Code quality focus

### Scope Control
- `--files <pattern>` - Review specific file patterns
- `--since <commit>` - Review changes since commit
- `--pr <number>` - Review pull request
- `--staged` - Review staged changes only

## Success Metrics

- All review streams complete successfully
- No timeout or resource issues
- Comprehensive coverage of all aspects
- Clear, actionable recommendations
- Prioritized issue list

## Error Handling

If a review stream fails:
1. Continue other streams
2. Mark stream as incomplete
3. Provide partial results
4. Offer rerun option for failed stream

## Related Commands

- `/fix-critical` - Auto-fix critical issues
- `/improve-tests` - Enhance test coverage
- `/update-docs` - Update documentation
- `/optimize` - Run optimization workflow