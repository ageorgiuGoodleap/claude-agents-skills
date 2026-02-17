---
name: integration-architecture
description: |
  Design API contracts, event schemas, and integration patterns for system communication.
  Use when user asks to design integration architecture, create API contracts, plan third-party
  integrations, design webhooks, plan event-driven architecture, design message queues, create REST/GraphQL/gRPC
  APIs, plan pub/sub patterns, design saga patterns, create API gateway architecture, or implement circuit breakers.
allowed-tools: Read, Write, Edit
---

# Integration Architecture

Design API contracts, event schemas, integration patterns, and error handling for inter-service and third-party communication.

## Workflow

### 1. Identify Integration Points
- List services needing communication
- Identify third-party systems (payment, email, SMS, analytics)
- Map data flows
- Determine synchronous vs asynchronous needs
- Note latency requirements and SLAs

### 2. Select Integration Patterns

**Synchronous**:
- **REST API**: CRUD operations, human-readable, wide compatibility, standard HTTP
- **GraphQL**: Flexible data fetching, multiple resources in one request, strong typing, complex dashboards/mobile
- **gRPC**: High-performance inter-service, protocol buffers, bi-directional streaming, microservices

**Asynchronous**:
- **Message Queue**: Decoupling producers/consumers, load leveling, guaranteed delivery, point-to-point (task processing, orders)
- **Pub/Sub (Event Bus)**: Multiple consumers per event, broadcasting state changes, loose coupling (notifications, data sync)
- **Webhooks**: Third-party pushes events, real-time notifications (payment confirmations, GitHub events)

### 3. Design API Contracts

**REST Naming**: Use nouns (plural), hierarchical (/users/{id}/orders), max 2-3 levels nesting

**HTTP Methods**: GET (retrieve), POST (create), PUT (replace), PATCH (update partial), DELETE (remove)

**Status Codes**: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Validation Error, 429 Rate Limit, 500 Internal Server Error, 503 Service Unavailable

Use OpenAPI 3.0 specification for documentation. Include: endpoints, parameters, request/response schemas, status codes, authentication.

### 4. Design Event Schemas

**Naming**: Past tense (UserCreated, OrderPlaced, PaymentProcessed) or domain.action (user.created, order.placed)

**Structure**: event_id, event_type, event_version, timestamp, source, correlation_id, data, metadata

**Versioning**: Include version in type (user.created.v1), support multiple versions during migration, use adapters to convert.

**Event Catalog**: For each event document producer, consumers, guaranteed delivery, schema.

### 5. Design Error Handling and Retry Logic

**Retry Strategy**: Exponential backoff (1s, 2s, 4s, 8s, 16s), max 5 attempts, jitter ±10%

**Idempotency**: Use idempotency keys for critical operations (payment, order creation), store result with key (24hr TTL), return cached result if duplicate.

**Dead Letter Queue**: Failed messages after max retries → DLQ, retention 14 days, alert on depth >10, manual review/replay.

### 6. Design Rate Limiting

**Strategy**: Token bucket (capacity = burst, refill rate = sustained) or sliding window

**Limits**: Public endpoints (100/hr per IP), authenticated (1000/hr per user), admin (500/hr), webhooks (10/min)

**Headers**: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After

**Response on Exceeded**: 429 with error code, message, retry_after

### 7. Design Circuit Breaker

**States**: Closed (normal), Open (failure threshold exceeded, fail fast), Half-Open (testing recovery)

**Configuration**: Failure threshold (5 consecutive failures), timeout (30s before trying half-open), success threshold (2 successes to close from half-open)

### 8. Design Webhook Integration

**Delivery**: POST to configured URL, include signature (HMAC-SHA256) for verification, retry on failure (exponential backoff), timeout 30s

**Signature**: Generate HMAC(payload, secret), send in X-Webhook-Signature header, receiver verifies with hmac.compare_digest

**Retry Policy**: Immediate, 1min, 5min, 30min, 2hr → give up after 5 attempts

### 9. Design API Gateway

**Responsibilities**: Authentication/authorization, request routing, rate limiting, request/response transformation, caching, logging/monitoring

**Configuration**: Routes (path, service, methods, auth required, rate limit, timeout, cache TTL), auth (JWT secret/algorithm), rate limiting (Redis backend), logging (level, format)

### 10. Design Saga Pattern (distributed transactions)

**Choreography** (event-driven): Each service publishes events, others subscribe and react, compensating transactions on failure (reverse order)

**Orchestration** (coordinator): Central orchestrator calls services in sequence, executes compensating transactions if any step fails

Use for multi-service transactions where ACID not feasible, eventual consistency acceptable.

### 11. Document Integration Specifications

Create markdown document with:
- Executive summary (pattern, API style, message broker, API gateway, third-party integrations)
- Integration overview diagram
- Synchronous communication (REST/GraphQL/gRPC contracts with OpenAPI/schema)
- Asynchronous communication (message broker config, event catalog with schemas)
- Error handling (retry policy, idempotency, DLQ)
- Rate limiting (strategy, limits per endpoint category, headers, response format)
- Circuit breaker configuration (per-service thresholds, timeout, fallback)
- Webhook specifications (delivery guarantees, payload format, signature verification, retry policy)
- Third-party integrations (per service: purpose, auth, endpoints, rate limits, error handling, fallback)
- Security (authentication, authorization, data protection)
- Monitoring and alerting (metrics, alert thresholds)

## Key Patterns

**REST API + Event-Driven Side Effects**: User action via API, immediate response, publish event for background processing

**API Gateway + Service Mesh**: Centralized auth/routing (gateway), service-to-service mTLS/observability (mesh)

**Saga with Compensation**: Distributed transaction with rollback capability (choreography or orchestration)

**Webhook Fan-Out with Retry**: Multiple clients, parallel delivery, exponential backoff

## Critical Anti-Patterns

**Synchronous Chain of Calls**: Latency compounds, failure cascades; use async for non-critical paths

**Shared Database Integration**: Tight coupling through schema; each service owns data, integrate via APIs/events

**Unbounded Retries**: Exponential backoff, max attempts, circuit breaker required

**No Idempotency**: Critical operations need idempotency keys to prevent duplicates

**Missing Webhook Signature**: Always verify webhook signatures to prevent spoofing
