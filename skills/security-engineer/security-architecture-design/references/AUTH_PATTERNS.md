# Authentication Architecture Patterns

## Overview

This document provides authentication architecture patterns for different application types, covering OAuth2, OIDC, SAML, JWT, and session-based authentication.

## Pattern Selection Guide

| Application Type | Recommended Pattern | Token Type | Use Case |
|------------------|---------------------|------------|----------|
| Web App (server-rendered) | Session-based | HTTP cookies | Traditional web apps with server-side rendering |
| Single Page App (SPA) | OAuth2 + PKCE | JWT (access + refresh) | React, Vue, Angular apps |
| Mobile App | OAuth2 + PKCE | JWT (access + refresh) | iOS, Android native apps |
| Server-to-Server | Client Credentials | JWT | Backend API integrations |
| Microservices | Service Mesh + mTLS | JWT + mTLS certificates | Internal service communication |
| Enterprise SSO | SAML 2.0 or OIDC | SAML assertion or JWT | Corporate identity integration |

## Pattern 1: Session-Based Authentication

**Best For:** Traditional server-rendered web applications

**Architecture:**
```
User → Login Form → Server validates credentials → Create session → Store session ID in cookie → User authenticated
```

**Implementation:**
- Server maintains session store (Redis, database, memory)
- Session ID stored in HTTP-only, Secure, SameSite cookie
- Session contains user ID, permissions, metadata
- Server validates session on each request

**Security Requirements:**
- Session cookies: `HttpOnly`, `Secure`, `SameSite=Strict` or `Lax`
- Session timeout: 30-minute idle, 8-hour absolute
- CSRF protection: Synchronizer tokens or SameSite cookies
- Secure session storage: encrypted, protected from unauthorized access

**Pros:**
- Simple to implement
- Easy to invalidate (server controls sessions)
- No token management on client
- Better for server-rendered apps

**Cons:**
- Requires server-side session storage
- Harder to scale horizontally (sticky sessions or shared storage)
- CSRF protection needed
- Not ideal for APIs or mobile apps

## Pattern 2: OAuth2 Authorization Code Flow with PKCE

**Best For:** Single Page Apps (SPAs), mobile apps, modern web applications

**Architecture (Sequence Diagram):**
```
1. User clicks "Login"
2. Client generates code_verifier (random string) and code_challenge (SHA256 hash)
3. Client redirects to Authorization Server with code_challenge
4. User authenticates with Authorization Server
5. Authorization Server redirects back with authorization code
6. Client exchanges code + code_verifier for tokens
7. Authorization Server validates code_verifier matches code_challenge
8. Authorization Server returns access_token + refresh_token
9. Client uses access_token for API requests
```

**PKCE (Proof Key for Code Exchange):**
- **code_verifier:** Random 43-128 character string
- **code_challenge:** Base64URL(SHA256(code_verifier))
- Prevents authorization code interception attacks

**Token Management:**
- **Access Token:** Short-lived (15 minutes), used for API requests
- **Refresh Token:** Long-lived (7 days), used to obtain new access tokens
- **Token Storage (SPA):** Memory (best), sessionStorage (acceptable), **NOT localStorage**
- **Token Storage (Mobile):** Secure enclave / keychain

**Security Requirements:**
- Always use PKCE (even for confidential clients)
- HTTPS required for all OAuth flows
- Validate redirect_uri strictly (exact match)
- Implement refresh token rotation
- Bind tokens to client (token binding, DPoP)

**Example Authorization Request:**
```
GET /authorize?
  response_type=code&
  client_id=abc123&
  redirect_uri=https://app.example.com/callback&
  scope=openid profile email&
  state=random_state_value&
  code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM&
  code_challenge_method=S256
```

**Example Token Exchange:**
```
POST /token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=authorization_code_here&
redirect_uri=https://app.example.com/callback&
client_id=abc123&
code_verifier=original_code_verifier_value
```

