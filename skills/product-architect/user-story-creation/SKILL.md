---
name: user-story-creation
description: |
  Generate user stories in standard format with acceptance criteria, story points, and dependencies.
  Use when writing user stories, creating backlog items, breaking down epics, performing story mapping,
  defining sprint scope, or when user mentions user stories, backlog, epic breakdown, story points,
  acceptance criteria, sprint planning, as a user, Given/When/Then, agile stories.
---

# User Story Creation

## Overview

Structured process for generating user stories that translate requirements into implementable work items with clear acceptance criteria and effort estimates.

## Output Location

**Default Output Location:** Save all user stories to `~/Documents/claude-code-skills-data/user-story-creation/` unless user specifies otherwise. Create the directory if needed.

## Workflow

### 1. Understand Source Requirements

- Review requirements document (from requirements-gathering skill or user input)
- Identify user personas and their goals
- Understand business priorities and constraints
- Map features to user journeys

### 2. Generate User Stories

**Standard Format:**
````
Story ID: US-XXX

Title: [Concise verb phrase describing the feature]

As a [role/persona]
I want [feature/capability]
So that [benefit/value]

Acceptance Criteria:
Given [context/precondition]
When [action/event occurs]
Then [expected outcome]

Story Points: [1/2/3/5/8/13/21]
Priority: Critical/High/Medium/Low
Dependencies: [US-XXX, US-YYY]
Technical Notes: [Implementation considerations]
````

**Example:**
````
Story ID: US-042

Title: User can register with email and password

As a new visitor
I want to create an account with my email and password
So that I can access personalized features and save my data

Acceptance Criteria:
Given I am on the registration page
When I enter a valid email and strong password (min 8 chars, 1 uppercase, 1 number, 1 special)
Then my account is created and I receive a confirmation email within 60 seconds

Given I am on the registration page
When I enter an email that's already registered
Then I see an error message "This email is already registered" and registration fails

Given I am on the registration page
When I enter a weak password
Then I see validation errors listing the password requirements

Story Points: 5
Priority: Critical
Dependencies: US-005 (Email Service Integration)
Technical Notes: Use bcrypt for password hashing, implement rate limiting on registration endpoint
````

### 3. Define Acceptance Criteria

Use **Given/When/Then** format (Gherkin syntax):

- **Given**: Precondition or context (system state before action)
- **When**: Action or event (what the user does)
- **Then**: Expected outcome (observable result)

**Best Practices:**
- Write 3-5 acceptance criteria per story (main path + edge cases)
- Make criteria testable and measurable
- Cover happy path, error cases, and boundary conditions
- Avoid implementation details in criteria (focus on behavior)
- Include non-functional criteria if relevant (performance, security)

**Example - Multiple Scenarios:**
````
Acceptance Criteria:

Scenario 1: Successful login
Given I have a registered account
When I enter correct email and password
Then I am redirected to dashboard
And I see a welcome message with my name

Scenario 2: Invalid credentials
Given I have a registered account
When I enter incorrect password
Then I see error message "Invalid credentials"
And I remain on login page
And login attempts are logged for security

Scenario 3: Account locked after failed attempts
Given I have failed login 5 times in 10 minutes
When I attempt to login again
Then I see message "Account temporarily locked. Try again in 15 minutes"
And an email is sent to my registered address
````

### 4. Estimate Story Points

Story points represent **complexity and effort**, not time.

**Fibonacci Scale: 1, 2, 3, 5, 8, 13, 21**

- **1 point**: Trivial change (fix typo, update constant)
- **2 points**: Simple feature (add validation, basic CRUD)
- **3 points**: Moderate feature (form with multiple fields, basic API integration)
- **5 points**: Complex feature (authentication flow, data migration)
- **8 points**: Very complex (payment integration, complex business logic)
- **13 points**: Extremely complex (should be broken down into smaller stories)
- **21+ points**: Epic (must be broken down)

**Estimation Factors:**
- Technical complexity (algorithm complexity, new technology)
- Unknowns and research required
- Dependencies on external systems
- Testing complexity
- Risk and uncertainty

**Example Estimates:**
````
US-001: Add "Remember me" checkbox to login form
Story Points: 2 (simple UI change + cookie management)

US-042: User registration with email verification
Story Points: 5 (form validation, hashing, email service integration, error handling)

US-089: Implement two-factor authentication
Story Points: 8 (multiple components: SMS service, QR code generation, backup codes, recovery flow)
````

### 5. Identify Dependencies

Map dependencies between stories:

- **Technical dependencies**: Story B requires Story A's implementation
- **Data dependencies**: Story B needs data from Story A
- **Sequence dependencies**: Story B logically follows Story A in user flow

**Visualization:**
````
US-001 (User Registration) → US-002 (Email Verification) → US-003 (Profile Creation)
                                                         ↘
US-005 (Email Service Setup) → US-006 (Email Templates) →
````

### 6. Break Down Epics

**Epic**: Large user story (13+ points) that must be decomposed.

