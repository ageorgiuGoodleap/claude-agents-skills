---
name: technical-specification-writing
description: |
  Create comprehensive technical specifications with system boundaries, data models, API contracts,
  and integration points. Use when writing technical specs, creating design documents, defining
  system specifications, documenting technical requirements, designing system architecture, or when
  user mentions technical spec, design document, system specification, data model, API contract,
  integration specification, error handling, edge cases, technical documentation.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Technical Specification Writing

## Overview

Technical specifications bridge the gap between product requirements and implementation. This skill guides you through creating comprehensive technical specs that define system boundaries, data models, API contracts, integration points, and implementation details that engineering teams need to build production systems.

**Key deliverables:**
- System context and scope definition
- Complete data models with schemas and constraints
- Detailed API contracts with error handling
- Integration specifications with retry policies
- Security and performance requirements
- Edge case catalog with solutions

## Output Location

**Default Output Location:** Save all specifications to `~/Documents/claude-code-skills-data/technical-specification-writing/` unless user specifies otherwise. Create the directory if needed.

---

## Workflow

### 1. Understand Context

**Gather inputs:**
- Requirements documents, user stories, or product briefs
- Existing system architecture diagrams
- Current technical documentation
- Stakeholder list (developers, architects, QA, product)
- Budget and timeline constraints

**Ask clarifying questions if needed:**
- What's the primary business goal?
- What systems does this integrate with?
- Are there regulatory or compliance requirements?
- What's the expected scale (users, requests, data volume)?
- What's the timeline and budget?

**Output:** Context summary documenting assumptions, constraints, and stakeholders.

---

### 2. Define System Boundaries

Create a clear picture of what's inside vs outside the system scope.

**System Context Diagram:**

Use ASCII art to show the system and its external dependencies:

```
┌─────────────────────────────────────┐
│      Authentication System          │
│  ┌──────────┐      ┌──────────┐   │
│  │   API    │◄────►│ Database │   │
│  │ Gateway  │      │          │   │
│  └────┬─────┘      └──────────┘   │
└───────┼────────────────────────────┘
        │
   ┌────┼────┐
   ▼    ▼    ▼
[User] [Email] [Analytics]
       Service  Service
```

**Scope Statement:**

Be explicit about what's included and excluded:

```markdown
**In Scope:**
- User registration with email verification
- Login with email/password
- Session management (create, validate, destroy)
- Password reset workflow
- User profile CRUD operations

**Out of Scope (Future Phases):**
- Social login (OAuth)
- Single Sign-On (SSO)
- Multi-factor authentication (MFA)
- Account recovery without email access

**Assumptions:**
- Single-region deployment initially
- English language support only (v1)
- Web and mobile clients (iOS/Android)

**Constraints:**
- Budget: $500/month for infrastructure
- Timeline: 4 weeks for MVP
- Team: 2 backend engineers, 1 frontend engineer
- Must comply with GDPR
```

**Output:** System context diagram and clear scope statement with assumptions.

---

### 3. Design Data Models

Define all entities, relationships, schemas, and constraints.

**Entity Relationship Diagram:**

```
┌─────────────┐         ┌─────────────┐
│     User    │         │   Profile   │
├─────────────┤         ├─────────────┤
│ id (PK)     │────1:1──│ user_id(FK) │
│ email       │         │ name        │
│ password    │         │ bio         │
│ created_at  │         │ avatar_url  │
│ updated_at  │         │ created_at  │
└─────────────┘         └─────────────┘
       │
       │ 1:N
       ▼
┌─────────────┐
│   Session   │
├─────────────┤
│ id (PK)     │
│ user_id(FK) │
│ token       │
│ expires_at  │
│ created_at  │
└─────────────┘
```

**Complete Schema Definition:**

Provide production-ready DDL with indexes and constraints:

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE UNIQUE INDEX idx_users_email ON users(LOWER(email));
CREATE INDEX idx_users_created_at ON users(created_at);

-- Profiles table
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255),
    bio TEXT,
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_profiles_user_id ON profiles(user_id);

-- Sessions table
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

