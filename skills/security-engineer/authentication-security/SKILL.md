---
name: authentication-security
description: |
  Implements comprehensive authentication security covering password hashing (bcrypt, Argon2), JWT configuration,
  multi-factor authentication (MFA/2FA), OAuth2/OIDC integration, session management, account lockout, and rate
  limiting. Use when implementing authentication, password security, JWT tokens, MFA, 2FA, two-factor authentication,
  OAuth2, OIDC, session management, rate limiting, account lockout, brute force protection, token security, or when
  hardening authentication systems against common attacks.
---

# Authentication Security

## Overview

This skill provides comprehensive guidance for implementing secure authentication systems hardened against common attacks. It covers password security, token-based authentication, multi-factor authentication, session management, and brute force protection.

**Core Capabilities:**
- Secure password hashing with bcrypt or Argon2
- JWT security configuration and best practices
- Multi-factor authentication (MFA/2FA) implementation
- OAuth2 and OpenID Connect (OIDC) integration
- Secure session management
- Account lockout and brute force protection
- Rate limiting for authentication endpoints

## When to Use This Skill

Trigger this skill when:
- Implementing authentication systems from scratch
- Hardening existing authentication implementations
- Configuring JWT token security
- Adding multi-factor authentication (MFA/2FA)
- Integrating OAuth2 or OpenID Connect
- Setting up session management
- Implementing account lockout policies
- Adding rate limiting to prevent brute force attacks
- Reviewing authentication security posture

## Implementation Guide

### 1. Password Security

Implement secure password hashing and policies to protect user credentials.

#### Password Hashing

Use bcrypt or Argon2 for password hashing:

**Python (bcrypt)**:
```python
import bcrypt

# Hash password on registration
def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt(rounds=12)  # Cost factor 12 (recommended)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# Verify password on login
def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
```

**Python (Argon2 - recommended)**:
```python
from argon2 import PasswordHasher

ph = PasswordHasher()

# Hash password
def hash_password(password: str) -> str:
    return ph.hash(password)

# Verify password
def verify_password(password: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, password)
        return True
    except:
        return False
```

**Node.js (bcrypt)**:
```javascript
const bcrypt = require('bcrypt');

// Hash password
async function hashPassword(password) {
    const saltRounds = 12;
    return await bcrypt.hash(password, saltRounds);
}

// Verify password
async function verifyPassword(password, hash) {
    return await bcrypt.compare(password, hash);
}
```

#### Password Policies

Implement strong password policies:

```python
import re
from typing import List, Optional

def validate_password(password: str) -> tuple[bool, Optional[List[str]]]:
    """
    Validate password against security policy.
    Returns (is_valid, list_of_errors)
    """
    errors = []

    # Minimum length
    if len(password) < 12:
        errors.append("Password must be at least 12 characters")

    # Complexity requirements
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain uppercase letter")
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain lowercase letter")
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain number")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain special character")

    # Common patterns to reject
    common_patterns = ['password', '12345', 'qwerty', 'admin']
    if any(pattern in password.lower() for pattern in common_patterns):
        errors.append("Password contains common pattern")

    return (len(errors) == 0, errors if errors else None)
```

For detailed password policy implementation, see [Password Policies](references/password-policies.md).

### 2. JWT Security

Configure JWT tokens securely to prevent common vulnerabilities.

#### JWT Configuration

**Python (PyJWT)**:
```python
import jwt
from datetime import datetime, timedelta
import os

# Configuration
PRIVATE_KEY = os.getenv('JWT_PRIVATE_KEY')
PUBLIC_KEY = os.getenv('JWT_PUBLIC_KEY')
ALGORITHM = 'RS256'  # Use RS256, not HS256

# Generate access token (short expiration)
def create_access_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=15),  # 15 minute expiration
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)

# Generate refresh token (longer expiration)
def create_refresh_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7),  # 7 day expiration
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)

# Verify token
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
```

