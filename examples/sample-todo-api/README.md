# Example Project: Simple Todo API

This example demonstrates the complete 5-phase workflow for building a REST API.

## Project Overview

**Goal**: Build a simple RESTful API for managing todo items with authentication.

**Tech Stack**: Python FastAPI, SQLite, JWT authentication

**Features**:
- User registration and authentication
- CRUD operations for todos
- Task categorization
- Due dates and priorities
- API documentation

## Workflow Phases

### Phase 0: Project Brief

See `00-project-brief.md` for the initial requirements and goals.

**Key Requirements**:
- User authentication with JWT
- Full CRUD for todos
- Category and priority support
- Comprehensive API docs
- < 2 second response times
- 90%+ test coverage

### Phase 1: Vision

See `01-vision.md` for the what and why.

**Key Decisions**:
- FastAPI chosen for performance and auto-docs
- SQLite for simplicity (production can use PostgreSQL)
- JWT for stateless authentication
- RESTful design principles
- OpenAPI 3.0 documentation

### Phase 2: Mission

See `02-mission.md` for technical research and dependencies.

**Key Findings**:
- FastAPI provides automatic OpenAPI docs
- Pydantic for data validation
- SQLAlchemy for ORM
- python-jose for JWT handling
- pytest for testing

**Dependencies Identified**:
- fastapi
- uvicorn
- sqlalchemy
- pydantic
- python-jose[cryptography]
- passlib[bcrypt]
- pytest
- httpx (for testing)

### Phase 3: Execution Plan

See `03-execution-plan.md` for detailed implementation tasks.

**Task Breakdown** (18 tasks):
1. Project structure setup
2. Database models (User, Todo)
3. Authentication system
4. User registration endpoint
5. Login endpoint
6. Todo CRUD endpoints
7. Category management
8. Priority system
9. Due date handling
10. API documentation
11. Error handling
12. Input validation
13. Unit tests
14. Integration tests
15. API tests
16. Performance testing
17. Security audit
18. Documentation finalization

**Agent Assignments**:
- backend-developer: Core API implementation
- database-architect: Schema design
- security-auditor: Authentication & authorization
- api-architect: Endpoint design
- qa-engineer: Test strategy
- documentation-expert: API docs

### Phase 3.5: Review Board

See `review-board-session-001/` for the C-suite review.

**CIO Review** (APPROVED):
- ✅ Dependencies well-researched
- ✅ FastAPI documentation comprehensive
- ✅ JWT best practices followed
- ⚠️ Consider rate limiting for production

**CTO Review** (APPROVED):
- ✅ Architecture sound
- ✅ RESTful design proper
- ✅ Database schema normalized
- ⚠️ Add database migration strategy for production

**COO Review** (APPROVED):
- ✅ Timeline realistic (2 weeks)
- ✅ Goals achievable
- ✅ API design intuitive
- ⚠️ Consider API versioning early

**Overall Verdict**: APPROVED_WITH_CONCERNS

Concerns noted but non-blocking. Proceed to implementation with attention to production considerations (rate limiting, migrations, versioning).

### Phase 4: Implementation

See `04-implementation-report.md` for build progress.

**Completed**:
- ✅ All 18 tasks completed
- ✅ 95% test coverage achieved
- ✅ All endpoints functional
- ✅ Security audit passed
- ✅ Documentation complete

**Challenges**:
- JWT token expiry handling required additional testing
- Category hierarchies needed refactoring
- Performance target met (avg 150ms response time)

**Code Stats**:
- 1,200 lines of Python
- 45 test cases
- 18 API endpoints
- 100% endpoint coverage

### Phase 5: Testing

See `05-test-plan.md` for validation results.

**Test Results**:
- ✅ Unit tests: 35/35 passed
- ✅ Integration tests: 8/8 passed
- ✅ API tests: 18/18 passed
- ✅ Performance tests: All passed (< 500ms)
- ✅ Security tests: No vulnerabilities found
- ✅ Load testing: Handles 100 req/sec

**Quality Metrics**:
- Code coverage: 95%
- Documentation coverage: 100%
- Performance: 150ms average response
- Security: A+ rating

**Final Status**: APPROVED

Project meets all requirements and success criteria. Ready for deployment.

## Key Learnings

1. **Review Board is valuable**: Caught production considerations early
2. **Explicit approval gates**: Ensured understanding at each phase
3. **Agent specialization**: Security-auditor found issues in design phase
4. **Template-driven docs**: Kept documentation consistent
5. **Test-first approach**: Achieved high coverage naturally

## Project Files

```
sample-todo-api/
├── 00-project-brief.md
├── 01-vision.md
├── 02-mission.md
├── 03-execution-plan.md
├── 04-implementation-report.md
├── 05-test-plan.md
├── review-board-session-001/
│   ├── CIO-review.md
│   ├── CTO-review.md
│   ├── COO-review.md
│   └── verdict.md
├── research/
│   ├── fastapi-research.md
│   ├── jwt-best-practices.md
│   └── database-design.md
├── examples/
│   ├── api-request-examples.md
│   └── authentication-flow.md
└── README.md (this file)
```

## How to Use This Example

1. **Read the brief**: Start with `00-project-brief.md`
2. **Follow the phases**: Read each phase document in order
3. **Review the Review Board**: See how C-suite evaluated the plan
4. **Study the implementation**: See what was actually built
5. **Check the testing**: See comprehensive validation

This example shows:
- How to write a good project brief
- What each phase deliverable looks like
- How the Review Board works
- What a complete workflow produces

## Replicating for Your Project

To create a similar project:

```bash
# 1. Create project directory
mkdir -p ~/.claude/projects/my-api

# 2. Copy the project brief template
cp ~/.claude/templates/phases/00-project-brief-template.md \
   ~/.claude/projects/my-api/00-project-brief.md

# 3. Fill out YOUR project details

# 4. Start the workflow
/start-project my-api

# 5. Follow the phases
/start-vision
# ... review and approve each phase ...
```

## Timeline

This example project took:
- Phase 0: 2 hours (writing brief)
- Phase 1: 1 hour (vision)
- Phase 2: 3 hours (research)
- Phase 3: 2 hours (planning)
- Phase 3.5: 30 minutes (review board)
- Phase 4: 1 week (implementation)
- Phase 5: 2 days (testing)

**Total**: ~2 weeks from idea to deployment.

---

**This example demonstrates the power of structured workflows! 🚀**