**Document Data Constraints:**
- Email must be unique (case-insensitive)
- Email must be RFC 5322 compliant
- Password hash uses bcrypt with cost factor 12
- Session tokens are cryptographically random (32 bytes, base64-encoded)
- Session expiry: 7 days (normal), 30 days (with "remember me" flag)
- Profile is created automatically on user registration
- Deleting a user cascades to profiles and sessions

**Indexing Strategy:**
- **Primary keys:** UUID v4 for distributed-friendly IDs
- **users.email:** Unique index with case-insensitive matching (LOWER function)
- **sessions.token:** Index for O(1) session validation
- **sessions.expires_at:** Index for efficient cleanup of expired sessions
- **sessions.user_id:** Index for fetching all user sessions

**Output:** Complete ERD, production-ready SQL schemas, and documented constraints.

---

### 4. Define API Contracts

Specify every API endpoint with request/response formats, status codes, and error handling.

**API Design Principles:**

```markdown
**Conventions:**
- RESTful resource-based URLs (e.g., /api/v1/users, not /api/v1/getUser)
- JSON for all request/response bodies
- JWT bearer tokens for authentication
- Semantic HTTP status codes (2xx success, 4xx client error, 5xx server error)
- Consistent error response format across all endpoints
- ISO 8601 timestamps (UTC)
- Pagination with cursor-based approach for scalability
```

**Complete Endpoint Specification:**

For each endpoint, document:

````markdown
### POST /api/v1/auth/register

**Purpose:** Create a new user account

**Authentication:** None (public endpoint)

**Rate Limit:** 5 requests per IP per hour

**Request Body:**
```json
{
  "email": "user@example.com",      // required, RFC 5322 email
  "password": "SecureP@ss123",      // required, min 8 chars, 1 upper, 1 number, 1 special
  "name": "John Doe"                // optional, max 255 chars
}
```

**Success Response (201 Created):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "email_verified": false,
    "created_at": "2025-02-08T10:30:00Z"
  },
  "message": "Account created. Please check your email for verification."
}
```

**Error Responses:**

*400 Bad Request - Validation Error:*
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "password",
        "message": "Password must contain at least one uppercase letter"
      }
    ]
  }
}
```

*409 Conflict:*
```json
{
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "An account with this email already exists"
  }
}
```

*429 Too Many Requests:*
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many registration attempts. Please try again in 1 hour.",
    "retry_after": 3600
  }
}
```
````

**Authentication Specification:**

```markdown
**JWT Bearer Token:**
- Header: `Authorization: Bearer <token>`
- Token format: JWT with HS256 signature
- Token payload:
  ```json
  {
    "sub": "user_id",
    "email": "user@example.com",
    "iat": 1675859400,
    "exp": 1676464200,
    "jti": "session_token_id"
  }
  ```
- Token expiry: 7 days
- Refresh strategy: Issue new token when < 24h remaining
```

**For comprehensive error handling:** See [error_handling.md](references/error_handling.md) for complete error taxonomy, retry logic, circuit breaker patterns, and implementation examples.

**Output:** Complete API specification for all endpoints with examples of every status code.

---

### 5. Specify Integration Points

Document every external service integration with authentication, error handling, and retry policies.

**Integration Template:**

For each integration, specify:

````markdown
### Email Service Integration (SendGrid)

**Purpose:** Send transactional emails (verification, password reset, welcome)

**Authentication:**
- Method: API key
- Storage: Environment variable `SENDGRID_API_KEY`
- Key rotation: Monthly (manual process)

**Base URL:** `https://api.sendgrid.com/v3`

**Rate Limits:**
- Free tier: 100 emails/day
- Paid tier: 100 emails/second
- Current plan: Paid tier

**Retry Policy:**
```python
# Exponential backoff with jitter
max_retries = 3
base_delay = 1  # seconds
for attempt in range(max_retries):
    try:
        send_email()
        break
    except TransientError:
        if attempt == max_retries - 1:
            raise
        delay = (base_delay * 2 ** attempt) + random.uniform(0, 1)
        time.sleep(delay)  # 1s, 2s, 4s (plus jitter)
```