**Node.js (jsonwebtoken)**:
```javascript
const jwt = require('jsonwebtoken');
const fs = require('fs');

const PRIVATE_KEY = fs.readFileSync('private_key.pem');
const PUBLIC_KEY = fs.readFileSync('public_key.pem');

// Generate access token
function createAccessToken(userId) {
    return jwt.sign(
        { userId, type: 'access' },
        PRIVATE_KEY,
        { algorithm: 'RS256', expiresIn: '15m' }
    );
}

// Generate refresh token
function createRefreshToken(userId) {
    return jwt.sign(
        { userId, type: 'refresh' },
        PRIVATE_KEY,
        { algorithm: 'RS256', expiresIn: '7d' }
    );
}

// Verify token
function verifyToken(token) {
    try {
        return jwt.verify(token, PUBLIC_KEY, { algorithms: ['RS256'] });
    } catch (err) {
        throw new Error('Invalid token');
    }
}
```

#### JWT Storage

**Web Applications**:
- Store access tokens in httpOnly, secure cookies with SameSite=Strict
- Never store tokens in localStorage (vulnerable to XSS)
- Implement refresh token rotation

**Mobile Applications**:
- Use platform secure storage (Keychain on iOS, Keystore on Android)
- Never store tokens in UserDefaults or SharedPreferences

For detailed JWT implementation, see [JWT Best Practices](references/jwt-best-practices.md).

### 3. Multi-Factor Authentication (MFA)

Add an additional layer of security with MFA.

#### TOTP Implementation

**Python (pyotp)**:
```python
import pyotp
import qrcode
from io import BytesIO

# Generate MFA secret for user
def generate_mfa_secret(user_email: str) -> tuple[str, str]:
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)

    # Generate provisioning URI for QR code
    provisioning_uri = totp.provisioning_uri(
        name=user_email,
        issuer_name='Your App Name'
    )

    return secret, provisioning_uri

# Generate QR code
def generate_qr_code(provisioning_uri: str) -> BytesIO:
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

# Verify TOTP code
def verify_totp(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)  # Allow 1 interval tolerance

# Generate backup codes
def generate_backup_codes(count: int = 10) -> List[str]:
    import secrets
    return [secrets.token_hex(4) for _ in range(count)]
```

**Enrollment Flow**:
1. User enables MFA
2. Generate secret and QR code
3. User scans QR code with authenticator app
4. User enters verification code to confirm setup
5. Generate and display backup codes
6. Store hashed backup codes in database

For detailed MFA implementation, see [MFA Implementation Guide](references/mfa-implementation.md).

### 4. OAuth2 and OpenID Connect

Integrate with external identity providers.

#### Authorization Code Flow with PKCE

**Python (Authlib)**:
```python
from authlib.integrations.flask_client import OAuth
import secrets

oauth = OAuth(app)

# Register OAuth provider
oauth.register(
    'provider_name',
    client_id=os.getenv('OAUTH_CLIENT_ID'),
    client_secret=os.getenv('OAUTH_CLIENT_SECRET'),
    server_metadata_url='https://provider.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile email',
        'code_challenge_method': 'S256'  # PKCE
    }
)

# Initiate authorization
@app.route('/login/oauth')
def oauth_login():
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state

    # Generate PKCE code verifier and challenge
    code_verifier = secrets.token_urlsafe(64)
    session['code_verifier'] = code_verifier

    redirect_uri = url_for('oauth_callback', _external=True)
    return oauth.provider_name.authorize_redirect(
        redirect_uri,
        state=state,
        code_verifier=code_verifier
    )

# Handle callback
@app.route('/login/oauth/callback')
def oauth_callback():
    # Verify state
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        abort(400, 'Invalid state')

    # Exchange code for token
    code_verifier = session.get('code_verifier')
    token = oauth.provider_name.authorize_access_token(
        code_verifier=code_verifier
    )

    # Get user info
    userinfo = oauth.provider_name.parse_id_token(token)

    # Create or update user
    user = get_or_create_user(userinfo)
    login_user(user)

    return redirect('/')
```

