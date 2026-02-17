---
name: secure-code-review
description: |
  Performs expert security code review focusing on OWASP Top 10 vulnerabilities, input validation,
  cryptography, authentication/authorization, and hardcoded secrets. Provides detailed line-by-line
  analysis with specific remediation guidance and secure code examples. Use when the user requests
  security code review, secure code audit, security patterns review, authentication review,
  authorization review, input validation review, cryptography review, secrets scan, or mentions
  reviewing code for security vulnerabilities, security best practices, or security anti-patterns.
---

# Secure Code Review

## Overview

This skill performs comprehensive security code review to identify security vulnerabilities and anti-patterns that automated tools miss. It provides context-aware analysis with specific remediation guidance and secure code examples.

**Core Focus Areas:**
- OWASP Top 10 vulnerabilities in context
- Input validation and sanitization logic
- Output encoding for XSS prevention
- Authentication and authorization logic
- Cryptographic implementations
- Hardcoded secrets detection
- Session management
- CSRF protection mechanisms
- Error handling for information disclosure

## When to Use This Skill

Trigger this skill when:
- Reviewing code changes for security vulnerabilities
- Analyzing pull requests with security-sensitive code
- Auditing authentication or authorization implementations
- Checking for input validation and output encoding issues
- Reviewing cryptographic code
- Scanning for hardcoded secrets or credentials
- Validating session management implementations
- Assessing security posture of code changes

## Review Process

### 1. Scope Identification

First, get the code to review:
```bash
# For pull requests
gh pr diff <pr-number>

# For specific files
git diff <branch> -- <file-path>

# For recent commits
git diff HEAD~1 HEAD
```

Identify security-sensitive areas:
- Authentication/authorization logic
- User input handling
- Database queries
- File operations
- Cryptographic operations
- Session management
- API endpoints

### 2. Security Analysis

Perform systematic review across these dimensions:

#### Input Validation
Check all user input handling:
- **Whitelist validation** preferred over blacklist
- **Reject unknown/dangerous input early** in the request lifecycle
- **Validate data type, format, length, and range**
- **Sanitize before processing**, not just before output

**Insecure:**
```python
# Blacklist approach - easily bypassed
if '<script>' not in user_input:
    process(user_input)
```

**Secure:**
```python
# Whitelist approach
import re
if re.match(r'^[a-zA-Z0-9_-]+$', user_input):
    process(user_input)
else:
    raise ValueError("Invalid input format")
```

#### Output Encoding
Verify context-aware encoding for all user-controlled output:
- **HTML context**: Use HTML entity encoding
- **JavaScript context**: Use JavaScript encoding
- **URL context**: Use URL encoding
- **CSS context**: Use CSS encoding

**Insecure:**
```javascript
// Direct interpolation - XSS vulnerable
element.innerHTML = `<div>${userInput}</div>`;
```

**Secure:**
```javascript
// Use framework encoding or DOM methods
element.textContent = userInput; // Automatically escaped
// Or use framework method: escapeHtml(userInput)
```

#### SQL Injection Prevention
Always use parameterized queries or ORM:

**Insecure:**
```python
# String concatenation - SQL injection vulnerable
query = f"SELECT * FROM users WHERE id = {user_id}"
db.execute(query)
```

**Secure:**
```python
# Parameterized query
query = "SELECT * FROM users WHERE id = ?"
db.execute(query, (user_id,))
```

#### Authentication & Authorization
Check for common authentication flaws:
- **Password hashing**: bcrypt/Argon2, not MD5/SHA1
- **JWT security**: RS256 signing, short expiration (≤15min)
- **Authorization checks**: Verify on every request, not just first
- **Session management**: Secure, httpOnly, SameSite cookies

**Insecure:**
```python
# Weak password hashing
import hashlib
hashed = hashlib.md5(password.encode()).hexdigest()
```

**Secure:**
```python
# Strong password hashing
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
```

#### Cryptography
Verify proper cryptographic implementations:
- **Algorithms**: AES-256-GCM for symmetric, RSA-4096/ECDSA P-384 for asymmetric
- **Key generation**: Use cryptographically secure random (secrets module, not random)
- **IV/Nonce**: Generate unique per encryption, never reuse
- **Key storage**: Environment variables or key management service, never in code

**Insecure:**
```python
# Weak random, reused IV
import random
from Crypto.Cipher import AES
key = bytes([random.randint(0, 255) for _ in range(32)])
iv = b'1234567890123456'  # Reused IV
cipher = AES.new(key, AES.MODE_CBC, iv)
```

**Secure:**
```python
# Cryptographically secure random, unique IV
import secrets
from Crypto.Cipher import AES
key = secrets.token_bytes(32)
iv = secrets.token_bytes(16)
cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
```

#### Secrets Detection
Scan for hardcoded secrets:
- API keys, access tokens, passwords
- Database credentials, connection strings
- Private keys, certificates
- AWS access keys, service account keys

