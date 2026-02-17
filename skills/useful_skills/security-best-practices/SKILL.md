---
name: security-best-practices
description: |
  Perform language and framework-specific security reviews and write secure-by-default code.
  Use when the user explicitly requests security best practices guidance, a security review,
  vulnerability scan, security report, or secure coding help. Supports Python (Django, Flask,
  FastAPI), JavaScript/TypeScript (React, Vue, jQuery, Express, Next.js), and Go backends.
  Do not trigger for general code review, debugging, or non-security tasks.
---

# Security Best Practices

## Overview

This skill helps you write secure-by-default code and identify security vulnerabilities in existing codebases. It provides language and framework-specific security guidance through comprehensive reference documents.

**Supported languages and frameworks:**

- **Python**: Django, Flask, FastAPI (web servers)
- **JavaScript/TypeScript**: React, Vue, jQuery (frontend), Express, Next.js (backend)
- **Go**: General backend security

## Operating Modes

### 1. Secure-by-default mode (Primary)

When writing new code or implementing features, follow security best practices from the start:

- Apply relevant security guidance automatically
- Use safe APIs and proven libraries over custom security code
- Avoid introducing risky patterns (XSS sinks, SQL injection, command injection, etc.)
- Follow framework-specific secure coding patterns

### 2. Passive review mode (Always active)

While working on code, passively detect critical security issues:

- Notice major vulnerabilities in code you're reading or editing
- Flag critical or high-severity issues as you encounter them
- Focus on the highest-impact vulnerabilities
- Provide brief explanation and safe fix when flagging issues

### 3. Active audit mode (On request)

When the user asks for a security scan, audit, or vulnerability report:

- Systematically search the codebase for security violations
- Produce a comprehensive security report
- Prioritize findings by severity (Critical, High, Medium, Low)
- Offer to implement fixes after report review

## Workflow

### Step 1: Identify Languages and Frameworks

Determine ALL languages and frameworks in scope:

1. Check project files (package.json, requirements.txt, go.mod, etc.)
2. Inspect code structure and imports
3. Identify both frontend AND backend frameworks for web apps
4. Focus on primary/core frameworks

### Step 2: Load Relevant Security Guidance

Check this skill's `references/` directory for matching documentation.

**Filename format:** `<language>-<framework>-<stack>-security.md`

**Reference files available:**

| Language | Framework | Stack | Reference File |
|----------|-----------|-------|----------------|
| Python | Django | Web Server | `python-django-web-server-security.md` |
| Python | Flask | Web Server | `python-flask-web-server-security.md` |
| Python | FastAPI | Web Server | `python-fastapi-web-server-security.md` |
| JavaScript/TypeScript | Express | Web Server | `javascript-express-web-server-security.md` |
| JavaScript/TypeScript | Next.js | Web Server | `javascript-typescript-nextjs-web-server-security.md` |
| JavaScript/TypeScript | React | Web Frontend | `javascript-typescript-react-web-frontend-security.md` |
| JavaScript/TypeScript | Vue | Web Frontend | `javascript-typescript-vue-web-frontend-security.md` |
| JavaScript | jQuery | Web Frontend | `javascript-jquery-web-frontend-security.md` |
| JavaScript | General | Web Frontend | `javascript-general-web-frontend-security.md` |
| Go | General | Backend | `golang-general-backend-security.md` |

**Important:**
- For web apps with frontend AND backend, load BOTH reference files
- For unspecified frontend frameworks, use `javascript-general-web-frontend-security.md`
- Load ALL relevant reference files for the specific languages/frameworks in use

### Step 3: Apply Security Guidance

**For secure-by-default mode:**
- Use the loaded guidance to write secure code from this point forward
- Apply best practices automatically without being asked

**For passive review mode:**
- Notice violations as you work through the code
- Flag critical issues with brief explanation
- Suggest safe fixes for important vulnerabilities

**For active audit mode:**
- Proceed to the audit workflow below

## Active Audit Workflow

When the user requests a security scan or report:

### 1. Scan the Codebase

Systematically search for security violations based on loaded guidance:

**Recommended scan order:**
1. Authentication and authorization mechanisms
2. Input validation and sanitization
3. Dangerous sinks (XSS, SQL injection, command injection)
4. Secrets and credential management
5. CORS and cross-origin security
6. Session management and cookies
7. File upload and serving
8. Third-party dependencies and integrity

### 2. Generate Security Report

Create a markdown report at `security_best_practices_report.md` (or user-specified location).

**Report structure:**

