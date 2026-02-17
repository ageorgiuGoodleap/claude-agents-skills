# API Security Architecture Patterns

## Overview

This document covers security patterns for REST APIs, GraphQL APIs, and API gateways, including authentication, authorization, rate limiting, input validation, and output filtering.

## API Gateway Pattern

**Architecture:**
```
Client → [1] API Gateway → [2] Backend Services
              ↓
        [Authentication]
        [Authorization]
        [Rate Limiting]
        [Input Validation]
        [Logging]
```

**Gateway Responsibilities:**
- Authentication (JWT validation, API key verification)
- Authorization (role checks, scope validation)
- Rate limiting (per-user, per-IP, per-endpoint)
- Request validation (schema, size limits)
- Response transformation (remove sensitive fields)
- Logging and monitoring
- TLS termination

## Core API Security Controls

### 1. Authentication

**JWT Validation:**
```
1. Verify signature (using public key)
2. Check expiration (exp claim)
3. Validate issuer (iss claim)
4. Validate audience (aud claim)
5. Check not-before (nbf claim)
```

**API Key Security:**
- Use strong random keys (32+ characters)
- Rotate regularly (90 days)
- Hash keys in database
- Rate limit by API key
- Monitor for leaked keys

### 2. Authorization

**Scope-Based (OAuth2):**
```
Access Token contains scopes: "read:users write:documents"

POST /api/documents → requires "write:documents" scope
GET /api/users → requires "read:users" scope
```

**Resource-Based:**
```
GET /api/documents/123
1. Validate JWT
2. Extract user ID from token
3. Query database: does user have access to document 123?
4. If yes, return document; if no, return 403
```

### 3. Rate Limiting

**Strategies:**

| Strategy | When to Use | Example Limits |
|----------|-------------|----------------|
| Per-User | Prevent individual user abuse | 100 req/min per user |
| Per-IP | Prevent anonymous abuse | 1000 req/min per IP |
| Per-Endpoint | Protect expensive operations | 10 req/min for /search |
| Global | Protect overall system | 100,000 req/min total |

**Implementation (Token Bucket Algorithm):**
```
For each user/IP:
- Bucket capacity: 100 tokens
- Refill rate: 100 tokens per minute
- Each request consumes 1 token
- When bucket empty, return 429 Too Many Requests
```

**Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1625097600
Retry-After: 60
```

### 4. Input Validation

**JSON Schema Validation:**
```json
{
  "type": "object",
  "properties": {
    "email": {"type": "string", "format": "email"},
    "age": {"type": "integer", "minimum": 0, "maximum": 150},
    "name": {"type": "string", "minLength": 1, "maxLength": 100}
  },
  "required": ["email", "name"],
  "additionalProperties": false
}
```

**Size Limits:**
- Request body: 10 MB max (adjust per endpoint)
- URL length: 2048 characters max
- Header size: 8 KB max
- Number of headers: 100 max

**Content-Type Validation:**
- Expect: `application/json`
- Reject: `text/html`, `application/xml` (unless explicitly supported)
- Validate actual content matches Content-Type header

### 5. Output Filtering

**Remove Sensitive Fields:**
```python
def filter_user_response(user, requester_role):
    safe_fields = ['id', 'name', 'email']
    
    if requester_role == 'admin':
        safe_fields += ['phone', 'address', 'created_at']
    
    # Remove sensitive fields not in safe_fields
    return {k: v for k, v in user.items() if k in safe_fields}
```

**Data Masking:**
```
SSN: 123-45-6789 → ***-**-6789
Credit Card: 4532-1234-5678-9010 → ****-****-****-9010
Email: john.doe@example.com → j***.***@example.com
```

## API Security Headers

**Essential Headers:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: no-referrer
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

## REST API Security Patterns

### GET Requests

**Security Considerations:**
- No sensitive data in URL (logged, cached, visible in browser history)
- Validate query parameters
- Implement pagination (limit, offset)
- Cache control headers

**Example:**
```
GET /api/users?limit=20&offset=0&sort=created_at
Authorization: Bearer <jwt>

Validation:
- limit ≤ 100 (prevent large responses)
- offset ≥ 0
- sort in allowed fields
```

### POST/PUT/DELETE Requests

**Security Considerations:**
- Validate Content-Type header
- Require authentication
- Check authorization (can user perform this action?)
- Implement idempotency (prevent duplicate operations)
- Use CSRF tokens (for browser-based clients)

**Example:**
```
POST /api/documents
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "title": "My Document",
  "content": "Document content"
}

