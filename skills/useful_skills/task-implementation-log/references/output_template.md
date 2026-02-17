# Task Implementation Log Template

Use this template to structure the output. Fill in all bracketed placeholders.

---

### Task Summary

**- Title:** [One-line title from PR or Jira]
**- ID:** [Jira ticket ID, e.g., PROJ-123]
**- Type:** [Bug Fix | Feature | Refactor | Chore | Enhancement]
**- Description:** [2-3 sentence summary explaining the "why"]

### Implementation Details

**- Key Changes:**
- [First major change]
- [Second major change]
- [Third major change]
[Continue for 3-7 total changes]

**- Files Changed:**
- `path/to/file1.ext`: [One-line description of change]
- `path/to/file2.ext`: [One-line description of change]
- `path/to/file3.ext`: [One-line description of change]
[Continue for 5-10 significant files]

### References

**- Pull Request:** [PR URL]
**- Jira Ticket:** [Jira URL or "N/A"]

---

## Template Usage Notes

**Title:**
- Extract from PR title (preferred) or Jira summary
- Keep under 80 characters
- Remove ticket IDs if already in ID field

**ID:**
- Pattern: `[A-Z]+-\d+` (e.g., PROJ-123, BUG-456)
- Extract from Jira URL or PR title
- Use "N/A" if no ticket exists

**Type:**
- Determine from PR labels or Jira issue type
- Options: Bug Fix, Feature, Refactor, Chore, Enhancement
- Default to "Change" if unclear

**Description:**
- Synthesize from PR description and Jira body
- Focus on business value and "why"
- Keep to 2-3 sentences maximum
- Avoid implementation details (those go in Key Changes)

**Key Changes:**
- Use bullet points
- 3-7 items total
- Focus on functionality, not implementation
- Group related changes
- For features: What capability was added
- For bugs: What broke and how it's fixed
- For refactors: What improved and why

**Files Changed:**
- 5-10 most significant files only
- Use relative paths from repo root
- Format: `path/to/file.ext: Brief change description.`
- Prioritize core logic over tests
- One line per file, under 80 characters total
