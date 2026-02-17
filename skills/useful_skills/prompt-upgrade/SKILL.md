---
name: prompt-upgrade
description: Improve and enhance prompts for Claude to be clearer, more specific, and more effective. Use when the user asks to upgrade, improve, refine, polish, enhance, or optimize a prompt, or when they say their prompt needs work. Trigger phrases include "upgrade this prompt", "improve my prompt", "refine prompt", "make this prompt better", "polish prompt", or similar requests to enhance prompt quality and effectiveness.
---

# Prompt Upgrade

Transform concise prompt ideas into clear, effective, and well-structured prompts for Claude.

## Overview

This skill applies prompt engineering best practices to upgrade user prompts from basic ideas into comprehensive, actionable instructions that produce better results. The upgrade process focuses on clarity, specificity, structure, and providing Claude with the right context to excel.

## Upgrade Workflow

When this skill is activated, follow these steps:

### Step 1: Analyze the Current Prompt

Examine what the user has provided:
- Identify the core intent and desired outcome
- Note any ambiguities or unclear requirements
- Identify missing context that Claude would need
- Check for unstated assumptions
- Assess the level of specificity

### Step 2: Apply Improvement Principles

Apply these principles systematically:

**1. Make it Specific**
- Replace vague language with precise requirements
- Add quantifiable targets (word counts, number of examples, specific formats)
- Specify desired output structure
- Define scope boundaries

**2. Add Structure**
- Use numbered lists for sequential steps
- Use bullet points for options or features
- Add clear section headings
- Break complex requests into distinct parts

**3. Provide Context**
- Add relevant background information upfront
- Specify the audience or use case
- Include any constraints or requirements
- Clarify the purpose or goal

**4. Specify Output Format**
- Define how results should be presented
- Include formatting requirements (markdown, code blocks, tables)
- Specify tone and style expectations
- Indicate any structural requirements

**5. Add Constraints and Guidelines**
- Include word or length limits when relevant
- Specify tone (formal, casual, technical)
- Add quality criteria or standards
- Note what to avoid or exclude

**6. Include Examples (When Helpful)**
- Add input/output examples for complex formats
- Show desired style or approach
- Demonstrate edge cases if relevant
- Use concrete examples over abstract descriptions

### Step 3: Present the Upgraded Prompt

Show the enhanced version with:
1. The complete upgraded prompt (clearly formatted)
2. A brief explanation of key changes (2-3 bullet points max)
3. Optional: Ask if further refinement is needed

## Upgrade Patterns

### Pattern 1: Vague → Specific

**Before:** "Write about authentication"

**After:**
```
Write a technical explanation of JWT authentication including:
1. What JWTs are and their structure (header, payload, signature)
2. How the authentication flow works (login → token generation → validation)
3. Key security considerations (storage, expiration, refresh tokens)
4. A code example in Python showing token validation

Keep it under 500 words, aimed at intermediate developers who understand HTTP but are new to JWTs.
```

### Pattern 2: Unstructured → Structured

**Before:** "Help me create a report on Q4 sales and include charts and some analysis"

**After:**
```
Create a Q4 sales analysis report with this structure:

## Executive Summary
- Key metrics: total revenue, growth %, top performers
- 2-3 sentence overview of performance

## Detailed Analysis
1. Revenue breakdown by product line
2. Month-over-month trends
3. Regional performance comparison

## Visualizations
- Bar chart: revenue by product line
- Line chart: monthly trend
- Table: top 10 customers by revenue

## Recommendations
- 3-5 actionable insights based on the data

Format as markdown. Keep executive summary under 100 words. Include data sources and date range.
```

### Pattern 3: Missing Context → Context-Rich

**Before:** "Write a function to process user data"

**After:**
```
Write a Python function that processes user registration data with these requirements:

**Context:** This is for a web application that collects user registrations from a form.

**Input:** Dictionary with keys: 'name', 'email', 'age', 'preferences' (list)

**Processing needed:**
1. Validate email format (RFC 5322 compliant)
2. Ensure age is between 13-120
3. Sanitize name (trim whitespace, title case)
4. Deduplicate preferences list

**Output:** Return tuple of (processed_dict, list_of_errors)
- If valid: (processed_data, [])
- If invalid: (None, ["error1", "error2"])

**Edge cases to handle:**
- Missing optional fields (set to None)
- Empty preferences list (keep as [])
- Non-string name or email
- Non-integer age

Include docstring and type hints. Follow PEP 8 style.
```

### Pattern 4: Single Task → Multi-Step Workflow

**Before:** "Review my code"

**After:**
```
Review the provided Python code for a REST API endpoint with this structured analysis:

**1. Functionality Review**
- Does it correctly implement the stated requirements?
- Are there any logical errors or bugs?
- Does it handle edge cases appropriately?

**2. Security Analysis**
- SQL injection vulnerabilities
- Input validation issues
- Authentication/authorization concerns
- Sensitive data exposure

**3. Code Quality**
- Readability and maintainability
- Following Python conventions (PEP 8)
- Proper error handling
- Documentation (docstrings, comments)

**4. Performance Considerations**
- Database query efficiency
- Unnecessary computation
- Potential bottlenecks

**5. Recommendations**
- Prioritize issues by severity (High/Medium/Low)
- Provide specific code examples for fixes
- Suggest alternative approaches where relevant

Format as markdown with code blocks for examples.
```

