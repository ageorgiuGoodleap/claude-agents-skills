---
name: security-review
description: |
  Security vulnerability analysis for OWASP Top 10 and common security issues.

  WHAT: Reviews code for security vulnerabilities including injection (SQL, XSS, command), broken authentication/authorization, sensitive data exposure, hardcoded secrets, insecure deserialization, security misconfigurations, and vulnerable dependencies. Checks input validation, password handling, session management, CSRF protection. Rates severity as Critical, High, Medium, or Low with remediation guidance.

  WHEN: Use for security-sensitive code reviews, pre-merge checks, or audits. Trigger on: "security review", "security check", "vulnerability review", "OWASP", "injection", "XSS", "SQL injection", "authentication", "authorization", "hardcoded secrets", "sensitive data".
allowed-tools: Read, Grep, Glob
---

# Security Review Skill

## Overview

This skill conducts focused security analysis on code changes, checking for OWASP Top 10 vulnerabilities, input validation issues, authentication/authorization flaws, and hardcoded secrets. It rates vulnerabilities by severity and provides specific remediation guidance with secure code examples.

## OWASP Top 10 (2021)

This skill checks for these critical security risks:

1. **A01:2021 – Broken Access Control**
2. **A02:2021 – Cryptographic Failures**
3. **A03:2021 – Injection** (SQL, XSS, Command, LDAP)
4. **A04:2021 – Insecure Design**
5. **A05:2021 – Security Misconfiguration**
6. **A06:2021 – Vulnerable and Outdated Components**
7. **A07:2021 – Identification and Authentication Failures**
8. **A08:2021 – Software and Data Integrity Failures**
9. **A09:2021 – Security Logging and Monitoring Failures**
10. **A10:2021 – Server-Side Request Forgery (SSRF)**

## Workflow

### 1. Identify Security-Sensitive Code Areas

Prioritize review of these high-risk areas:

- **Authentication logic:** Login, logout, password reset, session management
- **Authorization checks:** Permission verification, role-based access control
- **Input handling:** User input processing, form submissions, API parameters
- **Database operations:** SQL queries, ORM usage, raw database access
- **API endpoints:** REST/GraphQL endpoints accepting external input
- **File operations:** Uploads, downloads, path handling
- **Cryptographic operations:** Encryption, hashing, token generation
- **Command execution:** Shell commands, subprocess calls
- **Serialization/deserialization:** JSON, XML, YAML, pickle processing
- **Session management:** Cookie handling, JWT tokens, session storage

### 2. Check for SQL Injection (A03 - Injection)

SQL injection occurs when untrusted data is concatenated directly into SQL queries.

**Vulnerable patterns:**

```python
# Python - VULNERABLE
query = f"SELECT * FROM users WHERE email = '{user_email}'"
cursor.execute(query)

# JavaScript - VULNERABLE
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

# PHP - VULNERABLE
$query = "SELECT * FROM users WHERE name = '" . $_POST['name'] . "'";
mysqli_query($conn, $query);
```

**Secure alternatives:**

```python
# Python - SECURE (parameterized)
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (user_email,))

# JavaScript - SECURE (parameterized)
const query = "SELECT * FROM users WHERE id = ?";
db.query(query, [userId]);

# PHP - SECURE (prepared statement)
$stmt = $conn->prepare("SELECT * FROM users WHERE name = ?");
$stmt->bind_param("s", $_POST['name']);
$stmt->execute();
```

**ORM-specific checks:**

```python
# Django ORM - SAFE by default
User.objects.filter(email=user_email)  # Safe

# Django raw() - VULNERABLE if concatenating
User.objects.raw(f"SELECT * FROM users WHERE email = '{email}'")  # VULNERABLE

# Django raw() - SECURE with parameters
User.objects.raw("SELECT * FROM users WHERE email = %s", [email])  # Safe
```

### 3. Check for Cross-Site Scripting (XSS) (A03 - Injection)

XSS occurs when user input is rendered in HTML without proper escaping.

**Vulnerable patterns:**

```javascript
// JavaScript - VULNERABLE
document.getElementById('output').innerHTML = userInput;

// React - VULNERABLE
<div dangerouslySetInnerHTML={{__html: userInput}} />

// Vue - VULNERABLE
<div v-html="userInput"></div>
```

**Secure alternatives:**

```javascript
// JavaScript - SECURE (textContent)
document.getElementById('output').textContent = userInput;

// React - SECURE (default escaping)
<div>{userInput}</div>

// Vue - SECURE (default escaping)
<div>{{ userInput }}</div>
```

**Template-specific checks:**

