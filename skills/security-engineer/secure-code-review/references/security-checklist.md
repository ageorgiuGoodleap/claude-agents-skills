# Security Review Checklist

Use this comprehensive checklist to ensure thorough security code review coverage.

## Input Validation

- [ ] All user input is validated (type, format, length, range)
- [ ] Whitelist validation used instead of blacklist
- [ ] Validation happens at API boundary (early rejection)
- [ ] File upload size limits enforced
- [ ] File type validation uses magic bytes, not just extension
- [ ] Input length limits prevent buffer overflows
- [ ] Numeric inputs validated for range (prevent integer overflow)
- [ ] Email addresses validated with proper regex
- [ ] URLs validated and sanitized before use

## Output Encoding

- [ ] All user-controlled output is encoded
- [ ] Context-aware encoding (HTML, JS, URL, CSS)
- [ ] Framework encoding functions used (not manual encoding)
- [ ] No direct interpolation of user input into HTML
- [ ] No direct interpolation into JavaScript
- [ ] JSON responses properly encoded
- [ ] XML output properly escaped

## SQL Injection Prevention

- [ ] Parameterized queries or ORM used exclusively
- [ ] No string concatenation for SQL queries
- [ ] No dynamic table/column names from user input
- [ ] Stored procedures used where appropriate
- [ ] Least privilege database accounts
- [ ] Database error messages not exposed to users

## Authentication

- [ ] Password hashing uses bcrypt (cost ≥10) or Argon2
- [ ] No weak hashing algorithms (MD5, SHA1, plain SHA256)
- [ ] Unique salt per password
- [ ] Password minimum length ≥12 characters
- [ ] Password complexity requirements enforced
- [ ] Password breach checking integrated
- [ ] JWT signed with RS256 (not HS256 with weak secret)
- [ ] JWT access tokens expire ≤15 minutes
- [ ] Refresh tokens stored securely, can be revoked
- [ ] MFA available for sensitive accounts
- [ ] Account lockout after 5 failed attempts
- [ ] Rate limiting on login endpoint
- [ ] Passwords never logged or included in error messages

## Authorization

- [ ] Authorization checked on every request
- [ ] Object-level authorization verified (user owns resource)
- [ ] Least privilege principle applied
- [ ] No authorization checks only on client side
- [ ] Direct object reference protected (no IDOR)
- [ ] Role-based access control (RBAC) implemented consistently
- [ ] Privilege escalation prevented
- [ ] API endpoints protected with authentication
- [ ] Admin endpoints require admin role

## Session Management

- [ ] Session cookies have httpOnly flag
- [ ] Session cookies have secure flag (HTTPS only)
- [ ] Session cookies have SameSite=Strict or Lax
- [ ] Session ID regenerated after login
- [ ] Session ID regenerated after privilege change
- [ ] Inactivity timeout ≤30 minutes
- [ ] Absolute session timeout ≤8 hours
- [ ] Sessions stored server-side, not client-side
- [ ] Session invalidation on logout
- [ ] Concurrent session limits enforced

## CSRF Protection

- [ ] State-changing operations protected from CSRF
- [ ] CSRF tokens validated on all POST/PUT/DELETE
- [ ] SameSite cookie attribute set
- [ ] Double-submit cookie pattern or synchronizer token
- [ ] Framework CSRF protection enabled
- [ ] GET requests are side-effect free

## Cryptography

- [ ] Strong algorithms: AES-256-GCM, RSA-4096, ECDSA P-384
- [ ] No weak algorithms: DES, 3DES, RC4, MD5, SHA1
- [ ] Cryptographically secure random: secrets module, not random
- [ ] Unique IV/nonce generated per encryption
- [ ] IV/nonce never reused
- [ ] Keys stored in environment variables or KMS
- [ ] No hardcoded keys in source code
- [ ] Key rotation implemented
- [ ] TLS 1.2+ only (no SSLv3, TLS 1.0, TLS 1.1)
- [ ] Strong cipher suites configured
- [ ] Certificate validation not disabled
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit

## Secrets Management

- [ ] No API keys hardcoded in source
- [ ] No passwords hardcoded in source
- [ ] No database credentials hardcoded
- [ ] No AWS/cloud provider keys hardcoded
- [ ] No private keys committed to repository
- [ ] Secrets loaded from environment variables
- [ ] Secrets loaded from key management service
- [ ] .env files in .gitignore
- [ ] Secrets not logged or exposed in errors

## Error Handling

- [ ] Generic error messages shown to users
- [ ] Detailed errors logged server-side
- [ ] Stack traces not exposed to users
- [ ] Passwords/tokens not included in logs
- [ ] HTTP status codes appropriate (400, 401, 403, 500)
- [ ] Database errors not exposed to users
- [ ] File paths not exposed in errors
- [ ] Error pages don't reveal framework/version

## File Operations

- [ ] File upload size limits enforced
- [ ] File type validation (magic bytes, not extension)
- [ ] Uploaded files stored outside webroot
- [ ] Uploaded files scanned for malware
- [ ] File downloads validate user permissions
- [ ] Path traversal prevented (no ../../ access)
- [ ] Filename sanitization before storage
- [ ] Execute permissions not granted to uploaded files

## API Security

- [ ] Rate limiting on all API endpoints
- [ ] API authentication required
- [ ] API versioning implemented
- [ ] CORS configured restrictively
- [ ] Content-Type validation
- [ ] Request size limits enforced
- [ ] API responses don't leak sensitive data
- [ ] GraphQL depth limiting (if applicable)
- [ ] GraphQL query complexity limiting (if applicable)

## Logging & Monitoring

- [ ] Authentication events logged (login, logout, failures)
- [ ] Authorization failures logged
- [ ] Sensitive operations logged
- [ ] Logs don't contain passwords/tokens
- [ ] Log injection prevented (newlines escaped)
- [ ] Security events monitored and alerted
- [ ] Audit trail for sensitive data access

## Dependencies & Configuration

- [ ] Dependencies up-to-date (no known vulnerabilities)
- [ ] Dependency scanning enabled (Dependabot, Snyk)
- [ ] Debug mode disabled in production
- [ ] Default credentials changed
- [ ] Unnecessary services disabled
- [ ] Security headers configured (CSP, X-Frame-Options, etc.)
- [ ] HSTS header enabled
- [ ] Framework security features enabled

## Race Conditions & TOCTOU

- [ ] File existence checks followed immediately by operations
- [ ] Resource locks used for critical operations
- [ ] Atomic operations preferred over separate check-then-act
- [ ] Concurrent requests to same resource handled safely

## Information Disclosure

- [ ] Framework/version not exposed in headers
- [ ] Directory listing disabled
- [ ] Source code not accessible via web
- [ ] .git directory not accessible via web
- [ ] Backup files not accessible via web
- [ ] Comments removed from production code
- [ ] Debug endpoints disabled in production

## Severity Guidelines

**Critical**: Immediate exploitation possible, high impact (data breach, full system compromise)
- SQL injection in production database
- Authentication bypass
- Remote code execution
- Hardcoded production credentials

**High**: Exploitation likely, significant impact
- XSS with session hijacking capability
- Authorization bypass
- Weak password hashing (MD5, SHA1)
- Secrets in source code
- Missing CSRF protection on critical operations

**Medium**: Exploitation possible, moderate impact
- Information disclosure
- Missing rate limiting
- Weak session timeout
- Missing security headers
- Insecure direct object reference

**Low**: Difficult to exploit or low impact
- Verbose error messages
- Missing input validation (low-risk fields)
- Outdated dependencies (no known exploits)
- Security best practices not followed