```markdown
# Security Best Practices Report

**Project:** [Project name]
**Date:** [Date]
**Frameworks:** [List of frameworks]

## Executive Summary

[2-3 paragraph overview of overall security posture and key findings]

## Critical Findings

### [C-1] [Brief title]
- **Location:** [file:line]
- **Impact:** [One sentence describing potential impact]
- **Evidence:**
  ```[language]
  [code snippet]
  ```
- **Fix:** [Specific remediation steps]

[Repeat for each critical finding]

## High Severity Findings

[Same format as critical]

## Medium Severity Findings

[Same format as critical]

## Low Severity Findings

[Same format as critical]

## Recommendations

1. [Priority recommendation]
2. [Next priority recommendation]
...

## Summary Statistics

- Total findings: [number]
- Critical: [number]
- High: [number]
- Medium: [number]
- Low: [number]
```

**Report guidelines:**
- Include numeric IDs for each finding (e.g., C-1, H-2, M-3, L-4)
- Always include file paths and line numbers for findings
- Provide specific code snippets as evidence
- Focus on critical findings with clear impact statements
- Keep findings concise but actionable

### 3. Present Findings

After writing the report:

1. Summarize key findings to the user (less verbose than full report)
2. Tell the user where the report was written
3. Offer to explain any findings in detail
4. Ask if they want to begin implementing fixes

## Implementing Fixes

When implementing security fixes:

### Fix One Finding at a Time

- Work through findings systematically
- Complete one fix fully before moving to the next
- Allow user to review between fixes

### Make Thoughtful Changes

Before implementing a fix:

1. **Consider impact:** Will this change break existing functionality?
2. **Check dependencies:** Does other code rely on the current behavior?
3. **Verify context:** Are there project-specific requirements that require an override?
4. **Test implications:** What tests need to run to verify no regressions?

**Important:** Insecure code often persists because other parts of the system depend on it. Avoid breaking the project, as this discourages future security improvements.

### Follow Project Conventions

- Use the project's existing commit workflow
- Write clear commit messages explaining the security fix
- Reference the finding ID in commit messages (e.g., "Fix C-1: SQL injection in user search")
- Avoid bundling unrelated findings in a single commit
- Run existing test suites to verify no regressions
- Inform the user about potential second-order impacts before making changes

### Add Clear Comments

When implementing fixes, add concise comments:

```python
# Security: Use parameterized query to prevent SQL injection (C-1)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

Keep comments brief and reference the security best practice being followed.

## Overrides and Project-Specific Requirements

Pay attention to project documentation (CLAUDE.md, README, security docs) that may require overriding certain best practices.

**When an override is needed:**

1. Don't fight with the user if they have a specific requirement
2. You MAY report the override but respect the decision
3. Suggest documenting the override and its rationale in project docs
4. This helps maintain context for future security reviews

## General Security Principles

These principles apply across all languages and frameworks:

### Use UUIDs for Public Resource IDs

**Don't:**
```python
# Predictable, sequential IDs
resource_id = 1, 2, 3...
```

**Do:**
```python
import uuid
resource_id = str(uuid.uuid4())  # Random, unguessable
```

**Why:** Sequential IDs let attackers enumerate resources and learn quantity.

### TLS and Secure Cookies - Handle Carefully

**Important notes on TLS:**

- Most development work runs without TLS (handled by proxies in production)
- Don't report missing TLS as a security issue unless it's a production deployment concern
- Be careful with "secure" cookie flags - they break non-TLS environments

**Safe pattern for secure cookies:**

```python
# Use environment flag to control secure cookie setting
is_production = os.getenv("ENVIRONMENT") == "production"
cookie_settings = {
    "secure": is_production,  # Only set secure flag in production
    "httponly": True,
    "samesite": "Lax"
}
```

**Avoid recommending HSTS:**
- HSTS has lasting impacts and can cause major outages
- It requires full understanding of implications
- Not recommended for most project scopes

### Never Disable Security Protections

When encountering security obstacles, never suggest:

- Weakening CSP with `unsafe-inline` or `unsafe-eval`
- Making CORS fully permissive (`*` with credentials)
- Removing input validation or sanitization
- Disabling CSRF protection
- Turning off TLS verification
- Skipping authentication checks

**Instead:** Find the secure solution that meets the requirement.

## No Matching Guidance Available

If no reference file exists for the identified language/framework:

1. Use your knowledge of well-known security best practices
2. Focus on critical vulnerabilities (OWASP Top 10)
3. If asked for a report, inform the user that framework-specific guidance isn't available
4. You can still generate the report and detect critical issues

## Reference Files

All language and framework-specific security guidance is in the `references/` directory. Load relevant files based on the languages and frameworks identified in Step 1.

Each reference file contains:

- Security requirements (MUST/SHOULD/MAY)
- Audit rules and detection patterns
- Safe coding examples
- Fix guidance for common vulnerabilities
- Framework-specific security considerations

**Progressive disclosure:** Only load reference files relevant to the current project. The references contain detailed security specifications and should be consulted when writing code or performing security reviews.
