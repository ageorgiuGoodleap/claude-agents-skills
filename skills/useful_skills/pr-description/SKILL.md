---
name: pr-description
description: Generates comprehensive PR descriptions from git changes for GitHub/GitLab. Use when the user asks to create, write, generate, or draft a pull request description, PR summary, merge request description, or mentions documenting code changes for review. Automatically triggered when analyzing diffs, branches, or commits for PR documentation.
---

# PR Description Generator

This skill generates complete, copy-paste-ready pull request descriptions by analyzing git diffs and extracting context from commits, modified files, and branch metadata.

## Purpose

Transform code changes into professional PR descriptions that help reviewers understand what changed, why it changed, and how to validate the changes. Produces structured documentation suitable for GitHub and GitLab workflows.

## When to Use

Activate this skill when the user:
- Asks to create or generate a PR description
- Mentions documenting a pull request or merge request
- Wants to analyze changes for a PR
- Needs help writing PR documentation
- References specific PR numbers or URLs

## Process

### 1. Input Validation

Accept one of:
- **PR URL**: GitHub (`https://github.com/org/repo/pull/123`) or GitLab (`https://gitlab.com/org/repo/-/merge_requests/123`)
- **PR number**: If in repo directory (e.g., `123`)
- **No input**: Analyze current branch changes against target branch

### 2. Change Analysis

Fetch PR details using available tools:
- **GitHub**: Use `gh pr view <number> --json title,body,commits,files,url` to get PR metadata
- **GitLab**: Use `glab mr view <number>` to get merge request details
- **Fallback**: Use `git diff <target-branch>...HEAD` to analyze changes directly

Extract the following information:
- Files modified (group by type: source code, tests, configs, docs)
- Functions/classes added, modified, or removed
- Dependencies added or updated
- Database migrations or schema changes
- Environment variable or config changes
- Test coverage additions

### 3. Context Gathering

Ask up to 3 questions using `AskUserQuestion` ONLY if critical information is missing and cannot be inferred:

1. **Jira ticket**: "What Jira ticket does this relate to? (provide full URL or key like PROJ-123, or 'none')"
2. **CI/CD run**: "Provide the last successful CI/CD run URL (or 'pending' if not run yet)"
3. **Screenshots**: "Are there UI changes requiring screenshots? (yes/no)"

**Important**: Do NOT ask if information can be inferred from commits, branch names, or code changes.

### 4. Description Generation

Create `PR_DESCRIPTION.md` with this exact structure:

```markdown
# [Title]

<action>: <concise description of change>

Examples:
- feat: Add user authentication middleware
- fix: Resolve race condition in payment processing
- refactor: Extract database layer into separate module

---

## Summary

2-3 sentences describing what changed and the user-facing impact. Focus on outcomes, not implementation mechanics.

---

## Jira Ticket

- **Ticket**: [PROJ-123](full-jira-url) or `N/A`
- **Type**: Feature | Bug Fix | Refactor | Hotfix | Documentation

---

## Why This Change?

1-2 paragraphs explaining:
- Problem being solved or feature being added
- Business context or user pain point addressed
- Why this approach was chosen (if non-obvious)

---

## Implementation Details

Organized by logical groupings, not file-by-file:

### Core Changes
- Describe primary logic changes in plain English
- Reference key files modified (e.g., `src/auth/middleware.ts`)
- Highlight architectural decisions

### Database/Schema Changes
- Migrations added or modified
- Schema impact (new tables, columns, indexes)

### API Changes
- New endpoints or modified contracts
- Breaking changes flagged explicitly

### Dependencies
- New packages added with justification
- Version bumps with reason

### Configuration
- New environment variables required
- Config file changes

### Tests
- Test coverage added (unit, integration, e2e)
- Specific edge cases tested

---

## Validation

Checklist format:
- [ ] Tests pass locally (`npm test` / `pytest` / etc.)
- [ ] Linting and type checking pass
- [ ] Manually tested in <environment> environment
- [ ] Database migrations tested (if applicable)
- [ ] API contract validated (if applicable)
- [ ] Reviewed for security implications
- [ ] Breaking changes documented

---

## Last CI/CD Run

- **Link**: [CI Run #123](url) or `Not run yet`

---

## Screenshots/Evidence

If UI changes or visual output:
- Include before/after screenshots
- Add captions explaining what changed

If data/API changes:
- Show sample request/response payloads
- Include relevant logs or metrics

If no visual evidence needed: `N/A`

---

## Reviewer Notes

(Optional section for highlighting specific areas needing scrutiny)
- Focus review on: <specific files or logic>
- Known limitations: <temporary workarounds or tech debt introduced>
```

