---
name: jira-ticket-writer
description: |
  Generates comprehensive Jira ticket descriptions from task requirements and code analysis.
  Use when the user asks to create, write, generate, or document a Jira ticket, story, task,
  or issue. Also use when documenting completed work from PRs/MRs, creating feature specs,
  or generating engineering documentation for cross-functional visibility. Trigger phrases
  include "create a Jira ticket", "write up this work", "document this PR", "generate a ticket",
  or any request for structured engineering task documentation.
---

# Jira Ticket Writer

Technical product management skill for documenting engineering work with comprehensive, actionable Jira ticket descriptions.

## Overview

This skill generates complete, copy-paste-ready Jira ticket descriptions by analyzing task requirements and optional code changes. It creates clear, actionable documentation suitable for cross-functional visibility and audit trails.

## Output Location

Unless specified by the user, save all output files to:
```
~/Documents/claude-code-skills-data/jira-ticket-writer/
```

## Process

### 1. Input Collection

Accept:
- **Required**: Task description (what needs to be built, fixed, or changed)
- **Optional**: PR/MR URL for completed work documentation
- **Optional**: Related ticket links or dependencies

Parse input for:
- Explicit requirements or acceptance criteria
- Technical constraints mentioned
- User impact or business value
- References to existing systems or components

### 2. Code Analysis (if PR provided)

When PR/MR URL is provided:
- Use `gh pr view <number>` (GitHub) or `glab mr view <number>` (GitLab) to fetch details
- Extract changed files, added dependencies, config updates
- Identify affected components from file paths and imports
- Determine implementation approach from diff analysis

### 3. Codebase Context (if no PR provided)

If documenting future work:
- Use `Grep` and `Glob` to identify relevant existing code
- Locate similar implementations or patterns to reference
- Identify components that will be affected
- Find related configuration or infrastructure files

### 4. Clarification Phase

Ask 2-4 targeted questions using `AskUserQuestion` only if critical information is missing:

**For new features/tasks:**
1. "What triggered this work?" → Options: user request | bug report | technical debt | compliance | other
2. "Who is impacted?" → Options: end users | internal team | specific role | system-to-system
3. "Priority and timeline?" → Options: urgent/blocker | high/this sprint | medium/next sprint | low/backlog

**For documentation of completed work:**
1. "What problem did this solve?" → (provide 1-2 sentence context)
2. "Any follow-up work required?" → Options: yes with details | no

Do not ask questions whose answers are evident from the PR diff or task description.

### 5. Ticket Generation

Create `JIRA_TICKET.md` using the template structure below.

## Ticket Template

### Title Format
```
[Type] Brief, actionable description
```

**Types:**
- `[Feature]` - New functionality
- `[Bug]` - Defect correction
- `[Task]` - Engineering work without user-facing changes
- `[Tech Debt]` - Refactoring or cleanup
- `[Spike]` - Research or investigation

**Title Examples:**
- `[Feature] Add OAuth2 authentication for API endpoints`
- `[Bug] Fix race condition in payment processing queue`
- `[Tech Debt] Extract database layer into separate service`

---

### Complete Ticket Structure