Validation:
1. Verify JWT signature and expiration
2. Check user has "write:documents" scope
3. Validate request body against JSON schema
4. Check request size ≤ 10 MB
5. Sanitize inputs
6. Process request
```

## GraphQL API Security

**Key Differences from REST:**
- Single endpoint (usually `/graphql`)
- Client controls response shape
- Nested queries (depth, breadth concerns)
- Introspection (can expose schema)

**Security Controls:**

### Query Depth Limiting
```javascript
// Prevent deeply nested queries
const depthLimit = require('graphql-depth-limit');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(5)] // Max depth: 5
});
```

### Query Complexity Analysis
```javascript
// Prevent expensive queries
const queryComplexity = require('graphql-query-complexity');

const server = new ApolloServer({
  validationRules: [
    queryComplexity({
      maximumComplexity: 1000,
      variables: {},
      onComplete: (complexity) => {
        console.log('Query complexity:', complexity);
      },
    }),
  ],
});
```

### Disable Introspection in Production
```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
});
```

### Field-Level Authorization
```javascript
const resolvers = {
  User: {
    email: (user, args, context) => {
      // Only return email if requester is user or admin
      if (context.user.id === user.id || context.user.role === 'admin') {
        return user.email;
      }
      return null;
    },
  },
};
```

## Common API Vulnerabilities

### 1. Broken Object Level Authorization (IDOR)

**Vulnerability:**
```
GET /api/users/123 → returns user 123 data (no authorization check)
```

**Fix:**
```python
@app.route('/api/users/<user_id>')
@require_auth
def get_user(user_id):
    # Check if current user can access this user's data
    if current_user.id != user_id and not current_user.is_admin:
        return jsonify({"error": "Forbidden"}), 403
    
    user = db.get_user(user_id)
    return jsonify(user)
```

### 2. Excessive Data Exposure

**Vulnerability:**
```json
GET /api/users/123
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "password_hash": "$2b$12$...",  ← EXPOSED!
  "ssn": "123-45-6789",            ← EXPOSED!
  "salary": 150000                 ← EXPOSED!
}
```

**Fix:**
```python
def serialize_user(user, requester):
    public_fields = {'id', 'name', 'email'}
    admin_fields = {'phone', 'created_at'}
    
    fields = public_fields
    if requester.is_admin:
        fields = fields.union(admin_fields)
    
    return {k: v for k, v in user.items() if k in fields}
```

### 3. Mass Assignment

**Vulnerability:**
```
POST /api/users/123
{
  "name": "John Doe",
  "is_admin": true  ← User sets themselves as admin!
}
```

**Fix:**
```python
ALLOWED_UPDATE_FIELDS = {'name', 'email', 'phone'}

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    # Only update allowed fields
    updates = {k: v for k, v in data.items() if k in ALLOWED_UPDATE_FIELDS}
    
    db.update_user(user_id, updates)
    return jsonify({"success": True})
```

### 4. API Abuse (No Rate Limiting)

**Vulnerability:**
```
for i in range(100000):
    requests.post('/api/expensive-operation')
```

**Fix:**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.headers.get('X-User-ID'))

@app.route('/api/expensive-operation')
@limiter.limit("10 per minute")
def expensive_operation():
    # ... expensive operation ...
    return jsonify({"success": True})
```

## API Versioning and Deprecation

**Versioning Strategy (URL-based):**
```
/api/v1/users
/api/v2/users
```

**Deprecation Process:**
1. Announce deprecation (6 months notice)
2. Add deprecation header:
   ```
   Deprecation: Sat, 1 Jan 2025 00:00:00 GMT
   Link: </api/v2/users>; rel="successor-version"
   ```
3. Monitor usage of deprecated endpoints
4. Contact remaining users
5. Shut down deprecated version

## API Security Checklist

**Authentication & Authorization:**
- [ ] JWT signature validation
- [ ] Token expiration checks
- [ ] Authorization on every endpoint
- [ ] Scope validation (OAuth2)
- [ ] Resource-level access control

**Input Validation:**
- [ ] JSON schema validation
- [ ] Request size limits
- [ ] Content-Type validation
- [ ] Query parameter validation
- [ ] Pagination limits

**Rate Limiting:**
- [ ] Per-user rate limits
- [ ] Per-IP rate limits
- [ ] Per-endpoint rate limits
- [ ] 429 responses with Retry-After
- [ ] Monitoring for abuse

**Output Security:**
- [ ] Remove sensitive fields
- [ ] Data masking for PII
- [ ] No error details in production
- [ ] Proper CORS configuration
- [ ] Security headers

**Logging & Monitoring:**
- [ ] Log all API requests
- [ ] Log authentication failures
- [ ] Log authorization denials
- [ ] Monitor for anomalies
- [ ] Alert on suspicious patterns

**TLS & Transport:**
- [ ] HTTPS only (no HTTP)
- [ ] TLS 1.3 preferred
- [ ] Strong cipher suites
- [ ] HSTS header
- [ ] Certificate pinning (mobile apps)
