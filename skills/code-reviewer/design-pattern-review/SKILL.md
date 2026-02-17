---
name: design-pattern-review
description: |
  Design pattern analysis for architectural consistency and appropriate abstraction levels.

  WHAT: Reviews code for design pattern usage (Factory, Strategy, Observer, Decorator, Adapter, Singleton, etc.). Identifies over-engineering (patterns where simple code suffices), under-engineering (missing abstractions where patterns would help), and architectural inconsistencies. Suggests refactorings to improve structure using proven patterns.

  WHEN: Use for architectural reviews, refactoring analysis, design discussions, or when evaluating code structure. Trigger on: "design patterns", "architecture review", "pattern review", "design review", "structural review", "refactoring patterns", "over-engineering", "under-engineering", "architectural consistency".
allowed-tools: Read, Grep, Glob
---

# Design Pattern Review

## Overview

This skill analyzes the application of design patterns in code, identifying appropriate usage, over-engineering, under-engineering, and opportunities for pattern-based improvements. It evaluates architectural consistency, suggests refactorings to improve structure, and ensures patterns are used effectively rather than dogmatically.

## Review Workflow

Follow these steps to conduct a thorough design pattern review:

### 1. Identify Existing Pattern Usage

- Scan for common pattern signatures (Factory methods, Strategy interfaces, Observer subscribers)
- Document which patterns are already in use
- Note consistency of pattern application

### 2. Evaluate Pattern Appropriateness

For each pattern found, ask:

- **Strategy Pattern:** Is polymorphic behavior needed? Are algorithms varying independently?
- **Factory Pattern:** Is object creation complex or configurable?
- **Observer Pattern:** Is there a one-to-many dependency requiring notification?
- **Decorator Pattern:** Is functionality being added dynamically?
- **Adapter Pattern:** Are incompatible interfaces being bridged?

### 3. Identify Over-Engineering

Look for these signs:

- Patterns used for simple, static scenarios (e.g., Factory for one product type)
- Abstract classes with single implementation
- Interfaces with single implementer and no planned extensions
- Excessive layers of indirection

### 4. Identify Under-Engineering

Look for these signs:

- Switch statements on type that should be polymorphism (Strategy pattern)
- Repeated conditional logic that should be extracted (Strategy/State pattern)
- Hard-coded object creation that needs flexibility (Factory pattern)
- Tight coupling that should be decoupled (Adapter/Dependency Injection)

### 5. Check Architectural Consistency

- Verify similar problems solved with similar patterns
- Ensure pattern usage follows project conventions
- Identify inconsistent abstraction levels
- Check for mixing architectural styles

### 6. Evaluate Creational Patterns

Check for appropriate usage of:

- **Factory Method:** Object creation delegated to subclasses
- **Abstract Factory:** Families of related objects
- **Builder:** Complex object construction step-by-step
- **Singleton:** Single instance enforcement (often anti-pattern - flag for DI alternatives)
- **Prototype:** Object cloning for new instances

### 7. Evaluate Structural Patterns

Check for appropriate usage of:

- **Adapter:** Interface translation between incompatible systems
- **Bridge:** Separation of abstraction from implementation
- **Composite:** Tree structures for part-whole hierarchies
- **Decorator:** Dynamic behavior addition
- **Facade:** Simplified interface to complex subsystem
- **Flyweight:** Shared object instances for efficiency
- **Proxy:** Surrogate or placeholder for another object

### 8. Evaluate Behavioral Patterns

Check for appropriate usage of:

- **Chain of Responsibility:** Pass requests through handler chain
- **Command:** Encapsulate requests as objects
- **Iterator:** Sequential access to collection elements
- **Mediator:** Centralized communication between objects
- **Memento:** Capture/restore object state
- **Observer:** Publish-subscribe for state changes
- **State:** Behavior changes based on internal state
- **Strategy:** Encapsulate interchangeable algorithms
- **Template Method:** Algorithm skeleton with variable steps
- **Visitor:** Operations on object structure elements

### 9. Suggest Refactorings

- Recommend patterns that would improve specific code sections
- Provide before/after examples
- Explain benefits of suggested pattern
- Estimate refactoring effort

### 10. Document Architectural Intent

- Clarify which patterns are intentional vs accidental
- Note areas where patterns should NOT be used
- Identify technical debt related to pattern misuse

## Output Format

Present findings in this structure:

```markdown
# Design Pattern Review

## Summary
**Status:** [WELL-ARCHITECTED / NEEDS IMPROVEMENT / REQUIRES REFACTORING]
**Patterns Identified:** [count]
**Over-Engineering Cases:** [count]
**Under-Engineering Cases:** [count]

---

## Current Pattern Usage

### Effective Patterns
- **[Pattern Name]** in `file.py` - [Why it works well]

### Questionable Patterns
- **[Pattern Name]** in `file.py` - [Concern about appropriateness]

---

## Over-Engineering Cases (Unnecessary Complexity)

### 1. [Case Title]
- **File:** `path/to/file.py:42-95`
- **Pattern:** [Pattern being over-applied]
- **Issue:** [Why this is over-engineered]
- **Impact:** Increased complexity without benefit
- **Recommendation:** Simplify to [simpler approach]
- **Example:**
  ```python
  # Simplified approach
  ```

---

## Under-Engineering Cases (Missing Abstractions)

### 1. [Case Title]
- **File:** `path/to/file.py:120-150`
- **Current Approach:** [What's currently being done]
- **Issue:** [Why this is under-engineered]
- **Impact:** Code duplication, poor extensibility
- **Recommended Pattern:** [Pattern that would help]
- **Example:**
  ```python
  # Pattern-based refactoring
  ```

---

## Architectural Inconsistencies

### 1. [Inconsistency Title]
- **Issue:** [Description of inconsistency]
- **Impact:** [Why consistency matters]
- **Recommendation:** [How to align]

---

## Refactoring Priorities

1. **[High Priority]**: [Refactoring description] - [Effort: Low/Medium/High]
2. **[Medium Priority]**: [Refactoring description] - [Effort: Low/Medium/High]
3. **[Low Priority]**: [Refactoring description] - [Effort: Low/Medium/High]

---

## Positive Observations

- [Good pattern usage 1]
- [Good pattern usage 2]
```

## Quality Checklist

Before presenting findings, verify:

- [ ] All patterns identified by name (Factory, Strategy, etc.)
- [ ] Over-engineering cases include simplified alternatives
- [ ] Under-engineering cases include pattern-based solutions
- [ ] Architectural inconsistencies explained with impact
- [ ] Refactoring priorities ranked by value vs effort
- [ ] Code examples provided for all suggestions
- [ ] Benefits of suggested patterns clearly articulated

## Common Patterns

Be aware of these typical issues and their solutions:

### Factory Over-Application
**Pattern:** Single product type doesn't need Factory
**Solution:** Use direct instantiation

### Strategy Under-Application
**Pattern:** Large switch/if-else on type suggests missing Strategy pattern
**Solution:** Extract algorithms into Strategy implementations

### Singleton Misuse
**Pattern:** Global state often better handled with Dependency Injection
**Solution:** Replace Singleton with DI container

### Adapter Necessity
**Pattern:** Legacy system integration often requires Adapter pattern
**Solution:** Create Adapter to bridge incompatible interfaces
