---
name: api-contract-design
description: |
  Design OpenAPI/Swagger specifications, GraphQL schemas, and REST/gRPC API contracts with validation rules.
  Use when designing API contracts, creating OpenAPI specs, defining REST APIs, designing GraphQL schemas,
  specifying API endpoints, documenting API specifications, or when user mentions API contract, OpenAPI,
  Swagger, REST API, GraphQL schema, endpoint design, API documentation, request/response schemas,
  authentication requirements, rate limits.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# API Contract Design

Design production-ready API contracts with OpenAPI 3.0, GraphQL schemas, or gRPC definitions.

## Output Location

**Default Output Location:** Save all API specifications to `~/Documents/claude-code-skills-data/api-contract-design/` unless user specifies otherwise. Create the directory if needed.

## Quick Start

The typical API contract design process:

1. **Understand requirements** - Gather API purpose, resources, and use cases
2. **Choose API style** - REST, GraphQL, or gRPC based on needs
3. **Design endpoints** - Define resource paths and operations
4. **Specify schemas** - Create request/response data models
5. **Add validation** - Define validation rules for all inputs
6. **Configure auth** - Specify authentication and authorization
7. **Document errors** - Define error codes and responses
8. **Set rate limits** - Configure rate limiting strategy
9. **Add examples** - Include request/response examples
10. **Validate spec** - Run validation script

## Workflow

### 1. Gather Requirements

Ask the user:
- **API purpose**: What will this API do?
- **Resources**: What entities/data will be exposed?
- **Operations**: What actions are needed (create, read, update, delete)?
- **Clients**: Who will use this API (web apps, mobile, internal services)?
- **Auth needs**: What authentication is required?
- **Scale**: Expected traffic and rate limits

### 2. Choose API Style

**Decision matrix:**

| Choose REST if: | Choose GraphQL if: | Choose gRPC if: |
|----------------|-------------------|-----------------|
| Public API | Complex data fetching | Internal microservices |
| Simple CRUD operations | Mobile-first application | High performance needed |
| Standard HTTP clients | Flexible querying needed | Binary protocol suitable |
| Wide compatibility required | Multiple related resources | Bidirectional streaming |

**For most product APIs: Use REST with OpenAPI 3.0**

### 3. Design REST API Structure

**URL Structure:**
```
/api/v1/users                    # Collection - GET (list), POST (create)
/api/v1/users/{userId}           # Resource - GET, PATCH, DELETE
/api/v1/users/{userId}/posts     # Nested resource
```

**Design principles:**
- Use nouns, not verbs: `/users` not `/getUsers`
- Plural resource names: `/users` not `/user`
- HTTP methods for actions: GET (read), POST (create), PATCH (update), DELETE (delete)
- Nest related resources: `/users/{id}/posts` for relationships
- Version in URL: `/api/v1/` for breaking changes

### 4. Create OpenAPI Specification

**Start with template:**
```bash
cp assets/openapi_template.yaml spec.yaml
```

**Update info section:**
```yaml
info:
  title: [API Name]
  version: 1.0.0
  description: |
    [Detailed API description]

    **Base URL:** https://api.example.com/v1
    **Authentication:** Bearer token (JWT)
    **Rate Limits:**
    - Anonymous: 100 req/hour
    - Authenticated: 1000 req/hour
```

**Define servers:**
```yaml
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging
```

### 5. Define Endpoints

**For each endpoint, specify:**

1. **HTTP method and path**
2. **Summary and description**
3. **operationId** (unique identifier)
4. **Tags** (for grouping)
5. **Security requirements**
6. **Parameters** (path, query, header)
7. **Request body** (if applicable)
8. **Responses** (all status codes)
9. **Examples** (request and response)

**Example endpoint:**
```yaml
/users:
  post:
    summary: Create new user
    operationId: createUser
    tags: [Users]
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CreateUserRequest'
          examples:
            valid_user:
              value:
                email: user@example.com
                name: John Doe
                password: SecureP@ss123
    responses:
      '201':
        description: User created
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      '400':
        $ref: '#/components/responses/BadRequest'
      '409':
        $ref: '#/components/responses/Conflict'
```

### 6. Design Data Schemas

**Define schemas in components/schemas:**

