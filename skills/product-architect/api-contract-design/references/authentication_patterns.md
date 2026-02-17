# Authentication and Authorization Patterns

## Table of Contents
1. [JWT Bearer Token](#jwt-bearer-token)
2. [API Key Authentication](#api-key-authentication)
3. [OAuth 2.0](#oauth-20)
4. [Basic Authentication](#basic-authentication)
5. [Session-Based Authentication](#session-based-authentication)
6. [Multi-Factor Authentication](#multi-factor-authentication)

## JWT Bearer Token

### Security Scheme Definition
```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT token obtained from /auth/login endpoint.
        Include in Authorization header: Bearer <token>
```

### Authentication Flow Endpoints
```yaml
paths:
  /auth/login:
    post:
      summary: Authenticate user
      tags: [Authentication]
      security: []  # Public endpoint
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
                remember_me:
                  type: boolean
                  default: false
                  description: Extend token lifetime to 30 days
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                    description: JWT bearer token
                    example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                  refresh_token:
                    type: string
                    description: Token for refreshing access token
                  expires_at:
                    type: string
                    format: date-time
                    description: Token expiration time
                  user:
                    $ref: '#/components/schemas/User'
        '401':
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /auth/refresh:
    post:
      summary: Refresh access token
      tags: [Authentication]
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [refresh_token]
              properties:
                refresh_token:
                  type: string
      responses:
        '200':
          description: Token refreshed
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                  expires_at:
                    type: string
                    format: date-time
        '401':
          description: Invalid or expired refresh token

  /auth/logout:
    post:
      summary: Invalidate token
      tags: [Authentication]
      security:
        - BearerAuth: []
      responses:
        '200':
          description: Logout successful
        '401':
          $ref: '#/components/responses/Unauthorized'
```

### JWT Token Structure
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "role": "user",
    "permissions": ["read", "write"],
    "iat": 1707388200,
    "exp": 1707993000,
    "jti": "unique-token-id"
  },
  "signature": "..."
}
```

### Token Validation Headers
```yaml
responses:
  '401':
    description: Invalid or expired token
    headers:
      WWW-Authenticate:
        schema:
          type: string
        description: Authentication scheme
        example: 'Bearer realm="api", error="invalid_token", error_description="Token expired"'
```

## API Key Authentication

### Security Scheme Definition
```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for external integrations
```

### Key Management Endpoints
```yaml
/api-keys:
  post:
    summary: Create API key
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [name]
            properties:
              name:
                type: string
                description: Descriptive name for the key
                example: "Production Integration"
              scopes:
                type: array
                items:
                  type: string
                  enum: [read, write, admin]
                description: Permissions for this key
              expires_at:
                type: string
                format: date-time
                description: Optional expiration date
    responses:
      '201':
        description: API key created
        content:
          application/json:
            schema:
              type: object
              properties:
                key:
                  type: string
                  description: The API key (only shown once)
                  example: "sk_live_1234567890abcdef"
                id:
                  type: string
                  format: uuid
                name:
                  type: string
                scopes:
                  type: array
                  items:
                    type: string
                created_at:
                  type: string
                  format: date-time

  get:
    summary: List API keys
    security:
      - BearerAuth: []
    responses:
      '200':
        description: List of API keys (keys are masked)
        content:
          application/json:
            schema:
              type: object
              properties:
                keys:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                        format: uuid
                      name:
                        type: string
                      key_preview:
                        type: string
                        description: Last 4 characters
                        example: "...cdef"
                      scopes:
                        type: array
                        items:
                          type: string
                      last_used_at:
                        type: string
                        format: date-time
                        nullable: true
                      created_at:
                        type: string
                        format: date-time

/api-keys/{keyId}:
  delete:
    summary: Revoke API key
    security:
      - BearerAuth: []
    parameters:
      - name: keyId
        in: path
        required: true
        schema:
          type: string
          format: uuid
    responses:
      '204':
        description: API key revoked
```

## OAuth 2.0

### Authorization Code Flow
```yaml
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://api.example.com/oauth/authorize
          tokenUrl: https://api.example.com/oauth/token
          refreshUrl: https://api.example.com/oauth/refresh
          scopes:
            read: Read access to user data
            write: Write access to user data
            admin: Administrative access

paths:
  /oauth/authorize:
    get:
      summary: OAuth authorization endpoint
      description: Redirects to login and authorization page
      security: []
      parameters:
        - name: client_id
          in: query
          required: true
          schema:
            type: string
        - name: redirect_uri
          in: query
          required: true
          schema:
            type: string
            format: uri
        - name: response_type
          in: query
          required: true
          schema:
            type: string
            enum: [code]
        - name: scope
          in: query
          schema:
            type: string
            example: "read write"
        - name: state
          in: query
          description: CSRF protection token
          schema:
            type: string
      responses:
        '302':
          description: Redirect to redirect_uri with code

  /oauth/token:
    post:
      summary: Exchange authorization code for access token
      security: []
      requestBody:
        required: true
        content:
          application/x-www-form-urlencoded:
            schema:
              type: object
              required: [grant_type, code, client_id, client_secret, redirect_uri]
              properties:
                grant_type:
                  type: string
                  enum: [authorization_code, refresh_token]
                code:
                  type: string
                  description: Authorization code from /oauth/authorize
                client_id:
                  type: string
                client_secret:
                  type: string
                redirect_uri:
                  type: string
                  format: uri
                refresh_token:
                  type: string
                  description: Required if grant_type is refresh_token
      responses:
        '200':
          description: Token issued
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  token_type:
                    type: string
                    example: Bearer
                  expires_in:
                    type: integer
                    description: Seconds until expiration
                  refresh_token:
                    type: string
                  scope:
                    type: string
```

## Basic Authentication

### Security Scheme Definition
```yaml
components:
  securitySchemes:
    BasicAuth:
      type: http
      scheme: basic
      description: |
        Username and password credentials encoded in Base64.
        Format: Basic base64(username:password)
```

**Note:** Basic auth should only be used over HTTPS and is generally discouraged for modern APIs. Prefer JWT or OAuth 2.0.

## Session-Based Authentication

### Cookie Authentication
```yaml
components:
  securitySchemes:
    CookieAuth:
      type: apiKey
      in: cookie
      name: SESSIONID
      description: Session cookie set after login

paths:
  /auth/login:
    post:
      summary: Login with credentials
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        '200':
          description: Login successful
          headers:
            Set-Cookie:
              schema:
                type: string
                example: SESSIONID=abc123; Path=/; HttpOnly; Secure; SameSite=Strict
              description: Session cookie
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
```

## Multi-Factor Authentication

### MFA Flow Endpoints
```yaml
/auth/mfa/enable:
  post:
    summary: Enable MFA for user
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [method]
            properties:
              method:
                type: string
                enum: [totp, sms]
                description: MFA method
    responses:
      '200':
        description: MFA setup initiated
        content:
          application/json:
            schema:
              type: object
              properties:
                secret:
                  type: string
                  description: TOTP secret (for totp method)
                qr_code:
                  type: string
                  format: uri
                  description: QR code image URL
                backup_codes:
                  type: array
                  items:
                    type: string
                  description: One-time backup codes

/auth/mfa/verify:
  post:
    summary: Verify MFA code
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [code]
            properties:
              code:
                type: string
                minLength: 6
                maxLength: 6
                pattern: '^\d{6}$'
                description: 6-digit MFA code
    responses:
      '200':
        description: MFA verified
        content:
          application/json:
            schema:
              type: object
              properties:
                verified:
                  type: boolean
      '401':
        description: Invalid MFA code

/auth/login-mfa:
  post:
    summary: Complete login with MFA
    security: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [email, password, mfa_code]
            properties:
              email:
                type: string
                format: email
              password:
                type: string
              mfa_code:
                type: string
                pattern: '^\d{6}$'
    responses:
      '200':
        description: Login successful
        content:
          application/json:
            schema:
              type: object
              properties:
                token:
                  type: string
                user:
                  $ref: '#/components/schemas/User'
```

## Role-Based Access Control (RBAC)

### Authorization Patterns
```yaml
# Define roles in user schema
components:
  schemas:
    User:
      properties:
        role:
          type: string
          enum: [admin, moderator, user, guest]
        permissions:
          type: array
          items:
            type: string
            enum: [read, write, delete, manage_users, manage_content]

# Document required permissions per endpoint
paths:
  /admin/users:
    get:
      summary: List all users (admin only)
      security:
        - BearerAuth: []
      x-required-permissions: [admin]
      x-required-roles: [admin]
      responses:
        '200':
          description: User list
        '403':
          description: Insufficient permissions
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error:
                  code: AUTHORIZATION_ERROR
                  message: Admin role required
```

## Rate Limiting

### Rate Limit Headers
```yaml
responses:
  '200':
    headers:
      X-RateLimit-Limit:
        schema:
          type: integer
        description: Request limit per window
        example: 1000
      X-RateLimit-Remaining:
        schema:
          type: integer
        description: Requests remaining
        example: 999
      X-RateLimit-Reset:
        schema:
          type: integer
        description: Unix timestamp when limit resets
        example: 1707993000

  '429':
    description: Rate limit exceeded
    headers:
      Retry-After:
        schema:
          type: integer
        description: Seconds until retry allowed
        example: 3600
      X-RateLimit-Limit:
        schema:
          type: integer
      X-RateLimit-Remaining:
        schema:
          type: integer
          example: 0
      X-RateLimit-Reset:
        schema:
          type: integer
```

### Custom Rate Limit Extension
```yaml
x-rate-limits:
  global:
    anonymous:
      limit: 100
      window: 3600
    authenticated:
      limit: 1000
      window: 3600
  endpoints:
    /auth/login:
      limit: 20
      window: 3600
      key: ip_address
    /auth/register:
      limit: 5
      window: 3600
      key: ip_address
```