**Vertical Slicing**: Break by end-to-end user flow (preferred)
````
Epic: User Profile Management (21 points)
↓
US-101: View own profile (3 points)
US-102: Edit profile basic info (5 points)
US-103: Upload profile picture (5 points)
US-104: Change password (3 points)
US-105: Delete account (5 points)
````

**Horizontal Slicing**: Break by technical layer (avoid if possible)
````
❌ Avoid this pattern:
US-201: Build database schema for profiles (5 points)
US-202: Build API endpoints for profiles (8 points)
US-203: Build UI components for profiles (8 points)

Problem: No deliverable user value until all three are done
````

### 7. Create Story Map

Organize stories by user journey and priority:
````
User Journey: Onboarding Flow

Must Have (MVP):
- US-001: User registration
- US-002: Email verification
- US-003: Basic profile creation

Should Have (v1.1):
- US-004: Password reset
- US-005: Social login (Google)

Could Have (v2.0):
- US-006: Two-factor authentication
- US-007: Profile customization themes

Won't Have (Out of scope):
- US-008: Single sign-on (SSO)
````

### 8. Generate Output Document

````markdown
# User Stories: [Feature/Epic Name]
**Version:** 1.0
**Date:** [Current date]
**Author:** Product Architect

## Epic Overview
**Epic ID:** EPIC-001
**Title:** [Epic name]
**Business Goal:** [Why this epic exists]
**Target Users:** [Who will benefit]
**Success Metrics:**
- [Measurable outcome 1]
- [Measurable outcome 2]

## User Personas
**Primary Persona: [Name (Role)]**
- [Characteristic 1]
- [Characteristic 2]
- [Characteristic 3]

**Secondary Persona: [Name (Role)]**
- [Characteristic 1]
- [Characteristic 2]
- [Characteristic 3]

## User Stories

### US-XXX: [Story Title]
**As a** [role/persona]
**I want** [feature/capability]
**So that** [benefit/value]

**Acceptance Criteria:**
```gherkin
Given [context/precondition]
When [action/event occurs]
Then [expected outcome]

Given [context for edge case]
When [different action]
Then [different expected outcome]
```

**Story Points:** X
**Priority:** Critical/High/Medium/Low
**Dependencies:** [US-XXX, US-YYY]
**Technical Notes:**
- [Implementation consideration 1]
- [Implementation consideration 2]
- [Security/performance notes]

**Testing Notes:**
- Unit tests: [what to test]
- Integration tests: [what to test]
- E2E tests: [what to test]

---

[Repeat for all stories]

## Story Dependency Graph
````
US-001 → US-002 → US-003
  ↓       ↓
US-005 → US-006
````

## Sprint Allocation

**Sprint 1 (2 weeks - [X] points capacity):**
- US-XXX: [Story title] (X points)
- US-XXX: [Story title] (X points)
- US-XXX: [Story title] (X points)
**Total: X points**

**Sprint 2 (2 weeks - [X] points capacity):**
- US-XXX: [Story title] (X points)
- US-XXX: [Story title] (X points)
**Total: X points**

## Risks and Mitigations
- **Risk:** [Identified risk]
  - **Mitigation:** [How to address it]
- **Risk:** [Another risk]
  - **Mitigation:** [How to address it]

## Definition of Done
- [ ] Code implemented and peer reviewed
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passing
- [ ] Manual QA testing completed
- [ ] Acceptance criteria verified by Product Owner
- [ ] Documentation updated
- [ ] Deployed to staging environment
````

## Quality Checks

Before presenting user stories, verify:

- [ ] Every story follows "As a/I want/So that" format
- [ ] All acceptance criteria use Given/When/Then format
- [ ] Story points are assigned using Fibonacci scale
- [ ] Stories with 13+ points are broken down into smaller stories
- [ ] Dependencies are identified and documented
- [ ] Priorities align with business goals
- [ ] Each story is independently deliverable (vertical slice)
- [ ] Technical notes include security and performance considerations
- [ ] Testing approach is specified
- [ ] Sprint allocation doesn't exceed team velocity

## Common Patterns

**Anti-pattern: Technical stories**
````
❌ Bad: "Create user table in database"
✅ Good: "As a new visitor, I want to register an account, so that I can save my preferences"
````

**Anti-pattern: Too large**
````
❌ Bad: "Implement entire user management system" (21 points)
✅ Good: Break into registration, login, profile, password reset (5 points each)
````

**Anti-pattern: Implementation details in story**
````
❌ Bad: "As a developer, I want to use JWT for authentication"
✅ Good: "As a user, I want to stay logged in across sessions, so that I don't have to re-enter credentials"
````

**Pattern: Spike stories for unknowns**
````
When facing high uncertainty:
US-SPIKE-01: Research OAuth2 integration with Google
- Time-box: 4 hours
- Output: Technical feasibility document
- Story Points: 2
````

**Pattern: Non-functional requirements as stories**
````
US-NFR-01: System must handle 1000 concurrent users
As a system administrator
I want the application to support 1000 concurrent users with <2s response time
So that the system remains responsive under normal load

Acceptance Criteria:
Given 1000 concurrent users are active
When they perform typical operations (login, browse, search)
Then 95th percentile response time is under 2 seconds
And no requests fail due to timeout
````
