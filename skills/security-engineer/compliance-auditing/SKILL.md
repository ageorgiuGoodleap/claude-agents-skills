---
name: compliance-auditing
description: |
  Conducts comprehensive compliance audits against regulatory frameworks (GDPR, SOC2, HIPAA, PCI-DSS)
  by analyzing system architecture, security controls, policies, and evidence. Generates detailed compliance
  reports with gap analysis, remediation plans, and evidence documentation. Use when conducting compliance audit,
  GDPR compliance, SOC2, HIPAA, PCI-DSS, security compliance, audit preparation, compliance assessment, regulatory
  compliance, data protection compliance, privacy compliance, compliance framework, compliance gap analysis, or
  preparing for audit readiness.
---

# Compliance Auditing

## Overview

This skill conducts thorough compliance audits against major regulatory frameworks by analyzing system architecture, security controls, policies, and documentation. It generates detailed reports with gap analysis and actionable remediation plans for certification and audit readiness.

**Supported Frameworks:**
- GDPR (General Data Protection Regulation)
- SOC 2 (Service Organization Control 2)
- HIPAA (Health Insurance Portability and Accountability Act)
- PCI-DSS (Payment Card Industry Data Security Standard)

## When to Use This Skill

Trigger this skill when:
- Conducting compliance audits
- Preparing for certification (SOC 2, ISO 27001)
- Assessing GDPR, HIPAA, or PCI-DSS compliance
- Performing gap analysis against frameworks
- Documenting evidence for auditors
- Creating remediation plans
- Reviewing security posture for compliance

## Audit Process

### 1. Scope Definition

Determine audit scope and frameworks:

```markdown
## Audit Scope

**Frameworks**: GDPR, SOC 2 Type II
**System**: Production web application and database
**Data Types**: Personal data (PII), payment information (PCI)
**Locations**: AWS us-east-1, AWS eu-west-1
**Time Period**: Last 12 months
**Exclusions**: Development and testing environments
```

Identify compliance requirements:
- **GDPR**: If processing EU personal data
- **HIPAA**: If handling protected health information (PHI)
- **PCI-DSS**: If processing, storing, or transmitting cardholder data
- **SOC 2**: For service organizations handling customer data

### 2. Control Inventory

Document all security controls and configurations.

**Use Glob and Read tools to gather evidence:**

```bash
# Read security configurations
Read: config/security.yml
Read: docker-compose.yml
Read: infrastructure/terraform/

# Find authentication implementations
Glob: **/*auth*.py
Glob: **/*auth*.ts

# Find encryption implementations
Glob: **/*encrypt*.py
Grep: pattern="TLS|SSL" path=nginx/
Grep: pattern="bcrypt|Argon2" path=src/

# Find access control
Grep: pattern="@require_auth|@login_required"
Grep: pattern="RBAC|role.*required"
```

**Evidence to collect:**
- System architecture diagrams
- Data flow diagrams
- Security policies and procedures
- Access control configurations (RBAC, authentication)
- Encryption implementations (TLS, database encryption)
- Logging and monitoring setup
- Incident response plan
- Data retention and deletion policies
- Vendor agreements and third-party risk assessments

### 3. Framework Mapping

Map technical controls to compliance requirements.

#### GDPR Requirements

**Key GDPR Articles:**
- **Art. 5**: Data protection principles (lawfulness, fairness, transparency, purpose limitation, data minimization, accuracy, storage limitation, integrity/confidentiality)
- **Art. 6**: Lawful basis for processing (consent, contract, legal obligation, vital interests, public task, legitimate interests)
- **Art. 15-22**: Data subject rights (access, rectification, erasure, restriction, portability, objection)
- **Art. 25**: Data protection by design and default
- **Art. 32**: Security of processing (encryption, pseudonymization, resilience, testing)
- **Art. 33**: Breach notification (within 72 hours to supervisory authority)
- **Art. 35**: Data protection impact assessment (DPIA) for high-risk processing

**Technical Controls for GDPR:**
- Consent management system for lawful basis
- Data subject rights implementation (access, deletion, portability)
- Encryption at rest and in transit for security
- Access controls and authentication
- Audit logging for accountability
- Data retention and deletion automation
- Breach detection and notification procedures
- Privacy by design in development lifecycle

#### SOC 2 Requirements

**Trust Services Criteria (TSC):**
- **CC1-CC5**: Common Criteria (control environment, communication, risk assessment, monitoring, control activities)
- **CC6**: Logical and physical access controls
- **CC7**: System operations (monitoring, incident response, change management)
- **CC8**: Change management
- **CC9**: Risk mitigation

