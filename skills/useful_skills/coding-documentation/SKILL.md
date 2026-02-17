---
name: coding-documentation
description: |
  Generates professional documentation artifacts from code diffs and changes including PR descriptions, changelog entries, README updates, API documentation, migration notes, ADRs, and runbooks. Follows engineering best practices for minimal diffs, language-specific conventions (Python, TypeScript), and audience-appropriate documentation. Use when the user explicitly requests documentation for code changes with phrases like "document the diff", "create documentation", "write PR description", "generate changelog", "document this change", "create migration notes", or when analyzing code changes that require documentation artifacts.
---

# Coding Documentation

Generate professional documentation artifacts from code diffs and changes following engineering best practices.

## Overview

This skill produces documentation that:
- Accurately reflects code changes without speculation
- Follows language-specific conventions (Python PEP standards, TypeScript strict typing)
- Matches the appropriate artifact type to change impact
- Separates what changed, why it changed, and how to validate
- Provides clear guidance for reviewers, users, and maintainers

## When to Use This Skill

Activate this skill when the user explicitly requests:
- "Document the diff" or "document these changes"
- "Write a PR description" or "create PR documentation"
- "Generate changelog" or "create release notes"
- "Update README" or "document setup changes"
- "Write migration notes" or "document breaking changes"
- "Create ADR" or "document design decision"
- "Write runbook" or "document operational changes"

## Core Engineering Principles

### Ground Truth Rules

**Diff and tests define truth.** Never claim behavior not supported by the actual diff or explicit user statements.

**Existing docs define current public contract.** If the diff changes the contract, documentation must be updated or migration notes must be produced.

### Change Classification

Analyze the diff to identify change impact:

**Public API surface changes:**
- Exported functions, classes, or interfaces
- HTTP routes or RPC endpoints
- CLI flags or configuration keys
- Data schemas or contracts

**Runtime behavior changes:**
- Performance characteristics
- Concurrency patterns
- Retry semantics or error handling
- Logging or metrics

**Operational risk changes:**
- Failure modes
- On-call response procedures
- Rollout or rollback steps

## Artifact Selection Logic

Map change impact to required documentation artifacts:

| Change Type | Required Artifacts |
|-------------|-------------------|
| **Any reviewed change** | PR description with context, what changed, why, and review order |
| **User-facing change** | Changelog entry and release notes (curated, SemVer-framed) |
| **Usage path change** | README updates with new setup steps or corrected examples |
| **API/config change** | API reference updates, configuration schema documentation |
| **Breaking change** | Migration notes with explicit steps for callers |
| **Design decision** | ADR documenting durable choice, new dependencies, or tradeoffs |
| **Operational change** | Runbook with rollout steps, observability changes, failure modes |

## Documentation Artifact Types

### 1. PR Description and Reviewer Guide

**Warranted:** Almost always, when change is reviewed by someone else.

**Structure:**

```markdown
## What Changed
[Concise summary of changes]

## Why
[Business or technical justification]

## How to Validate
[Exact test commands and expected outcomes]

## Review Order
[Suggested file review sequence when multiple modules changed]

## Risk List
[Point to exact files or behaviors at risk]
```

**Writing rules:**
- Keep "What Changed" to 2-3 sentences maximum
- "Why" should explain the problem being solved, not repeat the diff
- "How to Validate" must include exact commands: `pytest tests/test_foo.py::test_bar`
- Review order matters when change crosses boundaries: "Start with schema.py, then handlers.py"
- Risk list should be specific: "auth.py lines 45-67 change error handling behavior"

### 2. Changelog Entry and Release Notes

**Warranted:** When change ships to users or other teams.

**Structure:**

```markdown
## [Version] - YYYY-MM-DD

### Breaking Changes
- [List changes that require user action]

### Added
- [New features or capabilities]

### Changed
- [Modifications to existing behavior]

### Fixed
- [Bug fixes]

### Deprecated
- [Soon-to-be-removed features]
```

**Writing rules:**
- Default to user impact and outcomes, not internal refactors
- Mention breaking changes prominently at the top
- Use SemVer framing: breaking = major, additive = minor, fix = patch
- Link to migration notes for breaking changes
- Avoid implementation details unless they affect observable behavior

