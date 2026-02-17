---
name: log-analysis
description: |
  Analyzes log files from test runs, CI/CD pipelines, application servers, and GitHub Actions.
  Produces comprehensive diagnostic reports with root cause analysis and actionable fixes.
  Use when the user mentions analyzing logs, debugging test failures, investigating build failures,
  understanding CI/CD errors, GitHub Actions issues, Playwright logs, or wants help diagnosing
  errors from log files. Automatically triggered for *.log, *.txt, *.out, *.err files or when
  user asks to analyze logs in a directory.
---

# Log Analysis Skill

This skill performs comprehensive analysis of log files, identifying errors, warnings, and issues across all log types, providing root cause analysis with specific file/line references and actionable fixes.

## Supported Log Types

- Test execution logs (Playwright, Jest, Vitest, pytest, Mocha)
- CI/CD pipeline logs (GitHub Actions, GitLab CI, Jenkins, CircleCI)
- Application server logs (Node.js, Python, Java, Ruby, Go)
- Build/compilation logs (TypeScript, webpack, Vite, Rollup, esbuild)
- Deployment logs and container logs (Docker, Kubernetes)
- Runtime error logs and crash dumps

## When to Use

Activate this skill when the user:
- Asks to analyze logs in a directory
- Mentions test failures, build failures, or CI/CD errors
- Requests debugging help with log files
- Wants to understand error patterns across multiple logs
- Needs root cause analysis of failures
- Mentions GitHub Actions, Playwright, test runs, or pipeline failures
- Provides paths to .log, .txt, .out, or .err files

## Analysis Workflow

### Phase 1: File Discovery and Inventory

**1.1 Locate All Log Files**
- Use Glob tool to find log files with patterns:
  - `**/*.log`
  - `**/*.txt`
  - `**/*.out`
  - `**/*.err`
  - User-specified patterns if provided
- If user specifies a directory, search within that directory
- If no directory specified, ask user for the target directory

**1.2 Assess File Sizes**
- Use Bash `ls -lh` to check sizes of discovered files
- Identify files exceeding 2000 lines that need chunked reading
- For large files (>100KB), use Read tool with offset/limit parameters
- Create complete inventory before starting analysis

**1.3 Prioritize Reading Order**
- Start with most recent logs (by modification time)
- Prioritize error logs (*.err) and test output logs
- Read CI/CD logs chronologically if multiple runs present

### Phase 2: Sequential Analysis

**2.1 Extract Metadata from Each File**
- **Timestamps**: First and last entry times to establish time range
- **Log source**: Application name, service, test suite
- **Environment**: OS, Node version, Python version, runtime details
- **Run type**: Test run, deployment, build, server runtime
- **Log purpose**: What component/process generated this log

**2.2 Issue Identification**

For each log file, identify and catalog:

**Critical Issues (Errors)**:
- Fatal errors and uncaught exceptions
- Test failures with assertion details
- Compilation/build errors with file:line references
- HTTP 4xx/5xx server errors
- Database connection failures
- Timeout errors
- Segmentation faults and crashes
- Missing dependencies or modules
- Authentication/authorization failures

**Warnings and Non-Critical Issues**:
- Deprecation warnings
- Performance warnings (memory, slow queries)
- Resource warnings (disk space, handles)
- Type mismatches or implicit conversions
- Unused variables or imports
- Configuration recommendations

**Test-Specific Issues**:
- Failed test cases with assertion messages
- Timeouts in tests
- Selector not found errors (Playwright/Selenium)
- Screenshot/video capture failures
- Test setup/teardown failures

**Build/Compilation Issues**:
- TypeScript type errors with file:line
- Linting errors and warnings
- Module resolution failures
- Circular dependencies
- Asset optimization failures

**2.3 Extract Full Context for Each Issue**

For every identified issue, capture:
- **Full error message**: Complete exception or error text
- **Stack trace**: All frames with file:line references
- **Surrounding context**: 3-5 lines before and after the error
- **Timestamp**: When the error occurred
- **Triggering action**: What operation was being performed
- **Related logs**: References to same error in other files

**2.4 Cross-File Pattern Analysis**

- Identify recurring errors across multiple files
- Detect cascading failures (error A causes error B)
- Find timing patterns (errors at specific times)
- Correlate errors with environmental factors
- Group related errors by root cause
- Establish chronological error sequence when timestamps available

