---
name: architecture-decision-records
description: |
  Document architectural decisions with context, alternatives, and consequences using ADR format.
  Use when user asks to document architecture decisions, create ADRs, record technical decisions, document
  design rationale, create decision records, document trade-offs, justify architectural choices, create ADR
  files, maintain decision logs, or document alternatives considered for significant architectural decisions.
allowed-tools: Read, Write, Edit
---

# Architecture Decision Records (ADR)

Document significant architectural decisions with context, alternatives, trade-offs, and consequences for historical reference.

## Workflow

### 1. Identify Decision Worth Documenting

**Document**:
- Technology selection (languages, frameworks, databases, cloud providers)
- Architectural patterns (microservices, monolith, serverless, event-driven)
- Integration approaches (REST, GraphQL, gRPC, message queues)
- Security mechanisms (authentication, authorization, encryption)
- Data strategies (database choice, caching, sharding)
- Deployment strategies (CI/CD, blue-green, canary)
- Significant refactoring or re-architecture

**Don't Document**:
- Routine implementation details (variable naming, code organization)
- Reversible low-stakes choices (library versions, minor configs)
- Temporary workarounds or experiments

### 2. Create ADR File

**Naming**: NNNN-title-with-dashes.md (e.g., 0001-use-postgresql-for-primary-database.md)

**Numbering**: Sequential, zero-padded to 4 digits, never reuse numbers

**Location**: Save to designated ADR directory or project /adr/ folder

### 3. Document Using ADR Template

```markdown
# ADR-NNNN: [Title]

## Status

[Proposed | Accepted | Rejected | Deprecated | Superseded]

Date: YYYY-MM-DD

## Context

[Describe the problem, opportunity, or forces at play. Explain why this decision is needed.
Include relevant requirements, constraints, and business/technical drivers.]

## Decision

[State the decision clearly and specifically. Include key parameters, technologies, or
approaches chosen.]

## Alternatives Considered

### Alternative 1: [Name]

**Description**: [What is this alternative?]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Rejected Because**: [Why was this not chosen?]

### Alternative 2: [Name]

[Repeat structure for each alternative - minimum 2 alternatives]

## Consequences

### Positive
- [Benefit 1 with specific impact]
- [Benefit 2 with specific impact]

### Negative
- [Trade-off 1 with specific impact]
- [Trade-off 2 with specific impact]

### Neutral
- [Change 1]
- [Change 2]

## Related Decisions

- Supersedes: [ADR-XXXX: Title](XXXX-title.md)
- Superseded by: [ADR-YYYY: Title](YYYY-title.md)
- Related to: [ADR-ZZZZ: Title](ZZZZ-title.md)

## Implementation Notes

[Optional: Key implementation considerations, migration strategy, success criteria]

## Reviewers

- [Name, Role] - YYYY-MM-DD
- [Name, Role] - YYYY-MM-DD

## Approval

Approved by: [Name, Role]
Date: YYYY-MM-DD
```

### 4. Write Context Section

Include:
- Problem or opportunity prompting the decision
- Current situation and pain points
- Business or technical drivers
- Requirements and constraints
- Stakeholders affected

Be specific with metrics and concrete examples.

### 5. State Decision Clearly

One sentence summary that is specific and actionable:

✅ Good: "We will adopt microservices with User Service, Content Service, Video Service, and Notification Service. Services communicate via REST APIs (synchronous) and Kafka (asynchronous). Each service has its own database. Deploy to AWS EKS."

❌ Bad: "We will use microservices because it's better."

### 6. Document Alternatives (minimum 2-3)

For each alternative:
- Describe the option clearly
- List pros and cons
- State why it was ultimately rejected with specific reasoning

### 7. Document Consequences

**Positive**: Benefits realized, problems solved, opportunities unlocked

**Negative**: Trade-offs accepted, new challenges, risks taken on

**Neutral**: Changes that are neither good nor bad, new processes needed

Be specific with measurable impact where possible (e.g., "20-30% cost increase", "reduce merge conflicts by 80%", "2x longer to debug initially")

### 8. Add Related Decisions and Dependencies

Link to:
- Supersedes: ADRs this replaces
- Superseded by: ADR that replaces this (when deprecated)
- Related to: ADRs on related topics
- Depends on: ADRs that must be implemented first

### 9. Include Implementation Notes (optional but recommended)

- Migration strategy with phases and timeline
- Required infrastructure or tooling
- Success criteria or acceptance tests
- Risks and mitigation strategies

### 10. Maintain ADR Index

Create README.md in ADR directory:

```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-title.md) | Title | Accepted | YYYY-MM-DD |
| [0002](0002-title.md) | Title | Accepted | YYYY-MM-DD |

## Status Definitions

- **Proposed**: Under consideration
- **Accepted**: Decision made and approved
- **Rejected**: Considered but not chosen
- **Deprecated**: Was accepted, now outdated
- **Superseded**: Replaced by another ADR
```

## ADR Status Lifecycle

```
Proposed → Accepted (decision made)
Proposed → Rejected (alternative chosen)
Accepted → Deprecated (no longer relevant)
Accepted → Superseded (replaced by new ADR)
```

## Key ADR Patterns

**Technology Selection**: Requirements → alternatives comparison → decision with version/config → operational impact, learning curve, vendor lock-in, migration path

**Architectural Pattern**: Current pain points → pattern alternatives → selected pattern with boundaries → complexity trade-offs, migration path, operational impact

**Security Decision**: Security requirements, compliance, threat model → mechanisms evaluated → selected approach with protocols/algorithms → security posture, usability, audit implications

## Critical Guidelines

**Decisions, Not Details**: Document significant decisions with long-term impact, not routine choices or style preferences. Reserve ADRs for decisions that:
- Have significant impact on system behavior or architecture
- Involve trade-offs between competing alternatives
- Affect multiple teams or systems
- Are difficult or costly to reverse

**Specific Context**: Include concrete metrics, examples, and current state to make context clear

**Multiple Alternatives**: Document at least 2-3 alternatives considered to show thoughtful evaluation

**Measurable Consequences**: Use specific numbers where possible (cost increase, performance impact, timeline)

**Review and Approval**: Document reviewers and get formal approval before marking as Accepted

**Update Index**: Always update README.md index when creating new ADRs
