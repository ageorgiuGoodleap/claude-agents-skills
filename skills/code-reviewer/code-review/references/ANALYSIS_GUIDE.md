# Comprehensive Analysis Guide

This guide provides detailed methodology for analyzing code changes. Use this as a reference when performing thorough code reviews.

## Change Comprehension

### Structural Diff Parsing

**What to identify:**
- Lines added, removed, modified (with context)
- File moves, renames, permission changes
- Generated files (package-lock.json, dist/, vendor/, *.min.js)
- Method/function signature changes
- Whitespace-only and formatting changes

**How to analyze:**
```bash
# Get full diff with context
git diff -U10 <base>..<head>

# Show only modified files
git diff --name-status <base>..<head>

# Identify file moves
git diff --find-renames <base>..<head>

# Show function-level changes
git diff --function-context <base>..<head>
```

**Classification checklist:**
- [ ] All changed files identified
- [ ] Generated/vendored files marked
- [ ] Signature changes documented
- [ ] Structural changes vs logic changes separated

### Change Intent Classification

**Primary intents:**
- **Bug fix**: Corrects existing incorrect behavior
- **Feature**: Adds new functionality
- **Refactor**: Restructures without changing behavior
- **Performance**: Optimizes existing functionality
- **Security**: Addresses security concerns
- **Test**: Adds or modifies tests only
- **Config**: Changes configuration only

**Detection patterns:**
- Bug fix: Usually references issue/bug number, has "fix" in commit message
- Feature: Adds new files, classes, or public methods
- Refactor: Changes structure but preserves behavior, no test changes needed
- Performance: Has benchmarks, profiling, optimization comments
- Security: Addresses vulnerabilities, adds validation
- Test: Only modifies test files
- Config: Only changes config files, environment variables

**Scope creep indicators:**
- Unrelated formatting changes (whitespace, import ordering)
- Drive-by refactors ("while I was here" changes)
- Multiple unrelated features in one PR
- Test changes that don't relate to code changes
- Documentation updates unrelated to functionality

### Change Mapping

**Requirements alignment:**
1. Read PR description and linked issues
2. Map each code change to stated requirement
3. Identify gaps:
   - Requirements not implemented
   - Implementation without requirement
   - Behavior changes not documented

**Example mapping:**
```
Requirement: "Add user logout functionality"
Code changes:
✓ src/auth/logout.ts - implements logout endpoint
✓ src/auth/session.ts - adds session cleanup
✗ src/ui/header.tsx - adds random animation (scope creep)
? src/auth/login.ts - modifies login flow (undocumented change)
```

## Impact Analysis

### API Surface Impact

**What to check:**
- Public method signatures changed or removed
- Exported symbols (functions, classes, types)
- Database schema changes
- API contract changes (request/response formats)
- Configuration contract changes
- Feature flags added or modified
- Deprecations introduced

**Assessment template:**
```markdown
### API Changes
- **Breaking**: [List breaking changes with migration path]
- **Deprecated**: [List deprecations with sunset timeline]
- **New**: [List new public APIs with purpose]
- **Modified**: [List signature changes with rationale]
```

### Call Graph Impact

**Analysis steps:**
1. Identify all modified functions/methods
2. Find all callers (direct and transitive)
3. Check if callers' assumptions still hold
4. Identify new call edges introduced
5. Detect circular dependencies

**Tools and techniques:**
```bash
# Find function definition
grep -r "function functionName" .

# Find callers (simple)
grep -r "functionName(" .

# Find imports
grep -r "import.*functionName" .
```

**Questions to answer:**
- How many call sites are affected?
- Do callers handle new error conditions?
- Are new dependencies safe (no cycles)?
- Is dead code being removed safely?

### Data Flow Impact

**Trace data through:**
1. **Inputs**: Where does data enter the system?
   - User input (forms, API requests)
   - External APIs
   - Database reads
   - File reads
   - Environment variables

2. **Transformations**: How is data modified?
   - Parsing (JSON, XML, CSV)
   - Validation and sanitization
   - Business logic calculations
   - Formatting and encoding

3. **Outputs**: Where does data go?
   - Database writes
   - API responses
   - File writes
   - External API calls
   - Logs and metrics

**Validation checklist:**
- [ ] All inputs validated at boundary
- [ ] Transformations preserve data integrity
- [ ] Output format matches expectations
- [ ] Error states handled gracefully

