---
name: static-analysis-enforcement
description: |
  Automated code quality enforcement through linters, formatters, type checkers, and static analysis.

  WHAT: Configures and runs language-specific linters (ESLint, Pylint, Flake8, RuboCop, golangci-lint), code formatters (Prettier, Black, gofmt, rustfmt), type checkers (TypeScript strict mode, mypy, Flow, Sorbet), and static analysis platforms (SonarQube, CodeClimate, DeepSource, Semgrep). Interprets results, prioritizes issues, and generates actionable reports.

  WHEN: Use for automated quality checks, pre-commit hooks, CI/CD integration, or manual code analysis. Trigger on: "linting", "static analysis", "code analysis", "run linter", "ESLint", "Pylint", "Flake8", "type checking", "mypy", "code formatting", "Prettier", "Black", "SonarQube", "CodeClimate", "format code".
allowed-tools: Bash, Read, Grep, Glob
---

# Static Analysis Enforcement

## Overview

This skill configures, runs, and interprets results from automated code quality tools including linters, formatters, type checkers, and static analysis platforms. It ensures consistent code style, catches common errors, enforces type safety, and integrates quality gates into the development workflow.

## Analysis Workflow

Follow these steps to conduct comprehensive static analysis:

### 1. Detect Language and Framework

- Scan for language identifiers (`.py`, `.ts`, `.js`, `.go`, `.rb`)
- Identify framework-specific files (`package.json`, `requirements.txt`, `go.mod`)
- Determine appropriate tools for this stack

### 2. Configure Linter (if not already configured)

**Python:**
- Create/update `.flake8` or `pyproject.toml` for Pylint
- Set severity levels and rule exceptions

**JavaScript/TypeScript:**
- Create/update `.eslintrc.js` or `.eslintrc.json`
- Configure parser options and plugins

**Go:**
- Create/update `.golangci.yml`
- Enable relevant linters

**Ruby:**
- Create/update `.rubocop.yml`
- Set style preferences

### 3. Configure Formatter (if not already configured)

**Python:**
- Create/update `pyproject.toml` for Black

**JavaScript/TypeScript:**
- Create/update `.prettierrc`

**Go:**
- Use gofmt (no config needed)

**Rust:**
- Use rustfmt with `rustfmt.toml`

### 4. Configure Type Checker (if applicable)

**TypeScript:**
- Enable `strict` mode in `tsconfig.json`

**Python:**
- Create `mypy.ini` or add `[mypy]` to `pyproject.toml`

**Flow:**
- Create `.flowconfig`

**Ruby:**
- Configure Sorbet with `sorbet/config`

### 5. Run Linter

- Execute linter on modified files or entire codebase
- Capture output (STDOUT, STDERR, exit codes)
- Parse results into structured format (file, line, rule, severity, message)

### 6. Run Formatter

- Check formatting without auto-fixing: `--check` flag
- Identify files that need formatting
- Optionally auto-fix with `--write` flag (if permission mode allows)

### 7. Run Type Checker

- Execute type checker on modified files or entire codebase
- Capture type errors (incompatible types, missing annotations, etc.)
- Parse results into structured format

### 8. Run Static Analysis Platform (if available)

**SonarQube:**
- Trigger scan and fetch results via API

**CodeClimate:**
- Parse JSON report

**DeepSource:**
- Check analysis status

**Semgrep:**
- Run security and correctness rules

### 9. Aggregate Results

- Combine linter, formatter, type checker, and platform results
- Deduplicate issues reported by multiple tools
- Categorize by severity (Error, Warning, Info)
- Group by file for easier navigation

### 10. Prioritize Issues

**Critical (Block Merge):**
- Type errors
- Security vulnerabilities
- Syntax errors

**High (Should Fix):**
- Logic errors flagged by linters
- Complexity violations

**Medium (Consider):**
- Code smells
- Style inconsistencies

**Low (Informational):**
- Suggestions
- Minor style preferences

### 11. Generate Report

- Summary statistics (total issues, breakdown by severity)
- File-by-file breakdown
- Rule-specific grouping for common violations
- Trends (compared to previous run if available)

### 12. Provide Fix Guidance

- For auto-fixable issues: Mention `--fix` flag
- For manual issues: Link to rule documentation
- For complex issues: Provide example fix