**Examples:**

```markdown
### Breaking Changes
- **Authentication**: JWT tokens now expire after 1 hour (previously 24 hours). Update token refresh logic. See MIGRATION.md.

### Added
- **API**: New `/health/detailed` endpoint returns component-level health checks

### Fixed
- **Database**: Fix connection pool exhaustion under high load (#234)
```

### 3. README Updates and Usage Examples

**Warranted:** When primary usage path changes, new setup steps exist, or examples become misleading.

**Structure:**

```markdown
## Installation
[Updated prerequisites and install commands]

## Quick Start
[Corrected minimal working example]

## Configuration
[New or changed configuration options]

## Common Use Cases
[Updated real-world examples]
```

**Writing rules:**
- Update installation if new dependencies added
- Fix examples that would break with the new code
- Add new sections only when usage patterns genuinely change
- Keep examples minimal and runnable
- Include expected output for clarity

**Example:**

```markdown
## Configuration

### New: API Rate Limiting (v2.0.0)

Configure rate limits in `config.yaml`:

```yaml
rate_limit:
  requests_per_minute: 100
  burst_size: 20
```

Requests exceeding the limit return 429 status.
```

### 4. API Reference and Configuration Schema

**Warranted:** When any public interface, endpoint, CLI option, or config key is added, removed, renamed, or changes semantics.

**Structure for API changes:**

```markdown
### `function_name(param1: Type1, param2: Type2) -> ReturnType`

**Description:** [What the function does]

**Parameters:**
- `param1` (Type1): [Description and constraints]
- `param2` (Type2): [Description and constraints]

**Returns:** ReturnType - [Description of return value]

**Raises:**
- `ExceptionType`: [When this exception is raised]

**Example:**
```python
result = function_name("value1", 42)
```
```

**Structure for config changes:**

```markdown
### Configuration Key: `section.key_name`

**Type:** `string | number | boolean`

**Required:** Yes/No

**Default:** `default_value`

**Description:** [What this controls and when to change it]

**Example:**
```yaml
section:
  key_name: "example_value"
```
```

**Writing rules:**
- Document all parameters with types and constraints
- Include return types and possible exceptions
- Show realistic examples, not toy data
- For breaking changes, show before/after examples

### 5. Migration Notes for Breaking Changes

**Warranted:** When existing callers must change code or configuration, or when behavior changes in a way that can silently alter outputs.

**Structure:**

```markdown
## Migration Guide: [Version or Change Description]

### Summary
[One sentence describing what changed]

### Impact
[Who is affected and how]

### Required Actions

**Before:**
```python
# Old usage that will break
old_function(param1, param2)
```

**After:**
```python
# New required usage
new_function(param1=param1, param2=param2, new_param=value)
```

### Breaking Changes Detail

1. **[Specific change]**
   - **What changed:** [Precise description]
   - **Migration:** [Exact steps to update code]
   - **Validation:** [How to verify migration succeeded]

### Timeline
- **Deprecation:** [Date when old behavior is deprecated]
- **Removal:** [Date when old behavior is removed]
```

**Writing rules:**
- Lead with the required action, not the justification
- Show exact before/after code snippets
- Include validation steps: "Run `pytest` and expect 0 failures"
- For phased deprecation, provide explicit timeline
- Link to ADR if decision rationale is complex

**Example:**

```markdown
## Migration Guide: v2.0.0 - JWT Token Expiration

### Summary
JWT token expiration reduced from 24 hours to 1 hour.

### Impact
All applications using JWT authentication must implement token refresh.

### Required Actions

**Before:**
```python
# Tokens lasted 24 hours
token = auth.login(username, password)
# Use token for entire day
```

**After:**
```python
# Tokens last 1 hour, must refresh
token = auth.login(username, password)
# Implement refresh before expiration
if auth.is_token_expiring(token):
    token = auth.refresh_token(token)
