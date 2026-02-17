---
name: code-quality-review
description: |
  Comprehensive code quality analysis for readability, maintainability, and engineering principles.

  WHAT: Reviews code for adherence to SOLID principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion), DRY (Don't Repeat Yourself), KISS (Keep It Simple, Stupid). Identifies code smells (long methods, god objects, feature envy, shotgun surgery, primitive obsession, data clumps). Evaluates naming conventions, code organization, complexity, and maintainability.

  WHEN: Use for pull request reviews, pre-merge quality checks, refactoring analysis, code audits, or when enforcing coding standards. Trigger on: "code review", "review code", "quality check", "code quality", "maintainability review", "readability review", "SOLID principles", "code smells", "refactoring review", "technical debt".
allowed-tools: Read, Grep, Glob
---

# Code Quality Review

## Overview

This skill conducts comprehensive code quality analysis focused on readability, maintainability, and adherence to fundamental software engineering principles (SOLID, DRY, KISS). It identifies code smells, anti-patterns, and opportunities for improvement through systematic examination of code structure, naming conventions, complexity, and design.

## Review Workflow

Follow these steps to conduct a thorough code quality review:

### 1. Analyze Code Structure

- Identify class/function boundaries
- Measure function lengths (flag >50 lines as potential smell)
- Measure class sizes (flag >300 lines as potential god object)
- Check nesting depth (flag >4 levels as complexity smell)

### 2. Evaluate SOLID Principles

Check each principle:

- **Single Responsibility:** Each class/function should have one reason to change
- **Open/Closed:** Open for extension, closed for modification
- **Liskov Substitution:** Derived classes must be substitutable for base classes
- **Interface Segregation:** Many specific interfaces > one general interface
- **Dependency Inversion:** Depend on abstractions, not concretions

### 3. Check for DRY Violations

- Identify duplicated code blocks (>5 lines)
- Find repeated logic patterns
- Detect copy-pasted implementations
- Suggest extraction to functions/classes

### 4. Verify KISS Principle

- Identify over-engineered solutions
- Find unnecessary abstractions
- Detect premature optimization
- Flag overly complex conditionals

### 5. Identify Code Smells

Look for these common smells:

- **Long methods** (>50 lines)
- **God objects** (>300 lines, >10 methods)
- **Feature envy** (method uses other object's data more than its own)
- **Shotgun surgery** (single change requires many small edits)
- **Primitive obsession** (using primitives instead of small objects)
- **Data clumps** (same data items together repeatedly)

### 6. Review Naming Conventions

- Check variable, function, class names for clarity
- Verify consistency with language conventions (snake_case, camelCase)
- Flag abbreviations or unclear names
- Ensure names reveal intent

### 7. Assess Complexity

- Calculate cyclomatic complexity (flag >10)
- Identify deeply nested conditionals
- Find long parameter lists (flag >4 params)
- Check for complex boolean expressions

### 8. Evaluate Code Organization

- Verify logical grouping of related functions
- Check separation of concerns
- Review import/dependency structure
- Ensure consistent formatting

## Output Format

Present findings in this structure:

```markdown
# Code Quality Review

## Summary
**Status:** [PASS / NEEDS IMPROVEMENT / REQUIRES REFACTORING]
**Files Reviewed:** [count]
**Issues Found:** [count] ([Critical count], [Major count], [Minor count])

---

## Critical Issues (Fix Now)

### 1. [Issue Title]
- **File:** `path/to/file.py:42-68`
- **Smell:** [Code smell name]
- **Issue:** [Detailed description]
- **Impact:** [Why this matters for maintainability]
- **Fix:**
  ```python
  # Refactored code example
  ```

---

## Major Issues (Should Fix)

### 1. [Issue Title]
- **File:** `path/to/file.py:89`
- **Principle:** [SOLID/DRY/KISS violated]
- **Issue:** [Description]
- **Suggestion:** [How to improve]

---

## Minor Issues (Consider)

### 1. [Issue Title]
- **File:** `path/to/file.py:120`
- **Category:** [Naming/Organization/Complexity]
- **Suggestion:** [Improvement idea]

---

## Positive Observations

- [Good practice 1]
- [Good practice 2]

---

## Metrics

- **Average Function Length:** [lines]
- **Average Class Size:** [lines]
- **Max Cyclomatic Complexity:** [value]
- **Code Duplication:** [percentage]%
```

## Quality Checklist

Before presenting findings, verify:

- [ ] All code smells identified with specific file/line references
- [ ] SOLID principle violations explained with concrete examples
- [ ] DRY violations include refactoring suggestions
- [ ] Complexity metrics calculated and flagged where excessive
- [ ] Naming issues include specific improvement recommendations
- [ ] Each issue includes working code example for the fix
- [ ] Positive practices acknowledged

## Common Patterns

Be aware of these typical issues and their solutions:

### God Objects
**Pattern:** Often result from incremental feature additions
**Solution:** Suggest splitting by responsibility

### Long Methods
**Pattern:** Frequently have embedded business rules
**Solution:** Extract to separate functions

### Duplicated Code
**Pattern:** In similar branches suggests missing abstraction
**Solution:** Extract common logic

### Deeply Nested Conditionals
**Pattern:** Indicate missing strategy pattern or state machine
**Solution:** Suggest appropriate design pattern
