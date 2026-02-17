# Security Baseline for Everyday Coding

Use OWASP secure coding practices as a default checklist. Bake security into every line of code.

## 1. Input Validation

### Treat All External Data as Untrusted
* Validate all inputs from users, APIs, files, databases, environment variables
* Define expected format, type, length, range, and enforce it
* Reject invalid input - do not attempt to sanitize dangerous input

### Validation Rules
* **Whitelist over blacklist**: Define what is allowed, not what is forbidden
* **Type checking**: Ensure data matches expected type before processing
* **Length limits**: Enforce maximum lengths for strings, arrays, files
* **Range checking**: Validate numeric values are within acceptable range
* **Format validation**: Use regex or parsers for structured data (email, URL, date)

### Examples
```python
# Python
def create_user(email: str, age: int) -> User:
    # Validate email format
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError("Invalid email format")

    # Validate age range
    if not 0 <= age <= 150:
        raise ValueError("Age must be between 0 and 150")

    return User(email=email, age=age)
```

```typescript
// TypeScript
function createUser(email: unknown, age: unknown): User {
  // Type guard validation
  if (typeof email !== 'string' || typeof age !== 'number') {
    throw new Error('Invalid input types');
  }

  // Format validation
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailRegex.test(email)) {
    throw new Error('Invalid email format');
  }

  // Range validation
  if (age < 0 || age > 150) {
    throw new Error('Age must be between 0 and 150');
  }

  return { email, age };
}
```

## 2. Output Encoding

### Encode Data for the Target Context
* **HTML context**: Use HTML entity encoding to prevent XSS
* **JavaScript context**: Use JavaScript encoding
* **SQL context**: Use parameterized queries (never string concatenation)
* **URL context**: Use URL encoding
* **Shell context**: Avoid shell execution; if necessary, use proper escaping

### Examples
```python
# Python - HTML escaping
import html
user_input = "<script>alert('XSS')</script>"
safe_output = html.escape(user_input)  # &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;

# Python - SQL parameterized queries
import sqlite3
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
# Good - parameterized
cursor.execute("SELECT * FROM users WHERE email = ?", (user_email,))
# Bad - SQL injection vulnerable
# cursor.execute(f"SELECT * FROM users WHERE email = '{user_email}'")

# Python - avoid shell injection
import subprocess
# Good - list of arguments
subprocess.run(['ls', '-l', user_directory])
# Bad - shell=True with user input
# subprocess.run(f'ls -l {user_directory}', shell=True)
```

```typescript
// TypeScript - parameterized queries (with a hypothetical DB library)
const email = userInput;
// Good - parameterized
await db.query('SELECT * FROM users WHERE email = $1', [email]);
// Bad - SQL injection vulnerable
// await db.query(`SELECT * FROM users WHERE email = '${email}'`);

// TypeScript - HTML escaping (if not using a framework that auto-escapes)
function escapeHtml(unsafe: string): string {
  return unsafe
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
```

## 3. Error Handling Without Leaking Secrets

### Safe Error Handling
* Log detailed errors internally (for debugging)
* Return generic errors externally (to users/APIs)
* Never expose stack traces, file paths, database schemas, or internal logic in production
* Never log sensitive data (passwords, tokens, credit cards, PII)

### Examples
```python
# Python
import logging

logger = logging.getLogger(__name__)

def process_payment(card_number: str, amount: float) -> dict:
    try:
        # Process payment logic
        payment_service.charge(card_number, amount)
        return {"status": "success"}
    except PaymentError as e:
        # Log detailed error internally (sanitized)
        logger.error(f"Payment failed for amount {amount}: {e}", exc_info=True)
        # Return generic error to user
        return {"status": "error", "message": "Payment processing failed"}
    except Exception as e:
        # Catch-all for unexpected errors
        logger.critical(f"Unexpected error in payment processing: {e}", exc_info=True)
        return {"status": "error", "message": "An unexpected error occurred"}
```

```typescript
// TypeScript
async function processPayment(cardNumber: string, amount: number): Promise<PaymentResult> {
  try {
    await paymentService.charge(cardNumber, amount);
    return { status: 'success' };
  } catch (error) {
    // Log detailed error internally
    logger.error('Payment failed', { amount, error });

    // Return generic error to user (never expose internal details)
    if (error instanceof PaymentError) {
      return { status: 'error', message: 'Payment processing failed' };
    }
    return { status: 'error', message: 'An unexpected error occurred' };
  }
}
```

## 4. Logging Security Events

### What to Log
* Authentication attempts (success and failure)
* Authorization failures
* Input validation failures
* Security-relevant configuration changes
* Administrative actions

