# Coding Documentation Skill

Professional documentation generation from code diffs and changes following engineering best practices.

## Overview

This skill generates high-quality documentation artifacts from code changes, including:

- **PR Descriptions and Reviewer Guides**: Structured summaries with validation steps, review order, and risk assessment
- **Changelog Entries and Release Notes**: SemVer-framed, user-focused change documentation
- **README Updates**: Installation steps, usage examples, and configuration changes
- **API Reference Documentation**: Type-safe function signatures, parameters, and examples
- **Migration Notes**: Explicit before/after code snippets for breaking changes
- **ADRs (Architecture Decision Records)**: Design decisions with alternatives and tradeoffs
- **Runbooks**: Deployment procedures, monitoring, and failure mode responses

## When to Use This Skill

Activate this skill when you need to document code changes:

- "Document the diff"
- "Write a PR description"
- "Generate changelog entries"
- "Update README with these changes"
- "Create migration notes for breaking changes"
- "Write an ADR for this design decision"
- "Create a runbook for this deployment"

## Key Features

### Ground Truth Focused
- Documentation reflects actual code changes, not speculation
- References specific files, functions, and line numbers
- Only documents behavior supported by the diff or tests

### Language-Specific Conventions
- **Python**: PEP 257 docstrings, type hints, pytest conventions
- **TypeScript**: Strict mode compatibility, type guards, interface changes

### Audience-Appropriate
- **Reviewers**: Risk assessment, review order, validation steps
- **Users**: Observable behavior changes, migration steps
- **Operators**: Deployment procedures, monitoring, failure modes

### Change Classification
Automatically identifies change impact and selects appropriate documentation artifacts:
- Public API changes → API reference updates
- Breaking changes → Migration notes
- Design decisions → ADRs
- Operational changes → Runbooks

## Artifact Types

### 1. PR Description and Reviewer Guide
Structured format: What Changed, Why, How to Validate, Review Order, Risk List

### 2. Changelog Entry and Release Notes
SemVer-framed with Breaking Changes, Added, Changed, Fixed, Deprecated sections

### 3. README Updates and Usage Examples
Updated installation steps, quick start guides, and configuration examples

### 4. API Reference and Configuration Schema
Type-safe function signatures with parameters, return types, and realistic examples

### 5. Migration Notes for Breaking Changes
Before/after code snippets, impact analysis, validation steps, and timelines

### 6. ADR (Architecture Decision Record)
Context, decision, consequences, alternatives considered, implementation notes

### 7. Runbook and Operational Notes
Deployment steps, rollback procedures, monitoring, failure modes

## Quality Standards

All documentation includes:
- Exact test commands and expected outputs
- Specific file and line number references
- Copy-pasteable code examples
- Language-appropriate conventions
- Validation checklists

## Usage Example

```
User: "Document the changes in the JWT authentication update"

Skill Output:
1. Analyzes git diff to identify breaking changes (token expiration time)
2. Generates PR description with review order and risk assessment
3. Creates changelog entry marking breaking change
4. Writes migration notes with before/after code snippets
5. Updates README with new token refresh configuration
6. Produces runbook for deployment monitoring
```

## Best Practices

- Always provide the actual code diff or changes
- Specify the documentation artifact type if you have a preference
- Mention the version number for changelog entries
- Indicate the target audience (reviewers, users, operators)
- Provide context about the change motivation if available

## Integration

Works seamlessly with:
- Git diffs and commits
- GitHub PR descriptions
- Version control workflows
- CI/CD documentation requirements
- Code review processes

## Output Location

Documentation artifacts are generated inline in the conversation. For file output, specify the desired file path or use standard locations:
- `CHANGELOG.md` for changelog entries
- `docs/ADR-XXX.md` for architecture decisions
- `docs/runbooks/` for operational runbooks
- `MIGRATION.md` for migration guides
