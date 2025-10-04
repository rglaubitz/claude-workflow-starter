# Research Quality Standards

**Version:** 1.0
**Last Updated:** 2025-10-04
**Purpose:** Enforce high-quality research practices across all projects

---

## Core Principle

**High-quality results come from high-quality research.** All decisions must be grounded in current, credible, well-documented sources. This document defines the standards for acceptable research sources and organization.

---

## Source Quality Hierarchy

### Tier 1: Official Documentation (HIGHEST PRIORITY) ⭐

**Always check these sources first:**
- **Anthropic & Claude**: docs.anthropic.com, claude.ai, Anthropic blog
- **Framework Official Sites**: react.dev, fastapi.tiangolo.com, nextjs.org, etc.
- **Technical Standards**: W3C specs, RFCs, ECMA standards
- **Language Official Docs**: python.org, developer.mozilla.org, golang.org

**Quality Criteria:**
- Published by the authoritative organization
- Current and actively maintained
- Includes version-specific information
- Clear licensing and usage guidelines

---

### Tier 2: Verified GitHub Repositories

**Acceptable when:**
- **MINIMUM 1.5k+ stars** for code examples and alternatives
- Active maintenance (commits within last 6 months)
- Clear documentation (comprehensive README, examples)
- Explicit license (MIT, Apache 2.0, etc.)
- Demonstrates the specific pattern being researched

**How to Validate:**
```bash
# Check GitHub repo stats
- Stars: 1,500+ ✅
- Last commit: Within 6 months ✅
- Documentation: README + examples ✅
- License: Present and clear ✅
- Issues: Active community ✅
```

**Documentation Format:**
```markdown
**Source:** [Repo Name](https://github.com/org/repo)
**Stars:** 2.3k ⭐ | **Last Update:** 2025-09-15
**License:** MIT
**Relevance:** Demonstrates [specific pattern]
```

---

### Tier 3: Authoritative Technical Sources

**Acceptable sources:**
- Known technical leaders (Martin Fowler, Kent Beck, Dan Abramov, etc.)
- Reputable company engineering blogs:
  - Anthropic Blog
  - Google Research Blog
  - Netflix Tech Blog
  - Airbnb Engineering
  - etc.
- Peer-reviewed academic papers from reputable institutions
- Conference talks from recognized conferences (React Conf, PyCon, etc.)

**Quality Criteria:**
- Author has established credibility in the field
- Content is technical, not promotional
- Includes working examples or rigorous analysis
- Published within last 2 years (or explicitly validated as current)

---

### Tier 4: Official Package Registries

**Acceptable sources:**
- npm (verified publishers badge preferred)
- PyPI (verified projects)
- Maven Central
- RubyGems
- Crates.io (for Rust)

**Quality Criteria:**
- Package is actively maintained
- Clear version history
- Security advisories checked
- Dependency tree reviewed

---

## REJECTED Sources ❌

**Never use these as primary sources:**
- ❌ Random blogs without author credentials
- ❌ Stack Overflow (except for understanding specific error messages)
- ❌ GitHub repos with <1.5k stars (for alternatives/examples)
- ❌ Documentation >2 years old without explicit validation
- ❌ Unverified tutorials or Medium posts from unknown authors
- ❌ YouTube videos (unless from official channels or recognized experts)
- ❌ Reddit posts, forum discussions (except for community sentiment)
- ❌ Unmaintained repos (no commits in 6+ months)

---

## Folder Organization Standard

**Every project MUST follow this structure:**

```
research/
├── documentation/              # Official docs and guides (SAVE or LINK)
│   ├── anthropic-docs/        # Claude/Anthropic official documentation
│   │   └── [saved PDFs, links, or markdown extracts]
│   ├── framework-docs/        # Framework official documentation
│   │   └── [react-docs.md, fastapi-guide.md, etc.]
│   └── api-specs/             # API specifications and standards
│       └── [openapi-spec.yaml, graphql-schema.md, etc.]
│
├── examples/                  # High-quality code samples
│   ├── implementation-patterns/
│   │   ├── authentication-example.md
│   │   ├── data-fetching-pattern.md
│   │   └── [Pattern descriptions with source links]
│   └── best-practices/
│       ├── error-handling.md
│       ├── testing-strategies.md
│       └── [Best practice implementations]
│
├── architecture-decisions/    # ADRs with research backing
│   ├── 001-choose-database.md
│   ├── 002-authentication-strategy.md
│   └── [Numbered ADR files with citations]
│
└── references.md              # Master index of all sources
```

