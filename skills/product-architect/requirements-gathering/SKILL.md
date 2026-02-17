---
name: requirements-gathering
description: |
  Extract and categorize functional and non-functional requirements from business goals and stakeholders.
  Use when gathering requirements, defining product scope, conducting user needs analysis, performing
  stakeholder interviews, analyzing business requirements, creating requirement documents, or when
  user mentions requirements gathering, scope definition, functional requirements, non-functional
  requirements, stakeholder analysis, acceptance criteria.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Requirements Gathering

## Overview
Systematic process for extracting, categorizing, and documenting functional and non-functional requirements from stakeholders, business goals, and market research.

## Output Location

**Default Output Location:** Save all requirements documents to `~/Documents/claude-code-skills-data/requirements-gathering/` unless user specifies otherwise. Create the directory if needed.

## Workflow

### 1. Understand Context
- Identify project/feature name and business objectives
- List all stakeholders (business owners, end users, technical team)
- Gather input sources: stakeholder interviews, market research, competitive analysis, existing documentation
- Define success metrics and constraints (budget, timeline, team size)

### 2. Extract Functional Requirements
Functional requirements describe what the system must do.

For each requirement:
- **ID**: FR-XXX (sequential numbering)
- **Description**: Clear, specific capability statement
- **Priority**: Critical / High / Medium / Low
- **Source**: Which stakeholder or document provided this
- **Acceptance Criteria**: Testable conditions for completion
- **Dependencies**: Related requirements or external systems

**Example:**
```
FR-001: User Registration
Description: System must allow new users to create accounts with email and password
Priority: Critical
Source: Product Owner, User Research
Acceptance Criteria:
  - Email validation (RFC 5322 compliant)
  - Password strength requirements (min 8 chars, 1 uppercase, 1 number, 1 special)
  - Unique email constraint enforced
  - Confirmation email sent within 60 seconds
Dependencies: FR-005 (Email Service Integration)
```

### 3. Extract Non-Functional Requirements
Non-functional requirements describe how the system performs.

Categories:
- **Performance**: Response time, throughput, latency
- **Scalability**: Concurrent users, data volume growth
- **Availability**: Uptime percentage, disaster recovery
- **Security**: Authentication, authorization, encryption, compliance
- **Usability**: User experience, accessibility standards
- **Maintainability**: Code quality, documentation, testing
- **Compatibility**: Browsers, devices, operating systems

For each requirement:
- **ID**: NFR-XXX
- **Category**: Performance/Scalability/Security/etc.
- **Metric**: Measurable target (e.g., "95th percentile response time < 200ms")
- **Rationale**: Why this target matters
- **Verification Method**: How to test/measure compliance

**Example:**
```
NFR-001: API Response Time
Category: Performance
Metric: 95th percentile API response time < 200ms under normal load (1000 req/min)
Rationale: User research shows 200ms is perceptual threshold for "instant" feedback
Verification Method: Load testing with k6, monitoring with Prometheus
```

### 4. Create Stakeholder Matrix

| Stakeholder | Role | Priority | Key Concerns | Influence |
|-------------|------|----------|--------------|-----------|
| John Smith | Product Owner | High | Time to market, user adoption | Final approval |
| Sarah Lee | Engineering Lead | High | Technical feasibility, maintainability | Architecture decisions |
| Mike Johnson | End User Rep | Medium | Ease of use, feature completeness | Feature validation |
| Legal Team | Compliance | Medium | Data privacy, regulatory compliance | Security requirements |

### 5. Build Requirements Traceability Matrix

Link business goals → requirements → user stories → implementation

| Business Goal | Requirement ID | Type | User Story | Implementation Component |
|---------------|----------------|------|------------|--------------------------|
| Increase user signups | FR-001 | Functional | US-042 | Auth Service |
| Reduce support tickets | NFR-003 | Usability | US-089 | Help System |

### 6. Identify Gaps and Conflicts
- **Missing Requirements**: Areas not covered (error handling, edge cases, internationalization)
- **Conflicting Requirements**: Where stakeholders disagree (prioritization conflicts)
- **Ambiguous Requirements**: Unclear or subjective statements needing clarification
- **Out of Scope**: Explicitly document what's NOT included

