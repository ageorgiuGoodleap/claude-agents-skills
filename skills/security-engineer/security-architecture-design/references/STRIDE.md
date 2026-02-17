# STRIDE Threat Modeling Methodology

## Overview

STRIDE is a threat modeling methodology developed by Microsoft for identifying security threats. The acronym represents six categories of security threats that can affect a system.

## STRIDE Categories

### S - Spoofing Identity

**Definition:** An attacker pretends to be someone or something they are not.

**Common Attack Vectors:**
- Credential theft (phishing, keylogging, credential stuffing)
- Session hijacking (stealing session tokens/cookies)
- IP spoofing (forging source IP addresses)
- Email spoofing (forging sender addresses)
- Certificate forgery or theft
- Replay attacks (reusing captured authentication data)

**Example Threats:**
- Attacker steals user credentials and logs in as that user
- Attacker intercepts and reuses authentication tokens
- Attacker forges emails appearing to be from legitimate sources
- Attacker uses stolen API keys to impersonate a legitimate service

**Mitigation Controls:**
- Strong authentication (MFA, certificate-based auth)
- Secure credential storage (hashing, encryption)
- Token-based authentication with expiration
- Digital signatures and certificates
- Anti-phishing controls (SPF, DKIM, DMARC)
- Anomaly detection for suspicious login patterns

### T - Tampering with Data

**Definition:** Malicious modification of data in transit or at rest.

**Common Attack Vectors:**
- Man-in-the-middle attacks (intercepting and modifying network traffic)
- SQL injection (manipulating database queries)
- Parameter tampering (modifying URL parameters, form fields, cookies)
- File system tampering (modifying application files)
- Memory tampering (modifying process memory)
- Database tampering (direct unauthorized modifications)

**Example Threats:**
- Attacker intercepts API request and modifies parameters
- Attacker uses SQL injection to modify database records
- Attacker tampers with price fields in e-commerce transactions
- Attacker modifies application configuration files
- Attacker alters log files to hide malicious activity

**Mitigation Controls:**
- Encryption in transit (TLS/HTTPS)
- Encryption at rest (database encryption, file encryption)
- Input validation and sanitization
- Parameterized queries (prevent SQL injection)
- Digital signatures for data integrity
- File integrity monitoring
- Tamper-evident logging

### R - Repudiation

**Definition:** Users deny performing actions without proof to the contrary.

**Common Attack Vectors:**
- Lack of audit logging
- Insufficient logging detail
- Log tampering or deletion
- Non-attributed actions
- Missing transaction records
- Unsigned transactions

**Example Threats:**
- User claims they didn't make a purchase (no audit trail)
- Administrator denies making unauthorized changes (logs disabled)
- Attacker deletes logs after malicious activity
- User disputes transaction without proof of authorization
- Actions performed without attribution to specific users

**Mitigation Controls:**
- Comprehensive audit logging (who, what, when, where)
- Secure, tamper-proof log storage
- Digital signatures for critical transactions
- Non-repudiation mechanisms (signed receipts, blockchain)
- Centralized log aggregation (SIEM)
- Time synchronization (NTP)
- Log integrity verification

### I - Information Disclosure

**Definition:** Exposure of sensitive information to unauthorized parties.

**Common Attack Vectors:**
- SQL injection (extracting database data)
- Path traversal (accessing unauthorized files)
- Verbose error messages (revealing system details)
- Insecure data storage (unencrypted backups)
- Insufficient access controls
- Memory leaks (sensitive data in memory dumps)
- Metadata leakage (comments, headers, EXIF data)

**Example Threats:**
- Attacker extracts customer PII from database via SQL injection
- Error messages reveal database structure and queries
- Backup files left on publicly accessible storage
- API responses include sensitive fields not needed by client
- Source code comments contain passwords or API keys
- Directory listing exposes sensitive files

**Mitigation Controls:**
- Principle of least privilege (restrict data access)
- Data encryption (at rest and in transit)
- Output filtering (remove sensitive fields from responses)
- Generic error messages (avoid revealing internals)
- Secure data disposal (secure deletion, shredding)
- Data loss prevention (DLP) tools
- Access control lists (ACLs)
- Data classification and labeling

### D - Denial of Service

**Definition:** Making a system unavailable to legitimate users.

**Common Attack Vectors:**
- Resource exhaustion (CPU, memory, disk, bandwidth)
- Application-layer attacks (slowloris, slow HTTP POST)
- Network-layer attacks (SYN flood, UDP flood, ICMP flood)
- Distributed denial of service (DDoS)
- Logic flaws causing crashes
- Unhandled exceptions
- Algorithmic complexity attacks

**Example Threats:**
- Attacker floods API with requests exceeding capacity
- Malicious input triggers infinite loop or memory leak
- Large file uploads exhaust disk space
- Regex injection causes catastrophic backtracking (ReDoS)
- Database query without pagination consumes all connections
- Unvalidated user input causes application crash