```

### Breaking Changes Detail

1. **Token Expiration Time**
   - **What changed:** `JWT_EXPIRATION` reduced from 86400 seconds to 3600 seconds
   - **Migration:** Add token refresh logic in your auth middleware
   - **Validation:** Run integration tests with `SIMULATE_TIME_PASSAGE=true`

### Timeline
- **Deprecation:** 2024-01-01 (warning logged for tokens >1hr)
- **Removal:** 2024-02-01 (24hr tokens rejected)
```

### 6. ADR (Architecture Decision Record)

**Warranted:** When diff introduces a durable design choice, new dependency, new pattern, new constraint, or tradeoff that future maintainers must understand.

**Structure:**

```markdown
# ADR-[Number]: [Decision Title]

**Date:** YYYY-MM-DD

**Status:** Proposed | Accepted | Superseded

## Context

[Problem or situation requiring a decision]

## Decision

[The decision made and approach taken]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

### Neutral
- [Neutral consequence]

## Alternatives Considered

### [Alternative 1]
**Pros:** [Benefits]
**Cons:** [Drawbacks]
**Why rejected:** [Reason]

### [Alternative 2]
**Pros:** [Benefits]
**Cons:** [Drawbacks]
**Why rejected:** [Reason]

## Implementation Notes

[Technical details about how decision is implemented in the diff]
```

**Writing rules:**
- Context should explain the problem, not the solution
- Decision should be stated as a clear choice: "We will use Redis for caching"
- Consequences must list both positive and negative outcomes
- Alternatives must show you considered other options seriously
- Implementation notes tie the ADR to actual code changes

**Example:**

```markdown
# ADR-003: Use Redis for Session Storage

**Date:** 2024-01-15

**Status:** Accepted

## Context

Current in-memory session storage causes user logouts during deployments and cannot scale horizontally. We need persistent, distributed session storage.

## Decision

Use Redis for session storage with 1-hour TTL and automatic failover.

## Consequences

### Positive
- Sessions persist across deployments
- Horizontal scaling without session affinity
- Sub-millisecond read latency

### Negative
- New infrastructure dependency
- Network latency for every session read
- Requires Redis monitoring and ops knowledge

### Neutral
- Session data schema remains unchanged

## Alternatives Considered

### PostgreSQL
**Pros:** Already in stack, good for structured data
**Cons:** Higher latency, requires table design, overkill for ephemeral data
**Why rejected:** 10-20ms latency unacceptable for every request

### DynamoDB
**Pros:** Fully managed, auto-scaling
**Cons:** Higher cost, vendor lock-in, less familiar to team
**Why rejected:** Cost increase >300% for session use case

## Implementation Notes

- Added `redis-py` dependency (see `requirements.txt`)
- Session interface unchanged (`auth/session.py`)
- Redis connection pooling in `infrastructure/redis.py`
- Deployment adds Redis sidecar container
```

### 7. Runbook and Operational Notes

**Warranted:** When rollout steps, observability, incident response, or failure modes change.

**Structure:**

```markdown
# Runbook: [Feature or System Name]

## Overview
[What this system does and when operators need this runbook]

## Deployment Steps

1. **Pre-deployment checks**
   - [ ] [Check 1 with validation command]
   - [ ] [Check 2 with validation command]

2. **Deployment sequence**
   - [ ] [Step 1 with exact command]
   - [ ] [Step 2 with exact command]

3. **Post-deployment validation**
   - [ ] [Validation 1 with success criteria]
   - [ ] [Validation 2 with success criteria]

## Rollback Procedure

**Trigger conditions:** [When to rollback]

**Steps:**
1. [Exact rollback command or action]
2. [Validation that rollback succeeded]

## Monitoring and Alerts

**Key Metrics:**
- `metric.name`: [What it measures, normal range, alert threshold]
- `metric.name`: [What it measures, normal range, alert threshold]

**Dashboards:**
- [Dashboard name and URL]

## Failure Modes and Response

### Failure Mode: [Specific failure scenario]

**Symptoms:**
- [Observable symptoms]

**Diagnosis:**
```bash
# Commands to confirm diagnosis
kubectl logs pod-name | grep ERROR
```

**Resolution:**
1. [Step 1]
2. [Step 2]

**Escalation:** [When to escalate and to whom]

## Configuration Changes

**Environment Variables:**
- `VAR_NAME`: [Purpose, valid values, when to change]

**Feature Flags:**
- `feature.flag.name`: [Purpose, rollout percentage, rollback steps]
```