```markdown
# [Title]

## Description

**What**: 2-3 sentences describing what this ticket accomplishes and who benefits.

**Why**: 1-2 sentences explaining the business or technical motivation.

**Success Criteria**: Bullet list of measurable outcomes that define "done."
- User can [specific action] without [specific problem]
- System maintains [performance/reliability metric]
- Team has [tooling/documentation/capability]

---

## Current State

**Behavior**: How the system works today (or doesn't).

**Limitations**: Specific pain points, gaps, or failures.

**Data Points**: Error rates, user complaints, performance metrics if available.

If documenting completed work: "Issue resolved as of [date/PR]."

---

## Target State

**Expected Behavior**: How the system should work after this ticket.

**User Experience**: What users will be able to do that they couldn't before.

**Technical Outcome**: Architecture, performance, or reliability improvements achieved.

Use concrete examples: "User authentication completes in <200ms" not "Authentication is faster."

---

## Scope

**In Scope:**
- Specific features, components, or changes included
- Boundaries of this work defined clearly

**Out of Scope:**
- Related work explicitly deferred
- Similar features not addressed
- Future enhancements planned separately

**Dependencies:**
- Upstream: Work that must complete before this starts
- Downstream: Work blocked by this ticket
- Related tickets: [PROJ-123], [PROJ-456]

---

## Technical Implementation

**Approach**: High-level strategy (1-2 paragraphs).
- Architecture pattern used (e.g., middleware, pub/sub, microservice extraction)
- Key technology choices and why
- Integration points with existing systems

**Key Changes**:
- Core logic modifications (reference specific modules/files if known)
- Database schema changes (migrations, new tables, indexes)
- API changes (new endpoints, modified contracts, breaking changes)
- Configuration updates (env vars, feature flags, infrastructure)

**Testing Strategy**:
- Unit test coverage for [specific logic]
- Integration tests for [system interactions]
- Manual verification steps

**Risks and Mitigations**:
- Potential failure modes identified
- Rollback strategy
- Performance or security considerations

---

## Affected Components

Organized by system layer:

**Backend:**
- `component-name` - [Brief description of change]
- `service-name` - [What changed and why]

**Frontend:**
- `page/feature` - [UI changes or new screens]
- `component-library` - [Shared component updates]

**Infrastructure:**
- `database` - [Schema/query changes]
- `cache` - [Redis/caching strategy updates]
- `deployment` - [CI/CD, environment config]

**Third-Party:**
- `external-api` - [New integrations or updated contracts]
- `monitoring` - [New metrics, alerts, dashboards]

If unknown: "To be determined during implementation."

---

## Acceptance Criteria

Checklist format for QA validation:
- [ ] [Specific functional requirement verified]
- [ ] [Performance threshold met]
- [ ] [Error handling validated]
- [ ] [Documentation updated]
- [ ] [Tests pass in CI]
- [ ] [Security review completed] (if applicable)
- [ ] [Stakeholder sign-off] (if required)

---

## Additional Context

(Optional sections as needed)

**References:**
- Design docs: [Link]
- API documentation: [Link]
- Related incidents: [Link to postmortem]

**Open Questions:**
- [Question requiring PM/leadership decision]
- [Technical uncertainty requiring spike]
```

## Output Delivery

1. Save to `JIRA_TICKET.md` in the output directory
2. Display markdown for immediate copy-paste into Jira
3. Suggest: "Use Jira's markdown mode or convert to Jira wiki markup if needed"

## Quality Guidelines

**The ticket must be:**
- Actionable by an engineer who didn't participate in planning
- Explicit about what's unknown (avoid assumptions)
- Written in present tense for current state, future tense for target state
- Detailed enough for accurate estimation but not implementation-level
- Based on actual implementation if PR is provided, not proposed approach

## Anti-Patterns to Avoid

- Vague descriptions like "improve performance" without specifics
- Internal slack threads or ephemeral links
- Implementation details that belong in code comments
- Tickets for completed work without PR context
- Placeholder text like "TBD" without flagging as requiring follow-up
- Generic success criteria that could apply to any ticket
- Over-specified implementation that constrains engineering decisions

## Example: Feature Ticket