**Pros:**
- Industry standard
- Secure for SPAs and mobile apps
- No client secret needed (PKCE provides security)
- Supports refresh tokens

**Cons:**
- More complex than session-based
- Requires token management
- Clock skew issues (token expiration)

## Pattern 3: OpenID Connect (OIDC)

**Best For:** Applications needing user identity information (SSO, profile data)

**Architecture:**
- Builds on OAuth2 Authorization Code Flow
- Adds ID Token (JWT) with user claims
- Provides standardized user info endpoint

**Tokens:**
- **Access Token:** For API authorization (opaque or JWT)
- **ID Token:** For user identity (always JWT)
- **Refresh Token:** For obtaining new tokens

**ID Token Structure (JWT):**
```json
{
  "iss": "https://auth.example.com",
  "sub": "user123",
  "aud": "client_id",
  "exp": 1625097600,
  "iat": 1625094000,
  "nonce": "random_nonce",
  "name": "John Doe",
  "email": "john@example.com",
  "email_verified": true
}
```

**Standard Claims:**
- `sub` - Subject (user ID)
- `name`, `given_name`, `family_name` - User names
- `email`, `email_verified` - Email address
- `picture` - Profile picture URL

**Security Requirements:**
- Validate ID Token signature (RS256 recommended)
- Verify `iss` (issuer) matches authorization server
- Verify `aud` (audience) matches client ID
- Check `exp` (expiration) is not past
- Validate `nonce` matches original request

**Pros:**
- Standardized identity layer
- Rich user profile information
- Interoperable across providers
- Built-in SSO support

**Cons:**
- More complex than plain OAuth2
- ID Token may contain PII (handle carefully)
- Requires JWT validation

## Pattern 4: JWT (JSON Web Tokens)

**Best For:** Stateless authentication in APIs and microservices

**JWT Structure:**
```
Header.Payload.Signature
```

**Header:**
```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key-id-123"
}
```

**Payload:**
```json
{
  "sub": "user123",
  "iss": "https://auth.example.com",
  "aud": "api.example.com",
  "exp": 1625097600,
  "iat": 1625094000,
  "scope": "read:data write:data"
}
```

**Signature:**
```
RS256(base64UrlEncode(header) + "." + base64UrlEncode(payload), privateKey)
```

**Security Requirements:**
- Use RS256 (RSA with SHA-256) for asymmetric signing
- Never use HS256 with public clients
- Keep JWTs short-lived (15 minutes max)
- Validate signature before trusting claims
- Validate `exp`, `iss`, `aud` claims
- Use `kid` (key ID) for key rotation

**JWT Validation Checklist:**
```python
def validate_jwt(token):
    # 1. Decode header (don't verify yet)
    header = decode_header(token)
    
    # 2. Get public key using kid
    public_key = get_public_key(header['kid'])
    
    # 3. Verify signature
    payload = verify_signature(token, public_key)
    
    # 4. Validate claims
    assert payload['exp'] > current_time()
    assert payload['iss'] == 'https://auth.example.com'
    assert payload['aud'] == 'api.example.com'
    
    return payload
```

**Pros:**
- Stateless (no server-side session storage)
- Self-contained (includes claims)
- Scales horizontally easily
- Works well for APIs and microservices

**Cons:**
- Cannot be revoked (until expiration)
- Larger than session IDs
- Requires secure key management
- Clock skew issues

## Pattern 5: Client Credentials Flow

**Best For:** Server-to-server API authentication (no user context)

**Architecture:**
```
Service A → POST /token with client_id + client_secret → Authorization Server → Returns access_token → Service A calls Service B with access_token
```

**Token Request:**
```
POST /token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&
client_id=service_a_id&
client_secret=service_a_secret&
scope=read:data write:data
```

**Security Requirements:**
- Protect client secret (environment variables, secret manager)
- Rotate client secrets regularly (90 days)
- Use strong, random secrets (32+ characters)
- Limit scope to minimum necessary
- Monitor for secret exposure

