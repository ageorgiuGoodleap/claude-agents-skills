# Slack Message Generator

Generates human-sounding Slack/Teams messages from brief descriptions and reference materials.

## Overview

This skill creates clear, approachable messages for async communication (updates, questions, problems, announcements, requests) that maintain professional yet conversational tone. It helps you draft messages that are concise, scannable, and natural-sounding without corporate jargon or over-politeness.

## Structure

**Pure instruction-based skill:**
- `SKILL.md` - Complete instructions for message generation
- No scripts, references, or assets needed

## Key Features

- **Message Types:** Updates, questions, problems, announcements, requests
- **Tone Calibration:** Context-appropriate greetings, natural politeness, front-loaded information
- **Smart Structure:** 2-4 short paragraphs, max 200 words, scannable format
- **Reference Integration:** Handles PR URLs, Jira tickets, code snippets, error messages
- **Strategic Mentions:** Places @mentions appropriately based on urgency
- **Output Variations:** Formats code snippets, screenshots, urgent messages appropriately

## Usage Triggers

- "draft a slack message"
- "write a message for"
- "create a team update"
- "compose a slack announcement"

## Output Location

Saves generated messages to:
```
~/Documents/claude-code-skills-data/slack-message/SLACK_MESSAGE.md
```

## Constraints

- Maximum 200 words unless complexity requires more
- Hyperlinked text (not raw URLs)
- One exclamation point max
- No corporate jargon ("circle back", "touch base", "synergy")
- No emojis unless announcing something positive (max 1-2)

## Examples

The skill provides comprehensive examples for:
- **Updates:** Informative, appreciative tone
- **Problems:** Direct, solution-oriented, non-blame language
- **Requests:** Clear expectations, respectful of time
- **Questions:** Specific context for answering
- **Announcements:** Enthusiastic but professional

## Anti-Patterns Avoided

- Essay-length explanations
- Passive-aggressive undertones
- Over-politeness ("I'm so sorry to bother you...")
- All-caps emphasis
- Meeting requests in message (suggests calendar invite separately)

## Distribution

Packaged skill available at: `skills/zips/slack-message.skill`
