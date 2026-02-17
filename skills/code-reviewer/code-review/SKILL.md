---
name: code-review
description: |
  Analyze pull requests, commits, and code changes to produce comprehensive CODE_REVIEW.md reports.
  Use when the user asks to review code, analyze diffs, validate PRs, check correctness/security/performance,
  assess impact/blast radius, or mentions reviewing branches, commits, or code changes. Produces structured
  reviews with risk assessment, correctness validation, security analysis, and actionable feedback.
---

# Code Review Skill

Comprehensive code review capability that analyzes pull requests and code changes, producing structured `CODE_REVIEW.md` reports with correctness validation, impact analysis, security checks, and actionable feedback prioritized by severity.

## When to Use This Skill

Trigger this skill when the user:
- Asks to review a PR, commit, or code change
- Mentions code review, diff analysis, or change validation
- Wants to check correctness, security, or performance of changes
- Needs impact analysis or blast radius assessment
- Requests review of test coverage or quality
- Mentions reviewing a specific branch or commit SHA
- Asks "is this code correct/safe/good"

## Core Workflow

### Step 1: Gather Context

Before analyzing, collect necessary information:

1. **Get the changes**:
   - For PRs: `gh pr diff <pr-number>` or `gh pr view <pr-number> --json files`
   - For commits: `git show <commit-sha>` or `git diff <base>..<head>`
   - For branches: `git diff <base-branch>...<feature-branch>`
   - For staged changes: `git diff --staged`

2. **Get additional context**:
   - PR description: `gh pr view <pr-number>`
   - Commit messages: `git log <base>..<head>`
   - Linked issues: Check PR description for issue references
   - Recent history: `git log --oneline -10`

3. **Understand the codebase**:
   - Read changed files completely (not just diffs)
   - Understand the surrounding context
   - Identify dependencies and call sites

### Step 2: Comprehensive Analysis

Perform analysis in this order (see [ANALYSIS_GUIDE.md](references/ANALYSIS_GUIDE.md) for details):

1. **Change Comprehension**
   - Parse structural diffs (added/removed/modified lines)
   - Classify change intent (bug fix, feature, refactor, etc.)
   - Assess reviewability (size, logical grouping)
   - Detect scope creep (unrelated changes)

2. **Impact Analysis**
   - API surface changes (breaking changes, deprecations)
   - Call graph impact (affected callers, new dependencies)
   - Data flow changes (inputs, transformations, persistence)
   - Behavioral changes (invariants, edge cases, concurrency)
   - Compatibility (backward compatibility, migrations)
   - Operational impact (logging, metrics, performance, cost)
   - Security impact (trust boundaries, input validation)

3. **Correctness Review**
   - Business logic validation
   - Invariant preservation
   - Error handling completeness
   - Edge case coverage

4. **Code Quality Assessment**
   - Complexity (cyclomatic complexity, nesting depth)
   - Readability (naming, local reasoning, duplication)
   - Consistency with existing patterns

5. **Test Review**
   - Coverage of new functionality
   - Quality of test code
   - Regression test adequacy
   - Boundary testing

6. **Security Review**
   - Input validation at boundaries
   - Authentication and authorization
   - Secrets handling
   - Common vulnerability patterns (see [SECURITY_PATTERNS.md](references/SECURITY_PATTERNS.md))

7. **Performance Review**
   - Algorithmic complexity changes
   - N+1 query patterns
   - Caching correctness
   - Resource allocation

8. **Flow Analysis**
   - Control flow changes
   - State machine completeness
   - Concurrency safety
   - Error propagation
   - Resource lifecycle

### Step 3: Generate CODE_REVIEW.md

Create a comprehensive report following this structure (see template below). Always save to current directory unless user specifies otherwise.

**Key Requirements**:
- Read EVERY changed line in execution order
- Follow call chains through changes
- Trace data flow through transformations
- Prioritize feedback: Blockers → Should-fix → Nits
- Provide concrete alternatives with code examples
- Focus on substance, not style already enforced by linters

## CODE_REVIEW.md Template