**Patterns to flag:**
```python
# Hardcoded secrets - INSECURE
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "password123"
aws_access_key = "AKIAIOSFODNN7EXAMPLE"
```

**Secure approach:**
```python
# Environment variables
import os
API_KEY = os.getenv('API_KEY')
DB_PASSWORD = os.getenv('DB_PASSWORD')
```

#### Session Management
Verify secure session handling:
- **Cookie flags**: httpOnly, secure, SameSite=Strict/Lax
- **Timeout**: Inactivity timeout (30min), absolute timeout (8 hours)
- **Regeneration**: Regenerate session ID after login/privilege change
- **Storage**: Server-side session storage, not client-side

#### CSRF Protection
Ensure state-changing operations are protected:
- **Synchronizer token pattern**: Token in form and session
- **Double-submit cookies**: Token in cookie and request
- **SameSite cookies**: SameSite=Strict or Lax attribute
- **Framework CSRF protection**: Use built-in CSRF middleware

#### Error Handling
Check for information disclosure in errors:
- **Generic messages to users**: "An error occurred" not "SQL syntax error"
- **Detailed logging**: Full errors with stack traces in logs
- **Sanitize sensitive data**: Remove passwords, tokens from logs
- **HTTP status codes**: Use appropriate codes (400, 401, 403, 500)

### 3. Report Generation

Create a comprehensive security review report:

```markdown
# Security Code Review Report

**Date**: [Current date]
**Reviewer**: Claude Sonnet 4.5
**Scope**: [PR/commit/file description]
**Status**: [APPROVED / CONDITIONAL / BLOCKED]

## Summary

- **Critical**: X findings
- **High**: Y findings
- **Medium**: Z findings
- **Low**: W findings

**Overall Assessment**: [Brief security posture summary]

## Findings

### [Severity] - [Vulnerability Type]

**Location**: `file.py:123`

**Issue**: [Specific description of the security issue]

**Threat**: [What attack this enables]

**Insecure Code**:
```[language]
[Code snippet showing the vulnerability]
```

**Secure Alternative**:
```[language]
[Code snippet showing the fix]
```

**Remediation**:
1. [Specific step-by-step remediation]
2. [With actionable guidance]

**Priority**: [Critical/High/Medium/Low]

---

[Repeat for each finding]

## Recommendations

1. [High-level security improvements]
2. [Process improvements for secure coding]

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Security checklist](references/security-checklist.md)
```

## Quality Standards

Every security review must meet these standards:

- [ ] **Specific line numbers**: Every finding includes file:line reference
- [ ] **Code examples**: Show insecure pattern AND secure alternative
- [ ] **Context-aware**: Recommendations specific to language/framework
- [ ] **Threat explanation**: Explain WHY it's a security issue
- [ ] **Actionable remediation**: Specific steps to fix, not vague suggestions
- [ ] **Priority justified**: Risk level explained by likelihood × impact
- [ ] **No false positives**: Validate findings in context before reporting
- [ ] **Tested solutions**: Secure code examples are tested and working

## Common Security Patterns

### Input Validation
- **Whitelist approach**: Define allowed characters/formats, reject everything else
- **Early rejection**: Validate at API boundary, not deep in logic
- **Type checking**: Enforce expected data types (int, email, UUID)
- **Length limits**: Prevent buffer overflows and DoS

### Output Encoding
- **Framework functions**: Use built-in encoding (escapeHtml, encodeURIComponent)
- **Context-aware**: Different encoding for HTML, JS, URL, CSS contexts
- **Don't trust sanitization**: Encode on output, even if input was sanitized

### Authentication
- **Password hashing**: bcrypt (cost ≥10) or Argon2
- **JWT**: RS256 signing, 15-minute access tokens, secure refresh tokens
- **MFA**: Implement for sensitive operations
- **Rate limiting**: Prevent brute force attacks

### Authorization
- **Check on every request**: Don't rely on client-side checks
- **Least privilege**: Grant minimum permissions needed
- **Object-level checks**: Verify user owns the resource
- **Role-based access control (RBAC)**: Centralized permission management

### Cryptography
- **Strong algorithms**: AES-256-GCM, RSA-4096, ECDSA P-384
- **Unique IV/nonce**: Generate new for each encryption
- **Secure random**: Use secrets module (Python) or crypto.getRandomValues (JS)
- **Key management**: Store keys in KMS/environment, never in code

## References

For detailed security guidelines, see:
- [Security Checklist](references/security-checklist.md) - Comprehensive security review checklist
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Most critical web application security risks

## Integration

This skill works with:
- **Backend Developer agent**: For implementing security fixes
- **Frontend Developer agent**: For client-side security fixes
- **Code Reviewer agent**: For integrating security into PR reviews
- **Authentication-security skill**: For deep auth implementation review