```markdown
# [Feature] Add OAuth2 authentication for API endpoints

## Description

**What**: Implement OAuth2 authentication flow for all public API endpoints, enabling third-party applications to securely access user data with proper authorization scopes.

**Why**: Current API uses basic auth which doesn't support granular permissions or token revocation. Partners need secure, scoped access for integrations.

**Success Criteria**:
- Third-party apps can authenticate using OAuth2 authorization code flow
- Token refresh works automatically for long-lived sessions
- Users can revoke app access from account settings
- API maintains <100ms auth overhead per request

---

## Current State

**Behavior**: API endpoints use HTTP Basic Authentication with username/password sent in every request header.

**Limitations**:
- No granular permissions (apps get full account access)
- Password exposure risk in third-party applications
- No token expiration or revocation mechanism
- Partners reluctant to integrate due to security concerns

**Data Points**: 3 enterprise partners blocked on integrations, 12 support tickets about credential management

---

## Target State

**Expected Behavior**: API supports OAuth2 authorization code flow with scoped tokens and refresh capability.

**User Experience**:
- Users authorize apps once via web interface
- Apps receive time-limited access tokens
- Users can view and revoke app permissions in settings
- Tokens refresh automatically without user interaction

**Technical Outcome**: API authentication response time <100ms, 99.9% auth success rate, zero password exposure in partner apps.

---

## Scope

**In Scope:**
- OAuth2 authorization server implementation
- Token generation, validation, and refresh endpoints
- Scope-based permission system (read, write, admin scopes)
- User consent and authorization UI
- Token revocation endpoint
- Migration guide for existing API users

**Out of Scope:**
- OAuth1 support (deprecated standard)
- Social login providers (Google, GitHub) - future enhancement
- Multi-factor authentication for OAuth flow - covered in PROJ-456
- Rate limiting per token - existing system applies

**Dependencies:**
- Upstream: User permissions model refactor (PROJ-789) must complete first
- Downstream: Partner integration guides (PROJ-790) blocked by this
- Related: API rate limiting review (PROJ-791)

---

## Technical Implementation

**Approach**: Implement OAuth2 using authorization code flow with PKCE. Use JWT for access tokens, opaque tokens for refresh. Build on existing user session management.

Architecture:
- Authorization server as new microservice (auth.example.com)
- Token validation middleware in API gateway
- Token storage in Redis with TTL, refresh tokens in PostgreSQL
- Scope enforcement in existing permission middleware

**Key Changes**:
- New auth-service microservice (Node.js/Express)
  - Authorization endpoint: GET /oauth/authorize
  - Token endpoint: POST /oauth/token
  - Revocation endpoint: POST /oauth/revoke
- API gateway updates
  - Token validation middleware in src/middleware/oauth.ts
  - Scope checking in src/middleware/permissions.ts
- Database schema
  - oauth_clients table (client_id, secret, redirect_uris)
  - oauth_grants table (grant codes, expiration)
  - oauth_tokens table (access/refresh tokens, scopes)
- User settings UI
  - New page: /settings/authorized-apps
  - Revoke token functionality

**Testing Strategy**:
- Unit tests for token generation/validation logic
- Integration tests for full OAuth flow
- Security tests for token tampering, replay attacks
- Load tests for token validation performance (<100ms requirement)
- Manual testing with sample third-party app

**Risks and Mitigations**:
- Risk: Token validation latency impacts API response time
  - Mitigation: Redis cache for token validation, 5min cache TTL
- Risk: Breaking change for existing API users
  - Mitigation: Support basic auth for 6 months, migration guide, email campaign
- Risk: Security vulnerabilities in OAuth implementation
  - Mitigation: Use battle-tested library (node-oauth2-server), security audit before launch

---

## Affected Components

**Backend:**
- `auth-service` - New microservice for OAuth2 authorization server
- `api-gateway` - Token validation middleware, scope enforcement
- `user-service` - Token revocation, authorized apps listing

**Frontend:**
- `settings/authorized-apps` - New page for managing app permissions
- `oauth-consent` - New OAuth authorization consent screen

**Infrastructure:**
- `database` - Three new tables (oauth_clients, oauth_grants, oauth_tokens)
- `redis` - Token validation cache with 5min TTL
- `deployment` - New auth-service deployment, environment variables for secrets
- `nginx` - New subdomain routing for auth.example.com

**Third-Party:**
- `monitoring` - New metrics: token_generation_time, token_validation_time, auth_success_rate
- `logging` - Structured logs for OAuth flow events

---

## Acceptance Criteria

- [ ] Third-party app can complete authorization code flow and receive access token
- [ ] Access tokens expire after 1 hour, refresh tokens after 30 days
- [ ] Token refresh works without user re-authentication
- [ ] Scope enforcement blocks access to out-of-scope resources
- [ ] User can view authorized apps in settings UI
- [ ] User can revoke app access (tokens immediately invalidated)
- [ ] Token validation completes in <100ms (p95)
- [ ] Migration guide published with code examples
- [ ] Security audit completed with no critical findings
- [ ] Documentation updated (API reference, integration guide)
- [ ] Existing basic auth continues to work during migration period

---

## Additional Context

**References:**
- OAuth2 RFC: https://tools.ietf.org/html/rfc6749
- PKCE RFC: https://tools.ietf.org/html/rfc7636
- Security audit requirements: [Link to security doc]

**Open Questions:**
- Should we support client credentials flow for server-to-server integrations? (Decision needed from PM)
- Token storage duration: 30 days for refresh tokens acceptable for compliance? (Legal review pending)
```

## Example: Bug Fix Ticket

