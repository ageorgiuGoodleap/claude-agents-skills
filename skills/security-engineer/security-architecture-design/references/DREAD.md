# DREAD Risk Scoring Methodology

## Overview

DREAD is a risk assessment model developed by Microsoft for rating security threats. It provides a quantitative risk score to help prioritize which threats to address first.

## DREAD Components

Each threat is scored 0-10 on five factors. The overall risk score is the average of all five scores.

**Formula:** `Risk Score = (D + R + E + A + D) / 5`

### D - Damage Potential

**Question:** How severe is the impact if this threat is successfully exploited?

**Scoring Guide:**

| Score | Damage Level | Description | Examples |
|-------|--------------|-------------|----------|
| 0-2 | Minimal | Negligible impact, cosmetic issues only | Typo in error message, minor UI glitch |
| 3-4 | Low | Limited impact, affects individual users | Single user account compromise |
| 5-6 | Medium | Moderate impact, affects business operations | Service degradation, data of some users exposed |
| 7-8 | High | Significant impact, major business disruption | Many user accounts compromised, revenue loss |
| 9-10 | Critical | Catastrophic impact, existential threat | Complete system compromise, all customer data exposed |

**Consider:**
- Financial loss potential
- Reputational damage
- Legal/regulatory consequences
- Data sensitivity
- System criticality
- Number of affected users
- Recovery cost and time

**Examples:**
- **Score 2:** XSS that displays an alert box (no data theft)
- **Score 5:** IDOR allowing access to another user's profile
- **Score 8:** SQL injection exposing 10,000 customer records
- **Score 10:** Root access allowing complete system control

### R - Reproducibility

**Question:** How easy is it to reproduce the attack? Can it be reliably repeated?

**Scoring Guide:**

| Score | Reproducibility | Description |
|-------|----------------|-------------|
| 0-2 | Very Hard | Extremely difficult, requires rare conditions, race conditions |
| 3-4 | Hard | Requires specific timing or environment, not consistently reproducible |
| 5-6 | Moderate | Can be reproduced with some effort and specific conditions |
| 7-8 | Easy | Can be reproduced most of the time with standard tools |
| 9-10 | Trivial | Works every time, no special conditions needed |

**Consider:**
- Consistency of exploit success
- Required timing or race conditions
- Environmental dependencies
- Need for specific configurations
- Availability of exploit tools

**Examples:**
- **Score 2:** Race condition that succeeds 1% of the time
- **Score 5:** Attack works only with specific browser/OS combination
- **Score 8:** SQL injection that works reliably with simple payload
- **Score 10:** Open API endpoint with no authentication required

### E - Exploitability

**Question:** How much skill, time, and resources are required to exploit this threat?

**Scoring Guide:**

| Score | Exploitability | Description | Attacker Profile |
|-------|---------------|-------------|------------------|
| 0-2 | Very Hard | Requires expert knowledge, custom tools, significant time | Nation-state, security researchers |
| 3-4 | Hard | Requires advanced skills, some tool development | Skilled penetration testers |
| 5-6 | Moderate | Requires intermediate skills, readily available tools | Experienced hackers |
| 7-8 | Easy | Requires basic technical knowledge, point-and-click tools | Script kiddies, automated scanners |
| 9-10 | Trivial | Requires no technical skill, can be done via web browser | Anyone, including non-technical users |

**Consider:**
- Required skill level
- Time investment needed
- Specialized tools required
- Knowledge prerequisites
- Availability of exploits/tutorials
- Need for insider access

**Examples:**
- **Score 2:** Cryptographic vulnerability requiring custom exploit development
- **Score 5:** XXE injection requiring XML knowledge
- **Score 8:** CSRF attack possible with simple HTML form
- **Score 10:** Open S3 bucket accessible via web browser

### A - Affected Users

**Question:** How many users or systems would be impacted if this threat is exploited?

**Scoring Guide:**

