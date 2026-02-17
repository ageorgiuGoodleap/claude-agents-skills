# Security Controls to Compliance Framework Mapping

## Overview

This document maps security controls to common compliance frameworks: GDPR, SOC 2, HIPAA, and PCI-DSS.

## GDPR (General Data Protection Regulation)

**Scope:** EU data privacy regulation

| GDPR Requirement | Security Controls | Implementation |
|------------------|-------------------|----------------|
| **Art. 5(1)(f) - Integrity and Confidentiality** | Encryption at rest, Encryption in transit, Access control | AES-256 encryption, TLS 1.3, RBAC |
| **Art. 15 - Right of Access** | Data inventory, Access logs, User data export | Data catalog, Audit logs, Export API |
| **Art. 17 - Right to Erasure** | Data deletion, Secure deletion | Crypto-shredding, Deletion workflows |
| **Art. 25 - Data Protection by Design** | Privacy by design, Default deny, Least privilege | Secure defaults, Minimal data collection |
| **Art. 32 - Security of Processing** | MFA, Encryption, Access control, Monitoring | All security controls |
| **Art. 33 - Breach Notification** | Incident detection, Alerting, Incident response | SIEM, 72-hour notification process |

**Key Controls:**
- Encryption of personal data (at rest and in transit)
- Access control (RBAC with least privilege)
- Audit logging (who accessed what data, when)
- Data deletion capability (right to be forgotten)
- Breach detection and notification (within 72 hours)

## SOC 2 (Service Organization Control 2)

**Scope:** Trust Services Criteria for service providers

### Trust Services Criteria

| Criterion | Security Controls | Evidence |
|-----------|-------------------|----------|
| **CC6.1 - Logical Access** | Authentication (MFA), Authorization (RBAC), Access reviews | Access control policies, Access logs |
| **CC6.2 - System Operations** | Logging, Monitoring, Alerting | SIEM, Log retention, Alert configuration |
| **CC6.3 - Change Management** | Version control, Code review, Deployment approvals | Git logs, PR approvals, Change tickets |
| **CC6.6 - Encryption** | TLS, Database encryption, Key management | TLS configuration, Encryption at rest enabled |
| **CC6.7 - Data Transmission** | VPN, TLS, API security | VPN logs, TLS certificates, API gateway logs |
| **CC7.2 - Monitoring** | SIEM, Anomaly detection, Incident response | Security alerts, Incident reports |

**Key Controls:**
- Multi-factor authentication
- Role-based access control with regular reviews
- Comprehensive logging and monitoring (SIEM)
- Encryption in transit and at rest
- Incident detection and response procedures
- Change management process

## HIPAA (Health Insurance Portability and Accountability Act)

**Scope:** US healthcare data protection

| HIPAA Requirement | Security Controls | Implementation |
|-------------------|-------------------|----------------|
| **§164.308(a)(3) - Workforce Security** | User provisioning/deprovisioning, Access reviews | IAM, Quarterly access reviews |
| **§164.308(a)(4) - Information Access Management** | RBAC, Least privilege, Authorization | RBAC with PHI-specific roles |
| **§164.308(a)(5)(ii)(B) - Log-in Monitoring** | Login logging, Failed attempt monitoring | SIEM, Account lockout |
| **§164.308(a)(6) - Security Incident Procedures** | Incident detection, Response, Reporting | IDS/IPS, Incident response plan |
| **§164.312(a)(1) - Access Control** | Unique user IDs, MFA, Session management | MFA for PHI access, Auto-logout |
| **§164.312(a)(2)(iv) - Encryption** | Encrypt ePHI at rest and in transit | AES-256, TLS 1.3 |
| **§164.312(b) - Audit Controls** | Audit logs, Log integrity, Log review | Centralized logging, Tamper-proof logs |
| **§164.312(d) - Authentication** | MFA, Strong passwords, Biometrics | TOTP-based MFA, Password policy |

**Key Controls:**
- Unique user identification and authentication (MFA)
- Role-based access control for ePHI
- Encryption of ePHI (at rest and in transit)
- Audit logging (access to ePHI, modifications)
- Automatic logoff (session timeout)
- Incident detection and response
- Business Associate Agreements (BAAs)

## PCI-DSS (Payment Card Industry Data Security Standard)

**Scope:** Credit card data protection

