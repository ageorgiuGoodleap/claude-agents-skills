# PR Description Generator Skill

Generate comprehensive, professional pull request descriptions from git changes for GitHub and GitLab workflows.

## What It Does

This skill analyzes git diffs, commits, and branch metadata to produce complete, copy-paste-ready PR descriptions that help reviewers understand:
- What changed and why
- The user-facing impact
- How to validate the changes
- Potential risks and considerations

## When to Use

Use this skill when you need to:
- Create PR descriptions for new pull requests
- Document code changes for team review
- Generate merge request descriptions for GitLab
- Analyze and summarize git diffs
- Produce structured documentation from code changes

## Key Features

- **Multi-platform support**: Works with GitHub and GitLab
- **Flexible input**: Accepts PR URLs, PR numbers, or analyzes current branch
- **Intelligent analysis**: Groups changes by logical concern, not file structure
- **Context gathering**: Asks clarifying questions only when necessary
- **Structured output**: Follows industry best practices for PR documentation
- **Quality checks**: Validates descriptions against comprehensive checklist

## Output Structure

Generates `PR_DESCRIPTION.md` with these sections:
- **Title**: Conventional commit format (feat/fix/refactor)
- **Summary**: User-facing impact in 2-3 sentences
- **Jira Ticket**: Links to issue tracking (if applicable)
- **Why This Change**: Business context and rationale
- **Implementation Details**: Organized by logical concern
- **Validation Checklist**: Testing and review items
- **CI/CD Status**: Last build run information
- **Screenshots/Evidence**: Visual proof of changes (if applicable)
- **Reviewer Notes**: Areas needing extra scrutiny

## Usage Examples

### Generate from PR number
```
User: "Generate a description for PR #456"
```

### Generate from current branch
```
User: "Create a PR description for my changes"
```

### Generate from PR URL
```
User: "Document this PR: https://github.com/org/repo/pull/123"
```

## Requirements

- Git repository with commit history
- Optional: `gh` CLI for GitHub integration
- Optional: `glab` CLI for GitLab integration

## Best Practices

- Run this skill after completing your changes and committing them
- Ensure your commits have descriptive messages
- Have your Jira ticket or issue tracking information ready
- Run CI/CD before generating the description for complete validation
- Include screenshots for UI changes when prompted

## Notes

- This skill generates documentation only; it does not create or modify PRs
- Works with both GitHub and GitLab workflows
- Output follows conventional commit standards
- Descriptions are optimized for code review efficiency
- No bundled scripts, references, or assets needed (pure instruction-based)
