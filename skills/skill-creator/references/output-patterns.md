# Output Patterns

Use these patterns when skills need to produce consistent, high-quality output.

## Template Pattern

Provide templates for output format. Match the level of strictness to your needs.

### For Strict Requirements

Use when output format is critical (API responses, data formats, official documents):

```markdown
## Report structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation

## Appendix
[Supporting data and methodology]
```

**Key phrases for strict templates:**
- "ALWAYS use this exact structure"
- "Follow this format precisely"
- "Do not deviate from this template"

### For Flexible Guidance

Use when adaptation is useful and context matters:

```markdown
## Report structure

Here is a sensible default format, but use your best judgment based on the analysis:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]

Adjust sections as needed for the specific analysis type.
```

**Key phrases for flexible templates:**
- "Here is a sensible default"
- "Use your best judgment"
- "Adjust as needed"
- "Adapt based on context"

## Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs. This is more effective than descriptions alone for style, tone, and format.

### When to Use Examples

- Output style matters (commit messages, documentation, communications)
- Specific formatting is needed but hard to describe
- Level of detail needs to be demonstrated
- Tone and voice are important

### How to Structure Examples

Provide 3+ examples showing variety:

```markdown
## Commit message format

Generate commit messages following these examples:

**Example 1: New feature**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2: Bug fix**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**Example 3: Multiple changes**
Input: Updated dependencies and refactored error handling
Output:
```
chore: update dependencies and refactor error handling

- Upgrade lodash to 4.17.21
- Standardize error response format across endpoints
```

Follow this style: type(scope): brief description, then detailed explanation.
```

**Best practices for examples:**
- Show 3+ examples to demonstrate variety
- Include edge cases and complex scenarios
- Label each example clearly
- Show both input and output
- Add a summary of the pattern at the end

**Real-world example from web-research skill:**
The skill provides detailed example scenarios showing different types of research (current statistics, market research, verification tasks) with complete workflows.

## Quality Checklist Pattern

Use checklists to help Claude verify output quality before presenting results. Especially useful for complex multi-step tasks.

```markdown
## Quality Checks

Before presenting findings, verify:
- [ ] All data sources are cited with URLs
- [ ] Statistics are verified across 2+ sources
- [ ] Conflicting information is acknowledged
- [ ] Recommendations are actionable and specific
- [ ] Output follows the required format
- [ ] All required sections are present

If any item is unchecked, revise the output before proceeding.
```

**When to use checklists:**
- Complex outputs with many requirements
- Quality-critical tasks (reports, analysis, documentation)
- Multi-step workflows where steps might be skipped
- Tasks with common failure modes

**Real-world example from web-research skill:**
The skill includes a quality checklist that Claude uses before presenting research findings to ensure completeness and accuracy.

## Structured Output Format

When the skill produces data or structured content, define the exact format:

```markdown
## Output Format

Present research findings in this structure:

```json
{
  "summary": "2-3 sentence overview",
  "findings": [
    {
      "theme": "Theme name",
      "insight": "Specific finding",
      "source": "Source name and URL",
      "date": "YYYY-MM-DD"
    }
  ],
  "conflicts": [
    {
      "issue": "Description of disagreement",
      "sources": ["Source 1", "Source 2"],
      "assessment": "Which is more credible and why"
    }
  ],
  "sources": [
    {
      "name": "Source name",
      "url": "https://...",
      "accessed": "YYYY-MM-DD"
    }
  ]
}
```
```

**When to use structured formats:**
- JSON/XML generation
- Database records
- API responses
- Data exports
- Configuration files

**Real-world example from web-research skill:**
The skill defines a markdown output structure with specific sections (Summary, Key Findings, Conflicting Information, Sources) to ensure consistent research reports.

## Philosophy-Driven Pattern

For creative skills, establish a philosophy or aesthetic framework first, then apply it:

```markdown
## Two-Step Process

### Step 1: Create Design Philosophy

Before creating the output, establish the design philosophy:
- Visual approach and aesthetic movement
- Core principles and values
- Style guidelines and constraints

Output this as a .md file for reference.

### Step 2: Execute Based on Philosophy

Use the philosophy as a guide while creating the actual output:
- Refer back to the philosophy document
- Apply principles consistently
- Make design choices that align with the framework
```

**Real-world example from canvas-design skill:**
The skill separates philosophy creation (defining the aesthetic movement) from execution (creating the visual art), ensuring thoughtful, cohesive design rather than ad-hoc decisions.

## Combining Patterns

Most effective skills combine multiple patterns:

```markdown
## Report Generation

**Template** (structure):
Use this report structure: [template here]

**Examples** (style):
See these example reports: [3 examples showing different scenarios]

**Checklist** (quality):
Before finalizing:
- [ ] All sections complete
- [ ] Data verified across sources
- [ ] Format matches template
- [ ] Citations included

**Structured Format** (data):
Export data as: [JSON schema]
```

## Pattern Selection Guide

| Pattern | Best For | Example Use Case |
|---------|----------|------------------|
| **Strict Template** | Format-critical outputs | API responses, legal documents, forms |
| **Flexible Template** | Adaptable outputs | Analysis reports, documentation, emails |
| **Examples** | Style and tone | Commit messages, communications, content |
| **Quality Checklist** | Complex tasks | Research, analysis, multi-step workflows |
| **Structured Format** | Data outputs | JSON/XML generation, database records |
| **Philosophy-Driven** | Creative work | Design, art, branding, content creation |

**General principle:** Start with templates for structure, add examples for style, include checklists for quality, define formats for data.

## Anti-Patterns to Avoid

1. **Overly verbose templates** - Keep templates concise; use examples to show details
2. **Single example** - One example suggests a rule; 3+ examples show a pattern
3. **Unchecked checklists** - If you include a checklist, actually use it
4. **Rigid templates for creative work** - Use philosophy/principles instead
5. **No escape hatch** - Always allow deviation when context demands it