### Phase 3: Root Cause Analysis

For each critical issue, perform deep analysis:

**3.1 Immediate Cause Identification**
- What specific operation failed?
- What was the direct trigger?
- Extract exact error code or message
- Identify the failing component

**3.2 Root Cause Inference**
- Why did this operation fail?
- Is this a code bug, configuration issue, or environmental problem?
- Are dependencies missing or misconfigured?
- Is this a timing/race condition issue?
- Is this a resource exhaustion problem?

**3.3 Impact Assessment**
- What functionality is affected?
- Is this blocking other operations?
- How many users/tests are impacted?
- Is this a regression or new issue?

**3.4 Fix Recommendation**
- Provide specific code changes with file:line references
- Suggest configuration updates
- Recommend dependency updates
- Propose architectural improvements if needed
- Include alternative approaches

### Phase 4: Report Generation

Create `LOGS_ANALYSIS.md` in the same directory as the logs (or user-specified location) with this exact structure:

```markdown
# Log Analysis Report

**Analysis Date**: [ISO timestamp]
**Total Files Analyzed**: [count]
**Total Issues Found**: [count] ([X] errors, [Y] warnings, [Z] other)

## Executive Summary

[2-3 sentences summarizing: purpose of these logs, main findings, most critical issues]

## Files Analyzed

| File Name | Size | Type | Time Range | Key Purpose |
|-----------|------|------|------------|-------------|
| example.log | 145KB | Test Run | 14:30-14:35 | Playwright E2E tests |
| build.log | 23KB | Build | 14:25-14:28 | TypeScript compilation |

## Critical Issues (Errors)

### Error 1: [Category] - [Brief Description]

**Severity**: Critical / High / Medium
**Source**: `path/to/file.log:line_number`
**Occurrence**: [count] times OR First seen at [timestamp]
**Error Message**:
```
[Full error message and stack trace verbatim]
```

**Context**: [What was happening when this error occurred]

**Root Cause**: [Deep analysis of why this happened]

**Impact**: [What functionality is affected, what breaks as a result]

**Potential Fixes**:
1. [Specific fix with code changes]
   ```typescript
   // Example fix in src/component.ts:42
   - const value = data.field
   + const value = data?.field ?? defaultValue
   ```
2. [Alternative approach if applicable]
3. **Related files**: `path/to/source.ts:line`, `path/to/config.json:line`

**Related Issues**: [Links to #Error2, #Error5 if connected]

---

### Error 2: [Next error with same structure]

[Continue for all critical errors...]

## Warnings & Non-Critical Issues

### Warning 1: [Category] - [Brief Description]

**Severity**: Warning / Info
**Source**: `path/to/file.log:line_number`
**Occurrence**: [count] times
**Message**: [Full warning message]
**Context**: [When this appears]
**Recommendation**: [What to do about it]

---

[Continue for all warnings...]

## Test Failures Summary

| Test Name | Failure Type | Source File | Reason | First Failed |
|-----------|--------------|-------------|--------|--------------|
| Login flow works | Assertion | auth.spec.ts:45 | Expected true, got false | 14:32:15 |
| Checkout process | Timeout | checkout.spec.ts:89 | Selector '.btn-pay' not found | 14:33:42 |

## Patterns & Observations

### Recurring Issues
- **[Pattern name]**: [Description of pattern, occurrence count, affected areas]
- **Example**: "Timeout errors in checkout tests" - Occurred 5 times across 3 test files, all involving payment button selector

### Timing Patterns
- **[Pattern name]**: [When errors occur, correlation with time]
- **Example**: "Database connection errors spike at 14:32" - All DB errors within 30-second window

### Environmental Factors
- **Operating System**: [OS version if detected]
- **Runtime Versions**: [Node.js, Python, etc. if detected]
- **Dependencies**: [Key dependency versions if mentioned]
- **Resource Constraints**: [Memory, disk, network issues if detected]

### Cascading Failures
- **[Failure chain]**: [How one error triggers others]
- **Example**: "TypeScript compilation error → Test imports fail → All tests skipped"

## Recommendations

### 1. Immediate Actions (Critical)
- **[Action 1]**: [What to fix immediately]
  - File: `path/to/file.ts:line`
  - Change: [Specific change needed]
- **[Action 2]**: [Next critical fix]

### 2. Code Changes
- **[Change 1]**: [Description]
  ```language
  // path/to/file.ext:line
  [Code snippet showing before/after]
  ```
- **[Change 2]**: [Description with file references]

### 3. Configuration Updates
- **[Config 1]**: Update `config/file.json`
  ```json
  {
    "setting": "new-value"
  }
  ```
- **[Config 2]**: Environment variables to set

### 4. Testing Improvements
- **[Improvement 1]**: [How to improve test stability]
- **[Improvement 2]**: [Coverage gaps to address]

### 5. Monitoring & Prevention
- **[Monitor 1]**: [What to watch for]
- **[Monitor 2]**: [Alerting to add]

## Appendix: File Contents Summary

### file1.log
- **Lines**: 1-500: Test initialization
- **Lines**: 501-1200: Test execution
- **Lines**: 1201-1300: Error output
- **Lines**: 1301-end: Cleanup and summary

### file2.log
- **Lines**: 1-100: Build configuration
- **Lines**: 101-800: Compilation output
- **Lines**: 801-end: Build summary

[Continue for each analyzed file...]
```