## Output Format

Present findings in this structure:

```markdown
# Static Analysis Report

## Summary
**Status:** [PASS / WARNINGS / ERRORS]
**Total Issues:** [count] ([Error count], [Warning count], [Info count])
**Auto-Fixable:** [count]

---

## Configuration

- **Linter:** [Tool name and version]
- **Formatter:** [Tool name and version]
- **Type Checker:** [Tool name and version]
- **Static Analysis:** [Platform name]

---

## Errors (Must Fix)

### Type Errors ([count])
- `file.py:42` - **Type incompatibility**: Expected `str`, got `int`
  - **Rule:** mypy/assignment
  - **Fix:** Cast or convert type

### Linter Errors ([count])
- `file.js:89` - **Undefined variable**: `userName` is not defined
  - **Rule:** ESLint/no-undef
  - **Fix:** Declare variable or import

---

## Warnings (Should Fix)

### Code Quality ([count])
- `file.py:120` - **Cyclomatic complexity**: 12 (threshold: 10)
  - **Rule:** Pylint/too-complex
  - **Fix:** Refactor to reduce complexity

### Code Style ([count])
- `file.ts:45` - **Missing semicolon**
  - **Rule:** ESLint/semi
  - **Fix:** Run `npm run lint -- --fix` (auto-fixable)

---

## Info (Consider)

### Suggestions ([count])
- `file.py:200` - **Consider using f-string** instead of `.format()`
  - **Rule:** Pylint/use-fstring
  - **Fix:** Modernize string formatting

---

## Formatting Issues

**Files Needing Formatting:** [count]
- `file1.py`
- `file2.js`

**Fix:** Run formatter:
```bash
# Python
black file1.py

# JavaScript/TypeScript
prettier --write file2.js
```

---

## Issues by File

### `path/to/file.py` ([count] issues)
1. Line 42: [Error] [Description]
2. Line 89: [Warning] [Description]

### `path/to/file.js` ([count] issues)
1. Line 120: [Warning] [Description]

---

## Auto-Fix Available

The following issues can be automatically fixed:
- [count] formatting issues: `prettier --write .`
- [count] linter issues: `eslint --fix .`

---

## Recommendations

1. **High Priority:** Fix [count] type errors in [files]
2. **Medium Priority:** Address [count] complexity warnings
3. **Low Priority:** Run auto-fix for [count] style issues

---

## Trend Analysis

- **Previous Run:** [count] issues
- **Current Run:** [count] issues
- **Change:** [+/- count] ([percentage]% [increase/decrease])
```

## Quality Checklist

Before presenting findings, verify:

- [ ] All tools detected and run successfully
- [ ] Results aggregated from multiple sources
- [ ] Issues categorized by severity (Error/Warning/Info)
- [ ] Auto-fixable issues flagged with fix command
- [ ] File-by-file breakdown provided
- [ ] Rule documentation links included
- [ ] Trend analysis compared to baseline (if available)

## Common Tool Patterns

Be aware of these typical patterns for each tool:

### ESLint
Most issues auto-fixable with `--fix` flag. Focus on errors before warnings.

### Pylint
Complexity warnings often indicate need for refactoring. Consider disabling overly strict rules if they don't add value.

### mypy
Incremental adoption via `# type: ignore` comments. Document as tech debt with issue tracker links.

### SonarQube
Focus on "Bugs" and "Vulnerabilities" categories first. "Code Smells" are lower priority.

## Language-Specific Commands

### Python
```bash
# Linting
pylint src/
flake8 src/

# Formatting
black --check src/
black src/  # auto-fix

# Type checking
mypy src/
```

### JavaScript/TypeScript
```bash
# Linting
eslint src/
eslint --fix src/  # auto-fix

# Formatting
prettier --check src/
prettier --write src/  # auto-fix

# Type checking (TypeScript)
tsc --noEmit
```

### Go
```bash
# Linting
golangci-lint run

# Formatting
gofmt -d .
gofmt -w .  # auto-fix

# Type checking (built into go)
go build ./...
```

### Ruby
```bash
# Linting
rubocop

# Formatting
rubocop --auto-correct  # auto-fix

# Type checking (Sorbet)
srb tc
```