### 7. Validate Requirements
- **Specific**: Is it clear and unambiguous?
- **Measurable**: Can acceptance criteria be tested?
- **Achievable**: Is it technically and financially feasible?
- **Relevant**: Does it align with business goals?
- **Time-bound**: Is there a timeline or priority?

### 8. Generate Output Document

Create structured markdown document:
```markdown
# Requirements Document: [Project Name]
**Version:** 1.0
**Date:** 2025-02-08
**Author:** Product Architect

## Executive Summary
- Project purpose and business objectives
- Key stakeholders and their priorities
- Success metrics
- Timeline and resource constraints

## Functional Requirements

### Authentication & Authorization
**FR-001: User Registration**
- Description: [detailed description]
- Priority: Critical
- Acceptance Criteria:
  - [criterion 1]
  - [criterion 2]
- Dependencies: FR-005
- Source: Product Owner

[Repeat for all FRs]

## Non-Functional Requirements

### Performance
**NFR-001: API Response Time**
- Metric: 95th percentile < 200ms
- Rationale: User experience research
- Verification: Load testing with k6

[Repeat for all NFRs]

## Stakeholder Matrix
[Table from step 4]

## Requirements Traceability
[Table from step 5]

## Assumptions and Constraints
- [Assumption 1]
- [Constraint 1]

## Out of Scope
- [Explicitly excluded feature 1]
- [Explicitly excluded feature 2]

## Risks and Mitigation
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Third-party API downtime | High | Medium | Implement fallback and caching |

## Approval
- Product Owner: ___________
- Engineering Lead: ___________
- Date: ___________
```

## Quality Checks

Before finalizing the requirements document, verify:
- [ ] All requirements have unique IDs
- [ ] Every functional requirement has acceptance criteria
- [ ] Every non-functional requirement has measurable metrics
- [ ] Stakeholder matrix is complete with priorities
- [ ] Traceability matrix links requirements to business goals
- [ ] Conflicts and gaps are documented
- [ ] Out of scope items are explicitly listed
- [ ] Success metrics are defined and measurable
- [ ] Requirements pass SMART validation (Specific, Measurable, Achievable, Relevant, Time-bound)

If any item is unchecked, revise the document before proceeding.

## Common Patterns

### Gathering from vague input
```
Vague: "The system should be fast"
Clarify: "What operations need to be fast? What's the target latency? How many concurrent users?"
Result: NFR-001: API response time < 200ms for read operations under 1000 req/min
```

### Resolving conflicts
```
Conflict: Marketing wants rich features, Engineering wants quick delivery
Resolution: Use MoSCoW prioritization - Must have (MVP), Should have (v1.1), Could have (v2.0), Won't have
Document the trade-off decision and rationale
```

### Handling missing information
```
When stakeholder says "I don't know the volume", provide estimates:
"Let's assume 10,000 users in year 1 based on similar products. We'll design for 50,000 to give headroom."
Document assumptions for future validation.
```

### Converting user stories to requirements
```
User Story: "As a customer, I want to reset my password so I can regain access to my account"

Extract:
FR-012: Password Reset
Description: System must provide self-service password reset via email verification
Priority: High
Acceptance Criteria:
  - User receives reset link via email within 60 seconds
  - Reset link expires after 24 hours
  - Link is single-use only
  - New password must meet strength requirements
Source: User Story US-087
```

### Identifying hidden non-functional requirements
```
From "Users upload photos", extract:
NFR-015: File Upload Size Limit
Category: Performance, Security
Metric: Max file size 10MB, file types limited to JPEG/PNG/WebP
Rationale: Prevent abuse, ensure reasonable load times
Verification: Integration tests with oversized files

NFR-016: Image Processing
Category: Performance
Metric: Image optimization completes within 5 seconds for 10MB files
Rationale: User should not wait excessively for upload confirmation
Verification: Performance tests with various file sizes
```
