# Code Review Skill

A comprehensive code review skill that analyzes pull requests and code changes to produce detailed, structured review reports with correctness validation, impact analysis, security checks, and actionable feedback.

## Overview

This skill transforms Claude into an expert code reviewer capable of:
- Analyzing pull requests, commits, and code diffs comprehensively
- Identifying correctness issues, security vulnerabilities, and performance problems
- Assessing blast radius and impact across API surface, call graphs, and data flows
- Generating structured CODE_REVIEW.md reports with prioritized feedback
- Providing concrete, actionable recommendations with code examples

## When to Use

Trigger this skill when you need to:
- Review a pull request before merging
- Analyze code changes for correctness and safety
- Assess the impact and blast radius of modifications
- Validate security practices in new code
- Check test coverage and quality
- Get a second pair of eyes on critical changes
- Understand the implications of a code change

## Key Features

### Change-First Comprehension
- Structural diff parsing with context
- Change classification (bug fix, feature, refactor, etc.)
- Scope creep detection (unrelated changes in same PR)
- Requirements alignment validation

### Impact Analysis (Blast Radius)
- **API Surface**: Breaking changes, deprecations, new public methods
- **Call Graph**: Affected callers, new dependencies, circular dependencies
- **Data Flow**: Input validation, transformations, persistence changes
- **Behavioral**: Invariant changes, edge cases, concurrency safety
- **Compatibility**: Backward compatibility, migration requirements
- **Operational**: Logging, metrics, performance, cost implications
- **Security**: Trust boundaries, input validation, vulnerability risks

### Correctness Validation
- Business logic verification against requirements
- Invariant preservation (preconditions, postconditions)
- Edge case coverage
- Error handling completeness
- State machine transition validation

### Security Review
- Input validation at all entry points
- Authentication and authorization checks
- Secrets handling verification
- OWASP Top 10 vulnerability patterns:
  - SQL Injection
  - XSS (Cross-Site Scripting)
  - Command Injection
  - Path Traversal
  - SSRF (Server-Side Request Forgery)
  - Insecure Deserialization
  - Broken Authentication
  - Broken Access Control
  - Security Misconfiguration
  - Insufficient Logging & Monitoring

### Performance Analysis
- Algorithmic complexity changes (Big O analysis)
- N+1 query pattern detection
- Caching correctness (keys, invalidation, TTL)
- Resource allocation and lifecycle management

### Test Assessment
- Coverage of new functionality
- Test quality (determinism, clarity, focus)
- Regression test adequacy
- Boundary and edge case testing

### Flow Analysis
- Control flow changes (branches, early returns, exception paths)
- State machine completeness
- Concurrency safety (race conditions, deadlocks)
- Error propagation consistency
- Resource lifecycle (acquisition, release, cleanup)

## Output

The skill generates a comprehensive `CODE_REVIEW.md` file in the current directory with:

1. **Change Summary**: What changed, why, and scope assessment
2. **Change Classification**: Intent, reviewability, scope creep
3. **Impact Analysis**: Multi-dimensional impact assessment
4. **Risk Assessment**: Prioritized issues (Blockers → Should-fix → Nits)
5. **Correctness Review**: Business logic and implementation quality
6. **Test Review**: Coverage and quality assessment
7. **Flow Analysis**: Control flow, state machines, concurrency
8. **Security Review**: Vulnerability patterns and risk assessment
9. **Performance Review**: Complexity and resource usage
10. **Maintainability Assessment**: Extensibility, observability, documentation
11. **Recommendations**: Prioritized actions with concrete examples
12. **Validation Plan**: Testing, monitoring, and rollback strategies
13. **Summary**: Approval status, strengths, concerns, confidence level

## Skill Structure

```
code-review/
├── SKILL.md                      # Main skill instructions and workflow
├── README.md                     # This file
└── references/
    ├── ANALYSIS_GUIDE.md         # Detailed analysis methodology
    └── SECURITY_PATTERNS.md      # Vulnerability patterns and checks
```

## Usage Examples

### Review a Pull Request
```
Review PR #123 from the my-feature branch
```

### Review Recent Commits
```
Review the last 3 commits on this branch
```

### Review Staged Changes
```
Review my staged changes before I commit
```

### Review Specific Diff
```
Review the changes between main and feature-branch
```

### Security-Focused Review
```
Do a security-focused review of PR #456
```