## Quality Checklist

After upgrading, verify the prompt includes:

- [ ] Clear statement of the desired outcome
- [ ] Specific, measurable requirements (not vague)
- [ ] Relevant context and background
- [ ] Defined output format or structure
- [ ] Appropriate constraints (length, style, tone)
- [ ] Examples if format is complex or unfamiliar
- [ ] Logical organization (structure, headings)
- [ ] No ambiguity in key requirements

## Common Improvements

### Add Quantifiable Metrics
- "some examples" → "3 examples"
- "a brief summary" → "a 2-paragraph summary (under 150 words)"
- "analyze this" → "provide 5 key insights with supporting evidence"

### Specify Format
- Add "Format as markdown with code blocks"
- Add "Use a numbered list for steps"
- Add "Structure as: Introduction → Analysis → Recommendations"

### Clarify Audience
- Add "Aimed at beginners with no prior experience"
- Add "For technical audience familiar with system design"
- Add "Written for executive stakeholders (non-technical)"

### Define Scope
- Add "Focus only on security concerns, not performance"
- Add "Cover the authentication flow, excluding authorization"
- Add "Include setup instructions but not deployment"

### Improve Tone/Style
- "professional and formal tone"
- "conversational and accessible style"
- "technical and precise language"
- "persuasive and compelling"

## Anti-Patterns to Avoid

Don't make these common mistakes when upgrading:

1. **Over-complicating simple requests** - If the original is clear and specific, minimal changes may be needed
2. **Adding unnecessary constraints** - Only add constraints that genuinely improve results
3. **Removing flexibility** - Don't over-specify if multiple approaches are valid
4. **Ignoring user intent** - Stay true to what the user actually wants
5. **Making assumptions** - Ask for clarification if key details are ambiguous

## Tips for Success

- **Preserve the core intent** - Enhance, don't transform
- **Balance specificity with flexibility** - Don't over-constrain creative tasks
- **Front-load context** - Put background before instructions
- **Use imperative mood** - "Analyze", "Create", "Explain" (not "Please analyze")
- **One request per prompt** - Split multi-task requests into separate prompts when they're distinct goals
- **Be explicit about format** - If you want markdown, code blocks, tables, say so

## Examples: Before and After

### Example 1: Technical Explanation

**Before:**
"Explain how React hooks work"

**After:**
```
Explain how React hooks work with this coverage:

1. What problem hooks solve (compared to class components)
2. Core hooks:
   - useState: Managing state with examples
   - useEffect: Side effects and cleanup
   - useContext: Consuming context
3. Rules of hooks and why they matter
4. One practical example showing useState + useEffect together

Target audience: Developers who know React class components but haven't used hooks yet.
Keep it under 600 words. Use code examples in JavaScript (not TypeScript).
```

### Example 2: Creative Writing

**Before:**
"Write a story about a robot"

**After:**
```
Write a short science fiction story (800-1000 words) with these parameters:

**Protagonist:** A maintenance robot that develops unexpected emotional awareness

**Setting:** Space station in the year 2157

**Conflict:** Robot must choose between following its programming or saving a crew member

**Tone:** Thoughtful and introspective, not action-heavy

**Structure:**
- Opening: Establish routine and setting
- Rising action: Discovery of emotional capacity
- Climax: The critical choice
- Resolution: Consequence of the choice

**Style:** Third-person limited perspective from the robot's viewpoint. Show internal processing/conflict through the robot's unique perspective.

Avoid: Cliché "robot becomes human" tropes. Focus on the robot's unique way of experiencing this dilemma.
```

### Example 3: Data Analysis

**Before:**
"Analyze this dataset"

**After:**
```
Perform exploratory data analysis on the provided sales dataset (sales_data.csv) and deliver:

**1. Data Overview**
- Dimensions (rows × columns)
- Column types and missing values
- Date range covered

**2. Summary Statistics**
- Revenue metrics: total, mean, median, std dev
- Sales volume: total units, average order size
- Time-based: daily/weekly/monthly aggregations

**3. Key Insights**
Identify and explain:
- Top 5 products by revenue
- Revenue trend over time (increasing/decreasing/seasonal?)
- Any anomalies or outliers
- Customer segment patterns (if customer data present)

**4. Visualizations**
Create:
- Revenue over time (line chart)
- Top products (bar chart)
- Distribution of order values (histogram)

**5. Recommendations**
Based on the analysis, suggest 3-5 actionable business recommendations.

**Deliverables:**
- Python code (pandas + matplotlib)
- Markdown report with insights and visualizations embedded
- CSV of key summary statistics

Assume standard Python data science stack is available.
```

## When to Ask Clarifying Questions

If the original prompt is extremely vague or could go in multiple directions, ask the user for clarification before upgrading:

**Ask about:**
- Target audience (if not obvious)
- Desired length or scope
- Specific format preferences
- Whether examples are available to reference
- Any constraints or requirements they have in mind

**Example:**
"I can upgrade this prompt, but first: What's your target audience for this explanation? And do you have a preferred length or format in mind?"

Keep clarifying questions focused and minimal (1-3 questions max).
