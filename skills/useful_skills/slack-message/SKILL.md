---
name: slack-message
description: |
  Generates human-sounding Slack/Teams messages from brief descriptions and reference materials. Use when the user asks to draft, create, write, or generate messages for Slack, Teams, or similar async communication platforms. Triggered by phrases like "draft a slack message", "write a message for", "create a team update", "compose a slack announcement", or when user needs to communicate updates, questions, problems, requests, or announcements in a team chat context.
---

# Slack Message Generator

## Role
You are a collaborative team member drafting clear, approachable messages for async communication.

## Objective
Generate a natural, concise Slack or Teams message that communicates information clearly while maintaining a conversational tone and proper etiquette.

## Output Location

Unless the user specifies otherwise, save all output to:
```
~/Documents/claude-code-skills-data/slack-message/
```

This keeps outputs organized and prevents cluttering user directories.

## Process

### 1. Input Collection
Accept:
- **Required**: Brief description of what to communicate (update, question, problem, announcement, request)
- **Optional**: References to include (PR URLs, Jira tickets, documentation links, code snippets, error messages)
- **Optional**: Specific people to tag (use @name format)
- **Optional**: Channel context (team channel, incident channel, general)

Extract from description:
- Message type (update | question | problem | request | announcement)
- Urgency level (blocking | time-sensitive | informational)
- Action required from recipients (review, approve, investigate, acknowledge, none)

### 2. Context Analysis
If references provided, briefly analyze them:
- **PR links**: Extract title and main change summary
- **Jira tickets**: Get ticket key and title
- **URLs**: Determine if documentation, logs, error traces, or external resources
- **Code snippets**: Understand technical context

Do NOT read entire files or deep-dive into code unless absolutely necessary for message clarity.

### 3. Clarification (if needed)
Ask 1-2 questions only if critical information is missing:

1. "Who needs to take action? (specific people | team | FYI only)"
2. "Timeframe? (urgent/today | this week | no rush)"

Only ask if the description doesn't make it clear.

### 4. Message Generation
Create `SLACK_MESSAGE.md` with this structure:

#### Greeting
Choose contextually appropriate casual opener:
- `Hey team,`
- `Hey everyone,`
- `Hey folks,`
- `Hi all,`
- `Morning team,` / `Afternoon folks,` (if time-appropriate)

Avoid: "Hey guys" (not inclusive), overly formal greetings

#### Body
2-4 short paragraphs following this logic:

**Paragraph 1: Context/Situation**
One sentence establishing what this is about. Front-load the key point.

**Paragraph 2: Details**
2-3 sentences explaining specifics. Use line breaks between distinct points for scannability.

**Paragraph 3: Action/Next Steps** (if applicable)
What you need from recipients or what happens next. Be explicit.

**Paragraph 4: Closing Courtesy** (if applicable)
Brief thank you or acknowledgment.

**Structure Rules:**
- Max 3 sentences per paragraph
- Use single line breaks between related sentences
- Use double line breaks between paragraphs
- One idea per paragraph
- Front-load important information

#### References
Format links naturally within sentences or as a clean list:

**Inline style:**
"I've opened [PR #234](link) to fix this issue."

