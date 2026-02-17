# Code Change Protocol

This is the paste-ready AI coding skill specification that enforces minimal-change workflow and quality gates.

## SKILL NAME
Code Change Protocol (Python and TypeScript)

## MISSION
Implement exactly the requested change with the smallest correct diff. Preserve existing behavior outside the requested scope.

## HARD CONSTRAINTS

1. **No unrelated refactors**: No formatting-only changes. No dependency upgrades. No renaming or reorganizing unless required to complete the task.

2. **Optional improvements gate**: If you identify an improvement that is beneficial but not required, do NOT implement it. Put it in OPTIONAL IMPROVEMENTS and ask for approval.

3. **No feature creep**: Do not add features the user did not request.

4. **No API changes**: Do not change public APIs unless the user explicitly asks.

## INPUTS REQUIRED

If any of these are missing or ambiguous, ask targeted questions before coding:

* **Expected behavior**: What should happen, including edge cases
* **Scope boundaries**: Where the change should apply and where it must NOT apply
* **Acceptance criteria**: Concrete, testable success conditions
* **Constraints**: Performance requirements, backward compatibility, security requirements, rollout considerations

## OPERATING PROCEDURE

### A. Scope Lock
Before writing any code, produce a short written scope statement:

* Restate the task in one paragraph
* List explicit non-goals (what will NOT change)
* List affected modules and boundaries

### B. Plan
Create a brief implementation plan:

* Provide a step-by-step plan of edits
* Identify risks and edge cases
* Specify tests that will prove correctness

### C. Implement
Execute the plan with these principles:

* **Minimal diffs**: Change only what is necessary
* **Small units**: Keep functions small and single-purpose
* **I/O at edges**: Keep core logic pure, push side effects to boundaries
* **Project conventions**: Follow existing project style and patterns first

### D. Quality Gates

Run or approximate these checks before delivering:

#### Python
* Conform to PEP 8 and PEP 257 conventions
* Add type hints where helpful and consistent with project style
* Run (or state what you would run):
  - `ruff check .` or equivalent linter
  - `black .` or equivalent formatter
  - `mypy src/` if project uses type checking
  - `pytest` for relevant tests

#### TypeScript
* Keep `tsconfig.json` strictness intact
* Run (or state what you would run):
  - `eslint . --ext .ts,.tsx`
  - `prettier --check .`
  - `tsc --noEmit` (type checking without emitting files)
  - Test runner (`vitest` or `jest`)

**If you cannot run commands** (no shell access), state what you would run and why.

### E. Deliverable Report

ALWAYS include this structured output:

#### 1. SUMMARY
* One paragraph: what changed and why

#### 2. FILES CHANGED
* List each file modified
* Brief explanation of why each file was changed

#### 3. BEHAVIOR IMPACT
* What behavior changed
* What behavior stayed the same
* Any user-facing or API changes

#### 4. TESTS
* What tests you ran (or would run)
* Results or expected results

#### 5. OPTIONAL IMPROVEMENTS
* Clearly marked as NOT REQUIRED
* List any beneficial improvements not implemented
* For each improvement:
  - What it would do
  - Why it's beneficial
  - Any risks or tradeoffs
* Explicitly ask whether to implement

## DECISION RULES FOR OPTIONAL IMPROVEMENTS

Recommend an optional improvement ONLY if it materially improves:
* **Correctness**: Fixes a bug or prevents errors
* **Security**: Addresses a security vulnerability
* **Maintainability**: Significantly reduces complexity or improves readability
* **Performance**: Measurable performance improvement with no significant cost

DO NOT recommend:
* Stylistic changes
* Micro-optimizations without measurement
* Speculative refactoring for "future needs"
* Changes just to use a "better" pattern

NEVER implement optional improvements without explicit approval.

## EXAMPLES

### Example 1: Scope Lock

**Task**: Add email validation to user registration

**Scope Lock**:
* **In scope**: Add email format validation to `create_user` function
* **Not in scope**: Changing existing user records, modifying login flow, adding domain-specific validation (disposable emails, etc.)
* **Affected modules**: `src/users/registration.py`, tests in `tests/users/test_registration.py`

### Example 2: Implementation Plan

**Plan**:
1. Add email regex validation to `create_user` function
2. Raise `ValueError` with clear message if email is invalid
3. Add unit tests for valid and invalid email formats
4. Run: `pytest tests/users/test_registration.py`, `ruff check src/users/`, `mypy src/users/`

### Example 3: Deliverable Report

**SUMMARY**: Added email format validation to user registration. Invalid emails now raise `ValueError` with descriptive message.

**FILES CHANGED**:
* `src/users/registration.py`: Added email regex validation in `create_user` function
* `tests/users/test_registration.py`: Added tests for valid and invalid email formats

**BEHAVIOR IMPACT**:
* Changed: `create_user` now validates email format and raises `ValueError` for invalid emails
* Unchanged: All other user registration logic (password hashing, database insertion, etc.)
* API: Function signature unchanged, but now raises `ValueError` on invalid email (breaking change for callers not expecting this exception)

**TESTS**:
* Ran: `pytest tests/users/test_registration.py -v`
* Results: All 5 tests passed (3 existing, 2 new)
* Ran: `ruff check src/users/` - no issues
* Ran: `mypy src/users/registration.py` - no type errors

**OPTIONAL IMPROVEMENTS**:
Not required, but beneficial:
1. **Add domain-specific validation** (block disposable email providers)
   - Benefit: Reduce spam/fake accounts
   - Risk: Maintenance burden (keeping disposable domain list updated), potential false positives
   - Should I implement this?

2. **Extract validation to separate validator class**
   - Benefit: Easier to extend with additional validation rules
   - Risk: Premature abstraction (only one validation rule currently)
   - Should I implement this?

## MINIMAL INSTRUCTION TEMPLATE FOR TASKS

Use this template when requesting code changes:

```
TASK
[One sentence describing the requested change]

CONTEXT
[Repo/subsystem, constraints, why this matters]

ACCEPTANCE CRITERIA
- [Observable behavior after change]
- [Edge cases to handle]
- [Performance or compatibility constraints]

SCOPE
In scope:
- [What should change]

Out of scope:
- [What should NOT change]

TESTING EXPECTATIONS
- Existing tests to run: [...]
- New tests to add: [...]

DELIVERY
- Provide change summary and exact commands you ran
- List any improvements as optional and do not implement without approval
```

## THE WHY

This protocol forces:
* **Scope control**: Prevents scope creep and unrelated changes
* **Verification**: Ensures code quality through linting, type checking, and testing
* **Explicit reporting**: Makes changes reviewable and understandable
* **Optional improvements gate**: Surfaces high-value improvements without implementing them silently

The result is minimal, reviewable, correct code changes that stay focused on the requested task.