**Writing rules:**
- Pre-deployment checks must have exact validation commands
- Deployment steps must be copy-pasteable
- Rollback triggers must be specific: "Error rate >5%" not "if things look bad"
- Failure modes must include diagnosis commands, not just theory
- Monitoring must specify exact metric names and alert thresholds

**Example:**

```markdown
# Runbook: JWT Token Migration (v2.0.0)

## Overview

This runbook covers the deployment of 1-hour JWT token expiration (previously 24 hours). Operators need this during the rollout window to monitor token refresh rates and handle user reports of unexpected logouts.

## Deployment Steps

1. **Pre-deployment checks**
   - [ ] Verify Redis cluster health: `redis-cli ping` returns `PONG`
   - [ ] Check token refresh endpoint: `curl /auth/refresh` returns 200

2. **Deployment sequence**
   - [ ] Deploy backend with `JWT_EXPIRATION=3600`: `kubectl apply -f backend-v2.yaml`
   - [ ] Wait for health checks: `kubectl rollout status deployment/backend`
   - [ ] Enable monitoring: `kubectl apply -f monitoring-alerts.yaml`

3. **Post-deployment validation**
   - [ ] Verify new token expiration: `curl /auth/login | jq .expires_in` returns `3600`
   - [ ] Check refresh rate metric: `token_refresh_rate` should be >0

## Rollback Procedure

**Trigger conditions:**
- Token refresh error rate >10%
- User logout complaints >50/hour
- Token refresh latency p99 >500ms

**Steps:**
1. Revert to previous deployment: `kubectl rollout undo deployment/backend`
2. Verify rollback: `curl /auth/login | jq .expires_in` returns `86400`

## Monitoring and Alerts

**Key Metrics:**
- `token_refresh_requests_total`: Refresh attempts (expect 100-500/min, alert >1000/min)
- `token_refresh_errors_total`: Refresh failures (expect <1%, alert >5%)
- `token_expiration_seconds`: Token lifespan (expect 3600, alert if ≠3600)

**Dashboards:**
- [JWT Token Health](https://grafana.example.com/d/jwt-tokens)

## Failure Modes and Response

### Failure Mode: High Token Refresh Error Rate

**Symptoms:**
- `token_refresh_errors_total` >5%
- User reports of "Token refresh failed" errors

**Diagnosis:**
```bash
# Check Redis connectivity
redis-cli ping

# Check error logs
kubectl logs deployment/backend | grep "token_refresh_error"
```

**Resolution:**
1. Verify Redis cluster health
2. Check network connectivity between backend and Redis
3. Increase Redis connection pool size if connections exhausted

**Escalation:** Page SRE lead if error rate >10% for >5 minutes
```

## Language-Specific Considerations

### Python Documentation

**Type Hints:**
- Document all type hints in API reference
- Show type narrowing when Union types are used
- Include mypy validation in migration notes if strict typing changes

**Docstring Standards:**
- Follow PEP 257 for docstring format
- Include `Args:`, `Returns:`, `Raises:` sections
- Show examples in docstrings for complex functions

**Testing:**
- Reference pytest conventions in PR descriptions
- Include pytest command with specific test file when adding regression tests
- Document fixtures if test setup changes

**Example:**

```markdown
### `process_data(input: List[Dict[str, Any]], strict: bool = False) -> Result`

**Description:** Processes input data according to schema validation rules.

**Parameters:**
- `input` (List[Dict[str, Any]]): List of data records to process. Each dict must contain 'id' and 'value' keys.
- `strict` (bool): If True, raise ValidationError on schema mismatch. If False, log warning and skip invalid records. Default: False.

**Returns:** Result - Object containing processed records and error count.

**Raises:**
- `ValidationError`: When strict=True and input fails schema validation.
- `TypeError`: When input is not a list or contains non-dict elements.

**Example:**
```python
from myapp import process_data