For OAuth2/OIDC integration, see [OAuth2 Implementation](references/oauth2-implementation.md).

### 5. Session Management

Implement secure session handling.

#### Secure Cookie Configuration

**Flask**:
```python
app.config.update(
    SESSION_COOKIE_SECURE=True,        # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,      # Not accessible via JavaScript
    SESSION_COOKIE_SAMESITE='Strict',  # CSRF protection
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)  # Inactivity timeout
)

# Session regeneration on login
@app.route('/login', methods=['POST'])
def login():
    # ... authenticate user ...

    # Regenerate session ID
    session.clear()
    session['user_id'] = user.id
    session.permanent = True

    return redirect('/')
```

**Express.js**:
```javascript
const session = require('express-session');

app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: true,         // HTTPS only
        httpOnly: true,       // Not accessible via JavaScript
        sameSite: 'strict',   // CSRF protection
        maxAge: 1800000       // 30 minutes
    }
}));

// Session regeneration on login
app.post('/login', async (req, res) => {
    // ... authenticate user ...

    // Regenerate session
    req.session.regenerate((err) => {
        if (err) return res.status(500).send('Error');
        req.session.userId = user.id;
        res.redirect('/');
    });
});
```

### 6. Account Lockout and Rate Limiting

Prevent brute force attacks with account lockout and rate limiting.

#### Account Lockout

```python
from datetime import datetime, timedelta

class AccountLockout:
    MAX_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=15)

    def __init__(self, cache):  # Use Redis or similar
        self.cache = cache

    def record_failed_attempt(self, username: str) -> int:
        """Record failed login attempt. Returns current attempt count."""
        key = f'login_attempts:{username}'
        attempts = self.cache.incr(key)

        if attempts == 1:
            # Set expiration on first attempt
            self.cache.expire(key, self.LOCKOUT_DURATION.seconds)

        if attempts >= self.MAX_ATTEMPTS:
            # Lock account
            lock_key = f'account_locked:{username}'
            self.cache.setex(
                lock_key,
                self.LOCKOUT_DURATION.seconds,
                'locked'
            )

        return attempts

    def is_locked(self, username: str) -> bool:
        """Check if account is locked."""
        key = f'account_locked:{username}'
        return self.cache.exists(key)

    def reset_attempts(self, username: str):
        """Reset attempts on successful login."""
        self.cache.delete(f'login_attempts:{username}')
        self.cache.delete(f'account_locked:{username}')
```

#### Rate Limiting

**Flask (Flask-Limiter)**:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Rate limit login endpoint
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ... authentication logic ...
    pass

# Rate limit password reset
@app.route('/reset-password', methods=['POST'])
@limiter.limit("3 per hour")
def reset_password():
    # ... password reset logic ...
    pass
```

**Express.js (express-rate-limit)**:
```javascript
const rateLimit = require('express-rate-limit');

// Login rate limiter
const loginLimiter = rateLimit({
    windowMs: 60 * 1000,  // 1 minute
    max: 5,  // 5 attempts per minute
    message: 'Too many login attempts, please try again later'
});

// Password reset rate limiter
const resetLimiter = rateLimit({
    windowMs: 60 * 60 * 1000,  // 1 hour
    max: 3,  // 3 attempts per hour
    message: 'Too many password reset requests'
});

app.post('/login', loginLimiter, async (req, res) => {
    // ... authentication logic ...
});

