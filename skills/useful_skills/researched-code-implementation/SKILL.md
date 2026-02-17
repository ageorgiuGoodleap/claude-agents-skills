---
name: researched-code-implementation
description: |
  Analyze comprehensive documentation (local files, URLs, codebase references) to understand
  implementation requirements, identify optimal code locations through intelligent discovery,
  and execute production-ready implementations that match existing patterns. Use when implementing
  features based on documentation, specifications, API docs, or when user requests 'implement
  based on these docs', 'follow this specification', or provides documentation files for implementation.
---

# Documentation-Driven Implementation

Analyze comprehensive documentation (local files, URLs, codebase references) to understand implementation requirements, identify optimal code locations through intelligent discovery, and execute production-ready implementations that match existing patterns.

## Overview

This skill performs deep documentation analysis and intelligent code implementation by:
1. Discovering and processing documentation from multiple sources (local files, URLs, embedded docs)
2. Extracting implementation requirements through hybrid analysis (skim → deep dive)
3. Identifying code locations via git diff analysis, semantic search, and pattern matching
4. Generating an implementation plan with documented assumptions
5. Executing code changes after explicit user approval

## When to Use This Skill

Trigger when:
- User provides documentation (markdown, PDF, txt) or file paths for a new feature/update
- Official API documentation or spec documents are referenced
- Implementation requires understanding external or internal documentation
- User says "implement based on these docs", "follow this specification", "use this guide to implement"
- Complex features requiring documentation review before coding

## Workflow

### Phase 1: Input Analysis & Documentation Discovery

**Extract from user request:**
- Task description (feature, update, fix)
- Documentation sources provided (file paths, URLs, references)
- Code area hints (file names, modules, or "find it yourself")
- Implementation constraints (deadlines, must-use libraries, architectural requirements)

**Documentation Discovery Protocol:**

**Explicit sources (user-provided):**
```bash
# Local files
Read tool: /path/to/spec.md
Read tool: /path/to/api-docs.pdf

# URLs
WebFetch tool: https://docs.example.com/api/v2
```

**Implicit sources (search codebase):**
```bash
# Find embedded documentation
Glob: "**/*.md" or "**/README.md" or "**/ARCHITECTURE.md"

# Search for doc comments referencing the feature
Grep: 'documentation|spec|reference' with appropriate filters
```

**Decision tree for source priority:**
1. User-provided paths/URLs → highest priority
2. Codebase README/ARCHITECTURE files → secondary
3. Inline code documentation → tertiary
4. External URLs mentioned in codebase → lowest priority

### Phase 2: Hybrid Documentation Extraction

**Step 2A: Skim Phase (Token-Efficient)**

For each documentation source:
1. Extract table of contents or section headers
2. Identify sections relevant to the implementation task
3. Create a relevance map (which sections to deep dive)

```bash
# For markdown - read first to see structure
Read tool with initial scan

# For PDFs - review first page and TOC only
Read tool with pages parameter for TOC
```

**Relevance scoring criteria:**
- Direct mentions of feature/component name
- API endpoints, function signatures, data structures
- Configuration, setup, or integration steps
- Error handling, edge cases, validation rules
- Examples matching the implementation task

**Step 2B: Deep Dive Phase (Targeted)**

For high-relevance sections only:
1. Extract complete section content
2. Identify concrete requirements (MUST, SHOULD, MAY)
3. Extract code examples, schemas, interfaces
4. Note dependencies, prerequisites, related components
5. Flag ambiguities or contradictions

**Extraction output format:**
```
REQUIREMENTS:
- [MUST] Requirement 1 from section X
- [SHOULD] Requirement 2 from section Y
- [MAY] Optional feature from section Z

INTERFACES/SCHEMAS:
- API endpoint: POST /api/resource
  - Request: { field: type, ... }
  - Response: { field: type, ... }

DEPENDENCIES:
- Library X version Y.Z
- Service A must be running

PATTERNS TO FOLLOW:
- Error handling: use try/catch with specific exceptions
- Validation: use schema validator from utils/

AMBIGUITIES:
- Documentation unclear on timeout behavior → ASSUME 30s default
- No mention of rate limiting → ASSUME no limits needed
```

