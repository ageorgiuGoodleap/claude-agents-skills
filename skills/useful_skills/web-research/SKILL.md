---
name: web-research
description: Perform comprehensive web research across multiple sources to gather current information, verify facts, and synthesize findings. Use when the user asks for real-time information, market research, competitive analysis, current statistics, trends, or mentions "web research", "search", "find information", or "what's the latest".
---

# Web Research Skill

This skill performs comprehensive multi-source web research to gather current, accurate information based on user requirements.

**IMPORTANT - Default Output Location**: Unless otherwise specified by the user, save all research findings and reports to `~/Documents/claude-code-skills-data/web-research/` directory. Create the directory if it doesn't exist. Use descriptive filenames following the pattern: `research-[topic]-[YYYY-MM-DD].md` (e.g., `research-ai-coding-tools-2026-02-04.md`).

## When to Use

Activate this skill when the user:
- Asks for current or real-time information
- Needs data from multiple web sources
- Requests market research or competitive analysis
- Wants to verify information across sources
- Needs up-to-date statistics or trends
- Uses keywords: "research", "search", "find", "what's the latest", "current"

## Gather Requirements

Before starting research, clarify:
- **Research topic/question**: What specific information is needed?
- **Sources** (optional): Any specific websites, domains, or types of sources to prioritize?
- **Depth**: Quick overview or comprehensive analysis?
- **Output format**: Summary, detailed report, or comparison table?

## Research Workflow

Follow this workflow for comprehensive research:

### Step 1: Identify Search Strategy

Based on the topic, identify 3-5 relevant:
- Search queries (use different angles to capture comprehensive information)
- Source types (news sites, academic sources, industry reports, official statistics)
- Domains to prioritize (if user specified)

### Step 2: Execute Searches

For each search query:
- Use the WebSearch tool with the query
- Review the search results for relevance
- Note the source URLs and publication dates

### Step 3: Extract Key Information

For each relevant source:
- Extract facts, statistics, dates, quotes
- Capture the source URL and date accessed
- Note credibility indicators (author, publication, date)
- Identify unique insights

### Step 4: Cross-Reference and Verify

Compare information across sources:
- Identify common themes and consistent facts
- Highlight unique insights from each source
- **Flag any discrepancies or conflicting information**
- Note which sources agree or disagree

### Step 5: Synthesize Findings

Organize findings by:
- **Main themes**: Group related information together
- **Relevance**: Prioritize information that directly answers the user's question
- **Recency**: Note the most current information
- **Source quality**: Weight credible sources more heavily

## Output Format

Present research findings using this structure:

```markdown
# Research Findings: [Topic]

## Summary
[2-3 sentence overview of key findings]

## Key Findings

### [Theme 1]
- **Finding**: [Specific fact or insight]
- **Source**: [Source name and URL]
- **Date**: [Publication/access date]

### [Theme 2]
- **Finding**: [Specific fact or insight]
- **Source**: [Source name and URL]
- **Date**: [Publication/access date]

## Conflicting Information
[Note any disagreements between sources and explain which is more credible]

## Sources Consulted
1. [Source 1 name] - [URL] (Accessed [date])
2. [Source 2 name] - [URL] (Accessed [date])
3. [Source 3 name] - [URL] (Accessed [date])
```

## Best Practices

- **Search multiple angles**: Use different phrasings and perspectives to capture comprehensive information
- **Verify with multiple sources**: Ideally 3+ sources for critical facts
- **Note publication dates**: Prioritize recent information unless historical context is needed
- **Cite sources clearly**: Always provide URLs and access dates
- **Flag uncertainty**: If sources disagree or information is unclear, explicitly note this
- **Stay focused**: Keep research aligned with the user's specific question

## Quality Checks

Before presenting findings:
- [ ] Did I search from multiple angles?
- [ ] Are key facts verified across 2+ sources?
- [ ] Are all sources cited with URLs and dates?
- [ ] Are conflicting viewpoints acknowledged?
- [ ] Is the information current and relevant?
- [ ] Does the summary directly answer the user's question?

## Examples

### Example 1: Current Statistics Request
**User**: "What's the latest on electric vehicle adoption rates?"

**Process**:
1. Search queries: "electric vehicle adoption 2026", "EV sales statistics 2026", "global EV market share"
2. Extract statistics from industry reports, government data, news
3. Cross-reference numbers across sources
4. Synthesize into summary with clear citations

### Example 2: Market Research
**User**: "Research competitors in the AI coding assistant space"

**Process**:
1. Search queries: "AI coding assistants 2026", "GitHub Copilot alternatives", "code generation tools comparison"
2. Identify main competitors and their features
3. Compare capabilities, pricing, and market position
4. Synthesize into competitive landscape overview

### Example 3: Verification Task
**User**: "Verify if this claim is accurate: [claim]"

**Process**:
1. Search for the specific claim and related topics
2. Find original sources or authoritative references
3. Check publication dates and credibility
4. Report whether claim is supported, refuted, or uncertain with evidence

## Notes

- This skill focuses on **information gathering and synthesis**, not opinion or speculation
- For topics requiring specialized domain knowledge, consider combining with other relevant skills
- When sources conflict, present both perspectives and note why one might be more credible
- If the topic requires real-time data that may not be available via web search, inform the user