## Review Philosophy

### Prioritized Feedback
1. **Blockers** (Must fix before merge):
   - Correctness bugs that cause incorrect behavior
   - Security vulnerabilities that expose data or systems
   - Data loss risks
   - Breaking changes without migration path

2. **Should-fix** (Strongly recommended before merge):
   - Significant complexity that will burden maintenance
   - Missing test coverage for new functionality
   - Poor abstractions that couple components tightly
   - Performance issues on hot paths

3. **Nits** (Nice to have):
   - Minor naming improvements
   - Small refactoring opportunities
   - Style preferences (only if not enforced by tools)

### Focus Areas
- **Correctness over style**: Substance matters more than formatting
- **Concrete over abstract**: Provide code examples, not vague suggestions
- **Context-aware**: Consider the codebase, team, and constraints
- **Actionable**: Every piece of feedback includes a clear fix
- **Balanced**: Acknowledge strengths, not just issues

### What We Don't Do
- Re-litigate style enforced by linters/formatters
- Bikeshed on subjective preferences
- Nitpick trivial changes
- Review generated code in detail
- Assume malice or incompetence

## Best Practices

1. **Read code completely**: Understand context beyond just the diff
2. **Follow execution flow**: Trace through call chains and data transformations
3. **Map to requirements**: Ensure implementation matches stated goals
4. **Check all paths**: Verify happy path, error paths, and edge cases
5. **Think about blast radius**: Consider all systems and components affected
6. **Provide examples**: Show concrete code for suggested fixes
7. **Explain tradeoffs**: When suggesting alternatives, explain why

## Reference Materials

### ANALYSIS_GUIDE.md
Detailed methodology covering:
- Structural diff parsing
- Change classification and mapping
- Multi-dimensional impact analysis
- Control flow and state machine analysis
- Code quality metrics
- Test review criteria
- Best practices and anti-patterns

### SECURITY_PATTERNS.md
Comprehensive security patterns covering:
- OWASP Top 10 vulnerability patterns with examples
- Safe and unsafe code patterns
- Secrets management
- Input validation principles
- Cryptography best practices
- Rate limiting strategies
- Security review checklists

## Edge Cases Handled

- **Empty/trivial changes**: Noted clearly, detailed analysis skipped
- **Generated code**: Identified and excluded from detailed review
- **Large changes (>1000 lines)**: Flagged as too large, split recommended
- **Multiple unrelated changes**: Scope creep flagged explicitly
- **Missing PR description**: Lack of context noted, clarification requested
- **Test-only changes**: Focus on test quality and coverage
- **Configuration-only changes**: Focus on operational impact and rollback
- **Dependency updates**: Focus on security and compatibility

## Success Criteria

A complete code review includes:
- ✓ Structural diff parsed with change classification
- ✓ Impact analysis covering all dimensions (API, call graph, data flow, etc.)
- ✓ Correctness validation of business logic and invariants
- ✓ Security review with specific vulnerability checks
- ✓ Performance analysis with complexity assessment
- ✓ Test coverage and quality evaluation
- ✓ Prioritized feedback (blockers → should-fix → nits)
- ✓ Concrete suggested fixes with code examples
- ✓ Validation plan for testing and monitoring
- ✓ Clear approval status with rationale

## Integration with Development Workflow

This skill integrates seamlessly with common development workflows:

1. **Pre-commit reviews**: Review staged changes before committing
2. **Pre-PR reviews**: Self-review before creating pull request
3. **PR reviews**: Comprehensive review as part of PR process
4. **Post-merge audits**: Review merged changes for learning
5. **Security audits**: Focused security review of critical changes
6. **Refactoring validation**: Ensure refactors preserve behavior

## Tips for Best Results

1. **Provide context**: Include PR descriptions, linked issues, or explanations
2. **Be specific**: Point to specific branches, commits, or file paths
3. **State priorities**: Mention if you want focus on security, performance, etc.
4. **Include requirements**: Share what the code is supposed to do
5. **Ask questions**: If you're unsure about an approach, ask during review

## Limitations

- Reviews are based on static analysis of code changes
- Cannot execute code or run tests (but can analyze test coverage)
- Cannot access external systems or databases
- Security review is comprehensive but not a replacement for automated security scanning tools
- Performance analysis is based on code inspection, not profiling

## Version

**Version**: 1.0.0
**Last Updated**: 2026-02-04