## Edge Cases and Special Handling

### Empty Logs or No Errors
If logs contain no errors:
```markdown
## Analysis Result

**Status**: ✓ No errors found

All analyzed logs show successful execution with no errors, warnings, or issues detected.

**Files Analyzed**: [list]
**Execution Summary**: [brief summary of what ran successfully]
```

### Truncated Logs
If logs appear truncated:
```markdown
**⚠️ LIMITATION**: File `name.log` appears truncated at line X.
Analysis covers available content only. Some errors may be missing.
```

### Missing Timestamps
If timestamps are not available:
```markdown
**Note**: Timestamps not available in these logs.
Chronological ordering cannot be established.
Issues listed by file and severity only.
```

### Unusual Formats
If log format is non-standard:
```markdown
**Log Format**: Custom/non-standard format detected.
**Parsing Approach**: [Describe how you adapted analysis]
**Confidence Level**: [High/Medium/Low based on format clarity]
```

### Multiple Runs in One Log
If single log contains multiple test runs:
```markdown
## Run Separation

**Run 1**: Lines 1-500 (Timestamp: 14:00-14:05)
**Run 2**: Lines 501-1000 (Timestamp: 14:30-14:35)
**Run 3**: Lines 1001-1500 (Timestamp: 15:00-15:05)

[Analyze each run separately in the report]
```

## File Reading Strategy for Large Logs

### Chunked Reading Approach

For files exceeding 2000 lines:

1. **First pass**: Read first 500 lines to understand format and metadata
2. **Error detection**: Use Grep to find error patterns:
   - `error|ERROR|Error|failed|FAILED|Failed`
   - `exception|Exception|EXCEPTION`
   - `fatal|FATAL|Fatal`
   - `timeout|Timeout|TIMEOUT`
3. **Targeted reading**: Read chunks around identified errors using offset/limit
4. **Context gathering**: Read ±10 lines around each error for context

Example sequence for a 10,000 line file:
```
1. Read lines 1-500 (metadata, format detection)
2. Grep for "error" patterns → finds matches at lines: 2341, 4567, 8923
3. Read lines 2331-2351 (error 1 + context)
4. Read lines 4557-4577 (error 2 + context)
5. Read lines 8913-8933 (error 3 + context)
6. Read last 100 lines (summary, final status)
```

### Tools for Different Scenarios

- **File discovery**: Use `Glob` tool with patterns
- **Size checking**: Use `Bash` with `ls -lh`
- **Small files (<2000 lines)**: Use `Read` tool once
- **Large files (>2000 lines)**: Use `Read` with offset/limit
- **Pattern matching**: Use `Grep` tool with `-A` and `-B` for context
- **Error counting**: Use `Grep` with count mode

## Issue Categories and Recognition Patterns

### Fatal Errors
**Patterns**: `FATAL`, `Fatal error`, `Uncaught exception`, `Segmentation fault`, `core dumped`
**Action**: Highest priority, analyze immediately