records = [{"id": 1, "value": 100}, {"id": 2, "value": 200}]
result = process_data(records, strict=True)
print(result.processed_count)  # 2
```

**Type Signature:**
```python
def process_data(
    input: List[Dict[str, Any]],
    strict: bool = False
) -> Result:
    ...
```
```

### TypeScript Documentation

**Type Safety:**
- Document strict mode compatibility in PR description
- Show type narrowing patterns when discriminated unions change
- Include TypeScript compiler errors in breaking change notes

**Interface Changes:**
- Show before/after interface definitions in migration notes
- Document generic type parameter constraints
- Include type guard functions when type narrowing is required

**Example:**

```markdown
### Interface: `ApiResponse<T>`

**Description:** Generic wrapper for all API responses.

**Type Parameters:**
- `T`: The data type contained in the response. Must extend `Serializable`.

**Properties:**
- `success: boolean` - Whether the request succeeded
- `data: T | null` - Response data if success=true, null otherwise
- `error?: ErrorDetails` - Error details if success=false

**Type Guards:**

```typescript
function isSuccessResponse<T>(
  response: ApiResponse<T>
): response is ApiResponse<T> & { success: true; data: T } {
  return response.success === true;
}
```

**Usage:**

```typescript
const response = await api.fetch<User>('/users/123');

if (isSuccessResponse(response)) {
  console.log(response.data.name);  // TypeScript knows data is not null
} else {
  console.error(response.error);
}
```

**Breaking Change (v2.0.0):**

**Before:**
```typescript
interface ApiResponse {
  data: any;
  status: number;
}
```

**After:**
```typescript
interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error?: ErrorDetails;
}
```

**Migration:**
Replace status code checks with success field checks and add generic type parameter.
```

## Output Format Standards

### Always Separate

Every documentation artifact must separate:

1. **What Changed**
   - Concise, factual summary of the changes
   - Reference specific files, functions, or modules
   - Use past tense: "Changed X to Y"

2. **Why It Changed**
   - Business or technical justification
   - Problem being solved
   - Do not repeat the diff, explain the motivation

3. **How to Validate**
   - Exact commands to run
   - Expected outputs
   - Specific test cases

### Minimal Diff Awareness

**Do not suggest changes outside the actual diff:**
- If the diff only changes `auth.py`, do not document changes to `database.py`
- If the diff adds a function, do not claim it modifies existing behavior unless the diff shows that
- If tests show the change, reference those specific tests

**Do not invent requirements:**
- Only document configuration keys present in the diff
- Only document API parameters shown in the diff
- Only document error codes raised in the diff

### Audience Awareness

**For reviewers:**
- Focus on risk, complexity, and validation steps
- Provide review order for multi-file changes
- Highlight subtle behavior changes

**For users:**
- Focus on observable behavior changes
- Hide internal refactors and implementation details
- Provide migration steps for breaking changes

**For operators:**
- Focus on deployment steps, monitoring, and failure modes
- Provide exact commands and validation criteria
- Include rollback procedures

## Validation Checklist

Before delivering documentation, verify:

- [ ] All claims are supported by the actual diff
- [ ] Code snippets are syntactically correct and use correct types
- [ ] Commands are copy-pasteable and include expected output
- [ ] Breaking changes are prominently marked
- [ ] Migration steps are specific and actionable
- [ ] Examples use realistic data, not toy examples
- [ ] Language-specific conventions are followed (PEP 8 for Python, TypeScript strict mode compatibility)
- [ ] Risk areas are identified with exact file and line references
- [ ] The artifact type matches the change impact (API change → API reference update)

## When NOT to Generate Documentation

**Do not generate documentation when:**
- The diff is purely cosmetic (whitespace, comments)
- The change is internal refactoring with zero public API impact
- The user has not explicitly requested documentation
- The diff does not exist or is not provided

**Ask for clarification when:**
- The diff touches multiple systems and it's unclear which to prioritize
- The change appears to be breaking but no migration path is obvious
- Required context is missing (e.g., what version number to use for changelog)