```markdown
# Code Review Report

**Review Date**: [timestamp]
**PR/Branch**: [identifier]
**Files Changed**: [count] (+[lines added] -[lines removed])
**Overall Risk**: Critical / High / Medium / Low

## Change Summary

[2-3 paragraph summary]
- What changed (components, modules, functionality)
- Why the change was made (requirements, bug fix, refactor)
- Scope assessment (focused or sprawling)

## Change Classification

- **Intent**: Bug fix / Feature / Refactor / Performance / Security / Test / Config
- **Reviewability**: Small / Medium / Large / Too Large
- **Scope Creep**: None / Minor / Significant

## Impact Analysis

### API Surface Impact
[Breaking changes, deprecations, new public methods]

### Call Graph Impact
**Callers Affected**: [count]
- [function/method]: [impact description]

**New Dependencies Introduced**:
- [dependency]: [reason and risk]

### Data Flow Impact
**New Inputs**: [validation status]
**Persistence Changes**: [schema, data format]
**External Systems**: [APIs, databases affected]

### Behavioral Changes
**Invariants Changed**: [list with old vs new]
**Edge Cases**: [newly handled or introduced]
**Concurrency**: [thread safety, race conditions]

### Compatibility Impact
**Backward Compatibility**: Maintained / Broken
**Migration Required**: Yes / No
**Versioning**: [strategy]

### Operational Impact
**Logging**: [volume change, new statements]
**Metrics**: [new metrics, cardinality]
**Performance**: [latency, throughput impact]
**Cost**: [infrastructure, API calls]

### Security Impact
**Trust Boundaries**: [authentication, authorization]
**Input Validation**: [status at boundaries]
**Sensitive Data**: [handling, exposure risk]
**Vulnerability Risk**: [patterns identified]

## Risk Assessment

### Critical Risks (Blockers)
1. **[Risk Category]** - [Severity: Critical]
   - **Location**: `file.ts:line`
   - **Issue**: [Specific problem]
   - **Impact**: [What breaks or fails]
   - **Fix**: [Concrete solution with code example]

### High Priority (Should Fix Before Merge)
[Same structure]

### Medium Priority (Improvements)
[Same structure]

### Low Priority (Nits)
[Same structure]

## Correctness Review

### Business Logic
- **Requirement Alignment**: [Does code match requirements]
- **Edge Cases**: [Handled comprehensively]
- **Invariants**: [Preserved correctly]
- **Error Paths**: [Complete and observable]

### Implementation Quality
- **Complexity**: [Appropriate for task]
- **Readability**: [Code clarity]
- **Coupling**: [Dependencies reasonable]
- **Naming**: [Intent-revealing]

## Test Review

### Coverage Assessment
- **New Functionality**: Covered / Partially / Not Covered
- **Regression Tests**: Present / Missing
- **Edge Cases**: Covered / Partially / Not Covered
- **Error Paths**: Covered / Partially / Not Covered

### Test Quality
| Test File | Coverage | Quality | Issues |
|-----------|----------|---------|--------|
| [file] | [%] | Good/Fair/Poor | [issues] |

### Specific Test Issues
1. [Test name]: [Issue and suggested fix]

## Flow Analysis

### Control Flow Changes
- [New branches, early returns, exception paths]

### State Machine Changes
- [New states, transitions, completeness]

### Concurrency Changes
- [Thread safety, async boundaries, races]

### Error Handling
- [Consistency, propagation, visibility]

### Resource Lifecycle
- [Acquisition, release, cleanup, leaks]

## Security Review

### Input Validation: Pass / Fail
[Details on boundary validation]

### Authentication/Authorization: Pass / Fail
[Details on access control]

### Secrets Handling: Pass / Fail
[Details on credential management]

### Vulnerability Patterns
- **SQL Injection**: Clear / At Risk
- **XSS**: Clear / At Risk
- **Path Traversal**: Clear / At Risk
- **SSRF**: Clear / At Risk
[Details and locations]

## Performance Review

### Algorithmic Complexity
- [O-notation changes and hot path impact]

### N+1 Patterns
- [Database/network calls in loops]

### Caching
- [Correctness of keying, invalidation, TTL]

### Resource Usage
- [Memory, I/O, connection patterns]

## Maintainability Assessment

### Extensibility: Good / Fair / Poor
[Can future requirements be accommodated]

### Observability: Good / Fair / Poor
[Metrics, logs, traces quality]

### Documentation: Good / Fair / Poor
[Comments, API docs, migration guides]

## Recommendations

### Required Actions (Blockers)
1. [Specific action with file:line reference]
2. [Specific action with code example]

### Strongly Recommended (Before Merge)
1. [Specific improvement]
2. [Specific improvement]

### Suggested Improvements (Can Address Later)
1. [Enhancement opportunity]
2. [Refactoring suggestion]

### Follow-up Items
1. [Technical debt to track]
2. [Future refactoring opportunities]

## Validation Plan

### Local Testing
- [How to test these changes locally]
- [Specific scenarios to exercise]

### Production Monitoring
- **Metrics to Watch**: [list]
- **Logs to Check**: [patterns]
- **Alerts to Configure**: [suggestions]

### Rollback Plan
- [How to safely revert if issues arise]

## Summary

**Approval Status**: Approved / Approved with Comments / Changes Requested / Blocked

**Key Strengths**:
- [What was done well]

**Key Concerns**:
- [What needs attention]

**Confidence Level**: High / Medium / Low
[Rationale for confidence assessment]
```