### What NOT to Log
* Passwords or password hashes
* Session tokens or API keys
* Credit card numbers or financial data
* Personal identifiable information (PII) unless required and protected

### Examples
```python
# Python
import logging

logger = logging.getLogger(__name__)

# Good - log security event without sensitive data
logger.warning(f"Failed login attempt for user {username} from IP {ip_address}")

# Bad - logging sensitive data
# logger.debug(f"Login attempt with password: {password}")
```

```typescript
// TypeScript
// Good - log security event
logger.warn('Failed login attempt', { username, ipAddress });

// Bad - logging sensitive data
// logger.debug('Login attempt', { username, password });
```

## 5. Authentication and Session Management

### Passwords
* Never store passwords in plaintext
* Use strong, adaptive hashing algorithms: bcrypt, scrypt, or Argon2
* Enforce strong password policies (length, complexity)
* Implement rate limiting on login attempts
* Use secure password reset flows (time-limited tokens, not security questions)

### Sessions and Tokens
* Use secure, random session identifiers (cryptographically strong PRNG)
* Set appropriate session timeouts
* Invalidate sessions on logout
* Use `httpOnly`, `secure`, and `sameSite` flags for cookies
* Regenerate session IDs after login (prevent session fixation)

### Examples
```python
# Python - password hashing with bcrypt
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

## 6. Least Privilege

### Principle
* Grant minimum permissions necessary to perform a task
* Run services with minimal OS privileges
* Use separate database accounts with minimal permissions for different operations
* Restrict file system access
* Avoid running as root/administrator

### Examples
```python
# Python - file permissions
import os
import stat

# Create file with restricted permissions (owner read/write only)
file_path = '/path/to/sensitive/file'
fd = os.open(file_path, os.O_CREAT | os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)
os.close(fd)
```

## 7. Cryptography

### Use Standard Libraries
* Never implement your own cryptography
* Use well-vetted libraries: `cryptography` (Python), `crypto` (Node.js)
* Use standard algorithms: AES-256-GCM for encryption, SHA-256 for hashing
* Use strong key sizes: 256-bit for symmetric, 2048-bit+ for RSA, 256-bit for ECC

### Secure Random Number Generation
```python
# Python - secure random
import secrets

# Generate secure random token
token = secrets.token_urlsafe(32)

# Generate random choice
secret_value = secrets.choice(['a', 'b', 'c'])
```

```typescript
// TypeScript - secure random (Node.js)
import crypto from 'crypto';

// Generate secure random token
const token = crypto.randomBytes(32).toString('base64url');
```

## 8. Dependency Management

### Keep Dependencies Updated
* Regularly update dependencies to patch security vulnerabilities
* Use automated tools: `pip-audit` (Python), `npm audit` (Node.js)
* Pin dependency versions for reproducibility
* Review security advisories for dependencies

### Examples
```bash
# Python - check for vulnerabilities
pip-audit

# Node.js - check for vulnerabilities
npm audit
npm audit fix
```

## 9. OWASP Top 10 Quick Reference

1. **Broken Access Control**: Enforce authorization checks on every request
2. **Cryptographic Failures**: Use strong encryption, secure key management
3. **Injection**: Use parameterized queries, validate input, encode output
4. **Insecure Design**: Threat model during design, use secure design patterns
5. **Security Misconfiguration**: Secure defaults, disable unnecessary features, patch regularly
6. **Vulnerable and Outdated Components**: Keep dependencies updated, remove unused dependencies
7. **Identification and Authentication Failures**: Strong authentication, secure session management
8. **Software and Data Integrity Failures**: Verify integrity of code and data (signatures, checksums)
9. **Security Logging and Monitoring Failures**: Log security events, monitor for anomalies
10. **Server-Side Request Forgery (SSRF)**: Validate and sanitize URLs, use allowlists

Reference: https://owasp.org/www-project-top-ten/

## 10. Secure Coding Checklist

Use this checklist for every code change:

- [ ] All external inputs validated (type, format, length, range)
- [ ] Outputs encoded for target context (HTML, SQL, URL, etc.)
- [ ] Parameterized queries used (no string concatenation for SQL)
- [ ] No sensitive data in logs (passwords, tokens, PII)
- [ ] Errors handled without leaking internal details
- [ ] Authentication and authorization enforced
- [ ] Secure password storage (bcrypt, scrypt, or Argon2)
- [ ] Session management secure (secure cookies, timeouts, regeneration)
- [ ] Least privilege applied (minimal permissions)
- [ ] Standard cryptography libraries used (no custom crypto)
- [ ] Dependencies updated and audited
- [ ] Security-relevant events logged

Reference: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/