### Behavioral Impact

**Invariants to check:**
- **Preconditions**: What must be true before function execution?
- **Postconditions**: What must be true after function execution?
- **Class invariants**: What must always be true for object state?

**Edge cases:**
- Null/undefined inputs
- Empty collections
- Boundary values (0, max int, negative numbers)
- Concurrent access
- Partial failures
- Timeout scenarios

**Concurrency analysis:**
- Thread safety maintained?
- Race conditions introduced?
- Deadlock potential?
- Atomic operations preserved?
- Idempotency maintained?

### Compatibility Impact

**Backward compatibility:**
- Can existing clients still function?
- Is old data format still readable?
- Are old API versions still supported?
- Can rollback happen safely?

**Migration requirements:**
- Data migration needed?
- Configuration migration needed?
- Client updates required?
- Deployment coordination required?

**Versioning strategy:**
- API versioning in place?
- Feature flags for gradual rollout?
- Blue-green deployment possible?
- Canary deployment suitable?

### Operational Impact

**Logging changes:**
- New log statements (frequency estimate)
- Log level appropriateness
- PII in logs?
- High-frequency loops with logging?

**Metrics changes:**
- New metrics introduced
- Label cardinality (avoid unbounded labels)
- High-frequency metric updates
- Metric retention implications

**Performance impact:**
- Latency changes (algorithm complexity)
- Throughput changes
- Memory footprint changes
- Database query count changes
- Cache hit rate changes

**Cost impact:**
- Additional API calls to paid services
- Database query volume increase
- Storage increase
- Compute resource increase

### Security Impact

**Trust boundaries:**
- New authentication checks?
- Authorization requirements?
- Input from untrusted sources?
- Output to trusted/untrusted destinations?

**Sensitive data:**
- PII handling (encryption at rest/transit)
- Secrets management
- Credential storage
- Data retention policies

**Vulnerability surface:**
- User input validation
- SQL injection potential
- XSS potential
- Path traversal potential
- SSRF potential
- Deserialization risks

## Flow and Control Analysis

### Control Flow Changes

**What to identify:**
- New conditional branches
- Early returns added/removed
- Exception handling changes
- Retry logic and backoff
- Timeout handling
- Circuit breakers
- Fallback mechanisms

**Review approach:**
1. Map all execution paths
2. Check each path reaches valid end state
3. Verify error paths are complete
4. Ensure cleanup happens on all paths

### State Machine Changes

**Completeness check:**
- All states enumerated?
- All valid transitions defined?
- Invalid transitions rejected?
- Initial state clearly defined?
- Terminal states reachable?

**Validation on transitions:**
- Preconditions checked?
- Postconditions ensured?
- State consistency maintained?
- Concurrent transitions handled?

### Concurrency Analysis

**Patterns to review:**
- Lock acquisition order (deadlock prevention)
- Lock scope (minimize critical sections)
- Async/await boundaries (promise chains)
- Shared mutable state access
- Atomic operation boundaries
- Memory visibility guarantees

**Common issues:**
- Race conditions (check-then-act)
- Lost updates (read-modify-write)
- Deadlocks (circular lock dependencies)
- Resource leaks (lock not released)

### Error Handling Flow

**Best practices:**
- Handle errors once at appropriate level
- Consistent error propagation (throw vs return)
- Error visibility (logging, metrics, user-facing)
- Recovery mechanisms (retry, fallback, circuit breaker)
- Cleanup on error paths (finally blocks, defer)
- Partial failure handling

**Anti-patterns:**
- Swallowing errors (empty catch blocks)
- Generic error handling (catch Exception)
- Error hiding (catching and not logging)
- Multiple error transformations (lost context)

### Resource Lifecycle

**Resources to track:**
- File handles (open/close)
- Network connections (connect/disconnect)
- Database connections (pooling, reuse)
- Memory allocations (prevent leaks)
- Locks and semaphores (acquire/release)
- Timers and intervals (start/stop)

**Patterns to enforce:**
- RAII (Resource Acquisition Is Initialization)
- try-with-resources / using statements
- Context managers (Python with statement)
- Defer/finally for cleanup
- Connection pooling for reuse
- Cancellation handling (cleanup on abort)

