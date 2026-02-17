# Security Patterns and Vulnerability Checks

This guide provides detailed patterns for identifying common security vulnerabilities during code review.

## OWASP Top 10 Patterns

### 1. SQL Injection

**Vulnerability pattern:**
```javascript
// BAD: String concatenation
const query = "SELECT * FROM users WHERE id = " + userId;
db.execute(query);

// BAD: Template literals
const query = `SELECT * FROM users WHERE email = '${email}'`;
```

**Safe pattern:**
```javascript
// GOOD: Parameterized queries
const query = "SELECT * FROM users WHERE id = ?";
db.execute(query, [userId]);

// GOOD: ORM with proper escaping
const user = await User.findById(userId);
```

**What to check:**
- [ ] All database queries use parameterized queries or prepared statements
- [ ] No string concatenation or template literals in SQL
- [ ] ORM usage follows safe patterns
- [ ] Dynamic table/column names are validated against allowlist

### 2. Cross-Site Scripting (XSS)

**Vulnerability pattern:**
```javascript
// BAD: Unescaped user input in HTML
element.innerHTML = userInput;

// BAD: Direct DOM manipulation
document.write(userInput);

// BAD: Unsafe attribute setting
element.setAttribute('href', userInput);
```

**Safe pattern:**
```javascript
// GOOD: Use textContent instead of innerHTML
element.textContent = userInput;

// GOOD: Framework-provided escaping
<div>{userInput}</div>  // React auto-escapes

// GOOD: Explicit sanitization
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

**What to check:**
- [ ] User input is escaped before rendering in HTML
- [ ] Framework's escaping mechanisms are used
- [ ] innerHTML is avoided or sanitized
- [ ] URL parameters are validated before use
- [ ] Event handlers don't execute untrusted code

### 3. Command Injection

**Vulnerability pattern:**
```python
# BAD: String concatenation in shell commands
os.system("ping " + user_input)

# BAD: Shell=True with user input
subprocess.call("ls " + directory, shell=True)
```

**Safe pattern:**
```python
# GOOD: Avoid shell entirely
subprocess.run(["ping", "-c", "1", user_input])

# GOOD: Input validation with allowlist
if re.match(r'^[a-zA-Z0-9_-]+$', user_input):
    subprocess.run(["ping", "-c", "1", user_input])
else:
    raise ValueError("Invalid input")
```

**What to check:**
- [ ] No shell=True with user input
- [ ] Avoid os.system, os.popen, eval, exec
- [ ] Use array form of subprocess calls
- [ ] Validate input against strict allowlist
- [ ] Consider if shell command is necessary at all

### 4. Path Traversal

**Vulnerability pattern:**
```javascript
// BAD: Direct path concatenation
const filePath = "/uploads/" + userFileName;
fs.readFile(filePath);

// BAD: No validation
app.get('/download/:file', (req, res) => {
  res.sendFile(req.params.file);
});
```

**Safe pattern:**
```javascript
// GOOD: Validate against directory
const path = require('path');
const uploadsDir = path.resolve('/uploads');
const filePath = path.resolve(uploadsDir, userFileName);
if (!filePath.startsWith(uploadsDir)) {
  throw new Error("Invalid file path");
}

// GOOD: Use allowlist
const allowedFiles = ['report.pdf', 'summary.txt'];
if (!allowedFiles.includes(userFileName)) {
  throw new Error("File not allowed");
}
```

**What to check:**
- [ ] File paths validated to stay within allowed directory
- [ ] No ../ or absolute paths from user input
- [ ] Path.resolve used to canonicalize paths
- [ ] File allowlist when possible
- [ ] Filesystem permissions properly restricted

### 5. Server-Side Request Forgery (SSRF)

**Vulnerability pattern:**
```javascript
// BAD: Fetch user-provided URL directly
app.post('/fetch', async (req, res) => {
  const response = await fetch(req.body.url);
  res.send(await response.text());
});

// BAD: No URL validation
const data = await axios.get(userProvidedUrl);
```

**Safe pattern:**
```javascript
// GOOD: Validate URL against allowlist
const allowedDomains = ['api.example.com', 'cdn.example.com'];
const url = new URL(userProvidedUrl);
if (!allowedDomains.includes(url.hostname)) {
  throw new Error("Domain not allowed");
}

// GOOD: Block internal IP ranges
const isInternal = (hostname) => {
  return hostname === 'localhost' ||
         hostname.startsWith('127.') ||
         hostname.startsWith('192.168.') ||
         hostname.startsWith('10.') ||
         hostname.startsWith('172.16.');
};
if (isInternal(url.hostname)) {
  throw new Error("Internal URLs not allowed");
}
```

**What to check:**
- [ ] External URLs validated against allowlist
- [ ] Internal IP ranges blocked (localhost, 127.x, 192.168.x, 10.x)
- [ ] Cloud metadata endpoints blocked (169.254.169.254)
- [ ] URL scheme validated (http/https only)
- [ ] Consider if external fetch is necessary

### 6. Insecure Deserialization

**Vulnerability pattern:**
```python
# BAD: Unpickling untrusted data
import pickle
data = pickle.loads(user_input)