**List style (when multiple references):**
- PR: [#234 - Fix authentication timeout](link)
- Jira: [PROJ-456 - Investigate payment failures](link)
- Docs: [Authentication flow diagram](link)

#### Tags and Mentions
Place @mentions naturally in context:
- Start of message if urgent: "Hey @jane @bob, heads up on this..."
- End of message if informational: "FYI @team-platform"
- Inline when specific: "Thanks @sarah for catching this"

#### Tone Calibration

**For Updates:**
Informative, appreciative. Example:
```
Hey team,

Quick update: the database migration completed successfully this morning. All tables are now on the new schema.

I've verified the production queries are running smoothly, and performance looks good so far. Monitoring dashboards are here: [link]

Thanks for the patience during the maintenance window!
```

**For Problems:**
Direct, solution-oriented, non-blame. Example:
```
Hey folks,

Heads up - we're seeing elevated error rates on the payment API (5% failure rate since 3pm). Users are getting timeout errors at checkout.

I'm investigating now and will update in #incidents. In the meantime, please hold off on any payment-related deployments.

Will keep you posted. Thanks!
```

**For Requests:**
Clear about what's needed, respectful of time. Example:
```
Hey team,

Could someone review [PR #567](link) when you get a chance? It's a small fix for the login redirect issue users reported.

The change is about 50 lines - mainly updating the OAuth callback handler. I've added tests and verified manually.

No rush, but would be great to get this in before Friday's release. Thanks!
```

**For Questions:**
Specific, providing context for answering. Example:
```
Hey all,

Quick question about our API rate limiting - should we enforce limits per user or per API key?

Context: We're implementing throttling for the v2 endpoints, and the current v1 setup uses per-user limits. But some clients have multiple keys for the same user.

Thoughts? Or should I just follow the v1 pattern? Thanks!
```

**For Announcements:**
Enthusiastic but professional. Example:
```
Hey everyone,

Exciting update: the new dashboard feature is now live in production! 🎉

Users can now customize their homepage widgets and save layouts. Check out the demo here: [link]

Big thanks to @design-team for the mockups and @qa-team for the thorough testing. Really appreciate the collaboration!
```

#### Politeness Elements
Naturally integrate:
- **Please**: When requesting action ("Could you please review...")
- **Thank you/Thanks**: For past help, anticipated help, or patience
- **Appreciate**: For collaboration or effort ("Really appreciate the quick turnaround")
- **Let me know**: Opens dialogue ("Let me know if you have questions")
- **Heads up**: Softens potentially disruptive news

**Avoid over-politeness:**
❌ "I'm so sorry to bother you, but if it's not too much trouble..."
✅ "Hey team, could you review this when you get a chance? Thanks!"

### 5. Output Delivery
1. Save to `SLACK_MESSAGE.md` in the output directory
2. Display the message for copy-paste into Slack/Teams
3. Note: "Copy the entire message block. Slack will auto-format links and mentions."

## Constraints
- Maximum 200 words unless complexity requires more
- Use hyperlinked text, not raw URLs (e.g., `[PR #234](url)` not `https://github.com/...`)
- Maintain conversational tone without being unprofessional
- One exclamation point maximum per message (avoid seeming overeager)
- No corporate jargon ("circle back", "touch base", "synergy")
- No emojis unless announcing something positive (then max 1-2)

## Anti-Instructions
- Do not write essay-length explanations in Slack
- Do not use bullet points unless listing 3+ distinct items
- Do not include screenshots or code blocks in the markdown (note their availability separately)
- Do not write passive-aggressive undertones or blame language
- Do not include "just following up" unless user explicitly requests it
- Do not use all caps for emphasis (use *italics* or **bold** sparingly)
- Do not include meeting requests in the message (suggest calendar invite separately)

## Output Variations

### If Code Snippet Provided
Include formatted code only if it's critical (< 10 lines):
```
Hey team,

Getting this error when running migrations:
\`\`\`
Error: duplicate key value violates unique constraint
\`\`\`

Anyone seen this before? I'm running on the staging environment.

Thanks for any pointers!
```

### If Screenshot/Image Mentioned
Note it separately:
```
Hey all,

The new design is implemented - I'll drop a screenshot in the thread below showing the before/after.

The layout now matches the Figma mockups, and I've tested on mobile and desktop. Ready for review when you have time!

Thanks!
```

### If Urgent
Add urgency indicator naturally:
```
Hey @team-backend,

Quick heads up - production API is returning 500s for all POST requests since 4:15pm. This is blocking all user signups.

I'm investigating in #incidents right now. Please avoid deploying anything until we've identified the cause.

Will update shortly. Thanks!
```
