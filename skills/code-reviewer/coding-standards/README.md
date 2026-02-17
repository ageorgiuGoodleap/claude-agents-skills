# Coding Standards Skill

A comprehensive Claude Skill that enforces clean code principles, language-specific best practices, security baseline, and minimal-change workflow for all code-related tasks.

## What This Skill Does

This skill automatically activates when you're working on code-related tasks and ensures:

1. **Clean Code Principles**: Enforces 5 non-negotiable principles for writing maintainable, readable code
2. **Structured Workflow**: Forces clarity before coding, implements in minimal increments, verifies quality gates, and requires structured reporting
3. **Language-Specific Standards**: Comprehensive best practices for Python and TypeScript
4. **Security Baseline**: OWASP secure coding practices baked into every code change
5. **Architecture Guidance**: Design patterns and decision rules to prevent over-engineering

## When This Skill Activates

The skill automatically triggers when you use code-related verbs:
- Write, implement, fix, update, improve, refactor, debug
- Create, build, develop, modify code

**Examples:**
- "Write a function to parse JSON data"
- "Fix this bug in the authentication module"
- "Implement a new API endpoint for user registration"
- "Refactor this class to use dependency injection"

## Structure

```
coding-standards/
├── SKILL.md                              # Core principles and workflow (231 lines)
└── references/                           # Detailed standards (loaded on-demand)
    ├── python-standards.md               # Complete Python best practices
    ├── typescript-standards.md           # Complete TypeScript best practices
    ├── security-baseline.md              # OWASP secure coding checklist
    ├── design-patterns.md                # Architecture patterns and decision rules
    └── code-change-protocol.md           # Paste-ready AI coding protocol
```

## Key Features

### Core Non-Negotiable Principles

1. **Optimize for the Next Reader**: Code is communication first - prefer boring, explicit solutions
2. **Keep Scope Tight**: Minimal blast radius - implement ONLY what was requested
3. **Make Correct Path Obvious**: Strong types, fail fast, validate early
4. **Maintainability Beats Optimization**: Optimize only after measuring
5. **Small Units with Single Purpose**: Each function/module does one thing

### Workflow Protocol

**Step 1: Force Clarity Before Writing Code**
- Produce implementation plan with what's changing, non-goals, acceptance criteria, files to touch, risks

**Step 2: Implement in Smallest Safe Increments**
- One logical change set, minimal diffs, follow existing conventions

**Step 3: Always Verify (Quality Gates)**
- Python: PEP 8/257, type hints, ruff, mypy, pytest
- TypeScript: strict mode, ESLint, Prettier, tsc, Vitest/Jest

**Step 4: Report Exactly What Changed**
- Summary, files changed, behavior impact, tests run, optional improvements (requires approval)

### Optional Improvements Gate

The skill prevents scope creep by requiring explicit approval for any improvements not directly requested. This ensures:
- Minimal, focused changes
- Reviewable diffs
- No surprise refactors or drive-by improvements

## Benefits

✅ **Prevents Messy Code**: Forces implementation plan before coding
✅ **Scope Control**: No unrelated refactors or feature creep
✅ **Quality Assurance**: Comprehensive verification gates
✅ **Security by Default**: OWASP baseline enforced on every change
✅ **Minimal Diffs**: Touch only what's necessary
✅ **Reviewable Changes**: Structured reporting makes code reviews easier
✅ **Language Best Practices**: Comprehensive standards for Python and TypeScript

## What Makes This Skill Effective

### Concise Core + Detailed References
- **SKILL.md**: Under 300 lines, contains core principles and workflow
- **references/**: Detailed standards (500+ lines total) loaded on-demand
- Optimizes context window usage through progressive disclosure

### Non-Negotiable Enforcement
- Principles are mandatory, not suggestions
- Quality gates must be verified before delivery
- Optional improvements require explicit approval

### Real-World Focus
- Based on proven clean code practices
- Includes security baseline (OWASP)
- Covers common languages (Python, TypeScript)
- Addresses scope creep with concrete safeguards

## Example Usage

**Without the skill:**
```
User: "Add email validation to user registration"
Claude: [Makes changes, adds email validation, refactors related code,
        updates tests, changes error handling approach, adds logging,
        formats entire file]
```

**With the skill:**
```
User: "Add email validation to user registration"
Claude:
1. Implementation Plan:
   - In scope: Add email regex validation to create_user function
   - Not in scope: Changing existing users, modifying login flow
   - Files: src/users/registration.py, tests/users/test_registration.py

2. [Makes minimal changes - only email validation]

3. Verification:
   - Ran: pytest tests/users/test_registration.py -v (all passed)
   - Ran: ruff check src/users/ (no issues)
   - Ran: mypy src/users/registration.py (no type errors)

4. SUMMARY: Added email format validation. Invalid emails raise ValueError.
   FILES CHANGED: registration.py (validation), test_registration.py (2 tests)
   BEHAVIOR IMPACT: Function now validates email format

5. OPTIONAL IMPROVEMENTS (not implemented):
   - Add domain-specific validation (block disposable emails)
   - Should I implement this?
```

## Success Criteria

The skill is successful if:
- ✅ SKILL.md is under 300 lines (actual: 231 lines)
- ✅ Description triggers on all code-related verbs
- ✅ References contain comprehensive standards without cluttering SKILL.md
- ✅ Enforces minimal-change workflow and quality gates
- ✅ Requires structured reporting with optional improvements gate
- ✅ Validates and packages successfully

## Installation

### For Claude UI (claude.ai)
1. Download `coding-standards.skill` from `skills/zips/`
2. Navigate to Skills section in Claude UI
3. Click "Upload Skill"
4. Select the .skill file

### For Claude Code
1. Copy the skill package to your Claude Code skills directory
2. The skill will be available in your next session

## Version

**Version**: 1.0.0
**Last Updated**: 2026-02-04

## License

This skill is provided as-is for use with Claude AI.