**Technical Controls for SOC 2:**
- Multi-factor authentication (CC6.1)
- Role-based access control (CC6.2)
- Encryption for data at rest and in transit (CC6.7)
- System monitoring and alerting (CC7.2)
- Log collection and review (CC7.3)
- Vulnerability management (CC7.1)
- Incident response procedures (CC7.4)
- Change management process (CC8.1)
- Backup and disaster recovery (CC9.1)

#### HIPAA Requirements

**HIPAA Safeguards:**
- **Administrative Safeguards**: Security management process, workforce security, information access management, security awareness training, security incident procedures
- **Physical Safeguards**: Facility access controls, workstation use/security, device and media controls
- **Technical Safeguards**: Access control, audit controls, integrity controls, transmission security

**Technical Controls for HIPAA:**
- Unique user identification and authentication
- Automatic logoff after inactivity
- Encryption of PHI at rest and in transit
- Audit logs for PHI access
- Integrity controls (checksums, digital signatures)
- Access control (role-based, least privilege)
- Emergency access procedures
- Workstation security (screen locks, physical security)
- Backup and disaster recovery for PHI

#### PCI-DSS Requirements

**PCI-DSS Requirements:**
- **Req 1**: Install and maintain firewall configuration
- **Req 2**: Don't use vendor-supplied defaults (passwords, security parameters)
- **Req 3**: Protect stored cardholder data (encrypt at rest)
- **Req 4**: Encrypt transmission of cardholder data (TLS 1.2+)
- **Req 7**: Restrict access to cardholder data (need-to-know basis)
- **Req 8**: Assign unique ID to each person with computer access
- **Req 9**: Restrict physical access to cardholder data
- **Req 10**: Track and monitor all access to network resources and cardholder data
- **Req 11**: Regularly test security systems and processes
- **Req 12**: Maintain policy that addresses information security

**Technical Controls for PCI-DSS:**
- Firewall rules restricting access to cardholder data environment
- No default passwords (all changed)
- Cardholder data encrypted with AES-256
- TLS 1.2+ for transmission (no SSLv3, TLS 1.0, TLS 1.1)
- Multi-factor authentication for remote access
- Unique user IDs, no shared accounts
- Role-based access control (RBAC)
- Audit logs for all access to cardholder data
- Log retention for at least 1 year
- Quarterly vulnerability scans
- Annual penetration testing
- Security policy documented and distributed

For detailed framework requirements, see:
- [GDPR Compliance Guide](references/gdpr-compliance.md)
- [SOC 2 Compliance Guide](references/soc2-compliance.md)
- [HIPAA Compliance Guide](references/hipaa-compliance.md)
- [PCI-DSS Compliance Guide](references/pci-dss-compliance.md)

### 4. Gap Analysis

Compare required controls vs implemented controls.

**Gap Analysis Template:**

```markdown
## Gap Analysis

### [Framework] - [Control Area]

**Requirement**: [Specific requirement from framework]
**Current State**: [What is currently implemented]
**Gap**: [What is missing or insufficient]
**Risk Level**: [Critical/High/Medium/Low]
**Impact**: [Business impact of non-compliance]
**Remediation**: [Specific steps to close gap]
**Effort**: [Estimated effort - hours/days/weeks]
**Priority**: [1-5, where 1 is highest]
**Owner**: [Team/person responsible]
**Timeline**: [Target completion date]

---

**Example:**

### GDPR - Data Subject Rights (Art. 15-22)

**Requirement**: Provide users ability to export their personal data (data portability)
**Current State**: No data export functionality exists
**Gap**: Missing data portability implementation
**Risk Level**: High
**Impact**: Non-compliance with GDPR, potential fines up to 4% of annual revenue
**Remediation**:
1. Implement API endpoint to export user data in JSON format
2. Add UI button for users to trigger export
3. Include all personal data from all systems
4. Deliver export within 30 days of request

**Effort**: 40 hours (1 week)
**Priority**: 1
**Owner**: Backend development team
**Timeline**: 2024-03-31
```

### 5. Evidence Collection

Organize evidence for audit readiness.

**Evidence Package Structure:**
```
evidence/
├── policies/
│   ├── security-policy.pdf
│   ├── incident-response-plan.pdf
│   ├── data-retention-policy.pdf
│   └── acceptable-use-policy.pdf
├── configurations/
│   ├── firewall-rules.txt
│   ├── tls-configuration.txt
│   ├── database-encryption-config.txt
│   └── access-control-matrix.xlsx
├── logs/
│   ├── authentication-logs-sample.txt
│   ├── audit-logs-sample.txt
│   └── security-events-sample.txt
├── certifications/
│   ├── ssl-certificate.pem
│   └── penetration-test-report.pdf
└── documentation/
    ├── system-architecture-diagram.png
    ├── data-flow-diagram.png
    ├── encryption-implementation.md
    └── incident-response-procedures.md
```