| Score | Affected Users | Description | Scale |
|-------|---------------|-------------|-------|
| 0-2 | Very Few | Individual users, isolated impact | 1-10 users |
| 3-4 | Some | Small group of users, limited scope | 10-100 users |
| 5-6 | Many | Significant user base affected | 100-1,000 users |
| 7-8 | Most | Majority of users affected | 1,000-100,000 users |
| 9-10 | All | All users, entire system compromised | 100,000+ users or entire system |

**Consider:**
- Number of users directly affected
- Percentage of user base
- System criticality
- Downstream impacts
- Public vs internal systems
- Business impact scope

**Examples:**
- **Score 2:** IDOR affecting individual user profiles (attacker chooses victim)
- **Score 5:** XSS on moderately trafficked page
- **Score 8:** Authentication bypass affecting all users
- **Score 10:** Database breach exposing all customer data

### D - Discoverability

**Question:** How easy is it for an attacker to discover this vulnerability?

**Scoring Guide:**

| Score | Discoverability | Description |
|-------|----------------|-------------|
| 0-2 | Very Hard | Extremely difficult to find, requires source code review or inside knowledge |
| 3-4 | Hard | Not obvious, requires manual testing and expertise |
| 5-6 | Moderate | Can be found with focused effort and testing |
| 7-8 | Easy | Easily found with automated scanners or basic testing |
| 9-10 | Trivial | Obvious, visible to anyone, no tools needed |

**Consider:**
- Is it visible in UI?
- Would automated scanners find it?
- Is it documented (accidentally or intentionally)?
- Does error message reveal it?
- Is it in common attack patterns?
- Has it been publicly disclosed?

**Examples:**
- **Score 2:** Logic flaw in complex business process
- **Score 5:** SQL injection requiring specific parameter combination
- **Score 8:** Missing authentication on /admin endpoint
- **Score 10:** Hardcoded API key visible in JavaScript source

## Risk Score Interpretation

After calculating the average DREAD score:

| Risk Score | Priority | Action |
|------------|----------|--------|
| 8.0 - 10.0 | CRITICAL | Fix immediately, emergency patch |
| 6.0 - 7.9 | HIGH | Fix in next sprint, high priority |
| 4.0 - 5.9 | MEDIUM | Fix in planned release, normal priority |
| 2.0 - 3.9 | LOW | Fix when convenient, low priority |
| 0.0 - 1.9 | MINIMAL | Consider accepting risk, document decision |

## DREAD Scoring Examples

### Example 1: SQL Injection in Login Form

| Factor | Score | Rationale |
|--------|-------|-----------|
| **Damage** | 9 | Could expose entire user database with passwords |
| **Reproducibility** | 8 | Works consistently with standard SQL injection payloads |
| **Exploitability** | 7 | Requires basic SQL knowledge, many tutorials available |
| **Affected Users** | 10 | All users' data at risk |
| **Discoverability** | 6 | Requires testing with SQL payloads, not immediately obvious |
| **TOTAL** | **8.0** | **CRITICAL** - Fix immediately |

### Example 2: XSS in Comment Field

| Factor | Score | Rationale |
|--------|-------|-----------|
| **Damage** | 6 | Could steal session cookies, limited to comment viewers |
| **Reproducibility** | 7 | Works reliably with basic XSS payloads |
| **Exploitability** | 8 | Many XSS payloads available, requires minimal skill |
| **Affected Users** | 5 | Affects users viewing specific comments |
| **Discoverability** | 7 | Easily found with automated scanners |
| **TOTAL** | **6.6** | **HIGH** - Fix in next sprint |

### Example 3: Missing Rate Limiting on API

| Factor | Score | Rationale |
|--------|-------|-----------|
| **Damage** | 5 | Could cause service degradation/downtime |
| **Reproducibility** | 9 | Works every time, simple to execute |
| **Exploitability** | 9 | Requires only a simple script, no special skills |
| **Affected Users** | 8 | All users affected by service degradation |
| **Discoverability** | 8 | Easy to discover by simply calling API repeatedly |
| **TOTAL** | **7.8** | **HIGH** - Fix in next sprint |

### Example 4: Information Disclosure in Error Message