| PCI-DSS Requirement | Security Controls | Implementation |
|---------------------|-------------------|----------------|
| **Req 1 - Firewall Configuration** | Firewall, Network segmentation, DMZ | WAF, Security groups, Network policies |
| **Req 2 - Default Passwords** | Remove defaults, Change passwords | Configuration management, Secrets rotation |
| **Req 3 - Protect Stored Cardholder Data** | Encryption, Tokenization, Data masking | AES-256, PCI-compliant tokenization |
| **Req 4 - Encrypt Transmission** | TLS 1.2+, Strong ciphers | TLS 1.3, HSTS |
| **Req 5 - Anti-Virus** | Malware protection, Regular scans | Anti-malware software, Container scanning |
| **Req 6 - Secure Development** | SAST, DAST, Code review, Patching | SonarQube, OWASP ZAP, Patch management |
| **Req 7 - Access Control** | RBAC, Least privilege, Need-to-know | RBAC with card data access restriction |
| **Req 8 - Unique IDs** | Unique user IDs, MFA, Password policy | SSO, MFA for card data access |
| **Req 9 - Physical Access** | Physical security, Visitor logs | Data center security (cloud provider) |
| **Req 10 - Logging** | Audit logs, Log review, Time sync | Centralized logging, NTP, SIEM |
| **Req 11 - Testing** | Vulnerability scanning, Penetration testing | Quarterly scans, Annual pentests |
| **Req 12 - Security Policy** | Security policies, Risk assessments, Training | Policy documentation, Annual training |

**Key Controls:**
- Network segmentation (cardholder data environment isolated)
- Encryption of cardholder data (at rest and in transit)
- Tokenization (replace card numbers with tokens)
- Strong access control (MFA for card data access)
- Comprehensive audit logging
- Vulnerability management (quarterly scans)
- Penetration testing (annually)

## Compliance Control Matrix

| Security Control | GDPR | SOC 2 | HIPAA | PCI-DSS |
|------------------|------|-------|-------|---------|
| **MFA** | Art. 32 | CC6.1 | §164.312(d) | Req 8 |
| **Encryption at Rest** | Art. 32 | CC6.6 | §164.312(a)(2)(iv) | Req 3 |
| **Encryption in Transit** | Art. 32 | CC6.6 | §164.312(e)(1) | Req 4 |
| **RBAC** | Art. 25 | CC6.1 | §164.308(a)(4) | Req 7 |
| **Audit Logging** | Art. 30 | CC6.2 | §164.312(b) | Req 10 |
| **Incident Response** | Art. 33 | CC7.2 | §164.308(a)(6) | Req 12.10 |
| **Access Reviews** | Art. 25 | CC6.1 | §164.308(a)(3) | Req 8.2 |
| **Vulnerability Scanning** | Art. 32 | CC7.1 | §164.308(a)(8) | Req 11.2 |
| **Penetration Testing** | Art. 32 | CC7.1 | §164.308(a)(8) | Req 11.3 |
| **Network Segmentation** | Art. 32 | CC6.1 | §164.312(a)(1) | Req 1 |
| **Data Deletion** | Art. 17 | - | - | Req 3.1 |
| **Breach Notification** | Art. 33 | CC7.3 | §164.408 | Req 12.10 |

## Compliance Checklist Template

When designing security architecture, use this checklist to ensure compliance requirements are met:

**For GDPR:**
- [ ] Encryption of personal data (at rest and in transit)
- [ ] Access control (RBAC) and least privilege
- [ ] Audit logging for personal data access
- [ ] Data deletion capability (right to be forgotten)
- [ ] Data export capability (right to access)
- [ ] Breach detection and 72-hour notification process
- [ ] Data processing agreements with vendors

**For SOC 2:**
- [ ] Multi-factor authentication implemented
- [ ] Role-based access control with regular reviews
- [ ] Centralized logging and monitoring (SIEM)
- [ ] Encryption in transit (TLS 1.3) and at rest (AES-256)
- [ ] Incident detection and response procedures
- [ ] Change management process (version control, approvals)
- [ ] Vulnerability management program

**For HIPAA:**
- [ ] Unique user identification and MFA
- [ ] RBAC for ePHI access
- [ ] Encryption of ePHI (at rest and in transit)
- [ ] Audit logging for ePHI access
- [ ] Automatic logoff (session timeout)
- [ ] Incident detection and response plan
- [ ] Business Associate Agreements (BAAs)
- [ ] Regular risk assessments

**For PCI-DSS:**
- [ ] Network segmentation (cardholder data environment)
- [ ] Encryption of cardholder data (at rest and in transit)
- [ ] Tokenization implementation
- [ ] MFA for access to cardholder data
- [ ] Comprehensive audit logging
- [ ] Quarterly vulnerability scans
- [ ] Annual penetration testing
- [ ] Security policies and procedures documented
- [ ] Security awareness training program

## References

- GDPR: https://gdpr.eu/
- SOC 2: AICPA Trust Services Criteria
- HIPAA: https://www.hhs.gov/hipaa/
- PCI-DSS: https://www.pcisecuritystandards.org/