**Evidence Checklist:**
- [ ] Security policies (documented and approved)
- [ ] Configuration exports (firewall, TLS, database)
- [ ] Log samples (authentication, audit, security events)
- [ ] Access control matrix (users, roles, permissions)
- [ ] Encryption certificates and configurations
- [ ] Incident response documentation and test results
- [ ] Penetration test and vulnerability scan reports
- [ ] Employee training records
- [ ] Vendor risk assessments
- [ ] Data processing agreements (DPAs)
- [ ] Privacy notices and consent forms
- [ ] Backup and disaster recovery test results

### 6. Report Generation

Create comprehensive compliance audit report.

**Report Template:**

```markdown
# Compliance Audit Report

**Date**: [Current date]
**Auditor**: Claude Sonnet 4.5 (Automated Compliance Audit)
**Frameworks**: [GDPR, SOC2, HIPAA, PCI-DSS]
**Scope**: [System description]
**Audit Period**: [Start date] to [End date]

---

## Executive Summary

**Overall Compliance Status**: [Compliant / Non-Compliant / Conditional]

**Compliance Scores:**
- GDPR: XX% compliant
- SOC 2: XX% compliant
- HIPAA: XX% compliant
- PCI-DSS: XX% compliant

**Critical Findings**: X critical gaps requiring immediate attention
**High Priority Findings**: Y high-priority gaps
**Medium/Low Findings**: Z lower-priority gaps

**Recommended Actions**:
1. [Most critical remediation]
2. [Second most critical]
3. [Third most critical]

**Timeline for Full Compliance**: [Estimated timeframe]

---

## Detailed Findings

### [Framework] Compliance

**Overall Score**: XX% compliant

#### [Control Area 1]

**Status**: ✅ Compliant / ❌ Non-Compliant / ⚠️ Partial

**Requirements Met**:
- [Requirement 1]: ✅ Implemented
- [Requirement 2]: ✅ Implemented

**Requirements Not Met**:
- [Requirement 3]: ❌ Missing [specific detail]
- [Requirement 4]: ⚠️ Partially implemented [what's missing]

**Evidence**:
- [Evidence reference 1]
- [Evidence reference 2]

**Gaps**:
1. [Gap description with severity]
2. [Gap description with severity]

---

[Repeat for each control area and framework]

---

## Gap Analysis Summary

| Framework | Control Area | Gap | Severity | Effort | Priority | Timeline |
|-----------|-------------|-----|----------|--------|----------|----------|
| GDPR | Data Subject Rights | No data export | High | 1 week | 1 | 2024-03-31 |
| SOC2 | Access Control | No MFA | Critical | 3 days | 1 | 2024-03-15 |
| HIPAA | Encryption | No PHI encryption | Critical | 2 weeks | 1 | 2024-04-15 |
| PCI-DSS | Logging | Insufficient log retention | High | 1 week | 2 | 2024-04-30 |

---

## Remediation Plan

### Phase 1: Critical Gaps (0-30 days)

1. **[Gap 1 - Critical]**
   - **Description**: [Detailed gap description]
   - **Remediation Steps**:
     1. [Step 1]
     2. [Step 2]
     3. [Step 3]
   - **Owner**: [Team/person]
   - **Deadline**: [Date]
   - **Success Criteria**: [How to verify completion]

[Repeat for each critical gap]

### Phase 2: High Priority Gaps (30-90 days)

[Similar structure for high-priority gaps]

### Phase 3: Medium/Low Priority (90+ days)

[Similar structure for medium/low gaps]

---

## Evidence Package

**Evidence Location**: [Path to evidence folder]

**Evidence Summary**:
- Policies: X documents
- Configurations: Y files
- Logs: Z samples
- Certifications: W items
- Documentation: V artifacts

**Evidence Index**:
- [Evidence 1]: [Description] → [Framework requirement]
- [Evidence 2]: [Description] → [Framework requirement]
- [Evidence 3]: [Description] → [Framework requirement]

---

## Compliance Controls Matrix

| Control ID | Control Description | Implementation Status | Evidence | Test Result | Framework Mapping |
|------------|-------------------|----------------------|----------|-------------|------------------|
| AC-1 | User authentication | ✅ Implemented | config/auth.yml | ✅ Pass | SOC2-CC6.1, HIPAA-Tech |
| AC-2 | Multi-factor auth | ❌ Not implemented | N/A | ❌ Fail | SOC2-CC6.1 |
| EN-1 | TLS encryption | ✅ Implemented | nginx/ssl.conf | ✅ Pass | GDPR-Art32, PCI-Req4 |

[Continue for all controls]

---

## Recommendations

### Immediate Actions (Next 7 days)
1. [Urgent recommendation]
2. [Urgent recommendation]

### Short-Term (Next 30 days)
1. [Important recommendation]
2. [Important recommendation]

### Long-Term (Next 90 days)
1. [Strategic recommendation]
2. [Strategic recommendation]

### Process Improvements
1. [Process improvement suggestion]
2. [Process improvement suggestion]

---

## Next Steps

1. **Review Report**: Stakeholders review findings and remediation plan
2. **Assign Owners**: Assign remediation tasks to responsible teams
3. **Track Progress**: Create tickets/tasks in project management system
4. **Re-Audit**: Schedule follow-up audit after remediation (suggested: 90 days)
5. **Continuous Monitoring**: Implement automated compliance monitoring

---

## Appendix

### A. Framework Requirements Summary
[Summary of key requirements for each framework]

### B. Risk Assessment
[Risk levels, likelihood, impact for each gap]

### C. Compliance Timeline
[Gantt chart or timeline for achieving full compliance]

### D. Definitions
[Glossary of compliance terms]

---

**Report Generated**: [Timestamp]
**Generated By**: Claude Sonnet 4.5 (Automated Compliance Audit)
**Contact**: [Your contact information]
```