---

## Source Validation Checklist

Before adding any source to research folders, validate:

- [ ] **Authority**: Source is from Tier 1-4 hierarchy
- [ ] **Currency**: Published <2 years ago OR validated as current
- [ ] **Relevance**: Directly relates to our project needs
- [ ] **Accessibility**: URL is accessible and likely to remain available
- [ ] **License**: Compatible with our project (if code)
- [ ] **Quality**: Technical depth appropriate for our needs

**If GitHub repo:**
- [ ] **Stars**: 1.5k+ minimum
- [ ] **Maintenance**: Commits within 6 months
- [ ] **Documentation**: README + examples present
- [ ] **License**: Clearly stated and compatible

**If documentation:**
- [ ] **Official**: Published by authoritative source
- [ ] **Version**: Matches our tech stack versions
- [ ] **Complete**: Covers the topic comprehensively
- [ ] **Examples**: Includes working code examples

---

## Research Documentation Format

### For references.md

```markdown
# Research References - [Project Name]

## Official Documentation

### Anthropic / Claude
- [Claude API Reference](https://docs.anthropic.com/api) - v2024-10 - Last checked: 2025-10-04 ✅
- [Prompt Engineering Guide](https://docs.anthropic.com/prompting) - Official - Last checked: 2025-10-04 ✅

### Framework Documentation
- [React 18 Docs](https://react.dev) - Official - Current ✅
- [FastAPI](https://fastapi.tiangolo.com) - v0.104 - Current ✅

## GitHub Examples (1.5k+ stars)

### Authentication Patterns
- **[next-auth](https://github.com/nextauthjs/next-auth)** - 18.2k ⭐
  - Last Update: 2025-09-28
  - License: ISC
  - Relevance: Complete authentication solution for Next.js
  - Used for: OAuth implementation pattern

### State Management
- **[zustand](https://github.com/pmndrs/zustand)** - 38.5k ⭐
  - Last Update: 2025-10-01
  - License: MIT
  - Relevance: Lightweight React state management
  - Used for: Global state patterns

## Technical Articles

### Performance Optimization
- [React Performance Optimization](https://kentcdodds.com/blog/react-performance) - Kent C. Dodds - 2024-03
  - Validated: 2025-10-04 ✅
  - Relevance: Component optimization strategies

## Source Quality Summary

- Total Sources: 12
- Official Docs: 6 (50%)
- GitHub (1.5k+): 4 (33%)
- Technical Articles: 2 (17%)
- Average Age: 4 months
- All Links Validated: ✅ 2025-10-04
```

---

## CIO Review Validation

During Phase 3.5 Review Board, the CIO will validate:

1. **Source Quality**: All sources meet tier requirements
2. **GitHub Stars**: All example repos have 1.5k+ stars
3. **Currency**: All sources <2 years or validated current
4. **Citations**: All research has proper citations with URLs
5. **Folder Structure**: Follows standard organization
6. **Completeness**: All Vision requirements have research backing

**Automatic Rejection Triggers:**
- Any GitHub example <1.5k stars
- Documentation >2 years without validation
- Missing citations or broken links
- Random blog posts as primary sources
- Stack Overflow as primary source (not error-specific)

---

## Research-Before-Action Protocol

**All agents must follow this protocol before task execution:**

1. **Check `research/documentation/`** for official guidance
2. **Review `research/examples/`** for proven patterns
3. **Validate approach** against research findings
4. **Reference sources** in implementation comments

**If research is missing or inadequate:**
- STOP implementation
- Request research-manager to gather proper sources
- Wait for quality research before proceeding

---

## Continuous Improvement

### Research Effectiveness Metrics

Track in project database:
- Sources gathered vs sources used
- Research quality scores from CIO reviews
- Implementation decisions backed by research (%)
- Research gaps identified during implementation

### Feedback Loop

- Review research effectiveness after each project
- Update standards based on lessons learned
- Share best practices across projects

---

**Last Updated:** 2025-10-04
**Maintained By:** research-manager, CIO
**Enforced By:** CIO during Phase 3.5 Review Board