# BAD: eval on untrusted data
result = eval(user_input)

# BAD: YAML unsafe load
import yaml
config = yaml.load(user_input)
```

**Safe pattern:**
```python
# GOOD: Use JSON instead of pickle
import json
data = json.loads(user_input)

# GOOD: Safe YAML loading
config = yaml.safe_load(user_input)

# GOOD: Validate schema
from jsonschema import validate
validate(data, schema)
```

**What to check:**
- [ ] No pickle, eval, exec on untrusted input
- [ ] JSON preferred over pickle/yaml
- [ ] YAML uses safe_load not load
- [ ] Deserialized data validated against schema
- [ ] Type checking on deserialized objects

### 7. Broken Authentication

**Vulnerability pattern:**
```javascript
// BAD: Storing passwords in plain text
db.insert({ username, password });

// BAD: Weak password hashing
const hash = md5(password);

// BAD: Predictable session tokens
const sessionId = Date.now().toString();

// BAD: No session expiration
sessions[sessionId] = user;
```

**Safe pattern:**
```javascript
// GOOD: Bcrypt for password hashing
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(password, 10);

// GOOD: Cryptographically random tokens
const crypto = require('crypto');
const sessionId = crypto.randomBytes(32).toString('hex');

// GOOD: Session expiration
sessions[sessionId] = {
  user,
  expiresAt: Date.now() + 30 * 60 * 1000  // 30 minutes
};
```

**What to check:**
- [ ] Passwords hashed with bcrypt/argon2/scrypt
- [ ] No weak hashing (MD5, SHA1)
- [ ] Session tokens are cryptographically random
- [ ] Sessions expire after timeout
- [ ] Multi-factor authentication for sensitive operations
- [ ] Rate limiting on authentication endpoints

### 8. Broken Access Control

**Vulnerability pattern:**
```javascript
// BAD: Only client-side authorization
if (user.role === 'admin') {
  showAdminPanel();  // Client-side only
}

// BAD: Insecure direct object reference
app.get('/document/:id', (req, res) => {
  const doc = db.getDocument(req.params.id);
  res.send(doc);  // No ownership check
});

// BAD: Missing authorization check
app.post('/deleteUser/:id', (req, res) => {
  db.deleteUser(req.params.id);  // No check if user can delete
});
```

**Safe pattern:**
```javascript
// GOOD: Server-side authorization
app.get('/admin/panel', requireAuth, requireRole('admin'), (req, res) => {
  // Authorized access
});

// GOOD: Ownership verification
app.get('/document/:id', requireAuth, async (req, res) => {
  const doc = await db.getDocument(req.params.id);
  if (doc.ownerId !== req.user.id && !req.user.isAdmin) {
    return res.status(403).send("Forbidden");
  }
  res.send(doc);
});
```

**What to check:**
- [ ] Authorization checked server-side for all protected resources
- [ ] Ownership verified for user-specific resources
- [ ] Role-based access control enforced consistently
- [ ] Default deny (require explicit permission grants)
- [ ] Horizontal privilege escalation prevented (user can't access other user's data)
- [ ] Vertical privilege escalation prevented (user can't perform admin actions)

### 9. Security Misconfiguration

**Vulnerability pattern:**
```javascript
// BAD: Debug mode in production
app.set('env', 'development');

// BAD: Verbose error messages
app.use((err, req, res, next) => {
  res.status(500).send(err.stack);  // Leaks implementation details
});

// BAD: Default credentials
const adminPassword = 'admin123';

// BAD: Unnecessary features enabled
app.use(cors({ origin: '*' }));  // Allow all origins
```

**Safe pattern:**
```javascript
// GOOD: Production-appropriate config
if (process.env.NODE_ENV === 'production') {
  app.disable('x-powered-by');
  app.set('trust proxy', 1);
}

// GOOD: Generic error messages
app.use((err, req, res, next) => {
  logger.error(err.stack);  // Log internally
  res.status(500).send("Internal server error");  // Generic message
});

// GOOD: Strong generated credentials
const adminPassword = crypto.randomBytes(32).toString('hex');

// GOOD: Restrictive CORS
app.use(cors({ origin: 'https://example.com' }));
```

**What to check:**
- [ ] Debug mode disabled in production
- [ ] Error messages don't leak implementation details
- [ ] Default credentials changed
- [ ] CORS configured restrictively
- [ ] Security headers set (CSP, HSTS, X-Frame-Options)
- [ ] Unnecessary features disabled

### 10. Insufficient Logging & Monitoring

**Vulnerability pattern:**
```javascript
// BAD: No logging of security events
app.post('/login', (req, res) => {
  if (checkPassword(req.body.password)) {
    return res.send({token});  // Success not logged
  }
  res.status(401).send("Invalid password");  // Failure not logged
});