```html
<!-- Django - SAFE by default -->
<div>{{ user.name }}</div>

<!-- Django - VULNERABLE if marked safe -->
<div>{{ user.name|safe }}</div>  <!-- Review carefully -->

<!-- Jinja2 - SAFE by default -->
<div>{{ user.name }}</div>

<!-- Jinja2 - VULNERABLE if marked safe -->
<div>{{ user.name|safe }}</div>  <!-- Review carefully -->
```

### 4. Check for Command Injection (A03 - Injection)

Command injection occurs when user input is passed to shell commands without sanitization.

**Vulnerable patterns:**

```python
# Python - VULNERABLE
import os
filename = request.GET['file']
os.system(f"cat {filename}")  # Attacker can inject commands

# Python - VULNERABLE
import subprocess
subprocess.call(f"ping {host}", shell=True)  # shell=True enables injection
```

**Secure alternatives:**

```python
# Python - SECURE (no shell, parameterized)
import subprocess
subprocess.run(["cat", filename], shell=False, check=True)

# Python - SECURE (validate input)
import shlex
safe_host = shlex.quote(host)
subprocess.run(f"ping {safe_host}", shell=True, check=True)

# Python - BEST (avoid shell entirely)
subprocess.run(["ping", "-c", "1", host], shell=False, check=True)
```

### 5. Check for Broken Authentication (A07)

Review authentication implementations for these weaknesses:

**Password Storage:**

```python
# VULNERABLE - Plain text
user.password = password

# VULNERABLE - Weak hashing (MD5, SHA1)
import hashlib
user.password = hashlib.md5(password.encode()).hexdigest()

# SECURE - bcrypt with salt
import bcrypt
salt = bcrypt.gensalt()
user.password_hash = bcrypt.hashpw(password.encode(), salt)
```

**Password Policies:**

```python
# WEAK - Too permissive
if len(password) >= 6:
    # Accept password

# STRONG - Enforces complexity
import re

def validate_password(password):
    if len(password) < 12:
        raise ValueError("Minimum 12 characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Must contain uppercase")
    if not re.search(r"[a-z]", password):
        raise ValueError("Must contain lowercase")
    if not re.search(r"[0-9]", password):
        raise ValueError("Must contain digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Must contain special character")
```

**Session Management:**

```python
# VULNERABLE - Predictable session IDs
session_id = str(user.id)

# SECURE - Cryptographically random session IDs
import secrets
session_id = secrets.token_urlsafe(32)

# VULNERABLE - No session expiration
session.save()

# SECURE - Session expiration
session.set_expiry(3600)  # 1 hour
session.save()
```

**JWT Token Issues:**

```python
# VULNERABLE - Weak secret
jwt.encode(payload, "secret", algorithm="HS256")

# SECURE - Strong secret from environment
import os
jwt.encode(payload, os.environ['JWT_SECRET'], algorithm="HS256")

# VULNERABLE - No expiration
payload = {"user_id": user.id}

# SECURE - Include expiration
import time
payload = {
    "user_id": user.id,
    "exp": int(time.time()) + 3600  # 1 hour
}
```

### 6. Check for Broken Access Control (A01)

Ensure proper authorization checks are in place:

**Insecure Direct Object References (IDOR):**

```python
# VULNERABLE - No ownership check
@app.route('/document/<int:doc_id>')
def view_document(doc_id):
    doc = Document.query.get(doc_id)
    return render_template('document.html', doc=doc)

# SECURE - Verify ownership
@app.route('/document/<int:doc_id>')
@login_required
def view_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.owner_id != current_user.id:
        abort(403)  # Forbidden
    return render_template('document.html', doc=doc)
```

**Missing Permission Checks:**

```python
# VULNERABLE - Admin action without check
@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    return redirect('/admin/users')

# SECURE - Verify admin role
@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)
    User.query.filter_by(id=user_id).delete()
    return redirect('/admin/users')
```

### 7. Check for Sensitive Data Exposure (A02)

**Hardcoded Secrets:**

```python
# VULNERABLE - Hardcoded credentials
API_KEY = "sk_live_abc123xyz789"
DB_PASSWORD = "admin123"

# SECURE - Environment variables
import os
API_KEY = os.environ.get('API_KEY')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
```

**Logging Sensitive Data:**

```python
# VULNERABLE - Logging passwords/tokens
logger.info(f"User {username} logged in with password {password}")
logger.debug(f"API call with token {api_token}")

# SECURE - Mask sensitive data
logger.info(f"User {username} logged in successfully")
logger.debug(f"API call with token {'*' * 10}")

# VULNERABLE - Logging credit cards
logger.info(f"Processing payment for card {card_number}")

# SECURE - Mask card numbers
masked = f"****-****-****-{card_number[-4:]}"
logger.info(f"Processing payment for card {masked}")
```