| Factor | Score | Rationale |
|--------|-------|-----------|
| **Damage** | 4 | Reveals technology stack, aids further attacks |
| **Reproducibility** | 8 | Error occurs consistently with invalid input |
| **Exploitability** | 9 | Just view error message, no exploitation needed |
| **Affected Users** | 3 | Information helps attacker but doesn't directly affect users |
| **Discoverability** | 9 | Obvious in error responses |
| **TOTAL** | **6.6** | **HIGH** - Fix in next sprint |

### Example 5: Weak Password Policy

| Factor | Score | Rationale |
|--------|-------|-----------|
| **Damage** | 7 | Individual accounts easier to compromise |
| **Reproducibility** | 7 | Consistent weakness |
| **Exploitability** | 6 | Requires password attack tools, moderate effort |
| **Affected Users** | 6 | Affects users with weak passwords (subset) |
| **Discoverability** | 5 | Requires testing or observation |
| **TOTAL** | **6.2** | **HIGH** - Fix in next sprint |

### Example 6: Insecure Direct Object Reference (IDOR)

| Factor | Score | Rationale |
|--------|-------|-----------|
| **Damage** | 6 | Attacker can access other users' data |
| **Reproducibility** | 9 | Works consistently by changing ID parameter |
| **Exploitability** | 8 | Simple parameter manipulation |
| **Affected Users** | 7 | Any user can be targeted |
| **Discoverability** | 6 | Requires parameter testing |
| **TOTAL** | **7.2** | **HIGH** - Fix in next sprint |

### Example 7: Cross-Site Request Forgery (CSRF)

| Factor | Score | Rationale |
|--------|-------|-----------|
| **Damage** | 6 | Unauthorized actions performed on behalf of user |
| **Reproducibility** | 8 | Works when user is authenticated and visits malicious site |
| **Exploitability** | 7 | Requires crafting malicious page, moderate skill |
| **Affected Users** | 5 | Affects users who visit attacker's site while authenticated |
| **Discoverability** | 6 | Requires testing for CSRF tokens |
| **TOTAL** | **6.4** | **HIGH** - Fix in next sprint |

## Best Practices for DREAD Scoring

### 1. Be Objective

- Base scores on facts, not assumptions
- Use evidence where possible
- Document your rationale
- Be consistent across similar threats

### 2. Consider Context

- Business impact varies by industry
- User base size affects Affected Users score
- System criticality influences Damage score
- Public vs internal systems affect Discoverability

### 3. Use Team Input

- Involve security, development, and business stakeholders
- Different perspectives improve accuracy
- Consensus-based scoring reduces bias
- Security team provides threat intelligence
- Development team provides technical feasibility
- Business team provides impact assessment

### 4. Update Regularly

- Scores change as systems evolve
- New attack techniques increase Exploitability
- Public disclosure increases Discoverability
- Mitigation reduces Damage and Affected Users

### 5. Document Assumptions

- Note any assumptions made during scoring
- Clarify scope and boundaries
- Document edge cases
- Explain controversial scores

## DREAD Limitations

**Subjectivity:**
- Scoring can vary between assessors
- Requires calibration across team
- Use scoring guidelines consistently

**Oversimplification:**
- Reduces complex risk to single number
- May not capture nuanced threats
- Combine with qualitative analysis

**Context Dependency:**
- Scores depend heavily on system context
- One size doesn't fit all
- Adjust scoring criteria for your environment

**Bias Towards Obvious Threats:**
- High Discoverability and Exploitability can inflate scores
- Low-likelihood, high-impact threats may be underweighted
- Balance quantitative score with qualitative judgment

## Integration with STRIDE

Use DREAD in combination with STRIDE:

1. **Identify threats with STRIDE** - Systematic threat enumeration
2. **Score threats with DREAD** - Quantitative risk assessment
3. **Prioritize by DREAD score** - Focus on highest risks first
4. **Design controls** - Mitigate high-priority threats
5. **Re-score after controls** - Assess residual risk

This combined approach ensures comprehensive threat modeling with prioritized remediation.