### Phase 3: Intelligent Code Location Discovery

**Discovery Strategy (execute in order until location found):**

**3A: Git Diff Analysis (if PR/branch context exists)**
```bash
# PR context
Bash: gh pr diff <pr-number>

# Branch context
Bash: git diff main...<branch-name>

# Recent changes in relevant areas
Bash: git log --oneline --since="1 month ago" | grep -i '<feature-keyword>'
```

**Extract from diffs:**
- Files already modified for this feature
- Import patterns (which modules are used)
- Code style (formatting, naming conventions)
- Testing patterns (where tests live, how they're structured)

**3B: Semantic Search (find related functionality)**
```bash
# Search for similar features/components
Grep: '<feature-keyword>|<related-term>' with appropriate type filters

# Find files by name pattern
Glob: '*<component>*' with appropriate filters
```

**3C: Architecture Analysis (understand structure)**
```bash
# Read project structure
Glob: top-level directories

# Read architecture docs if they exist
Read: ARCHITECTURE.md or README.md

# Analyze import patterns in main entry points
Read: src/main.py or index.js or app.py
```

**3D: Pattern Matching (find where similar code lives)**
```bash
# Find files with similar patterns
Grep: 'class.*Service|def.*handler|function.*Controller' to list files

# Analyze directory structure for conventions
Bash: tree -L 3 -d src/ (if available)
```

**Decision Matrix for Implementation Location:**

| Scenario | Discovery Method | Target Location |
|----------|-----------------|-----------------|
| PR/branch exists with changes | Git diff → analyze modified files | Add to existing modified files |
| Similar feature exists | Semantic search → find related code | Add alongside similar functionality |
| New feature area | Architecture analysis → understand structure | Create new file following project conventions |
| Service/API expansion | Pattern matching → find service/controller files | Extend existing service/controller |
| Utility function needed | Search for utils/helpers | Add to appropriate utility module |

**Output from this phase:**
```
IMPLEMENTATION LOCATIONS:
Existing files to modify:
- src/services/user_service.py (add new method at line 145, after get_user())
- src/api/routes/user_routes.py (add new endpoint, follow pattern from line 67)

New files to create:
- src/validators/user_validator.py (follow validator pattern from auth_validator.py)

Test files:
- tests/services/test_user_service.py (add test class)
- tests/api/test_user_routes.py (add endpoint tests)

REASONING:
- User service already handles user operations (lines 50-200)
- API routes follow RESTful pattern seen in existing endpoints
- Validators are separate files per domain (auth, product, user)
- Tests mirror source structure (tests/ matches src/)
```

### Phase 4: Implementation Plan Creation

Synthesize documentation requirements + code analysis into executable plan.

**Plan Structure:**

```markdown
# Implementation Plan: <Feature Name>

## Summary
<2-3 sentence overview of what will be implemented>

## Requirements (from documentation)
### Critical (MUST have)
1. Requirement A (source: docs.md section 3.2)
2. Requirement B (source: API spec, endpoint /resource)

### Important (SHOULD have)
1. Requirement C (source: docs.md section 4.1)

### Optional (MAY have)
1. Requirement D (source: docs.md section 5.3)

## Code Changes

### File 1: src/services/user_service.py
**Location:** After line 145, inside UserService class
**Change:** Add method `calculate_engagement_score(user_id: str) -> float`
**Reasoning:** Existing user operations live here, follows service pattern

**Implementation details:**
- Input validation: user_id must be valid UUID (per docs section 2.3)
- Calculation: sum of (posts * 2) + (comments * 1) + (likes * 0.5) (per docs algorithm)
- Error handling: raise UserNotFoundError if invalid (matches line 78 pattern)
- Return: float between 0.0-100.0 (per docs spec)

### File 2: tests/services/test_user_service.py
**Location:** New test class at end of file
**Change:** Add TestEngagementScore class
**Reasoning:** Tests follow one class per service method pattern (see line 45)

**Test coverage:**
- Valid user with activity
- Valid user with no activity (edge case)
- Invalid user_id (error case)
- Boundary testing (0 score, max score)

## Dependencies
- No new dependencies required
- Uses existing database connection from UserService base class

## Assumptions (documentation gaps)
1. **Engagement score calculation for users with zero activity**
   - Documentation silent on this edge case
   - ASSUMPTION: Return 0.0 (matches principle of "no activity = no engagement")

2. **Caching strategy**
   - Documentation mentions "efficient retrieval" but no cache spec
   - ASSUMPTION: No caching in first implementation (can add if performance issues)

3. **Score update frequency**
   - No mention of real-time vs batch calculation
   - ASSUMPTION: On-demand calculation (called when needed)

## Edge Cases Handled
1. User with massive activity (prevent overflow) → cap at 100.0
2. Deleted user → raise UserNotFoundError
3. Database connection failure → propagate exception (matches service pattern)
4. Negative activity counts (data corruption) → treat as 0

## Validation Steps
After implementation:
- [ ] Run test suite: `pytest tests/services/test_user_service.py -v`
- [ ] Lint check: `pylint src/services/user_service.py`
- [ ] Type check: `mypy src/services/user_service.py`
- [ ] Manual test: Call endpoint with test user (user_id: test-123)

## Risks & Mitigations
| Risk | Mitigation |
|------|-----------|
| Performance with large datasets | Assumption: Optimize later if needed; add TODO comment |
| Score formula may change | Formula isolated in method, easy to update |
| Inconsistent with existing score calculation | Verified no other score calculations exist in codebase |

---
**Estimated changes:** ~50 lines code, ~80 lines tests
**Estimated time:** 30-45 minutes
**Confidence level:** High (95%) - clear requirements, existing patterns identified
```

**Plan Review Checklist (internal validation before presenting):**
- [ ] All documentation requirements mapped to code changes
- [ ] Implementation locations identified with line numbers
- [ ] Existing code patterns analyzed and matched
- [ ] Assumptions explicitly documented
- [ ] Edge cases identified
- [ ] Testing strategy defined
- [ ] Validation steps concrete and runnable

### Phase 5: User Approval Gate

**Present plan to user:**

```
I've analyzed the documentation and codebase. Here's the implementation plan:

[Present plan from Phase 4]

**Questions before I proceed:**
1. Do these assumptions align with your expectations?
2. Should I prioritize any optional requirements?
3. Any additional edge cases I should handle?

Type 'approved' to proceed with implementation, or provide feedback to refine the plan.
```

**DO NOT PROCEED TO CODING UNTIL USER APPROVES OR PROVIDES REFINEMENT**

### Phase 6: Precision Implementation

Once approved, execute the plan with surgical precision.

**Implementation Protocol:**

**6A: Pre-implementation Setup**
```bash
# Ensure clean working state
Bash: git status

# Create feature branch if needed (ask user first)
# git checkout -b feature/<feature-name>
```

**6B: File-by-File Implementation**

For each file in the plan:

1. **Read current file content**
   ```bash
   Read: src/services/user_service.py
   ```

2. **Implement using Edit tool** (exact, minimal diffs)
   ```bash
   Edit tool with:
     - file_path: exact path
     - old_string: exact existing code
     - new_string: exact new code
   ```

3. **Verify change**
   ```bash
   # Show diff
   Bash: git diff src/services/user_service.py

   # Verify syntax (language-dependent)
   Bash: python -m py_compile src/services/user_service.py
   # or: node --check src/services/user_service.js
   ```

**Code Quality Standards (match existing patterns):**
- Indentation: Extract from existing file (spaces/tabs, width)
- Naming: Match existing conventions (camelCase, snake_case, etc.)
- Imports: Follow existing order (stdlib, third-party, local)
- Type hints: Use if project uses them (check existing functions)
- Docstrings: Match existing format (Google, NumPy, plain)
- Error handling: Use same exception types and patterns
- Logging: Use existing logger if present

**6C: Test Implementation**

```bash
# Create/modify test files
Edit tool to add test classes/functions following existing test patterns
```

**Test Requirements:**
- Cover all requirements from documentation
- Test happy path + edge cases from plan
- Match existing test style (unittest, pytest, assertions)
- Use existing test fixtures/mocks if available

**6D: Validation Execution**

Run all validation steps from plan:
```bash
# Run tests
Bash: pytest tests/services/test_user_service.py -v

# Lint
Bash: pylint src/services/user_service.py

# Type check
Bash: mypy src/services/user_service.py

# Full test suite (if fast)
Bash: pytest tests/ -x  # stop on first failure
```

**If validation fails:**
- Show exact error
- Fix issue
- Re-run validation
- Do NOT proceed until all validations pass

### Phase 7: Implementation Report

**Present final results:**

```markdown
# Implementation Complete: <Feature Name>

## Changes Summary
Files modified: 3
- src/services/user_service.py (+45 lines)
- tests/services/test_user_service.py (+78 lines)
- src/api/routes/user_routes.py (+23 lines)

## Validation Results
✅ All tests pass (12 new tests, 0 failures)
✅ Linter pass (no new issues)
✅ Type checker pass
✅ Manual verification: Endpoint responds correctly

## Diff Overview
[Show concise git diff or file-by-file summary]

## Documentation Alignment
Requirements implemented:
- ✅ Engagement score calculation (docs section 3.2)
- ✅ User validation (docs section 2.3)
- ✅ Error handling (docs section 6.1)
- ✅ Response format (docs API spec)

Assumptions applied:
- Zero-activity users return 0.0 score
- No caching (can be added later)
- On-demand calculation

## Next Steps (optional)
- Consider adding caching if performance becomes an issue
- Monitor engagement score distribution in production
- Update documentation to reflect new endpoint
```

## Speed Optimizations

**Token Management:**
- Skim docs first (headers only) → 100-500 tokens
- Deep dive only relevant sections → 2K-5K tokens per section
- Cache extracted requirements (don't re-read docs)
- Use git diff over full file reads when possible
- Parallel tool calls for independent tasks (read multiple docs simultaneously)

**Execution Efficiency:**
- Skip git diff if no PR/branch context (saves 5-10 seconds)
- Use semantic search before reading files (targeted discovery)
- Read only files you'll modify + 1-2 pattern examples (not entire codebase)
- Create implementation plan before reading all code (prevents over-analysis)

## Error Handling & Recovery

| Error Scenario | Recovery Strategy |
|----------------|-------------------|
| Documentation URL unreachable | Ask user for local copy or alternative source |
| PDF parsing fails | Request markdown conversion or extract manually |
| No similar code found | Use language best practices, document as assumption |
| Conflicting patterns in codebase | Follow most recent pattern (git log), document choice |
| Documentation contradicts codebase | Present conflict to user, ask for guidance |
| Validation fails after implementation | Show error, fix, re-validate (max 3 attempts before asking user) |
| User rejects plan | Refine based on feedback, present revised plan |

## Anti-Patterns (DO NOT DO)

❌ **Start coding before plan approval**
❌ **Read entire documentation without skimming first** (token waste)
❌ **Modify files not in the plan** (scope creep)
❌ **Introduce new dependencies without documenting** (assumption gap)
❌ **Skip validation steps** (quality compromise)
❌ **Refactor existing code unnecessarily** (increases diff size)
❌ **Copy documentation verbatim into code comments** (redundant)
❌ **Ignore edge cases mentioned in documentation** (incomplete implementation)

## Integration with Other Skills

Chain with:
- **log-analysis**: Analyze test failures during validation
- **pr-description**: Generate PR description from implementation plan
- **api-documentation**: Update API docs after implementation
- **code-review**: Self-review before presenting to user

---

**THE WHY**

This skill treats documentation as the source of truth and existing code as the implementation guide. The hybrid extraction (skim → deep dive) prevents token waste while ensuring critical details aren't missed. The approval gate exists because documentation-driven implementations often have multiple valid interpretations, and user confirmation eliminates costly rework. The intelligent discovery (git diff + semantic search + architecture analysis) handles the reality that users rarely specify exact file locations, making autonomous location discovery essential for practical use.
