---
name: test-strategy-design
description: |
  Design comprehensive test strategies with test pyramids, coverage plans, automation roadmaps, risk assessments, and quality gates. Use when planning testing approach, creating test strategy documents, defining coverage requirements, setting up QA processes, planning test automation, or when user mentions "test strategy", "test plan", "testing approach", "QA strategy", "test pyramid", "quality plan", "coverage requirements", "automation roadmap", or "test planning".
---

# Test Strategy Design

Design production-grade test strategies that balance coverage, automation, and resource constraints. This skill helps create test pyramids, define coverage requirements, plan automation roadmaps, establish quality gates, and assess testing risks.

## Output Location

Save all test strategy documents and artifacts to:
```
~/Documents/claude-code-skills-data/test-strategy-design/
```

## When to Use This Skill

Use this skill when:
- Starting a new project and need to plan the testing approach
- Existing project lacks structured testing strategy
- Need to improve test coverage systematically
- Planning test automation implementation
- Defining quality gates for CI/CD
- Assessing testing risks and priorities
- Creating test strategy documentation

## Core Capabilities

### 1. Test Pyramid Design

Design optimal test distribution across layers:

**Standard Test Pyramid:**
- **Unit Tests (70%)**: Fast, isolated tests of individual functions/classes
- **Integration Tests (20%)**: Tests of component interactions and APIs
- **E2E Tests (10%)**: Browser-based tests of critical user workflows

**Adjust ratios based on project type:**

| Project Type | Unit | Integration | E2E | Rationale |
|--------------|------|-------------|-----|-----------|
| Backend API | 75% | 20% | 5% | Focus on business logic and API contracts |
| Frontend SPA | 60% | 25% | 15% | More E2E for UI workflows |
| Microservices | 70% | 25% | 5% | Heavy integration testing for service contracts |
| Monolith | 70% | 20% | 10% | Balanced pyramid |

### 2. Coverage Requirements

Define coverage targets per layer with justification:

**Coverage Levels by Risk:**
- **Critical paths** (auth, payments, data loss): 100% coverage
- **Core business logic**: 90-95% coverage
- **Standard features**: 80-85% coverage
- **Utility functions**: 75-80% coverage
- **UI components**: 70-75% coverage

**Coverage Metrics:**
- **Line coverage**: Percentage of code lines executed
- **Branch coverage**: Percentage of decision branches tested
- **Function coverage**: Percentage of functions called
- **Integration coverage**: Percentage of API endpoints tested
- **E2E coverage**: Percentage of critical user flows tested

### 3. Risk Assessment

Identify and prioritize high-risk areas:

**Risk Categories:**

| Risk Level | Examples | Testing Approach |
|------------|----------|------------------|
| **Critical** | Authentication, payments, data deletion, security | 100% coverage, multiple test types, manual testing |
| **High** | Core business logic, data processing, integrations | 90%+ coverage, integration tests, E2E tests |
| **Medium** | Standard CRUD, UI components, utilities | 80%+ coverage, unit + integration tests |
| **Low** | Display logic, formatting, simple getters | 70%+ coverage, unit tests |

**Risk Assessment Questions:**
- What functionality could cause data loss?
- What failures would block users completely?
- What areas handle sensitive data (PII, payments)?
- What integrations are critical to business operations?
- What features have high usage/visibility?
- What code is complex or hard to understand?

### 4. Automation Roadmap

Plan phased test automation implementation:

**Phase 1: Foundation (Weeks 1-2)**
- Set up testing frameworks (Pytest, Jest, Playwright)
- Configure test environments (test DB, mock services)
- Create initial test data infrastructure
- Implement first unit tests for core modules
- Set up CI/CD test execution

**Phase 2: Core Coverage (Weeks 3-6)**
- Achieve 80% unit test coverage
- Implement integration tests for all API endpoints
- Create E2E tests for top 3 critical user flows
- Build test data factories and fixtures
- Generate coverage reports

**Phase 3: Comprehensive Testing (Weeks 7-10)**
- Reach 85-90% overall coverage
- Add E2E tests for remaining critical paths
- Implement contract tests for service boundaries
- Add performance/load testing for bottlenecks
- Set up automated regression testing

**Phase 4: Optimization (Ongoing)**
- Optimize slow tests
- Reduce flaky tests
- Improve test maintainability
- Expand E2E coverage for new features
- Continuously update test data

### 5. Test Data Strategy

Plan test data creation, management, and cleanup:

**Factory Pattern:**
- Create factory classes for each entity
- Generate realistic data with Faker
- Support relationships and dependencies
- Allow overrides for specific scenarios

**Database Seeding:**
- Seed baseline reference data (countries, categories)
- Create test users with different roles
- Populate minimal representative data
- Support clean slate reset

**Setup/Teardown:**
- Setup fixtures before each test
- Use database transactions for isolation
- Clean up test data after tests
- Ensure tests are independent