**Pros:**
- Simple for backend services
- No user involvement
- Clear service identity

**Cons:**
- Secret management burden
- Difficult to rotate secrets without downtime
- No user context

## Pattern 6: Mutual TLS (mTLS)

**Best For:** High-security microservices, zero-trust architectures

**Architecture:**
```
Service A (with client cert) → mTLS handshake → Service B (with server cert) → Both verify certificates → Secure connection established
```

**Certificate Requirements:**
- Short-lived certificates (24 hours recommended)
- Automated certificate issuance and rotation
- Certificate validation (expiration, revocation, chain)
- Service identity in certificate SAN (Subject Alternative Name)

**mTLS + JWT Pattern:**
- mTLS for transport security and service authentication
- JWT for authorization and user context
- Best of both worlds

**Security Requirements:**
- Use SPIFFE/SPIRE for service identity
- Automate certificate lifecycle
- Monitor certificate expiration
- Implement certificate revocation

**Pros:**
- Strongest authentication method
- No secrets to protect (certificates are public)
- Protects against MITM attacks
- Built-in encryption

**Cons:**
- Complex certificate management
- Requires certificate authority (CA)
- Performance overhead (minimal with modern TLS)

## Best Practices Across All Patterns

### Token Security

**Storage:**
- Never store tokens in localStorage (XSS risk)
- Prefer memory storage for SPAs
- Use secure enclave/keychain for mobile
- Encrypt tokens in backend storage

**Transmission:**
- Always use HTTPS
- Use `Authorization: Bearer <token>` header
- Never pass tokens in URL query parameters
- Implement token binding (DPoP)

**Lifecycle:**
- Short-lived access tokens (15 minutes)
- Long-lived refresh tokens (7 days)
- Implement refresh token rotation
- Revoke refresh tokens on logout

### Password Security

**Storage:**
- Use bcrypt, scrypt, or Argon2 (never MD5, SHA1)
- Minimum 12-character passwords
- Check against breach databases (Have I Been Pwned)
- Implement password history (prevent reuse)

**Policy:**
- Require: length (12+), no common passwords
- Don't require: special characters, rotation
- Implement account lockout (5 attempts, 15-minute lockout)
- Rate limit login attempts

### Multi-Factor Authentication (MFA)

**Options:**
- TOTP (Time-based One-Time Password) - Google Authenticator, Authy
- SMS (less secure, better than nothing)
- WebAuthn (FIDO2) - Hardware keys, biometrics
- Push notifications (Duo, Okta)

**Implementation:**
- Require MFA for privileged accounts
- Offer MFA for all users
- Provide backup codes
- Support multiple MFA methods

### Session Management

**Best Practices:**
- Regenerate session ID after login
- Implement idle timeout (30 minutes)
- Implement absolute timeout (8 hours)
- Clear sessions on logout
- Detect concurrent sessions
- Bind sessions to IP or user agent (with care)

## Anti-Patterns to Avoid

**DON'T:**
- ❌ Store passwords in plain text
- ❌ Use weak hashing (MD5, SHA1)
- ❌ Use OAuth2 Implicit Flow (deprecated)
- ❌ Store JWTs in localStorage
- ❌ Use long-lived access tokens (>1 hour)
- ❌ Embed secrets in client-side code
- ❌ Trust client-side validation
- ❌ Ignore token expiration
- ❌ Use symmetric JWT signing (HS256) for public clients
- ❌ Forget to validate JWT signatures

**DO:**
- ✅ Use OAuth2 Authorization Code Flow with PKCE
- ✅ Implement MFA for sensitive operations
- ✅ Use short-lived tokens
- ✅ Rotate refresh tokens
- ✅ Validate all tokens server-side
- ✅ Use HTTPS everywhere
- ✅ Implement proper error handling (don't leak info)
- ✅ Monitor authentication events
- ✅ Regularly review and update auth patterns
