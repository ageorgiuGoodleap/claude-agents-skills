# Error Handling Strategy

Comprehensive error handling patterns for technical specifications.

## Error Handling Framework

### 1. Input Validation Errors (400 Bad Request)

**When:** Client sends invalid data

**Handling:**
- Validate all inputs before processing
- Return detailed field-level errors
- Include validation rules in error message

**Example Scenarios:**
- Invalid email format → `{ field: "email", message: "Email format is invalid" }`
- Weak password → `{ field: "password", message: "Password must contain at least one uppercase letter" }`
- Missing required field → `{ field: "name", message: "Name is required" }`

### 2. Authentication Errors (401 Unauthorized)

**When:** User credentials are invalid or missing

**Handling:**
- Return generic message (don't reveal if email exists)
- Rate limit login attempts (5 per 15 minutes)
- Log failed attempts for security monitoring

**Example Scenarios:**
- Wrong password → `"Invalid email or password"`
- Expired session → `"Session expired. Please log in again."`
- Missing auth header → `"Authentication required"`

### 3. Authorization Errors (403 Forbidden)

**When:** User lacks permission for the resource

**Handling:**
- Return clear message about missing permission
- Don't reveal resource details if user shouldn't know it exists

**Example Scenarios:**
- Unverified email accessing protected resource → `"Email verification required"`
- User accessing another user's profile → `"Access denied"`

### 4. Not Found Errors (404 Not Found)

**When:** Resource doesn't exist

**Handling:**
- Return generic "not found" for security (don't confirm existence)
- Log suspicious patterns (enumeration attacks)

**Example Scenarios:**
- Invalid user ID → `"User not found"`
- Invalid session token → `"Session not found"`

### 5. Conflict Errors (409 Conflict)

**When:** Resource already exists or state conflict

**Handling:**
- Clearly explain the conflict
- Suggest resolution steps

**Example Scenarios:**
- Duplicate email registration → `"An account with this email already exists"`
- Concurrent update with stale data → `"Resource was modified. Please refresh and try again."`

### 6. Rate Limit Errors (429 Too Many Requests)

**When:** Client exceeds rate limit

**Handling:**
- Include `Retry-After` header (seconds until reset)
- Return clear message about limit and reset time
- Different limits for different endpoints

**Rate Limits:**
- Registration: 5 per hour per IP
- Login: 5 per 15 minutes per IP
- Password reset: 3 per hour per email
- API endpoints (authenticated): 1000 per hour per user

**Example Response:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many login attempts. Please try again in 15 minutes.",
    "retry_after": 900
  }
}
```

### 7. Server Errors (500 Internal Server Error)

**When:** Unexpected server-side failure

**Handling:**
- Log full stack trace and context
- Return generic message to client (don't leak internals)
- Include request ID for support tracking
- Alert on-call engineer if error rate spikes

**Example Scenarios:**
- Database connection failure
- External service timeout
- Unhandled exception

**Example Response:**
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred. Please try again later.",
    "request_id": "req_abc123xyz"
  }
}
```

---

## Retry Logic Implementation

### Idempotency

- Use idempotency keys for POST/PUT/PATCH requests
- Store processed keys in cache (Redis, 24h TTL)
- Return cached response for duplicate requests

### Exponential Backoff

```python
def retry_with_exponential_backoff(func, max_retries=3):
    """Retry transient failures with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError as e:
            if attempt == max_retries - 1:
                raise  # Give up after max retries
            delay = (2 ** attempt) + random.uniform(0, 1)  # 1s, 2s, 4s + jitter
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s")
            time.sleep(delay)
```

### Circuit Breaker

```python
# Stop calling failing service after threshold
circuit_breaker = {
    "failure_threshold": 5,  # Open circuit after 5 failures
    "success_threshold": 2,  # Close circuit after 2 successes
    "timeout": 60,  # Try again after 60 seconds
}
```

---

## Error Code Taxonomy

Create a consistent error vocabulary:

| Error Code | HTTP Status | Description | Client Action |
|------------|-------------|-------------|---------------|
| VALIDATION_ERROR | 400 | Input validation failed | Fix input and retry |
| AUTHENTICATION_ERROR | 401 | Invalid or missing credentials | Re-authenticate |
| AUTHORIZATION_ERROR | 403 | Insufficient permissions | Don't retry, show access denied |
| NOT_FOUND | 404 | Resource doesn't exist | Don't retry |
| CONFLICT | 409 | Resource already exists or state conflict | Resolve conflict, don't retry blindly |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests | Wait for retry_after seconds |
| INTERNAL_ERROR | 500 | Server error | Retry with exponential backoff |
| SERVICE_UNAVAILABLE | 503 | Temporary outage | Retry with exponential backoff |

---

## Error Response Format

Standard error schema for all endpoints:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": [
      {
        "field": "field_name",
        "message": "Field-specific error"
      }
    ],
    "request_id": "req_unique_id",
    "retry_after": 3600
  }
}
```

**Fields:**
- `code`: Machine-readable error identifier (required)
- `message`: Human-readable description (required)
- `details`: Array of field-level errors (optional, for validation errors)
- `request_id`: Unique request identifier for support (required for 5xx errors)
- `retry_after`: Seconds until retry allowed (required for 429 errors)