**Data Isolation:**
- Separate test database from development
- Use unique identifiers per test run
- Avoid shared test data across tests
- Use in-memory databases for speed when possible

### 6. Quality Gates

Define pass/fail criteria for releases:

**Mandatory Quality Gates:**
- [ ] All critical path tests passing (100%)
- [ ] Minimum coverage achieved (e.g., 85% overall)
- [ ] No high-severity bugs open
- [ ] All security tests passing
- [ ] Performance benchmarks met
- [ ] No flaky tests in CI/CD (max 1% flake rate)

**Metrics to Track:**
- Overall test pass rate (target: 98%+)
- Coverage percentage by layer
- Test execution time (keep under X minutes)
- Defect escape rate (bugs found in production)
- Test reliability (flake rate)
- Time to execute full test suite

## Workflow

Follow this workflow when designing a test strategy:

### Step 1: Analyze System Architecture

1. **Review codebase structure:**
   - Identify major components/modules
   - Map dependencies and integration points
   - Understand data flow

2. **Identify test boundaries:**
   - Unit boundaries: Individual functions/classes
   - Integration boundaries: API endpoints, database, services
   - E2E boundaries: Complete user workflows

3. **Assess technical constraints:**
   - Existing test infrastructure
   - Team testing expertise
   - Available testing tools
   - CI/CD pipeline capabilities

### Step 2: Map Critical Flows

1. **List all user workflows:**
   - User registration and onboarding
   - Authentication (login, password reset)
   - Core feature usage
   - Checkout/payment flows
   - Admin operations

2. **Prioritize by business impact:**
   - Revenue-generating flows (highest priority)
   - Security-sensitive operations
   - High-traffic features
   - Data modification operations

3. **Identify integration points:**
   - External API calls
   - Database operations
   - Third-party services
   - Inter-service communication

### Step 3: Assess Risks

1. **Technical risks:**
   - Complex algorithms
   - Concurrent operations
   - Data transformations
   - Performance bottlenecks

2. **Business risks:**
   - Financial transactions
   - User data handling
   - Compliance requirements
   - Customer-facing features

3. **Create risk matrix:**
   See [risk_assessment.md](references/risk_assessment.md) for template

### Step 4: Design Test Pyramid

1. **Determine appropriate ratios:**
   - Based on project type (API, frontend, microservices)
   - Based on team expertise
   - Based on existing test suite

2. **Define coverage targets per layer:**
   - Unit: X% line coverage
   - Integration: All endpoints + key interactions
   - E2E: All critical paths (top 10 flows)

3. **Document rationale:**
   - Why these ratios?
   - What trade-offs were considered?
   - How will this evolve over time?

### Step 5: Create Automation Roadmap

1. **Phase 1 scope:**
   - Quick wins (easy, high-value tests)
   - Foundation setup
   - Initial coverage targets

2. **Phase 2 scope:**
   - Expand coverage
   - Add integration tests
   - Create test infrastructure

3. **Phase 3+ scope:**
   - Comprehensive coverage
   - Advanced testing (performance, security)
   - Optimization and maintenance

4. **Define milestones:**
   - Measurable goals per phase
   - Timeline estimates
   - Success criteria

### Step 6: Plan Test Data

1. **Identify data needs:**
   - What entities are tested?
   - What relationships exist?
   - What edge cases need data?

2. **Choose data generation approach:**
   - Factories (factory_boy, FactoryBoy)
   - Fixtures (JSON files, YAML)
   - Database seeding scripts
   - Mock data generation (Faker)

3. **Plan data management:**
   - How is data created before tests?
   - How is data cleaned up after tests?
   - How to ensure data isolation?

### Step 7: Set Quality Gates

1. **Define mandatory criteria:**
   - Minimum coverage percentages
   - Required test types
   - Performance thresholds

2. **Set pass/fail thresholds:**
   - Test pass rate (e.g., 98%)
   - Max allowed flaky tests
   - Max regression duration

3. **Document consequences:**
   - Block merges/releases on failure
   - Require manual approval for exceptions
   - Escalation process

### Step 8: Document Strategy

1. **Create strategy document:**
   - Use template from [strategy_template.md](references/strategy_template.md)
   - Include all sections (pyramid, risks, roadmap, etc.)
   - Add diagrams and tables

2. **Review with stakeholders:**
   - Developers (feasibility)
   - Product (coverage of critical features)
   - DevOps (CI/CD integration)
   - Management (timeline and resources)

3. **Iterate based on feedback:**
   - Adjust coverage targets
   - Revise timeline
   - Clarify requirements

## Output Format

Generate a comprehensive test strategy document using this structure:

```markdown
# Test Strategy: [Project Name]

## Executive Summary
- **Project:** [Name and description]
- **Test Approach:** [Pyramid-based, risk-focused, etc.]
- **Coverage Targets:** Unit X%, Integration Y%, E2E Z%
- **Timeline:** [X weeks/months]
- **Key Risks:** [Top 3-5 risk areas]

## Test Pyramid

### Distribution
- **Unit Tests (70%)**: Test individual functions and classes in isolation
- **Integration Tests (20%)**: Test API endpoints and component interactions
- **E2E Tests (10%)**: Test critical user workflows through the browser

### Rationale
[Explain why these ratios fit this project]

### Coverage Targets
| Layer | Target | Scope |
|-------|--------|-------|
| Unit | 85% | All business logic, utilities, services |
| Integration | 100% | All API endpoints, database operations |
| E2E | 100% | Top 10 critical user paths |

## Critical User Flows

### Priority 1: Must Test (Revenue/Security Impact)
1. **User Registration & Authentication**
   - Sign up flow
   - Login/logout
   - Password reset
   - Coverage: Unit + Integration + E2E

2. **Payment Processing**
   - Add payment method
   - Complete purchase
   - Refund processing
   - Coverage: Unit + Integration + E2E

### Priority 2: Should Test (High Usage)
[List additional important flows]

### Priority 3: Nice to Test (Standard Features)
[List standard features]

## Risk Assessment

| Risk Area | Level | Impact | Testing Approach |
|-----------|-------|--------|------------------|
| Authentication | Critical | Complete system lockout | 100% coverage, security tests, manual testing |
| Payment Processing | Critical | Financial loss, compliance | 100% coverage, integration tests, E2E tests |
| Data Export | High | Data corruption | 90% coverage, integration tests |

## Automation Roadmap

### Phase 1: Foundation (Weeks 1-2)
**Goals:**
- Set up testing frameworks
- Configure test environments
- Implement first 20 unit tests

**Deliverables:**
- [ ] Testing frameworks configured
- [ ] CI/CD test execution working
- [ ] 20+ unit tests passing

### Phase 2: Core Coverage (Weeks 3-6)
**Goals:**
- Achieve 80% unit test coverage
- Test all API endpoints
- Implement E2E tests for top 3 flows

### Phase 3: Comprehensive Testing (Weeks 7-10)
**Goals:**
- Reach 85-90% overall coverage
- Complete E2E tests for all critical paths

## Test Data Strategy

### Approach: Factory Pattern + Database Seeding

**Data Generation:**
- Use factory_boy (Python) / FactoryBoy (JS)
- Use Faker for realistic data

**Data Isolation:**
- Use database transactions
- Each test creates its own data
- Teardown cleans up all test data

## Tool Selection

- **Unit Testing**: Pytest (Python), Jest (JavaScript)
- **Integration Testing**: Pytest + requests
- **E2E Testing**: Playwright
- **Test Data**: factory_boy, Faker

## Quality Gates

### Mandatory (Block Merge/Release)
- [ ] All critical path tests passing (100%)
- [ ] Minimum 85% overall coverage
- [ ] No high-severity open bugs

### Metrics Dashboard
- Test pass rate: 98%+ (target)
- Overall coverage: 85%+ (target)
- Execution time: <10min (target)
```

## Quality Checklist

Before finalizing the test strategy, verify:

- [ ] Test pyramid ratios justified for this project type
- [ ] Coverage targets defined for each layer
- [ ] Critical user flows identified and prioritized
- [ ] Risk assessment complete with mitigation plans
- [ ] Automation roadmap has clear phases and milestones
- [ ] Test data strategy addresses creation, isolation, and cleanup
- [ ] Quality gates defined with measurable criteria
- [ ] Tool selection justified with rationale
- [ ] Timeline is realistic given team size and constraints
- [ ] Stakeholders have reviewed and approved strategy

## Tips for Success

**Start Small, Iterate:**
- Don't try to achieve 100% coverage immediately
- Focus on critical paths first
- Build foundation, then expand

**Measure and Adjust:**
- Track metrics from day one
- Review coverage weekly
- Adjust strategy based on what's working

**Get Buy-In:**
- Involve developers in strategy design
- Demonstrate value early (catch bugs)
- Celebrate coverage milestones

**Keep Tests Fast:**
- Unit tests should be <1s each
- Full suite should be <10min
- Optimize slow tests proactively

## Common Pitfalls to Avoid

1. **Over-investing in E2E tests**: E2E tests are slow and brittle. Keep them to <15% of total tests.

2. **Ignoring test maintenance**: Tests require ongoing maintenance as code evolves.

3. **Achieving coverage without quality**: 90% coverage with bad tests is worse than 70% with good tests.

4. **No test data strategy**: Poor test data leads to flaky tests and hard-to-understand failures.

5. **Setting unrealistic timelines**: Comprehensive test automation takes time.

6. **Not involving developers**: Developers write most unit tests. They must be part of the strategy.

7. **Forgetting about test execution time**: A 2-hour test suite will block productivity.

## Reference Material

For detailed templates and examples, see:
- [Test Strategy Template](references/strategy_template.md)
- [Risk Assessment Matrix](references/risk_assessment.md)
- [Automation Roadmap Examples](references/roadmap_examples.md)
