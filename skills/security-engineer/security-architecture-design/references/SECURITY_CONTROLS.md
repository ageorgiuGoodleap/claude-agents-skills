# Security Controls Catalog

## Overview

This document catalogs security controls organized by type and layer. Use this as a reference when designing security control matrices and selecting appropriate controls for identified threats.

## Control Types

### Preventive Controls
Stop security incidents from occurring.

**Examples:**
- Authentication (passwords, MFA, biometrics)
- Authorization (RBAC, ABAC, ACLs)
- Input validation and sanitization
- Output encoding
- Encryption (at rest, in transit)
- Firewalls and network segmentation
- Security training and awareness
- Patch management
- Secure coding practices
- Code review and SAST

### Detective Controls
Identify security incidents in progress or after they occur.

**Examples:**
- Logging and monitoring
- SIEM (Security Information and Event Management)
- IDS/IPS (Intrusion Detection/Prevention Systems)
- Anomaly detection
- File integrity monitoring
- Vulnerability scanning
- Penetration testing
- Security audits
- Threat intelligence feeds
- Behavioral analytics

### Corrective Controls
Respond to and recover from security incidents.

**Examples:**
- Incident response procedures
- Backup and recovery
- Patch deployment
- Account lockout and reset
- Firewall rule updates
- Access revocation
- System restoration
- Forensic analysis
- Post-incident review
- Remediation workflows

## Security Controls by Defense-in-Depth Layer

### Layer 1: Perimeter Security

**Purpose:** Protect the network boundary from external threats.

| Control | Type | Implementation | Threats Mitigated |
|---------|------|----------------|------------------|
| Web Application Firewall (WAF) | Preventive/Detective | Cloud WAF (Cloudflare, AWS WAF) | SQL injection, XSS, OWASP Top 10 |
| DDoS Protection | Preventive | Cloud DDoS mitigation service | Volumetric attacks, application-layer DDoS |
| API Gateway | Preventive | Kong, Apigee, AWS API Gateway | Unauthorized API access, rate abuse |
| VPN | Preventive | IPSec VPN, WireGuard | Unauthorized network access |
| Edge Firewall | Preventive | Cloud firewall, network firewall | Network-layer attacks |

### Layer 2: Network Security

**Purpose:** Segment networks and control internal traffic.

| Control | Type | Implementation | Threats Mitigated |
|---------|------|----------------|------------------|
| Network Segmentation | Preventive | VLANs, subnets, security groups | Lateral movement, blast radius |
| Internal Firewall | Preventive | Security groups, network ACLs | Unauthorized internal access |
| Zero-Trust Network | Preventive | Identity-based access, microsegmentation | Lateral movement, insider threats |
| Network IDS/IPS | Detective/Preventive | Snort, Suricata, cloud IDS | Network-based attacks |
| Service Mesh | Preventive | Istio, Linkerd | Service-to-service attacks |

### Layer 3: Application Security

**Purpose:** Protect applications from code-level vulnerabilities.

| Control | Type | Implementation | Threats Mitigated |
|---------|------|----------------|------------------|
| Input Validation | Preventive | Validation libraries, schema validation | Injection attacks, XSS, XXE |
| Output Encoding | Preventive | Template engines, encoding libraries | XSS, injection |
| CSRF Tokens | Preventive | Synchronizer tokens, same-site cookies | Cross-site request forgery |
| Security Headers | Preventive | CSP, HSTS, X-Frame-Options | Clickjacking, MITM, XSS |
| Session Management | Preventive | Secure cookies, session timeouts | Session hijacking, fixation |
| Rate Limiting | Preventive/Detective | API gateway, application middleware | Brute force, DoS, abuse |
| SAST | Detective | SonarQube, Checkmarx, Semgrep | Code vulnerabilities |
| DAST | Detective | OWASP ZAP, Burp Suite | Runtime vulnerabilities |

### Layer 4: Data Security

**Purpose:** Protect data confidentiality, integrity, and availability.

| Control | Type | Implementation | Threats Mitigated |
|---------|------|----------------|------------------|
| Encryption at Rest | Preventive | AES-256, database encryption | Data theft, physical access |
| Encryption in Transit | Preventive | TLS 1.3, HTTPS | MITM, eavesdropping |
| Data Masking | Preventive | Dynamic masking, tokenization | Information disclosure |
| Database Firewall | Preventive | Database gateway, query filtering | SQL injection, unauthorized queries |
| Backup Encryption | Preventive | Encrypted backups | Backup theft, data exposure |
| Data Loss Prevention (DLP) | Detective/Preventive | DLP tools, egress filtering | Data exfiltration |
| Secure Deletion | Corrective | Crypto-shredding, secure wipe | Data remnants |

### Layer 5: Identity & Access Management

**Purpose:** Verify identity and control access to resources.

| Control | Type | Implementation | Threats Mitigated |
|---------|------|----------------|------------------|
| Multi-Factor Authentication | Preventive | TOTP, SMS, WebAuthn | Credential theft, phishing |
| Single Sign-On (SSO) | Preventive | SAML, OAuth2, OIDC | Password fatigue, weak passwords |
| Password Policy | Preventive | Length, complexity, rotation | Weak passwords, brute force |
| Account Lockout | Preventive | Failed attempt threshold | Brute force attacks |
| Least Privilege | Preventive | RBAC, minimal permissions | Privilege escalation |
| Privileged Access Management | Preventive | PAM solutions, just-in-time access | Credential theft, insider threats |
| Access Reviews | Detective | Periodic audits | Stale accounts, privilege creep |

### Layer 6: Monitoring & Response