// BAD: Logging sensitive data
logger.info("User login", { password: req.body.password });  // Don't log passwords

// BAD: No alerting on anomalies
// Silent failures with no notification
```

**Safe pattern:**
```javascript
// GOOD: Log security events
app.post('/login', (req, res) => {
  if (checkPassword(req.body.password)) {
    logger.info("Successful login", {
      userId: user.id,
      ip: req.ip,
      timestamp: Date.now()
    });
    return res.send({token});
  }
  logger.warn("Failed login attempt", {
    username: req.body.username,
    ip: req.ip,
    timestamp: Date.now()
  });
  res.status(401).send("Invalid credentials");
});

// GOOD: Monitor for anomalies
if (failedAttempts > 5) {
  alertSecurityTeam("Multiple failed login attempts", { ip: req.ip });
}
```

**What to check:**
- [ ] Security events logged (login, logout, access control failures)
- [ ] Sensitive data not logged (passwords, tokens, PII)
- [ ] Logs include context (user, IP, timestamp)
- [ ] Anomaly detection in place
- [ ] Alerts configured for security events
- [ ] Log retention appropriate for compliance

## Additional Security Patterns

### Secrets Management

**What to check:**
- [ ] No secrets in code (API keys, passwords, tokens)
- [ ] No secrets in config files committed to git
- [ ] Secrets loaded from environment variables or secret manager
- [ ] Secrets not logged or exposed in errors
- [ ] Secrets rotated regularly

**Example:**
```javascript
// BAD
const apiKey = "sk_live_abc123def456";

// GOOD
const apiKey = process.env.API_KEY;
if (!apiKey) {
  throw new Error("API_KEY environment variable not set");
}
```

### Input Validation

**Validation principles:**
- Validate on server-side (never trust client)
- Allowlist over blocklist
- Validate type, format, length, range
- Sanitize after validation
- Fail securely (reject on validation failure)

**Example:**
```javascript
// GOOD: Comprehensive validation
const validateEmail = (email) => {
  if (typeof email !== 'string') return false;
  if (email.length > 254) return false;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

if (!validateEmail(req.body.email)) {
  return res.status(400).send("Invalid email format");
}
```

### Cryptography

**What to check:**
- [ ] Use standard crypto libraries (not custom implementations)
- [ ] Strong algorithms (AES-256, RSA-2048+, SHA-256+)
- [ ] No weak algorithms (DES, MD5, SHA1)
- [ ] Proper key management
- [ ] Initialization vectors (IVs) are random and unique
- [ ] HTTPS/TLS for data in transit

**Example:**
```javascript
// GOOD: Proper encryption
const crypto = require('crypto');
const algorithm = 'aes-256-cbc';
const key = crypto.randomBytes(32);
const iv = crypto.randomBytes(16);

const cipher = crypto.createCipheriv(algorithm, key, iv);
let encrypted = cipher.update(text, 'utf8', 'hex');
encrypted += cipher.final('hex');
```

### Rate Limiting

**What to check:**
- [ ] Rate limiting on authentication endpoints
- [ ] Rate limiting on sensitive operations
- [ ] Per-user and per-IP limits
- [ ] Appropriate limits for use case
- [ ] 429 status code on rate limit exceeded

**Example:**
```javascript
// GOOD: Rate limiting
const rateLimit = require('express-rate-limit');

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,  // 5 requests per window
  message: "Too many login attempts, please try again later"
});

app.post('/login', loginLimiter, (req, res) => {
  // Login logic
});
```

## Review Checklist

### Input Validation
- [ ] All user input validated at entry points
- [ ] Type, format, length, range checks performed
- [ ] Allowlist validation where possible
- [ ] Sanitization after validation

### Authentication & Authorization
- [ ] Passwords hashed with strong algorithm
- [ ] Session tokens cryptographically random
- [ ] Authorization checked server-side
- [ ] Ownership verified for user resources
- [ ] Rate limiting on auth endpoints

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS/TLS for data in transit
- [ ] No secrets in code or logs
- [ ] PII handled according to regulations

### Injection Prevention
- [ ] Parameterized queries for SQL
- [ ] Output encoding for HTML
- [ ] No shell execution with user input
- [ ] Path validation for file access
- [ ] URL validation for SSRF prevention

### Error Handling
- [ ] Generic error messages to users
- [ ] Detailed errors logged internally
- [ ] No stack traces exposed
- [ ] Security events logged

### Dependencies
- [ ] Dependencies up to date
- [ ] No known vulnerabilities (check npm audit, safety)
- [ ] Minimal dependency footprint
- [ ] Trusted sources only