```markdown
# [Bug] Fix race condition in payment processing queue

## Description

**What**: Resolve race condition causing duplicate charge attempts when multiple workers process the same payment job concurrently.

**Why**: Production incidents showing double charges to customers (8 cases in last 2 weeks), causing refund requests and support escalations. Critical business impact.

**Success Criteria**:
- Zero duplicate charge attempts in production
- Payment job picked up by exactly one worker
- No increase in payment processing latency
- Monitoring alert when race condition is detected

---

## Current State

**Behavior**: Payment queue workers poll Redis queue every 100ms. When job found, worker processes payment but doesn't acquire lock before starting. If two workers poll simultaneously, both see same job.

**Limitations**: Redis LPOP operation not atomic with job processing. Window of 50-150ms where multiple workers can grab same job.

**Data Points**:
- 8 duplicate charges in 14 days
- Occurs during high-traffic periods (12pm-2pm, 6pm-8pm)
- Average duplicate window: 87ms
- Customer refunds: $1,247

---

## Target State

**Expected Behavior**: Worker acquires distributed lock before processing payment job. Lock held until job completes or times out.

**User Experience**: Customers charged exactly once per transaction, no duplicate charge errors, no refund delays.

**Technical Outcome**: Zero race conditions in payment processing. Lock acquisition adds <10ms overhead.

---

## Scope

**In Scope:**
- Distributed lock implementation using Redis SET NX
- Lock timeout and cleanup mechanism
- Retry logic for failed lock acquisition
- Monitoring for lock contention
- Alerting for suspected race conditions

**Out of Scope:**
- Refactoring entire payment queue system - covered in PROJ-892
- Payment retry logic improvements - separate ticket
- Database transaction isolation changes - not needed with lock

**Dependencies:**
- No upstream blockers
- Downstream: Refund automation tool (PROJ-893) can proceed after this
- Related: Payment monitoring dashboard (PROJ-894)

---

## Technical Implementation

**Approach**: Use Redis SET NX (set if not exists) with expiration for distributed lock. Worker attempts lock before processing job. If lock acquisition fails, skip job (another worker has it).

**Key Changes**:
- src/workers/payment-processor.ts:
  - Add acquireLock(jobId) method using Redis SET NX with 60s TTL
  - Wrap processPayment() with lock acquisition check
  - Add releaseLock(jobId) in finally block
  - Add lock timeout monitoring
- src/monitoring/payment-metrics.ts:
  - New metric: payment_lock_contention_total
  - New metric: payment_lock_timeout_total
  - New alert: duplicate_charge_attempt (triggers on lock already held)

**Testing Strategy**:
- Unit tests: Lock acquisition/release logic
- Integration tests: Simulate concurrent workers processing same job
- Load tests: High-traffic scenario with 50+ workers
- Chaos tests: Worker crash during lock hold (verify timeout cleanup)

**Risks and Mitigations**:
- Risk: Worker crashes while holding lock, job stuck until timeout
  - Mitigation: 60s lock TTL, dead letter queue for timed-out jobs
- Risk: Lock acquisition increases latency
  - Mitigation: Target <10ms overhead, monitor p95 latency
- Risk: Network partition causes split-brain scenario
  - Mitigation: Redis cluster consensus, job idempotency key in payment service

---

## Affected Components

**Backend:**
- `payment-worker` - Lock acquisition logic, retry handling
- `redis-client` - Distributed lock implementation

**Infrastructure:**
- `monitoring` - New lock contention and timeout metrics
- `alerting` - Duplicate charge attempt alert

---

## Acceptance Criteria

- [ ] Payment worker acquires lock before processing job
- [ ] Lock released after successful payment processing
- [ ] Lock released after payment failure (no lock leak)
- [ ] Lock timeout (60s) triggers automatic cleanup
- [ ] Concurrent workers cannot process same job (integration test passes)
- [ ] Lock acquisition adds <10ms to processing time (p95)
- [ ] Alert fires when duplicate charge attempt detected
- [ ] Production testing: No duplicate charges for 7 days post-deployment
- [ ] Runbook updated with lock troubleshooting steps

---

## Additional Context

**References:**
- Incident postmortem: [Link]
- Redis distributed locking: https://redis.io/docs/manual/patterns/distributed-locks/
- Payment processing architecture: [Link]

**Open Questions:**
- None - approach validated with payments team
```