**Mitigation Controls:**
- Rate limiting (per user, per IP, per endpoint)
- Resource quotas and throttling
- Load balancing and auto-scaling
- Input validation (size limits, format checks)
- Connection limits and timeouts
- CDN and DDoS protection services
- Circuit breakers and graceful degradation
- Caching to reduce backend load

### E - Elevation of Privilege

**Definition:** Users gain access to resources or functionality they shouldn't have.

**Common Attack Vectors:**
- Broken access control (missing authorization checks)
- Insecure direct object references (IDOR)
- Privilege escalation vulnerabilities
- Confused deputy attacks
- Path traversal to protected resources
- Horizontal privilege escalation (access other users' data)
- Vertical privilege escalation (gain admin privileges)

**Example Threats:**
- User modifies user_id parameter to access another user's data
- Regular user accesses admin functionality by guessing URLs
- Attacker exploits vulnerability to gain root/admin privileges
- User bypasses authorization by directly accessing API endpoints
- JWT manipulation to add admin claims
- SQL injection to modify user roles in database

**Mitigation Controls:**
- Robust authorization checks (at every access point)
- Principle of least privilege (minimal necessary permissions)
- Input validation (prevent parameter tampering)
- Indirect object references (use session/token data, not user input)
- Regular access reviews
- Separation of duties
- Strong session management
- Capability-based security

## STRIDE Application Workflow

### Step 1: Decompose the System

Break down the system into:
- **Components** - Services, applications, databases
- **Data Flows** - Movement of data between components
- **Trust Boundaries** - Where privilege or trust level changes
- **Entry Points** - Where data enters the system

### Step 2: Apply STRIDE to Each Element

For each component and data flow, ask:

**Spoofing:**
- Can an attacker impersonate a user or component?
- Are identities verified?

**Tampering:**
- Can data be modified without detection?
- Is data integrity protected?

**Repudiation:**
- Can actions be traced to specific users?
- Are audit logs sufficient?

**Information Disclosure:**
- Can sensitive data be accessed by unauthorized parties?
- Is data properly protected?

**Denial of Service:**
- Can the component be made unavailable?
- Are there resource limits?

**Elevation of Privilege:**
- Can users gain unauthorized access?
- Are authorization checks in place?

### Step 3: Document Threats

Create a threat table:

| Component | STRIDE Category | Threat Description | Attack Vector | Likelihood | Impact | Current Controls | Residual Risk |
|-----------|----------------|-------------------|---------------|------------|--------|------------------|---------------|
| Login API | Spoofing | Credential stuffing | Stolen passwords | High | High | Rate limiting | Medium |
| Database | Information Disclosure | SQL injection | User input | Medium | Critical | Parameterized queries | Low |

### Step 4: Prioritize with DREAD

Apply DREAD scoring to each threat to prioritize remediation (see DREAD.md).

## STRIDE Examples by Component Type

### Web Application

**Spoofing:**
- Session fixation attacks
- Cross-site request forgery (CSRF)

**Tampering:**
- Parameter manipulation
- Cookie tampering

**Repudiation:**
- Missing audit logs for user actions

**Information Disclosure:**
- XSS exposing sensitive data
- Verbose error messages

**Denial of Service:**
- Unvalidated file uploads
- Resource-intensive operations

**Elevation of Privilege:**
- Broken access control
- Insecure direct object references

### API Endpoint

**Spoofing:**
- API key theft
- Token hijacking

**Tampering:**
- Request manipulation
- Replay attacks

**Repudiation:**
- Missing API audit logs

**Information Disclosure:**
- Excessive data exposure
- Error messages revealing structure

**Denial of Service:**
- Missing rate limiting
- Lack of pagination

**Elevation of Privilege:**
- Missing authorization checks
- Scope elevation in JWT

### Database

**Spoofing:**
- Stolen database credentials

**Tampering:**
- SQL injection
- Direct database manipulation

**Repudiation:**
- Missing database audit logging

**Information Disclosure:**
- SQL injection data extraction
- Unencrypted backups

**Denial of Service:**
- Resource-intensive queries
- Connection exhaustion

**Elevation of Privilege:**
- Privilege escalation via SQL injection
- Weak database user permissions

## Best Practices

1. **Be Systematic** - Apply STRIDE to every component and data flow
2. **Think Like an Attacker** - Consider how each component could be abused
3. **Document Everything** - Create comprehensive threat tables
4. **Prioritize** - Use DREAD to focus on highest-risk threats
5. **Iterate** - Threat model should evolve with the system
6. **Involve Team** - Include developers, ops, and security in threat modeling
7. **Focus on Controls** - For each threat, identify existing and needed controls