```yaml
components:
  schemas:
    User:
      type: object
      required: [id, email]
      properties:
        id:
          type: string
          format: uuid
          example: "550e8400-e29b-41d4-a716-446655440000"
        email:
          type: string
          format: email
          maxLength: 255
          example: user@example.com
        name:
          type: string
          maxLength: 255
          nullable: true
          example: "John Doe"
```

**Use reusable schemas with $ref:**
```yaml
$ref: '#/components/schemas/User'
```

### 7. Add Validation Rules

**For each input field, specify:**
- `type` (string, number, integer, boolean, array, object)
- `format` (email, uuid, date-time, uri, etc.)
- `minLength` / `maxLength` for strings
- `minimum` / `maximum` for numbers
- `pattern` for regex validation
- `enum` for allowed values
- `required` array for mandatory fields

**Consult validation library:**
See [validation_rules.md](references/validation_rules.md) for comprehensive validation patterns for:
- Email addresses
- Passwords
- Usernames
- Phone numbers
- URLs
- Dates and times
- UUIDs
- Names
- Addresses
- Financial data

### 8. Configure Authentication

**Choose authentication method:**

1. **JWT Bearer Token** (recommended for most APIs)
   - See [authentication_patterns.md](references/authentication_patterns.md#jwt-bearer-token)
   - Define security scheme in components/securitySchemes
   - Add login/logout endpoints
   - Document token structure and expiration

2. **API Key** (for external integrations)
   - See [authentication_patterns.md](references/authentication_patterns.md#api-key-authentication)
   - Header-based: `X-API-Key`
   - Key management endpoints

3. **OAuth 2.0** (for third-party access)
   - See [authentication_patterns.md](references/authentication_patterns.md#oauth-20)
   - Authorization code flow
   - Define scopes and permissions

**Apply security to endpoints:**
```yaml
security:
  - BearerAuth: []  # Global default

paths:
  /public-endpoint:
    get:
      security: []  # Override for public endpoint
```

### 9. Define Error Responses

**Create standard error schema:**
```yaml
components:
  schemas:
    Error:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message]
          properties:
            code:
              type: string
              enum:
                - VALIDATION_ERROR
                - AUTHENTICATION_ERROR
                - AUTHORIZATION_ERROR
                - NOT_FOUND
                - CONFLICT
                - RATE_LIMIT_EXCEEDED
                - INTERNAL_ERROR
            message:
              type: string
            details:
              type: array
              items:
                type: object
                properties:
                  field: {type: string}
                  message: {type: string}
```

**Define reusable error responses:**
```yaml
components:
  responses:
    BadRequest:
      description: Invalid input
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

**Reference in endpoints:**
```yaml
responses:
  '400':
    $ref: '#/components/responses/BadRequest'
```

### 10. Configure Rate Limits

**Document rate limiting strategy:**

```yaml
x-rate-limits:
  global:
    anonymous:
      limit: 100
      window: 3600  # seconds
    authenticated:
      limit: 1000
      window: 3600
  endpoints:
    /auth/login:
      limit: 20
      window: 3600
    /auth/register:
      limit: 5
      window: 3600
```

**Add rate limit headers to responses:**
```yaml
responses:
  '200':
    headers:
      X-RateLimit-Limit:
        schema:
          type: integer
      X-RateLimit-Remaining:
        schema:
          type: integer
      X-RateLimit-Reset:
        schema:
          type: integer
```

### 11. Add Pagination (if needed)

**For list endpoints, add pagination:**

See [openapi_patterns.md](references/openapi_patterns.md#pagination) for:
- Offset-based pagination (most common)
- Cursor-based pagination (for real-time data)
- Filtering parameters
- Sorting parameters
- Field selection

**Example:**
```yaml
parameters:
  - name: page
    in: query
    schema:
      type: integer
      minimum: 1
      default: 1
  - name: limit
    in: query
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20
```

### 12. Add Examples

**Include examples for:**
- Request bodies (success cases)
- Response bodies (success and error cases)
- Edge cases and validation failures

```yaml
examples:
  valid_request:
    value:
      email: user@example.com
      password: SecureP@ss123
  invalid_email:
    value:
      email: not-an-email
      password: SecureP@ss123
```

### 13. Validate Specification

**Run validation script:**
```bash
python3 scripts/validate_openapi.py spec.yaml
```

**The validator checks:**
- Required OpenAPI fields
- Path definitions and operations
- Schema definitions
- Security schemes
- Examples presence
- REST best practices
- Naming conventions

**Fix any errors before finalizing.**

### 14. Generate Documentation

**Export the OpenAPI spec to:**
- **Swagger UI** - Interactive API documentation
- **ReDoc** - Clean, three-panel documentation
- **Postman Collection** - For API testing

**Create markdown summary:**
```markdown
# [API Name] Documentation

## Overview
[Brief description]

## Authentication
[Auth flow description]

## Endpoints

### POST /auth/login
**Description:** Authenticate user

**Request:**
\`\`\`json
{
  "email": "user@example.com",
  "password": "SecureP@ss123"
}
\`\`\`

**Success Response (200):**
\`\`\`json
{
  "token": "eyJhbGci...",
  "expires_at": "2025-02-15T10:30:00Z",
  "user": {...}
}
\`\`\`

[Repeat for all endpoints]
```

## GraphQL Alternative

If GraphQL was chosen in step 2:

**Use GraphQL template:**
```bash
cp assets/graphql_schema_template.graphql schema.graphql
```

**Design schema with:**
1. **Scalar types** - Custom scalars (DateTime, Email, URL)
2. **Object types** - Main data models
3. **Input types** - For mutations
4. **Enums** - For fixed value sets
5. **Queries** - Read operations
6. **Mutations** - Write operations
7. **Subscriptions** - Real-time updates (optional)

**See template for complete structure.**

## Common Patterns

**For advanced patterns, see [openapi_patterns.md](references/openapi_patterns.md):**
- Pagination (offset and cursor-based)
- Filtering and searching
- Sorting
- Field selection
- Batch operations
- File uploads
- Versioning strategies
- Error response standards

**For authentication patterns, see [authentication_patterns.md](references/authentication_patterns.md):**
- JWT bearer tokens
- API key management
- OAuth 2.0 flows
- Session-based auth
- Multi-factor authentication
- Role-based access control

## Quality Checklist

Before finalizing the API contract, verify:

- [ ] All endpoints have complete request/response schemas
- [ ] All required fields marked as required
- [ ] All optional fields have defaults or nullable: true
- [ ] Validation rules comprehensive (format, length, pattern)
- [ ] Authentication and authorization clearly specified
- [ ] Rate limits defined per endpoint
- [ ] Error codes cover all failure scenarios
- [ ] Examples provided for all major flows
- [ ] OpenAPI spec passes validation (scripts/validate_openapi.py)
- [ ] Consistent naming conventions (camelCase or snake_case)
- [ ] No hardcoded secrets or credentials
- [ ] All paths follow REST conventions (nouns, not verbs)
- [ ] Security schemes properly configured
- [ ] Documentation is clear and complete

## Output Format

Deliver the following artifacts:

1. **OpenAPI Specification** (spec.yaml or spec.json)
   - Complete, valid OpenAPI 3.0 document
   - All endpoints, schemas, and responses defined
   - Examples included

2. **API Documentation** (README.md or API_DOCS.md)
   - Overview and quick start
   - Authentication guide
   - Endpoint reference with examples
   - Error code reference
   - Rate limiting details

3. **Validation Report** (validation_report.txt)
   - Output from validate_openapi.py
   - Any warnings or issues noted

4. **Optional: Postman Collection**
   - Import-ready collection for testing
   - Pre-configured authentication
   - Example requests

## Anti-Patterns to Avoid

- **Verbs in URLs**: Use `/users` not `/getUsers` (HTTP methods convey the action)
- **Inconsistent naming**: Pick camelCase or snake_case and use everywhere
- **Missing examples**: Always provide request/response examples
- **Weak validation**: Don't rely on client-side validation alone
- **Exposing internals**: Don't leak database IDs or internal structure
- **No versioning**: Always version breaking changes (`/v1/`, `/v2/`)
- **Poor error messages**: Errors should be actionable and specific
- **Missing auth**: Don't forget to secure endpoints
- **No rate limits**: Always limit public endpoints
- **Hardcoded values**: Use environment-based server URLs