**Unencrypted Data:**

```python
# VULNERABLE - Storing sensitive data in plain text
user.ssn = request.form['ssn']

# SECURE - Encrypt before storage
from cryptography.fernet import Fernet
cipher = Fernet(encryption_key)
user.ssn_encrypted = cipher.encrypt(request.form['ssn'].encode())
```

### 8. Check for CSRF Protection (A01)

Cross-Site Request Forgery allows attackers to perform unauthorized actions using a victim's session.

**Vulnerable:**

```python
# Flask - No CSRF protection
@app.route('/update-email', methods=['POST'])
def update_email():
    current_user.email = request.form['email']
    db.session.commit()
    return redirect('/profile')
```

**Secure:**

```python
# Flask with CSRF protection
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

@app.route('/update-email', methods=['POST'])
@csrf.protect()  # CSRF token validated
def update_email():
    current_user.email = request.form['email']
    db.session.commit()
    return redirect('/profile')
```

**Framework-specific:**

- **Django:** CSRF protection enabled by default, ensure `{% csrf_token %}` in forms
- **Express.js:** Use `csurf` middleware
- **Rails:** Protect from forgery enabled by default

### 9. Check for Insecure Deserialization (A08)

**Vulnerable:**

```python
# Python - VULNERABLE (pickle can execute arbitrary code)
import pickle
data = pickle.loads(user_input)

# YAML - VULNERABLE (can execute code)
import yaml
data = yaml.load(user_input)  # Unsafe
```

**Secure:**

```python
# Python - SECURE (use JSON)
import json
data = json.loads(user_input)  # Safe

# YAML - SECURE (safe loader)
import yaml
data = yaml.safe_load(user_input)  # Safe
```

### 10. Check Input Validation

**Missing Validation:**

```python
# VULNERABLE - No validation
age = request.form['age']
user.age = age  # Could be negative, string, etc.

# SECURE - Validate type and range
age = int(request.form['age'])
if not (0 <= age <= 150):
    raise ValueError("Invalid age")
user.age = age
```

**Path Traversal:**

```python
# VULNERABLE - Path traversal
filename = request.args['file']
with open(f"/uploads/{filename}") as f:
    content = f.read()  # Attacker can use "../../../etc/passwd"

# SECURE - Validate path
import os
filename = os.path.basename(request.args['file'])  # Remove path components
filepath = os.path.join("/uploads", filename)
if not filepath.startswith("/uploads/"):
    raise ValueError("Invalid path")
with open(filepath) as f:
    content = f.read()
```

### 11. Check for Security Misconfigurations (A05)

**Debug Mode in Production:**

```python
# VULNERABLE
DEBUG = True  # Exposes stack traces, environment variables

# SECURE
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

**Missing Security Headers:**

```python
# Add security headers
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### 12. Check Vulnerable Dependencies (A06)

**Run security audits:**

```bash
# Python
pip install pip-audit
pip-audit

# JavaScript/Node.js
npm audit

# Ruby
bundle audit

# Rust
cargo audit
```

**Look for:**
- Dependencies with known CVEs
- Outdated packages with security patches
- Unmaintained libraries

### 13. Rate Vulnerability Severity

Use this severity rating system:

**Critical (Fix Immediately):**
- Exploitable remotely without authentication
- High impact: data breach, system compromise, privilege escalation
- Examples: SQL injection, authentication bypass, remote code execution

**High (Should Fix Before Merge):**
- Exploitable with moderate effort or authenticated access
- Significant impact: data exposure, unauthorized access
- Examples: XSS, CSRF, missing authorization checks

**Medium (Address Soon):**
- Difficult to exploit or requires specific conditions
- Moderate impact: information disclosure, DoS potential
- Examples: weak password policies, information leakage, insecure configurations

**Low (Improve Defense-in-Depth):**
- Informational or defense-in-depth improvements
- Low impact: minor information disclosure
- Examples: missing security headers, verbose error messages

## Output Format

Present findings in this structured format:

```markdown
# Security Review

## Summary
**Status:** [SECURE / MINOR CONCERNS / VULNERABILITIES FOUND / CRITICAL ISSUES]
**Critical Vulnerabilities:** [count]
**High Severity:** [count]
**Medium Severity:** [count]
**Low Severity:** [count]

---

## 🔴 CRITICAL VULNERABILITIES (Fix Immediately)

### [Number]. [Vulnerability Type] in `file.py:line`
- **Location:** `function_name()`
- **Vulnerability:** OWASP A0X:2021 - [Category]
- **CWE:** CWE-XXX ([CWE Name])
- **Current Code:**
  ```[language]
  [vulnerable code]
  ```
- **Attack Scenario:**
  [Description of how attacker could exploit]
  ```
  [Example malicious input]
  ```
- **Impact:** [Concrete consequences]
- **Fix:**
  ```[language]
  [secure code]
  ```
- **Verification:** [How to test the fix]

---

## 🟡 HIGH SEVERITY VULNERABILITIES (Should Fix)

[Same structure as Critical]

---

## 🟠 MEDIUM SEVERITY ISSUES (Consider Fixing)

[Same structure as Critical]

---

## 🟢 LOW SEVERITY / INFORMATIONAL

[Same structure as Critical]

---

## Hardcoded Secrets Found

### `file.py:line`
```[language]
[code showing secret]
```
**Fix:** Use environment variables
```[language]
[secure alternative]
```

---

## Dependency Vulnerabilities

**Run security audit:**
```bash
[audit command for language]
```

**Known Vulnerabilities:**
- `package==version` - [SEVERITY] - CVE-XXXX-XXXXX (upgrade to X.X.X)

---

## Recommendations

### Critical (Fix Immediately)
1. [Most critical security fixes]

### High (Should Fix Before Merge)
1. [Important security fixes]

### Medium (Address Soon)
1. [Moderate security improvements]

### Low (Improve Defense-in-Depth)
1. [Minor security enhancements]

---

## Security Checklist

- [ ] No SQL injection vulnerabilities (parameterized queries used)
- [ ] No XSS vulnerabilities (output escaped)
- [ ] CSRF protection on state-changing operations
- [ ] Passwords hashed with strong algorithm (bcrypt/Argon2)
- [ ] No hardcoded secrets in code
- [ ] Input validation on all user inputs
- [ ] Authorization checks on sensitive operations
- [ ] HTTPS enforced (no HTTP)
- [ ] Security headers configured
- [ ] Dependencies up-to-date and audited
- [ ] Error messages don't reveal sensitive info
- [ ] Logging doesn't expose sensitive data
```

## Quality Checklist

Before completing the review, verify:

- [ ] All OWASP Top 10 categories checked where applicable
- [ ] Vulnerabilities rated by severity (Critical/High/Medium/Low)
- [ ] OWASP and CWE references included
- [ ] Attack scenarios provided for critical issues
- [ ] Working fix examples included for all issues
- [ ] Hardcoded secrets identified with exact locations
- [ ] Dependency vulnerabilities checked with audit tools
- [ ] Security checklist provided for completeness

## Common Vulnerability Patterns

### SQL Injection

**Always use parameterized queries:**

```python
# VULNERABLE
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# SECURE
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### XSS (Cross-Site Scripting)

**Always escape output:**

```javascript
// VULNERABLE
element.innerHTML = userInput;

// SECURE
element.textContent = userInput;
```

### CSRF (Cross-Site Request Forgery)

**Always validate tokens on state-changing operations:**

```python
# VULNERABLE
@app.route('/delete', methods=['POST'])
def delete_item():
    item.delete()

# SECURE
@app.route('/delete', methods=['POST'])
@csrf.protect()
def delete_item():
    item.delete()
```

### Command Injection

**Never use shell=True with user input:**

```python
# VULNERABLE
subprocess.call(f"ping {host}", shell=True)

# SECURE
subprocess.run(["ping", "-c", "1", host], shell=False)
```

### Password Hashing

**Use bcrypt or Argon2, never MD5/SHA1:**

```python
# VULNERABLE
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# SECURE
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### Hardcoded Secrets

**Always use environment variables:**

```python
# VULNERABLE
API_KEY = "sk_live_abc123"

# SECURE
import os
API_KEY = os.environ.get('API_KEY')
```

## Tips

- **Check OWASP Top 10 systematically:** Go through each category
- **Rate severity objectively:** Use exploitability + impact formula
- **Provide attack scenarios:** Show how vulnerabilities could be exploited
- **Include CVE/CWE references:** Links to standard vulnerability databases
- **Show secure alternatives:** Working code examples for every issue
- **Test fixes:** Verify that recommended fixes actually work
- **Consider context:** Same code might be safe in one context, vulnerable in another
- **Use security linters:** Integrate tools like Bandit (Python), ESLint (JS), Brakeman (Rails)
- **Run dependency audits:** Check for known vulnerabilities in third-party packages
