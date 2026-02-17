# Log Analysis Skill

A comprehensive log analysis skill that processes log files from test runs, CI/CD pipelines, application servers, and GitHub Actions, producing actionable diagnostic reports with root cause analysis and fixes.

## What It Does

This skill performs deep analysis of log files to:
- Identify all errors, warnings, and issues across multiple log types
- Provide root cause analysis with specific file:line references
- Generate actionable fixes with code changes where applicable
- Detect cross-file patterns and cascading failure chains
- Produce prioritized recommendations by severity and impact

## Supported Log Types

- **Test Execution**: Playwright, Jest, Vitest, pytest, Mocha
- **CI/CD Pipelines**: GitHub Actions, GitLab CI, Jenkins, CircleCI
- **Application Servers**: Node.js, Python, Java, Ruby, Go
- **Build/Compilation**: TypeScript, webpack, Vite, Rollup, esbuild
- **Deployment**: Docker, Kubernetes, cloud platform logs
- **Runtime Errors**: Crash dumps, exception logs, error logs

## When to Use

Use this skill when you need to:
- Debug test failures across multiple log files
- Investigate CI/CD pipeline failures
- Analyze build or compilation errors
- Understand cascading failures in distributed systems
- Get root cause analysis from application crashes
- Generate comprehensive diagnostic reports from logs

Automatically triggered when you:
- Ask to analyze logs in a directory
- Mention test failures, build errors, or CI/CD issues
- Request debugging help with log files
- Want to understand error patterns
- Provide paths to `.log`, `.txt`, `.out`, or `.err` files

## Output

The skill generates a `LOGS_ANALYSIS.md` report in the same directory as the logs (or a specified location) containing:

1. **Executive Summary**: High-level overview of findings
2. **Files Analyzed**: Table of all processed log files
3. **Critical Issues**: Detailed error analysis with:
   - Full error messages and stack traces
   - Root cause analysis
   - Impact assessment
   - Specific fixes with code snippets
   - File:line references
4. **Warnings**: Non-critical issues that need attention
5. **Test Failures Summary**: Organized table of failed tests
6. **Patterns & Observations**: Cross-file patterns, timing issues, cascading failures
7. **Recommendations**: Prioritized action items organized by urgency
8. **Appendix**: Summary of file contents and line ranges

## Key Features

### Comprehensive Coverage
- Analyzes ALL log files in a directory
- Handles logs of any size through chunked reading
- Processes multiple log formats and types
- Identifies errors, warnings, and performance issues

### Deep Analysis
- Extracts full error messages and stack traces
- Provides root cause inference, not just error listing
- Cross-references errors across multiple files
- Identifies cascading failure chains
- Detects timing and environmental patterns

### Actionable Output
- Specific file:line references for all issues
- Code fix suggestions with before/after examples
- Configuration changes with exact syntax
- Prioritized recommendations by severity
- Clear impact assessment for each issue

### Intelligent Handling
- Adapts to different log formats
- Handles truncated or incomplete logs
- Separates multiple runs within single logs
- Documents limitations when timestamps missing
- Provides context lines around each error

## Example Use Cases

### Debugging Failed GitHub Actions
```
Analyze logs from: .github/workflows/ci.yml run
→ Identifies: "npm ERR! code ERESOLVE" with dependency conflict details
→ Provides: Specific package.json changes to resolve conflict
```

### Understanding Playwright Test Failures
```
Analyze logs from: test-results/
→ Identifies: 5 timeout errors all related to '.btn-checkout' selector
→ Root cause: Selector changed in recent commit
→ Provides: Updated selector and test stabilization recommendations
```

### Investigating Build Failures
```
Analyze logs from: build.log
→ Identifies: TypeScript TS2345 type errors in 12 files
→ Root cause: API response type changed, interfaces not updated
→ Provides: Specific interface updates with file:line references
```

### Debugging Production Server Crashes
```
Analyze logs from: server-crash-2026-02-04.log
→ Identifies: Uncaught exception in /api/checkout endpoint
→ Root cause: Null reference when payment provider times out
→ Provides: Error handling code with try-catch implementation
```

## Technical Details

### Analysis Process
1. **File Discovery**: Uses Glob to find all log files matching patterns
2. **Size Assessment**: Checks file sizes with Bash, plans chunked reading for large files
3. **Sequential Analysis**: Reads each file, extracting errors, warnings, and context
4. **Pattern Detection**: Cross-references issues across files, identifies cascading failures
5. **Root Cause Analysis**: Infers why each error occurred, not just what failed
6. **Report Generation**: Creates comprehensive LOGS_ANALYSIS.md with all findings

### Handles Edge Cases
- **Empty logs**: Reports successful execution explicitly
- **Truncated logs**: Documents limitations and partial analysis
- **Missing timestamps**: Notes inability to establish chronology
- **Unusual formats**: Adapts analysis approach, documents confidence level
- **Multiple runs**: Separates and analyzes each run independently

### Large File Strategy
For files exceeding 2000 lines:
1. Reads first 500 lines for format detection
2. Uses Grep to locate error patterns
3. Reads targeted chunks around errors with context
4. Reads final lines for summary/status
5. Ensures complete coverage without loading entire file at once

## Structure

This skill consists of a single comprehensive `SKILL.md` file with:
- YAML frontmatter defining name and description
- Detailed workflow instructions for all analysis phases
- Issue recognition patterns for different log types
- Report template structure
- Edge case handling guidelines
- Quality checklist for output validation
- Best practices for thorough analysis

No additional scripts, references, or assets are needed - the skill uses Claude's native tools (Read, Glob, Grep, Bash) to perform all analysis tasks.

## Quality Standards

Every analysis must satisfy:
- ✅ All log files completely read and processed
- ✅ Every error documented with full context
- ✅ Root cause analysis for critical issues
- ✅ Specific file:line references in all recommendations
- ✅ Cross-file patterns identified
- ✅ Clear severity-based prioritization
- ✅ Actionable fixes with code examples
- ✅ Professional markdown formatting in output

## Usage Example

```
User: "Analyze the logs in test-results/ directory"

Claude (using log-analysis skill):
1. Discovers 8 log files (*.log, *.txt)
2. Analyzes each file sequentially
3. Identifies 12 errors, 5 warnings
4. Performs root cause analysis
5. Generates LOGS_ANALYSIS.md
6. Reports top 3 critical issues to user

Output: Comprehensive report with:
- All errors cataloged with stack traces
- Root causes identified
- Specific fixes provided
- Patterns across files noted
- Actionable recommendations prioritized
```

## Version

- **Created**: 2026-02-04
- **Status**: Production ready
- **Lines**: 502 (slightly over recommended 500, but justified by comprehensive coverage)

## License

This skill is part of the claude-mastermind skills repository.
