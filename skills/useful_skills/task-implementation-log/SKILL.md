---
name: task-implementation-log
description: |
  Generate detailed task implementation logs from Pull Requests and Jira tickets. Use when the user asks to create a log, document a completed task, generate a task summary, or references a PR link with terms like "create log", "document this change", "summarize this PR", or "generate implementation log".
---

# Task Implementation Log Generator

Generate structured Markdown logs documenting completed engineering tasks from Pull Request and Jira ticket data.

## Output Location

Unless the user specifies otherwise, save all logs to:
```
~/Documents/claude-code-skills-data/task-implementation-log/
```

Name files using pattern: `<task-id>-<title-slug>.md`

## Required Inputs

- **Pull Request URL** (required): GitHub PR link
- **Jira Ticket URL** (optional): Atlassian Jira ticket link

## Workflow

### Step 1: Fetch PR Data

Use the GitHub MCP server to fetch PR data:
```
GitHub:get_pull_request(owner, repo, pull_number)
```

Extract:
- PR title
- PR description
- Files changed (with diffs)
- Commit messages
- Labels (to determine type: bug, feature, etc.)

### Step 2: Fetch Jira Data (if provided)

Use the Atlassian MCP server to fetch ticket data:
```
Atlassian:getJiraIssue(cloudId, issueIdOrKey)
```

Extract:
- Ticket ID
- Summary
- Description
- Issue type

### Step 3: Analyze and Synthesize

**Determine Task Type:**
- Check PR labels for: `bug`, `feature`, `refactor`, `chore`, `enhancement`
- Check Jira issue type if available
- Default to "Change" if unclear

**Generate Task Summary:**
- **Title**: Use PR title (preferred) or Jira summary
- **ID**: Extract Jira ticket ID from URL or PR title (e.g., "PROJ-123")
- **Type**: Use determined task type
- **Description**: Synthesize from PR description and Jira description
  - Focus on the "why" behind the change
  - Keep to 2-3 sentences
  - If both PR and Jira available, prefer Jira for business context

**Extract Key Changes:**
- Analyze commit messages and file diffs
- Group related changes together
- For each change:
  - Features: Describe the new functionality
  - Bug fixes: Explain the bug and the fix
  - Refactors: Explain the improvement
- Use bullet points, 3-7 items maximum

**List Significant Files:**
- Identify the 5-10 most significant files changed
- For each file, write a one-line description of the change
- Use format: `path/to/file.ext: Brief description of change.`
- Prioritize:
  - Core logic files over tests
  - New files over minor edits
  - Files with substantial changes

### Step 4: Generate Output

Use the template from [references/output_template.md](references/output_template.md).

Fill in all sections with synthesized data:
- Task Summary (title, ID, type, description)
- Implementation Details (key changes, files changed)
- References (PR URL, Jira URL if provided)

**Quality Checks:**
- [ ] Title is clear and concise (under 80 characters)
- [ ] Description explains the "why" (2-3 sentences)
- [ ] Key changes are specific and actionable (3-7 bullets)
- [ ] File list includes only significant changes (5-10 files)
- [ ] All URLs are valid and clickable
- [ ] No placeholder text remains (e.g., "[TODO]")

Save the generated log to the output directory.

## Example Usage

**Input:**
- PR: `https://github.com/owner/repo/pull/123`
- Jira: `https://company.atlassian.net/browse/PROJ-456`

**Output:**
```markdown
### Task Summary

**- Title:** Add token refresh logic to authentication service
**- ID:** PROJ-456
**- Type:** Feature
**- Description:** Implemented automatic token refresh to prevent users from being logged out unexpectedly. The auth service now detects expired tokens and refreshes them transparently, improving user experience during long sessions.

### Implementation Details

**- Key Changes:**
- Added token expiry detection in auth service
- Implemented automatic refresh mechanism using refresh tokens
- Added error state to login form for failed refresh attempts
- Created unit tests for token refresh logic
- Updated API client to handle token refresh responses

**- Files Changed:**
- `src/core/auth/service.py`: Added token refresh logic and expiry detection
- `src/ui/components/Login.tsx`: Updated form to show token refresh errors
- `src/api/client.py`: Added interceptor for handling token refresh responses
- `tests/test_auth_service.py`: Added unit tests for token refresh scenarios
- `docs/api/authentication.md`: Documented new token refresh behavior

### References

**- Pull Request:** https://github.com/owner/repo/pull/123
**- Jira Ticket:** https://company.atlassian.net/browse/PROJ-456
```

## Error Handling

**If PR URL is invalid or inaccessible:**
- Report: "Cannot access PR at [URL]. Verify the URL is correct and you have access."
- Do not proceed

**If Jira ticket is provided but inaccessible:**
- Report: "Cannot access Jira ticket. Proceeding with PR data only."
- Generate log using only PR information

**If no significant files can be identified:**
- List all changed files without descriptions
- Note: "Unable to determine significance of changes. All modified files listed."

**If description synthesis is unclear:**
- Use PR description verbatim
- Note: "Description based solely on PR information."