**Purpose:** Detect, respond to, and recover from security incidents.

| Control | Type | Implementation | Threats Mitigated |
|---------|------|----------------|------------------|
| Centralized Logging | Detective | ELK, Splunk, cloud logging | All threats (visibility) |
| SIEM | Detective | Splunk, QRadar, Sentinel | Advanced threats, coordinated attacks |
| Anomaly Detection | Detective | ML-based detection, UEBA | Insider threats, compromised accounts |
| Alerting | Detective | PagerDuty, Opsgenie | All threats (timely response) |
| Incident Response Plan | Corrective | Runbooks, playbooks | All incidents |
| Backup & Recovery | Corrective | Automated backups, DR plan | Ransomware, data loss |
| Security Orchestration (SOAR) | Corrective | Automated response workflows | All incidents (faster response) |

## Common Security Control Patterns

### Pattern 1: Web Application Stack

**Threat:** Web application vulnerabilities (OWASP Top 10)

**Controls:**
1. WAF (preventive) - Block common attack patterns
2. Input validation (preventive) - Validate all user input
3. Output encoding (preventive) - Prevent XSS
4. Parameterized queries (preventive) - Prevent SQL injection
5. CSRF tokens (preventive) - Prevent CSRF
6. Security headers (preventive) - Defense-in-depth
7. SAST (detective) - Find vulnerabilities in code
8. WAF logs + SIEM (detective) - Monitor attacks
9. Incident response (corrective) - Handle breaches

### Pattern 2: API Security

**Threat:** API abuse, unauthorized access, data exposure

**Controls:**
1. API Gateway (preventive) - Centralized authentication/authorization
2. JWT validation (preventive) - Verify token authenticity
3. OAuth2 scopes (preventive) - Limit API access
4. Rate limiting (preventive) - Prevent abuse
5. Input validation (preventive) - Validate request payloads
6. Output filtering (preventive) - Remove sensitive fields
7. API logging (detective) - Audit all API calls
8. Anomaly detection (detective) - Detect unusual patterns
9. API key rotation (corrective) - Respond to compromises

### Pattern 3: Database Protection

**Threat:** SQL injection, unauthorized data access, data theft

**Controls:**
1. Parameterized queries (preventive) - Prevent SQL injection
2. Least privilege DB access (preventive) - Limit permissions
3. Database firewall (preventive) - Filter malicious queries
4. Encryption at rest (preventive) - Protect stored data
5. Encryption in transit (preventive) - Protect data in motion
6. Database audit logging (detective) - Track all queries
7. Query monitoring (detective) - Alert on suspicious patterns
8. Backup encryption (preventive) - Protect backups
9. Backup restoration (corrective) - Recover from incidents

### Pattern 4: Authentication & Session Management

**Threat:** Credential theft, session hijacking, brute force

**Controls:**
1. Strong password policy (preventive) - Enforce complexity
2. MFA (preventive) - Require second factor
3. Account lockout (preventive) - Prevent brute force
4. Secure session cookies (preventive) - HttpOnly, Secure, SameSite
5. Session timeout (preventive) - Limit exposure window
6. Login anomaly detection (detective) - Detect suspicious logins
7. Failed login monitoring (detective) - Alert on patterns
8. Account reset workflow (corrective) - Recover compromised accounts
9. Session revocation (corrective) - Terminate active sessions

### Pattern 5: Microservices Security

**Threat:** Service-to-service attacks, lateral movement, data interception

**Controls:**
1. mTLS (preventive) - Authenticate both endpoints
2. Service mesh (preventive) - Centralized security
3. JWT with service scopes (preventive) - Limit service access
4. Network policies (preventive) - Explicit allow/deny
5. Certificate rotation (preventive) - Short-lived certs
6. Distributed tracing (detective) - Track requests across services
7. Service mesh monitoring (detective) - Detect anomalies
8. Circuit breakers (corrective) - Prevent cascading failures
9. Service isolation (corrective) - Contain compromised services

## Control Selection Guidelines

### 1. Map Controls to Threats

Each threat should have multiple controls (defense-in-depth):
- At least one preventive control
- At least one detective control
- At least one corrective control (for high/critical risks)

### 2. Prioritize by Risk Level

**Critical/High Risks:**
- Implement multiple strong controls
- Defense-in-depth with redundancy
- Automated detection and response

**Medium Risks:**
- Implement standard controls
- Balance prevention and detection
- Manual response acceptable

**Low Risks:**
- Basic controls sufficient
- Focus on prevention
- Periodic review

### 3. Consider Cost vs Benefit

**High-Value Controls (implement first):**
- Authentication (MFA, strong passwords)
- Input validation and output encoding
- Encryption (TLS, database encryption)
- Logging and monitoring
- Least privilege access

**Lower-Value Controls (implement after basics):**
- Advanced threat detection (ML-based)
- Automated response (SOAR)
- Specialized security tools

### 4. Balance Usability and Security

- Don't add friction without clear security benefit
- Use risk-based authentication (step-up for sensitive operations)
- Provide clear security guidance to users
- Make secure choices the default

### 5. Automate Where Possible

**Good Candidates for Automation:**
- Vulnerability scanning
- Patch management
- Log analysis and alerting
- Incident response workflows
- Security testing in CI/CD

**Requires Human Judgment:**
- Complex threat analysis
- Incident investigation
- Security architecture decisions
- Risk acceptance decisions

## References

- NIST Cybersecurity Framework - Control categories
- ISO 27001/27002 - Security control standards
- CIS Controls - Prioritized security actions
- OWASP ASVS - Application security verification
- MITRE ATT&CK - Threat-informed defense