## Analysis Best Practices

### Read Code Completely
- Never comment on code you haven't read in full
- Understand context beyond just the diff
- Follow execution flow, not file order
- Trace data through transformations

### Prioritize Feedback
1. **Blockers** (Must fix):
   - Correctness bugs
   - Security vulnerabilities
   - Data loss risks
   - Breaking changes without migration path

2. **Should-fix** (Before merge):
   - Significant complexity issues
   - Missing test coverage
   - Poor abstractions that will cause maintenance burden
   - Performance problems on hot paths

3. **Nits** (Nice to have):
   - Minor naming improvements
   - Small refactoring opportunities
   - Style preferences (only if not enforced by tools)

### Provide Concrete Solutions
- Don't just complain, suggest fixes
- Show example code for recommendations
- Explain tradeoffs of alternatives
- Reference specific line numbers

### Avoid Common Pitfalls
- Don't re-litigate style enforced by linters/formatters
- Don't bikeshed on subjective preferences
- Don't comment on generated code
- Don't nitpick trivial changes
- Focus on substance: correctness, clarity, maintainability

## Edge Cases

### Empty or Trivial Changes
State clearly that the change is trivial and skip detailed analysis sections.

### Generated Code
Identify auto-generated files (package-lock.json, dist/, *.min.js, etc.) and skip detailed review. Note them in Change Summary.

### Large Changes (>1000 lines)
Flag as "Too Large" in reviewability assessment. Recommend splitting into focused PRs.

### Multiple Unrelated Changes
Flag as "Significant" scope creep. List the different change categories and recommend splitting.

### Missing PR Description
Note lack of context in Change Summary. Request clarification on intent and requirements.

### Test-Only Changes
Focus review on:
- Test quality and determinism
- Coverage improvements
- Test code clarity
- Whether tests would catch real bugs

### Configuration-Only Changes
Focus review on:
- Operational impact
- Rollback plan
- Documentation
- Blast radius

### Dependency Updates
Focus review on:
- Security advisories addressed
- Breaking changes in dependencies
- Compatibility with existing code
- Lock file changes

## Additional Resources

For detailed guidance on specific aspects:
- **[ANALYSIS_GUIDE.md](references/ANALYSIS_GUIDE.md)** - Comprehensive analysis methodology
- **[SECURITY_PATTERNS.md](references/SECURITY_PATTERNS.md)** - Common vulnerability patterns to check

## Success Criteria

A complete code review includes:
- ✓ Structural diff parsed with change classification
- ✓ Impact analysis covering all dimensions
- ✓ Correctness validation of business logic
- ✓ Security review with vulnerability checks
- ✓ Performance analysis with complexity assessment
- ✓ Test coverage and quality evaluation
- ✓ Prioritized feedback (blockers, should-fix, nits)
- ✓ Concrete suggested fixes with code examples
- ✓ Validation plan for testing and monitoring
- ✓ Clear approval status with rationale