### Test Failures
**Patterns**: `FAIL`, `✗`, `❌`, `Expected X to be Y`, `AssertionError`, `Test failed`
**Action**: Catalog test name, file, assertion, and failure reason

### TypeScript/Compilation Errors
**Patterns**: `TS\d{4}:`, `error TS`, `Type 'X' is not assignable`, `Cannot find module`
**Action**: Extract error code, file:line, and type mismatch details

### Server Errors
**Patterns**: `HTTP 4xx`, `HTTP 5xx`, `ECONNREFUSED`, `ETIMEDOUT`, `Connection refused`
**Action**: Identify endpoint, status code, and request details

### Timeout Errors
**Patterns**: `timeout`, `TIMEOUT`, `exceeded`, `Waiting for selector`, `Navigation timeout`
**Action**: Identify operation, timeout duration, and selector/resource

### Deprecation Warnings
**Patterns**: `deprecated`, `DeprecationWarning`, `will be removed`, `use X instead`
**Action**: Note deprecated feature and recommended replacement

### Performance Warnings
**Patterns**: `slow query`, `memory usage`, `GC pause`, `heap size`, `took XXXXms`
**Action**: Capture metric, threshold, and affected operation

### Missing Dependencies
**Patterns**: `Cannot find module`, `ModuleNotFoundError`, `No module named`, `not found`
**Action**: Extract module name and where it's required

## Output Quality Checklist

Before finalizing `LOGS_ANALYSIS.md`, verify:

- [ ] All discovered log files have been analyzed
- [ ] Every error has full error message and stack trace included
- [ ] All critical errors have root cause analysis
- [ ] File:line references use backtick code format: `path/to/file.ts:42`
- [ ] Code suggestions use proper syntax highlighting
- [ ] Recommendations are specific and actionable
- [ ] Severity levels are assigned consistently
- [ ] Cross-file patterns are identified
- [ ] Executive summary is 2-3 sentences maximum
- [ ] Related issues are linked with clear references
- [ ] Table formatting is correct and readable
- [ ] Edge cases are documented if encountered
- [ ] File contents summary in appendix lists line ranges

## Success Criteria

The analysis is complete when:

1. ✅ All log files in target directory have been read completely
2. ✅ Every error, warning, and issue is documented with full context
3. ✅ Root cause analysis provided for each critical issue
4. ✅ Actionable fixes include specific file:line references
5. ✅ Cross-file patterns and cascading failures are identified
6. ✅ Issues are prioritized by severity and impact
7. ✅ `LOGS_ANALYSIS.md` is created in the target directory
8. ✅ Quality checklist is satisfied
9. ✅ User is informed of analysis completion and key findings

## Communication with User

### At Start
```
Starting log analysis...

📂 Discovered [N] log files in [directory]
📊 Total size: [size]
🔍 Beginning analysis...
```

### During Analysis
```
Analyzing [filename] ([X] of [N])...
- Found [Y] errors
- Found [Z] warnings
```

### At Completion
```
✅ Log analysis complete!

📋 Report saved to: LOGS_ANALYSIS.md

**Summary**:
- [N] files analyzed
- [X] critical errors found
- [Y] warnings identified
- [Z] test failures detected

**Top 3 Critical Issues**:
1. [Brief description] - [file:line]
2. [Brief description] - [file:line]
3. [Brief description] - [file:line]

Review the full report for detailed root cause analysis and fixes.
```

## Best Practices

1. **Be thorough**: Read every log file completely, don't skip files
2. **Extract verbatim**: Copy error messages exactly as they appear
3. **Provide context**: Always include surrounding lines for errors
4. **Cross-reference**: Link related errors across files
5. **Be specific**: Use exact file:line references, not vague descriptions
6. **Prioritize clearly**: Critical errors first, then warnings, then info
7. **Actionable fixes**: Provide concrete code changes, not generic advice
8. **Document limitations**: If logs are truncated or incomplete, say so
9. **Stay organized**: Follow the report template structure precisely
10. **Quality over speed**: Thorough analysis is more valuable than fast but incomplete analysis

## Notes

- The output directory is the same as the log directory by default
- User can specify a different output location if desired
- For very large sets of logs (>50 files), confirm with user before proceeding
- If multiple error types compete for attention, prioritize fatal/blocking errors
- Always preserve original error formatting and stack traces
- Use markdown formatting for readability in the report