**Error Handling:**
| Status Code | Error Type | Action |
|-------------|------------|--------|
| 401 Unauthorized | Invalid API key | Alert ops team, halt email sending |
| 429 Too Many Requests | Rate limit hit | Backoff and retry, queue if persistent |
| 5xx Server Error | Service outage | Queue for later retry, log incident |
| Network timeout | Connection issue | Retry with backoff |

**Fallback Strategy:**
- Failed emails queued in database (email_queue table)
- Background job retries every 5 minutes
- After 24 hours, mark as failed and alert
````

**Output:** Complete integration specifications with retry policies, error handling, and monitoring.

---

### 6. Document Error Handling Strategy

**For comprehensive error handling patterns:** See [error_handling.md](references/error_handling.md) covering:
- Input validation errors (400)
- Authentication errors (401)
- Authorization errors (403)
- Not found errors (404)
- Conflict errors (409)
- Rate limit errors (429)
- Server errors (500)
- Retry logic (exponential backoff, circuit breaker)
- Error code taxonomy
- Standard error response format

---

### 7. Define Edge Cases

**For comprehensive edge case catalog:** See [edge_cases.md](references/edge_cases.md) covering:
- Concurrent operations (duplicate registrations, double login)
- Token and session management (expired sessions, stale tokens)
- System state conflicts (profile updates, account deletion)
- Network issues (partial failures, connection loss)
- Race conditions (concurrent updates)

**Edge Case Template:**
```markdown
### [Edge Case Name]

**Problem:** [Describe the scenario]

**Without Solution:** [What goes wrong]

**Solution:** [Specific implementation with code/schema]

**Implementation Note:** [Technical details]
```

---

### 8. Define Security Requirements

**For comprehensive security implementation:** See [security_implementation.md](references/security_implementation.md) covering:
- Password security (bcrypt, validation, brute force protection)
- Session management (token generation, storage, lifecycle)
- Email verification (token generation, verification flow)
- API security (HTTPS, CORS, rate limiting, input sanitization, CSRF)
- Data privacy (GDPR compliance, encryption, logging, retention)
- Audit and monitoring (security events, alerts)

---

### 9. Specify Performance Requirements

**For comprehensive performance optimization:** See [performance_optimization.md](references/performance_optimization.md) covering:
- Latency targets (p95 response times)
- Throughput targets (requests per minute)
- Database query performance (indexing, connection pooling)
- Caching strategy (cache-aside, write-through, TTLs)
- Scalability plan (horizontal scaling, database replicas)
- Resource optimization (API server, database, cache sizing)
- Performance testing plan (load tests, spike tests, soak tests)
- Optimization patterns (N+1 queries, pagination, batch operations)

---

### 10. Generate Complete Technical Specification Document

Synthesize all sections into a comprehensive document following this structure:

```markdown
# Technical Specification: [System Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Author:** [Your Name]
**Status:** Draft / Review / Approved

---

## 1. System Overview
### 1.1 Purpose
### 1.2 Scope
### 1.3 System Context
### 1.4 Assumptions and Constraints

## 2. Architecture
### 2.1 High-Level Design
### 2.2 Technology Stack
### 2.3 Component Responsibilities

## 3. Data Models
### 3.1 Entity Relationship Diagram
### 3.2 Schema Definitions
### 3.3 Data Constraints
### 3.4 Indexing Strategy

## 4. API Contracts
### 4.1 API Design Principles
### 4.2 Authentication
### 4.3 Endpoints
### 4.4 Error Response Format

## 5. Integration Specifications
### 5.1 [External Service 1]
### 5.2 [External Service 2]

## 6. Error Handling
See [error_handling.md](references/error_handling.md)

## 7. Edge Cases
See [edge_cases.md](references/edge_cases.md)

## 8. Security
See [security_implementation.md](references/security_implementation.md)

## 9. Performance
See [performance_optimization.md](references/performance_optimization.md)

## 10. Testing Strategy
### 10.1 Unit Tests
### 10.2 Integration Tests
### 10.3 E2E Tests
### 10.4 Performance Tests
### 10.5 Security Tests

## 11. Monitoring and Observability
### 11.1 Metrics
### 11.2 Logging
### 11.3 Alerts
### 11.4 Dashboards

## 12. Deployment
### 12.1 Environments
### 12.2 Deployment Pipeline
### 12.3 Rollback Strategy

## 13. Migration Plan (if applicable)
### 13.1 Current State
### 13.2 Migration Strategy
### 13.3 Rollback Plan

## 14. Open Questions

## 15. Approvals

## 16. Appendices
### Appendix A: Glossary
### Appendix B: References
### Appendix C: Revision History
```

