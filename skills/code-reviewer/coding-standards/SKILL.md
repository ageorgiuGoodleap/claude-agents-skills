---
name: coding-standards
description: |
  Enforces clean code principles, language-specific best practices (Python/TypeScript),
  security baseline, and minimal-change workflow for all code-related tasks.
  Use when writing, implementing, fixing, updating, improving, refactoring, debugging,
  creating, building, developing, or modifying code in any programming language, with
  specialized support for Python and TypeScript.
---

# Coding Standards Skill

This skill enforces clean code principles, best practices, and a minimal-change workflow for all code-related tasks. It ensures code quality through non-negotiable principles, structured workflow, and comprehensive quality gates.

## Core Non-Negotiable Principles

### 1. Optimize for the Next Reader
* Code is a communication medium first
* Prefer boring, explicit solutions over clever ones
* If a construct needs a comment to explain what it does, rewrite it so the code explains itself
* Use meaningful names that reveal intent
* Make the code read like prose

### 2. Keep Scope Tight (Minimal Blast Radius)
* Implement ONLY what was requested
* No refactors, no drive-by improvements, no dependency swaps, no formatting of unrelated code
* Touch the fewest files and lines that correctly solve the problem
* Minimize blast radius - if something breaks, it should be obvious where

### 3. Make the Correct Path Obvious and the Wrong Path Hard
* Clear inputs and outputs with strong types at boundaries
* Validate external data early and fail fast with actionable errors
* Do not silently ignore failures
* Use the type system to prevent illegal states

### 4. Maintainability Beats Micro-Optimization
* Optimize only after measuring and only where it matters
* Prefer simple data structures and straightforward control flow
* Avoid premature abstraction
* Keep it simple until complexity is proven necessary

### 5. Small Units with Single Purpose
* Functions and modules should do one thing
* Each unit should have a tight, testable contract
* If a function name contains "and", it likely does too much
* Use composition over inheritance unless inheritance truly models the domain

## Workflow Protocol That Prevents Messy Code

### Step 1: Force Clarity Before Writing Code
Before making any code changes, produce a short **implementation plan**:

* **What is changing**: Specific functions, classes, modules to be modified
* **What is NOT changing**: Explicit non-goals to prevent scope creep
* **Acceptance criteria**: Concrete, testable conditions for success
* **Files to touch**: List of files likely to be modified
* **Risks and edge cases**: What could go wrong, what needs special handling

**If any of these are ambiguous, STOP and ask targeted questions.**

### Step 2: Implement in the Smallest Safe Increments
* Make one logical change set that is easy to review
* Keep diffs local and reversible
* Follow existing project conventions and patterns
* Do not mix refactoring with feature changes
* Do not mix formatting changes with logic changes

### Step 3: Always Verify (Quality Gates)
Run minimum verification steps before delivering:

**Python:**
* Conform to PEP 8 and PEP 257 conventions
* Add type hints where helpful and consistent with project style
* Run (or approximate): `ruff check .`, formatting tool, `mypy` (if present), `pytest`

**TypeScript:**
* Keep `tsconfig.json` strictness intact
* Run (or approximate): `eslint`, `prettier`, `tsc --noEmit`, test runner (vitest/jest)

**All languages:**
* Run the closest existing tests
* Add tests for new behavior or bug fixes
* Ensure no regressions in existing functionality

**If you cannot run commands, state what you would run and why.**

### Step 4: Report Exactly What Changed
Your final output MUST always include:

**1. SUMMARY**
* One paragraph describing what changed and why

**2. FILES CHANGED**
* List each file modified with brief explanation

**3. BEHAVIOR IMPACT**
* What behavior changed
* What behavior stayed the same
* Any API or user-facing changes

**4. TESTS**
* What tests you ran (or would run)
* Results or expected results

**5. OPTIONAL IMPROVEMENTS**
* Clearly marked as NOT REQUIRED
* List improvements identified but not implemented
* For each: what it does, benefits, risks
* **Explicitly ask for approval before implementing**

## Verification Gates

### Code Quality Checklist
Before delivering code, verify:

- [ ] Change is minimal and focused on the requested task
- [ ] No unrelated refactoring or formatting changes
- [ ] Code follows existing project conventions
- [ ] Functions are small and single-purpose
- [ ] I/O is at the edges, core logic is pure where possible
- [ ] Type hints/annotations are present at boundaries
- [ ] No obvious security vulnerabilities (see security-baseline.md)
- [ ] Error handling does not leak sensitive information
- [ ] Tests cover new behavior and edge cases
- [ ] Linting passes (or would pass if run)
- [ ] Type checking passes (or would pass if run)
- [ ] All tests pass (or would pass if run)

### Security Baseline Checklist
For every code change:

- [ ] All external inputs validated (type, format, length, range)
- [ ] Outputs encoded for target context (HTML, SQL, URL, etc.)
- [ ] Parameterized queries used (no string concatenation for SQL/commands)
- [ ] No sensitive data in logs (passwords, tokens, PII)
- [ ] Errors handled without leaking internal details
- [ ] Authentication and authorization enforced where applicable
- [ ] Dependencies are up-to-date and audited

## Language-Specific Best Practices

### Python Stack
* **Style**: PEP 8, PEP 257
* **Types**: PEP 484 type hints, mypy for static checking
* **Formatting**: Black or Ruff formatter
* **Linting**: Ruff (replaces Flake8, isort, pyupgrade, etc.)
* **Testing**: pytest
* **Config**: `pyproject.toml` for centralized tool configuration

**See `references/python-standards.md` for detailed practices.**

### TypeScript Stack
* **Compiler**: `strict: true` in `tsconfig.json`
* **Linting**: ESLint with typescript-eslint
* **Formatting**: Prettier
* **Testing**: Vitest (modern) or Jest
* **Types**: Use `unknown` over `any`, discriminated unions for state

**See `references/typescript-standards.md` for detailed practices.**

## Decision Rules for Optional Improvements

Recommend an optional improvement ONLY if it materially improves:
* **Correctness**: Fixes a bug or prevents errors
* **Security**: Addresses a security vulnerability
* **Maintainability**: Significantly reduces complexity
* **Performance**: Measurable improvement with no significant cost

**DO NOT recommend:**
* Stylistic changes
* Micro-optimizations without measurement
* Speculative refactoring for "future needs"
* Changes just to use a "better" pattern

**NEVER implement optional improvements without explicit approval.**

## Architecture and Design Patterns

### When to Add Structure
Add architectural patterns ONLY when:
* You need testability and isolation of side effects
* You expect multiple implementations of a dependency
* You need a stable boundary between domain logic and infrastructure

### Practical Patterns
* **Dependency Injection**: Pass dependencies explicitly
* **Ports and Adapters**: Domain defines interfaces, infrastructure implements
* **Strategy**: Select behavior by injected function/object
* **State Modeling**: Explicit state machines with exhaustive handling

### Architectural Defaults
* **Layered architecture**: Domain → Application → Infrastructure → Presentation
* **Keep domain logic free of frameworks** when feasible
* **Twelve-factor practices** for building services

**See `references/design-patterns.md` for detailed guidance.**

## Security Baseline

Bake security into every line of code:
* Validate input and treat all external data as untrusted
* Use safe output encoding and parameterized queries
* Handle errors without leaking secrets
* Log security-relevant events without logging sensitive data
* Use least privilege for credentials and runtime permissions

**See `references/security-baseline.md` for OWASP checklist.**

## References

Detailed standards are available in the `references/` directory:

* **`python-standards.md`**: Complete Python best practices stack
* **`typescript-standards.md`**: Complete TypeScript best practices stack
* **`security-baseline.md`**: OWASP secure coding practices checklist
* **`design-patterns.md`**: Architecture patterns and decision rules
* **`code-change-protocol.md`**: Paste-ready AI coding protocol

## The Why

This skill forces scope control, verification, and explicit reporting so code changes stay:
* **Minimal**: Touch only what's necessary
* **Reviewable**: Changes are easy to understand and verify
* **Correct**: Quality gates catch errors before delivery
* **Secure**: Security baseline is enforced by default

The optional improvements gate prevents scope creep while surfacing high-leverage fixes.

---

**Always apply these principles. No exceptions.**