app.post('/reset-password', resetLimiter, async (req, res) => {
    // ... password reset logic ...
});
```

## Implementation Checklist

Use this checklist to ensure comprehensive authentication security:

- [ ] **Password Hashing**
  - [ ] bcrypt (cost ≥10) or Argon2 implemented
  - [ ] Unique salt per password
  - [ ] No weak algorithms (MD5, SHA1, plain SHA256)

- [ ] **Password Policies**
  - [ ] Minimum length 12 characters
  - [ ] Complexity requirements enforced
  - [ ] Common patterns rejected
  - [ ] Password breach checking integrated (optional)

- [ ] **JWT Security**
  - [ ] RS256 signing algorithm (not HS256)
  - [ ] Access tokens expire ≤15 minutes
  - [ ] Refresh tokens expire ≤7 days
  - [ ] Keys stored in environment variables
  - [ ] Token revocation implemented

- [ ] **JWT Storage**
  - [ ] Web: httpOnly, secure, SameSite cookies
  - [ ] Mobile: Platform secure storage
  - [ ] Never in localStorage or client-side storage

- [ ] **Multi-Factor Authentication**
  - [ ] TOTP implementation with authenticator apps
  - [ ] Backup codes generated and stored hashed
  - [ ] MFA enrollment flow tested
  - [ ] Recovery procedures documented

- [ ] **OAuth2/OIDC**
  - [ ] Authorization code flow with PKCE
  - [ ] State parameter for CSRF protection
  - [ ] Token validation implemented
  - [ ] User provisioning from identity provider

- [ ] **Session Management**
  - [ ] Secure, httpOnly, SameSite cookies
  - [ ] Inactivity timeout ≤30 minutes
  - [ ] Absolute timeout ≤8 hours
  - [ ] Session regeneration on login
  - [ ] Session regeneration on privilege change

- [ ] **Account Lockout**
  - [ ] Lock after ≤5 failed attempts
  - [ ] Lockout duration ≥15 minutes
  - [ ] Lockout notification sent to user
  - [ ] Admin unlock capability

- [ ] **Rate Limiting**
  - [ ] Login endpoint: 5 attempts per minute
  - [ ] Password reset: 3 attempts per hour
  - [ ] Token refresh: 10 attempts per minute
  - [ ] Registration: 3 attempts per hour

- [ ] **General Security**
  - [ ] HTTPS enforced (HSTS header)
  - [ ] Secrets in environment variables
  - [ ] Authentication events logged
  - [ ] Security headers configured

## Security Best Practices

### Password Security
- Use bcrypt with cost factor 12 or Argon2
- Enforce minimum length of 12 characters
- Implement password complexity requirements
- Check passwords against breach databases (Have I Been Pwned API)
- Never log passwords or include in error messages

### JWT Security
- Always use RS256 (asymmetric), never HS256 with weak secrets
- Keep access tokens short-lived (≤15 minutes)
- Implement refresh token rotation
- Store tokens in httpOnly cookies for web applications
- Implement token revocation for logout and security events

### Session Security
- Use secure, httpOnly, SameSite=Strict cookies
- Implement both inactivity and absolute timeouts
- Regenerate session ID on login and privilege changes
- Store sessions server-side, not client-side
- Implement concurrent session limits

### Multi-Factor Authentication
- Support TOTP with authenticator apps as primary method
- Provide backup codes (at least 8-10 codes)
- Hash backup codes before storage
- Implement account recovery procedures
- Allow MFA reset via support with identity verification

### Brute Force Protection
- Implement account lockout after 5 failed attempts
- Use progressive delays between attempts
- Add rate limiting to all authentication endpoints
- Consider CAPTCHA after multiple failures
- Log and monitor authentication failures

## References

For detailed implementation guidance:
- [Password Policies](references/password-policies.md)
- [JWT Best Practices](references/jwt-best-practices.md)
- [MFA Implementation Guide](references/mfa-implementation.md)
- [OAuth2 Implementation](references/oauth2-implementation.md)

## Integration

This skill works with:
- **Backend Developer agent**: For implementing authentication endpoints
- **Frontend Developer agent**: For login UI and MFA enrollment
- **DevOps Engineer agent**: For secrets management (Vault, AWS Secrets Manager)
- **Secure Code Review skill**: For reviewing authentication implementations