**Output:** Complete technical specification document ready for stakeholder review.

---

## Quality Checks

Before finalizing the specification, verify:

- [ ] System boundaries are crystal clear - No ambiguity about what's in/out of scope
- [ ] All data models include indexes and constraints - Schemas are production-ready
- [ ] API contracts specify all status codes - Every error scenario has an example response
- [ ] Integration points document retry policies - Failure handling is explicit
- [ ] Edge cases have concrete solutions - Not just identified, but solved with code/schema
- [ ] Security requirements address OWASP Top 10 - SQL injection, XSS, authentication, etc.
- [ ] Performance targets are measurable - Specific latency numbers, not "fast"
- [ ] Testing strategy covers all layers - Unit, integration, E2E, performance, security
- [ ] Monitoring includes metrics and alerts - Observability is built in, not bolted on
- [ ] Open questions are documented - Unresolved decisions explicitly called out
- [ ] Examples are concrete - Real JSON payloads, real SQL queries, real code
- [ ] Terminology is consistent - Same terms used throughout document

---

## Common Patterns

### Pattern 1: Synchronous vs Asynchronous Processing

**Synchronous Processing** - Use when:
- Operation is fast (< 1 second)
- User needs immediate feedback
- Failure requires user action
- Examples: Login, form validation, simple CRUD

**Asynchronous Processing** - Use when:
- Operation is slow (> 1 second)
- User doesn't need to wait
- Retries can happen in background
- Examples: Email sending, report generation, batch processing

### Pattern 2: Optimistic vs Pessimistic Locking

**Optimistic Locking** - Use when:
- Conflicts are rare
- Performance is critical
- Pattern: Add version field, check on update
- Examples: Profile updates, document editing

**Pessimistic Locking** - Use when:
- Conflicts are common
- Data corruption must be prevented
- Pattern: SELECT FOR UPDATE
- Examples: Inventory decrement, financial transactions

### Pattern 3: API Versioning

**URL Versioning** (Recommended for REST):
- Example: `/api/v1/users`, `/api/v2/users`
- Pros: Clear, simple, cacheable
- Version only when breaking changes
- Support previous version for 6 months after new release

---

## Anti-Patterns to Avoid

❌ **Vague requirements** - "Should be fast" → ✅ "p95 latency < 200ms under 1000 req/min load"

❌ **Missing error handling** - Only happy path → ✅ Every endpoint has examples for all status codes

❌ **Incomplete edge cases** - "Handle race conditions" → ✅ Specific solution with code

❌ **Security as afterthought** - "Add security later" → ✅ Security requirements from start

❌ **No performance targets** - "Optimize for speed" → ✅ Specific latency/throughput SLAs

❌ **Generic API documentation** - "Returns 400 if invalid" → ✅ Exact JSON with field-level errors

---

## Tips for Effective Specifications

1. **Be concrete**: Use real examples, not placeholders
2. **Be complete**: Cover happy path AND all error scenarios
3. **Be measurable**: Specific numbers, not adjectives
4. **Be consistent**: Same terminology throughout
5. **Be visual**: Diagrams for architecture, ERDs for data
6. **Be explicit**: Don't assume "obvious" implementation details
7. **Be realistic**: Performance targets based on actual capacity planning
8. **Be collaborative**: Mark open questions, involve stakeholders early

---

**Remember**: A good technical specification is detailed enough that an engineer unfamiliar with the feature can implement it correctly without making significant architecture decisions. When in doubt, add more detail or reference the comprehensive guides.