## Code Quality Assessment

### Complexity Metrics

**Cyclomatic complexity:**
- 1-10: Simple, easy to test
- 11-20: Moderate, needs attention
- 21-50: Complex, hard to test
- 50+: Very high risk, refactor recommended

**Nesting depth:**
- Prefer flat code (guard clauses, early returns)
- Max 3-4 levels of nesting
- Extract methods to reduce nesting

**Function size:**
- Prefer functions under 50 lines
- 50-100 lines: acceptable if cohesive
- 100+ lines: likely doing too much

### Local Reasoning

**Can you understand the function by reading it alone?**
- Dependencies explicit (parameters, not globals)
- Side effects minimized and clearly marked
- Input/output relationship clear
- No hidden coupling to external state

**Tests for local reasoning:**
- Could this function be extracted to a library?
- Can you test it without complex setup?
- Is behavior predictable from signature?

### Naming and Readability

**Naming principles:**
- Reveal intent clearly
- Use domain language
- Avoid abbreviations (unless standard: HTTP, URL, API)
- Boolean names are positive (isValid not isNotInvalid)
- Functions are verbs (calculateTotal, validateInput)
- Classes are nouns (User, PaymentProcessor)

**Readability checklist:**
- [ ] Names reveal intent
- [ ] Code reads like prose
- [ ] Complex logic has explanatory comments
- [ ] Magic numbers are named constants
- [ ] Similar concepts use consistent terms

### Duplication vs Abstraction

**When to tolerate duplication:**
- Code is simple and unlikely to change together
- Abstraction would obscure behavior
- Only 2 instances exist (wait for 3)

**When to create abstraction:**
- 3+ actual callers exist (not speculative)
- Abstraction has clear name and purpose
- Reduces cognitive load
- Behavior truly is identical

**Anti-patterns:**
- Premature abstraction (no actual reuse)
- Over-generalization (too many parameters)
- Wrong abstraction (similar code, different reasons to change)

## Test Review

### Coverage Adequacy

**Required coverage:**
- Happy path (primary use case)
- Error paths (validation failures, exceptions)
- Edge cases (null, empty, boundaries)
- Integration points (external services, database)

**Coverage assessment:**
- New functionality: Must have tests
- Modified functionality: Tests updated?
- Deleted functionality: Tests removed?
- Bug fixes: Regression test added?

### Test Quality

**Good test characteristics:**
- Deterministic (no flakiness)
- Fast (runs in milliseconds)
- Isolated (no shared state)
- Clear (arrange-act-assert structure)
- Focused (one behavior per test)
- Meaningful (would catch real bugs)

**Bad test characteristics:**
- Flaky (time-dependent, race conditions)
- Slow (network calls, database operations without mocks)
- Coupled (depends on other tests)
- Obscure (unclear what's being tested)
- Brittle (implementation-dependent assertions)
- Weak (would pass even with bugs)

### Test Code Smells

**Excessive mocking:**
- Mocking entire dependency graph
- Mocks verify implementation details
- More mock setup than actual test
- Mocks don't match real behavior

**Weak assertions:**
- Just checking no exception thrown
- Asserting on mock calls, not outcomes
- Too many assertions (testing multiple things)
- Too few assertions (not verifying behavior)

**Test structure issues:**
- Unclear arrange-act-assert sections
- Setup in test body instead of beforeEach
- Assertions in loops (hard to debug failures)
- Copy-paste tests with minor variations

### Changed Tests

**Questions to ask:**
- Why was the test changed?
- Does it still test the same behavior?
- Are assertions weaker than before?
- Was it changed just to make CI pass?

**Red flags:**
- Assertions removed or weakened
- Expected values changed without justification
- Mocks added where real objects existed
- Test skipped or marked as pending

## Best Practices Summary

### Do
- Read all code in full, not just diffs
- Understand context and architecture
- Follow execution flow
- Ask clarifying questions
- Provide concrete examples in feedback
- Prioritize correctness over style
- Suggest alternatives, not just criticisms
- Consider maintainability and extensibility

### Don't
- Comment on code you haven't read
- Focus on style already enforced by linters
- Bikeshed on subjective preferences
- Nitpick trivial changes
- Re-litigate architectural decisions
- Assume malice or incompetence
- Review generated code in detail
- Forget to acknowledge what's done well