## Quality Standards

Every compliance audit must meet these standards:

- [ ] **Complete coverage**: All framework requirements evaluated
- [ ] **Evidence-based**: Every finding supported by evidence or lack thereof
- [ ] **Specific gaps**: Exact description of what's missing, not vague statements
- [ ] **Actionable remediation**: Step-by-step guidance with owners and timelines
- [ ] **Risk assessment**: Severity justified by business impact and regulatory risk
- [ ] **Evidence organized**: Clear structure and references
- [ ] **Compliance percentage calculated**: Objective measurement of compliance level
- [ ] **Controls matrix**: Technical controls mapped to framework requirements
- [ ] **Executive summary**: High-level overview for leadership
- [ ] **Detailed findings**: Technical details for implementation teams

## Common Patterns

### GDPR Compliance
- **Consent management**: Granular, opt-in consent with withdrawal mechanism
- **Data subject rights**: Automated processes for access, rectification, erasure, portability
- **Breach notification**: Detection within 72 hours, notification procedures documented
- **Privacy by design**: Security controls in development lifecycle
- **Data minimization**: Collect only necessary data, retention limits enforced
- **DPIAs**: Required for high-risk processing (automated decisions, large-scale sensitive data)

### SOC 2 Compliance
- **Logical access (CC6)**: MFA, RBAC, unique user IDs, password policies
- **System monitoring (CC7)**: Centralized logging, security alerts, incident response
- **Change management (CC8)**: Code review, testing, approval process, rollback capability
- **Risk mitigation (CC9)**: Backups, disaster recovery, business continuity

### HIPAA Compliance
- **Administrative**: Security officer, workforce training, sanctions policy
- **Physical**: Facility access, workstation security, device disposal
- **Technical**: Unique user IDs, encryption, audit logs, automatic logoff
- **Business Associates**: BAAs with all vendors handling PHI

### PCI-DSS Compliance
- **Network security (Req 1-2)**: Firewalls, no default passwords
- **Cardholder data protection (Req 3-4)**: Encrypt at rest and in transit
- **Access control (Req 7-9)**: Need-to-know, unique IDs, physical security
- **Monitoring (Req 10-11)**: Audit logs, vulnerability management, penetration testing
- **Policy (Req 12)**: Security policy maintained and communicated

## References

For detailed framework requirements:
- [GDPR Compliance Guide](references/gdpr-compliance.md)
- [SOC 2 Compliance Guide](references/soc2-compliance.md)
- [HIPAA Compliance Guide](references/hipaa-compliance.md)
- [PCI-DSS Compliance Guide](references/pci-dss-compliance.md)

## Integration

This skill works with:
- **System Architect agent**: For understanding architecture and data flows
- **Security Engineer agent**: For validating security controls
- **Data-encryption skill**: For validating encryption implementations
- **Authentication-security skill**: For reviewing auth/access controls
- **Secure-code-review skill**: For security code analysis
- **Backend/Frontend Developer agents**: For technical control implementation
- **DevOps Engineer agent**: For infrastructure and monitoring controls