### 5. Output Delivery

1. Save description to `PR_DESCRIPTION.md` in the current directory
2. Display the markdown content for immediate copy-paste
3. If `gh` CLI is available and PR exists, offer: "Run `gh pr edit <number> --body-file PR_DESCRIPTION.md` to update PR description automatically?"

## Title Formatting Guidelines

The title should follow conventional commit format:

**Action types:**
- `feat` - New feature or functionality
- `fix` - Bug fix
- `refactor` - Code restructuring without behavior change
- `perf` - Performance improvement
- `docs` - Documentation only changes
- `test` - Adding or updating tests
- `chore` - Build process, dependencies, tooling
- `style` - Code formatting, whitespace changes
- `ci` - CI/CD configuration changes

**Format**: `<type>(<optional-scope>): <description>`

Examples:
- `feat(auth): Add JWT token validation middleware`
- `fix(payments): Resolve race condition in checkout flow`
- `refactor(database): Extract query layer into repository pattern`
- `docs(api): Update authentication endpoint documentation`

## Implementation Details Guidelines

Organize by logical concern, not by file structure:

**Good (logical grouping):**
```markdown
### Authentication Flow
- Added middleware to validate JWT tokens (src/middleware/auth.ts)
- Integrated session management (src/services/session.ts)
- Updated user model to include token expiry (src/models/user.ts)
```

**Avoid (file-by-file listing):**
```markdown
### src/middleware/auth.ts
- Added JWT validation

### src/services/session.ts
- Added session management

### src/models/user.ts
- Updated user model
```

## Quality Checklist

Before finalizing the PR description, verify:
- [ ] Title follows conventional commit format
- [ ] Summary focuses on user-facing impact, not implementation details
- [ ] Implementation details are organized by logical concern
- [ ] All breaking changes are explicitly flagged
- [ ] Database migrations are documented with impact
- [ ] New environment variables are listed
- [ ] Test coverage is described
- [ ] No placeholder sections remain (no "TBD", "TODO", "To be filled")
- [ ] Description is understandable to someone who hasn't seen the code
- [ ] File paths use relative paths from repo root

## Anti-Patterns to Avoid

Do NOT do any of the following:
- Include commit hashes or author names in the main description
- List files without explaining what changed in them
- Use passive voice ("was changed", "has been updated")
- Include placeholder sections like "TBD" or "To be filled"
- Generate descriptions for changes you cannot analyze (e.g., if git diff is unavailable)
- Write file-by-file implementation details
- Explain implementation mechanics in the Summary section
- Add jargon without definition or context
- Omit warnings for breaking changes, migrations, or config updates

## Git Commands Reference

Common commands used during analysis:

```bash
# View PR details (GitHub)
gh pr view <number> --json title,body,commits,files,url

# View merge request details (GitLab)
glab mr view <number>

# Compare current branch to main
git diff main...HEAD

# Get list of modified files
git diff --name-only main...HEAD

# View commit history
git log main..HEAD --oneline

# Get detailed diff with context
git diff main...HEAD --unified=5

# Check current branch
git branch --show-current

# Check remote tracking
git status -sb
```

## Example Usage

### Example 1: Existing PR
```
User: "Generate a description for PR #456"
Claude: [Fetches PR details via gh CLI, analyzes changes, asks for Jira ticket, generates PR_DESCRIPTION.md]
```

### Example 2: Current Branch
```
User: "Create a PR description for my current changes"
Claude: [Runs git diff against main, analyzes files, generates description]
```

### Example 3: PR URL
```
User: "Document this PR: https://github.com/org/repo/pull/123"
Claude: [Fetches PR via gh CLI, generates comprehensive description]
```

## Best Practices

- **Be concise**: Maximum 500 words unless change complexity requires more
- **Be specific**: Reference exact file paths, function names, and endpoints
- **Be clear**: Write for someone unfamiliar with the codebase
- **Be honest**: Document known limitations and tech debt introduced
- **Be helpful**: Highlight areas needing extra review scrutiny
- **Be consistent**: Use active voice and present tense throughout
- **Be complete**: Ensure all validation checklist items are addressed

## Notes

- This skill does not create or modify PRs, only generates documentation
- The skill works with both GitHub and GitLab workflows
- Output can be used as-is or customized before submission
- Description format follows industry best practices for code review
