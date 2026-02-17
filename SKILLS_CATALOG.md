# Skills Catalog

A comprehensive catalog of all skills available in the claude-agents-skills repository, organized by agent role.

## Table of Contents

- [Agent Skills](#agent-skills)
  - [Code Reviewer](#code-reviewer)
  - [DevOps Engineer](#devops-engineer)
  - [Product Architect](#product-architect)
  - [QA Engineer](#qa-engineer)
  - [Security Engineer](#security-engineer)
  - [System Architect](#system-architect)
- [General Purpose Skills](#general-purpose-skills)
- [Meta Skills](#meta-skills)

---

## Agent Skills

### Code Reviewer

**Agent Role**: Senior code quality enforcement specialist for pull requests, pre-merge checks, and coding standards.

**Agent Location**: `agents/code-reviewer.md`

#### Skills

##### 1. code-review
**Invoke**: `/code-review`

**Description**: Analyze pull requests, commits, and code changes to produce comprehensive CODE_REVIEW.md reports.

**Trigger Keywords**: review code, code review, PR review, pull request, pre-merge, approve PR, check code quality, quality check, code audit, analyze diffs, validate PRs, check correctness/security/performance, assess impact/blast radius, reviewing branches, commits, code changes

**Path**: `skills/code-reviewer/code-review/`

---

##### 2. code-quality-review
**Invoke**: `/code-quality-review`

**Description**: Comprehensive code quality analysis for readability, maintainability, and engineering principles including SOLID principles, DRY, KISS, code smells, naming conventions, code organization, and complexity.

**Trigger Keywords**: code review, review code, quality check, code quality, maintainability review, readability review, SOLID principles, code smells, refactoring review, technical debt

**Path**: `skills/code-reviewer/code-quality-review/`

---

##### 3. coding-standards
**Invoke**: `/coding-standards`

**Description**: Enforces clean code principles, language-specific best practices (Python/TypeScript), security baseline, and minimal-change workflow for all code-related tasks.

**Trigger Keywords**: writing code, implementing, fixing, updating, improving, refactoring, debugging, creating, building, developing, modifying code

**Path**: `skills/code-reviewer/coding-standards/`

---

##### 4. design-pattern-review
**Invoke**: `/design-pattern-review`

**Description**: Design pattern analysis for architectural consistency and appropriate abstraction levels. Reviews Factory, Strategy, Observer, Decorator, Adapter, Singleton patterns. Identifies over-engineering and under-engineering.

**Trigger Keywords**: design patterns, architecture review, pattern review, design review, structural review, refactoring patterns, over-engineering, under-engineering, architectural consistency

**Path**: `skills/code-reviewer/design-pattern-review/`

---

##### 5. feature-spec
**Invoke**: `/feature-spec`

**Description**: Analyzes codebase and generates detailed implementation specs from requirements.

**Trigger Keywords**: plan feature implementation, create technical specifications, create a spec for, plan the implementation of, analyze requirements for, spec out this feature

**Path**: `skills/code-reviewer/feature-spec/`

---

##### 6. performance-review
**Invoke**: `/performance-review`

**Description**: Performance impact analysis for algorithmic complexity, query efficiency, and resource usage. Analyzes O(n²) loops, N+1 problems, missing indexes, unnecessary computations, memory patterns.

**Trigger Keywords**: performance review, code performance, optimization review, efficiency review, algorithmic complexity, slow code, performance impact, bottleneck, N+1 query, inefficient loop, memory usage

**Path**: `skills/code-reviewer/performance-review/`

---

##### 7. security-review
**Invoke**: `/security-review`

**Description**: Security vulnerability analysis for OWASP Top 10 and common security issues including injection, broken authentication/authorization, sensitive data exposure, hardcoded secrets.

**Trigger Keywords**: security review, security check, vulnerability review, OWASP, injection, XSS, SQL injection, authentication, authorization, hardcoded secrets, sensitive data

**Path**: `skills/code-reviewer/security-review/`

---

##### 8. static-analysis-enforcement
**Invoke**: `/static-analysis-enforcement`

**Description**: Automated code quality enforcement through linters, formatters, type checkers, and static analysis platforms like ESLint, Pylint, Prettier, Black, mypy, SonarQube, CodeClimate.

**Trigger Keywords**: linting, static analysis, code analysis, run linter, ESLint, Pylint, Flake8, type checking, mypy, code formatting, Prettier, Black, SonarQube, CodeClimate, format code

**Path**: `skills/code-reviewer/static-analysis-enforcement/`

---

### DevOps Engineer

**Agent Role**: Senior DevOps Engineer specializing in CI/CD pipelines, container orchestration, infrastructure automation, monitoring, logging, and cloud deployments.

**Agent Location**: `agents/devops-engineer.md`

#### Skills

##### 1. cicd-pipeline-setup
**Invoke**: `/cicd-pipeline-setup`

**Description**: Create production-grade CI/CD pipelines with automated testing, multi-stage builds, and environment-specific deployments. Supports GitHub Actions, GitLab CI, Jenkins, CircleCI, Travis CI.

**Trigger Keywords**: CI/CD, GitHub Actions, GitLab CI, Jenkins, automated deployment, build pipeline, continuous integration, continuous deployment, deployment automation, release automation, setting up automated deployments, creating build pipelines

**Path**: `skills/devops-engineer/cicd-pipeline-setup/`

---

##### 2. container-orchestration
**Invoke**: `/container-orchestration`

**Description**: Create production-grade Docker containers and Kubernetes deployments with multi-stage builds, Helm charts, auto-scaling, and resource management.

**Trigger Keywords**: Docker, Kubernetes, K8s, containers, pods, deployments, services, ingress, Helm, containerize, orchestration, ECS, containerizing applications, creating Dockerfiles, deploying to Kubernetes, writing Helm charts

**Path**: `skills/devops-engineer/container-orchestration/`

---

##### 3. logging-infrastructure
**Invoke**: `/logging-infrastructure`

**Description**: Configure centralized logging infrastructure with ELK Stack (Elasticsearch, Logstash, Kibana), Loki, or CloudWatch with log forwarding, aggregation, parsing, filtering, retention policies.

**Trigger Keywords**: logging, ELK, Elasticsearch, Logstash, Kibana, Loki, Promtail, Fluentd, Fluent Bit, CloudWatch Logs, log aggregation, log management, structured logging, centralized logging, log forwarding

**Path**: `skills/devops-engineer/logging-infrastructure/`

---

##### 4. monitoring-and-alerting
**Invoke**: `/monitoring-and-alerting`

**Description**: Configure production-grade monitoring with Prometheus metrics collection, Grafana dashboards, alerting rules, and health checks with SLO/SLI tracking.

**Trigger Keywords**: monitoring, alerting, Prometheus, Grafana, metrics, observability, health checks, dashboards, SLO, SLI, APM, setting up monitoring, creating Grafana dashboards

**Path**: `skills/devops-engineer/monitoring-and-alerting/`

---

##### 5. secrets-management
**Invoke**: `/secrets-management`

**Description**: Implement production-grade secrets management using HashiCorp Vault, AWS Secrets Manager, Google Secret Manager, or Kubernetes secrets with rotation, access policies, encryption, audit logging.

**Trigger Keywords**: secrets, credentials, API keys, passwords, certificates, Vault, AWS Secrets Manager, secret rotation, secret injection, environment variables, secure configuration, managing API keys

**Path**: `skills/devops-engineer/secrets-management/`

---

##### 6. vercel-deployment
**Invoke**: `/vercel-deployment`

**Description**: Configure production-grade Vercel deployments for Next.js, React, and frontend applications with edge functions, ISR, environment variables, custom domains, multi-environment strategy.

**Trigger Keywords**: Vercel, Next.js deploy, edge functions, serverless functions, preview URLs, Vercel deployment, ISR, edge middleware, Vercel configuration, Vercel environment variables, deploying to Vercel

**Path**: `skills/devops-engineer/vercel-deployment/`

---

### Product Architect

**Agent Role**: Product strategy and requirements specialist who translates business needs into technical specifications.

**Agent Location**: `agents/product-architect.md`

#### Skills

##### 1. api-contract-design
**Invoke**: `/api-contract-design`

**Description**: Design OpenAPI/Swagger specifications, GraphQL schemas, and REST/gRPC API contracts with validation rules.

**Trigger Keywords**: API contract, OpenAPI, Swagger, REST API, GraphQL schema, endpoint design, API documentation, request/response schemas, authentication requirements, rate limits, designing API contracts, creating OpenAPI specs

**Path**: `skills/product-architect/api-contract-design/`

---

##### 2. product-roadmap-planning
**Invoke**: `/product-roadmap-planning`

**Description**: Prioritize features and create milestone-based product roadmaps with sprint breakdown and dependency mapping.

**Trigger Keywords**: roadmap, release planning, milestone planning, feature prioritization, sprint planning, product backlog, MoSCoW, RICE, Kano, critical path, dependencies, creating product roadmaps, planning releases

**Path**: `skills/product-architect/product-roadmap-planning/`

---

##### 3. requirements-gathering
**Invoke**: `/requirements-gathering`

**Description**: Extract and categorize functional and non-functional requirements from business goals and stakeholders.

**Trigger Keywords**: requirements gathering, scope definition, functional requirements, non-functional requirements, stakeholder analysis, acceptance criteria, gathering requirements, defining product scope, user needs analysis

**Path**: `skills/product-architect/requirements-gathering/`

---

##### 4. technical-specification-writing
**Invoke**: `/technical-specification-writing`

**Description**: Create comprehensive technical specifications with system boundaries, data models, API contracts, and integration points.

**Trigger Keywords**: technical spec, design document, system specification, data model, API contract, integration specification, error handling, edge cases, technical documentation, writing technical specs

**Path**: `skills/product-architect/technical-specification-writing/`

---

##### 5. user-story-creation
**Invoke**: `/user-story-creation`

**Description**: Generate user stories in standard format with acceptance criteria, story points, and dependencies.

**Trigger Keywords**: user stories, backlog, epic breakdown, story points, acceptance criteria, sprint planning, as a user, Given/When/Then, agile stories, writing user stories, creating backlog items

**Path**: `skills/product-architect/user-story-creation/`

---

### QA Engineer

**Agent Role**: Expert QA engineer specializing in comprehensive test strategy design and automated testing implementation across all layers.

**Agent Location**: `agents/qa-engineer.md`

#### Skills

##### 1. api-test-automation
**Invoke**: `/api-test-automation`

**Description**: Automates comprehensive API testing with request/response validation, authentication testing, schema validation, and contract verification for REST and GraphQL APIs.

**Trigger Keywords**: API testing, Postman collections, pytest API tests, validating endpoints, testing authentication flows, verifying response schemas, API test automation, testing APIs, creating Postman collections

**Path**: `skills/qa-engineer/api-test-automation/`

---

##### 2. e2e-test-implementation
**Invoke**: `/e2e-test-implementation`

**Description**: Build end-to-end test scenarios using Playwright that test complete user workflows through the browser with Page Object Model pattern.

**Trigger Keywords**: E2E tests, Playwright tests, Cypress tests, browser automation, user flow testing, UI testing, end-to-end testing, implementing E2E tests, testing critical paths

**Path**: `skills/qa-engineer/e2e-test-implementation/`

---

##### 3. integration-test-implementation
**Invoke**: `/integration-test-implementation`

**Description**: Create integration tests that verify API endpoints, database interactions, service communication, and inter-component behavior using Pytest or Jest.

**Trigger Keywords**: integration tests, API endpoint tests, database integration tests, contract tests, authentication flow tests, testing components working together, implementing integration tests

**Path**: `skills/qa-engineer/integration-test-implementation/`

---

##### 4. test-data-management
**Invoke**: `/test-data-management`

**Description**: Creates and manages test data infrastructure including factory classes, database seeding, mock data generation, and test fixtures using factory_boy, Faker, and builder patterns.

**Trigger Keywords**: test data, fixtures, seeding test databases, creating data factories, mock data generation, pytest fixtures, test setup/teardown, test data management, factory patterns, database seeding

**Path**: `skills/qa-engineer/test-data-management/`

---

##### 5. test-strategy-design
**Invoke**: `/test-strategy-design`

**Description**: Design comprehensive test strategies with test pyramids, coverage plans, automation roadmaps, risk assessments, and quality gates.

**Trigger Keywords**: test strategy, test plan, testing approach, QA strategy, test pyramid, quality plan, coverage requirements, automation roadmap, test planning, planning testing approach

**Path**: `skills/qa-engineer/test-strategy-design/`

---

##### 6. unit-test-implementation
**Invoke**: `/unit-test-implementation`

**Description**: Implement comprehensive unit tests with high coverage (80%+) using Pytest (Python) or Jest (JavaScript/TypeScript) with fixtures, mocks, and parameterized tests.

**Trigger Keywords**: unit test, test coverage, pytest, jest, mock, fixture, test functions, test methods, coverage report, writing unit tests, testing functions/classes, mocking external dependencies

**Path**: `skills/qa-engineer/unit-test-implementation/`

---

### Security Engineer

**Agent Role**: Security engineering specialist responsible for application security, vulnerability identification, and secure coding enforcement.

**Agent Location**: `agents/security-engineer.md`

#### Skills

##### 1. authentication-security
**Invoke**: `/authentication-security`

**Description**: Implements comprehensive authentication security covering password hashing (bcrypt, Argon2), JWT configuration, multi-factor authentication (MFA/2FA), OAuth2/OIDC integration, session management, rate limiting.

**Trigger Keywords**: authentication, password security, JWT tokens, MFA, 2FA, two-factor authentication, OAuth2, OIDC, session management, rate limiting, account lockout, brute force protection, token security, implementing authentication

**Path**: `skills/security-engineer/authentication-security/`

---

##### 2. compliance-auditing
**Invoke**: `/compliance-auditing`

**Description**: Conducts comprehensive compliance audits against regulatory frameworks (GDPR, SOC2, HIPAA, PCI-DSS) with gap analysis, remediation plans, and evidence documentation.

**Trigger Keywords**: compliance audit, GDPR compliance, SOC2, HIPAA, PCI-DSS, security compliance, audit preparation, compliance assessment, regulatory compliance, data protection compliance, privacy compliance, compliance framework, gap analysis

**Path**: `skills/security-engineer/compliance-auditing/`

---

##### 3. data-encryption
**Invoke**: `/data-encryption`

**Description**: Implements comprehensive data encryption strategies including TLS/SSL for data in transit, database encryption at rest, field-level encryption for sensitive data (PII, PHI, PCI), and secure key management with KMS/HSM.

**Trigger Keywords**: encryption, TLS setup, SSL, HTTPS, database encryption, field encryption, key management, KMS, HSM, certificate management, data protection, encrypting PII, PHI, PCI data, implementing encryption

**Path**: `skills/security-engineer/data-encryption/`

---

##### 4. secure-code-review
**Invoke**: `/secure-code-review`

**Description**: Performs expert security code review focusing on OWASP Top 10 vulnerabilities, input validation, cryptography, authentication/authorization, and hardcoded secrets with line-by-line analysis and remediation guidance.

**Trigger Keywords**: security code review, secure code audit, security patterns review, authentication review, authorization review, input validation review, cryptography review, secrets scan, reviewing code for security vulnerabilities

**Path**: `skills/security-engineer/secure-code-review/`

---

##### 5. security-architecture-design
**Invoke**: `/security-architecture-design`

**Description**: Design comprehensive security architectures following zero-trust principles with defense-in-depth strategies. Perform threat modeling using STRIDE and DREAD methodologies.

**Trigger Keywords**: security architecture, threat modeling, zero trust, defense in depth, STRIDE, DREAD, OAuth design, RBAC design, microservices security, security requirements, designing system security, creating threat models

**Path**: `skills/security-engineer/security-architecture-design/`

---

##### 6. vulnerability-assessment
**Invoke**: `/vulnerability-assessment`

**Description**: Perform comprehensive vulnerability scanning and assessment covering OWASP Top 10, static code analysis (SAST), dynamic testing, dependency vulnerabilities. Identify SQL injection, XSS, broken access control, insecure dependencies.

**Trigger Keywords**: vulnerability scan, security scan, OWASP scan, SQL injection, XSS, broken access control, dependency vulnerabilities, SAST, DAST, CVE scan, performing security scans, vulnerability assessments, penetration testing

**Path**: `skills/security-engineer/vulnerability-assessment/`

---

### System Architect

**Agent Role**: Expert system architect who designs scalable, maintainable software architectures and technical foundations.

**Agent Location**: `agents/system-architect.md`

#### Skills

##### 1. architecture-decision-records
**Invoke**: `/architecture-decision-records`

**Description**: Document architectural decisions with context, alternatives, and consequences using ADR format.

**Trigger Keywords**: document architecture decisions, create ADRs, record technical decisions, document design rationale, create decision records, document trade-offs, justify architectural choices, create ADR files, maintain decision logs

**Path**: `skills/system-architect/architecture-decision-records/`

---

##### 2. database-architecture-design
**Invoke**: `/database-architecture-design`

**Description**: Design data architecture with database selection, data modeling, scaling, and operational strategies.

**Trigger Keywords**: design data architecture, select databases, create data models, plan database scaling, design persistence layer, SQL vs NoSQL, sharding, replication, design caching strategies, ER diagrams, backup and recovery

**Path**: `skills/system-architect/database-architecture-design/`

---

##### 3. infrastructure-planning
**Invoke**: `/infrastructure-planning`

**Description**: Plan cloud infrastructure with compute, storage, networking, cost optimization, and IaC templates.

**Trigger Keywords**: design cloud infrastructure, plan infrastructure, select cloud resources, estimate infrastructure costs, create IaC templates, design network architecture, plan deployment infrastructure, select compute instances, storage strategy, high availability

**Path**: `skills/system-architect/infrastructure-planning/`

---

##### 4. integration-architecture
**Invoke**: `/integration-architecture`

**Description**: Design API contracts, event schemas, and integration patterns for system communication.

**Trigger Keywords**: design integration architecture, create API contracts, plan third-party integrations, design webhooks, event-driven architecture, message queues, REST/GraphQL/gRPC APIs, pub/sub patterns, saga patterns, API gateway architecture, circuit breakers

**Path**: `skills/system-architect/integration-architecture/`

---

##### 5. scalability-planning
**Invoke**: `/scalability-planning`

**Description**: Analyze bottlenecks and design horizontal/vertical scaling strategies for system growth.

**Trigger Keywords**: scalability planning, capacity planning, performance architecture, scaling strategies, bottleneck analysis, load distribution, horizontal/vertical scaling, auto-scaling design, capacity forecasting, handling growth, eliminating single points of failure

**Path**: `skills/system-architect/scalability-planning/`

---

##### 6. system-architecture-design
**Invoke**: `/system-architecture-design`

**Description**: Design system architectures with C4 diagrams, component specifications, and technology selection.

**Trigger Keywords**: design system architecture, create architecture diagrams, select architectural patterns, define system components, choose technologies, design microservices, monoliths, high-level design, document system structure, evaluate architectural trade-offs

**Path**: `skills/system-architect/system-architecture-design/`

---

## General Purpose Skills

These skills are available to all agents and can be used independently.

**Skills Location**: `skills/useful_skills/`

### 1. coding-documentation
**Invoke**: `/coding-documentation`

**Description**: Generates professional documentation artifacts from code diffs and changes including PR descriptions, changelog entries, README updates, API documentation, migration notes, ADRs, and runbooks.

**Trigger Keywords**: document the diff, create documentation, write PR description, generate changelog, document this change, create migration notes, code changes documentation

**Path**: `skills/useful_skills/coding-documentation/`

---

### 2. feature-spec
**Invoke**: `/feature-spec`

**Description**: Analyzes codebase and generates detailed implementation specs from requirements.

**Trigger Keywords**: plan feature implementation, create technical specifications, create a spec for, plan the implementation of, analyze requirements for, spec out this feature

**Path**: `skills/useful_skills/feature-spec/`

---

### 3. frontend-design
**Invoke**: `/frontend-design`

**Description**: Create distinctive, production-grade frontend interfaces with high design quality for websites, landing pages, dashboards, React components, HTML/CSS layouts.

**Trigger Keywords**: build web components, pages, artifacts, posters, applications, websites, landing pages, dashboards, React components, HTML/CSS layouts, styling/beautifying web UI

**Path**: `skills/useful_skills/frontend-design/`

---

### 4. jira-ticket-writer
**Invoke**: `/jira-ticket-writer`

**Description**: Generates comprehensive Jira ticket descriptions from task requirements and code analysis for stories, tasks, or issues.

**Trigger Keywords**: create a Jira ticket, write up this work, document this PR, generate a ticket, create Jira ticket, write Jira story, structured engineering task documentation

**Path**: `skills/useful_skills/jira-ticket-writer/`

---

### 5. log-analysis
**Invoke**: `/log-analysis`

**Description**: Analyzes log files from test runs, CI/CD pipelines, application servers, and GitHub Actions with root cause analysis and actionable fixes.

**Trigger Keywords**: analyzing logs, debugging test failures, investigating build failures, CI/CD errors, GitHub Actions issues, Playwright logs, diagnose errors from log files, *.log files, *.txt files, *.out files, *.err files

**Path**: `skills/useful_skills/log-analysis/`

---

### 6. pr-description
**Invoke**: `/pr-description`

**Description**: Generates comprehensive PR descriptions from git changes for GitHub/GitLab.

**Trigger Keywords**: create PR description, write pull request, generate PR summary, draft merge request description, documenting code changes for review, analyzing diffs, branches, commits for PR

**Path**: `skills/useful_skills/pr-description/`

---

### 7. prompt-upgrade
**Invoke**: `/prompt-upgrade`

**Description**: Improve and enhance prompts for Claude to be clearer, more specific, and more effective.

**Trigger Keywords**: upgrade this prompt, improve my prompt, refine prompt, make this prompt better, polish prompt, optimize prompt, enhance prompt quality

**Path**: `skills/useful_skills/prompt-upgrade/`

---

### 8. researched-code-implementation
**Invoke**: `/researched-code-implementation`

**Description**: Analyze comprehensive documentation (local files, URLs, codebase references) to understand implementation requirements and execute production-ready implementations.

**Trigger Keywords**: implement based on these docs, follow this specification, implement from documentation, implement based on API docs, implementation from specifications

**Path**: `skills/useful_skills/researched-code-implementation/`

---

### 9. security-best-practices
**Invoke**: `/security-best-practices`

**Description**: Perform language and framework-specific security reviews and write secure-by-default code. Supports Python (Django, Flask, FastAPI), JavaScript/TypeScript (React, Vue, Express, Next.js), and Go.

**Trigger Keywords**: security best practices, security review, vulnerability scan, security report, secure coding help (explicit security requests only)

**Path**: `skills/useful_skills/security-best-practices/`

---

### 10. slack-message
**Invoke**: `/slack-message`

**Description**: Generates human-sounding Slack/Teams messages from brief descriptions and reference materials for updates, questions, problems, requests, or announcements.

**Trigger Keywords**: draft a slack message, write a message for, create a team update, compose a slack announcement, team chat communication

**Path**: `skills/useful_skills/slack-message/`

---

### 11. task-implementation-log
**Invoke**: `/task-implementation-log`

**Description**: Generate detailed task implementation logs from Pull Requests and Jira tickets.

**Trigger Keywords**: create log, document a completed task, generate task summary, create a log, document this change, summarize this PR, generate implementation log

**Path**: `skills/useful_skills/task-implementation-log/`

---

### 12. web-research
**Invoke**: `/web-research`

**Description**: Perform comprehensive web research across multiple sources to gather current information, verify facts, and synthesize findings.

**Trigger Keywords**: web research, search, find information, what's the latest, real-time information, market research, competitive analysis, current statistics, trends

**Path**: `skills/useful_skills/web-research/`

---

## Meta Skills

Skills for creating and managing other skills.

**Skills Location**: `skills/skill-creator/`

### skill-creator
**Invoke**: `/skill-creator`

**Description**: Guide for creating effective skills that extend Claude's capabilities with specialized knowledge, workflows, or tool integrations.

**Trigger Keywords**: create a new skill, update an existing skill, skill creation, extend Claude's capabilities

**Path**: `skills/skill-creator/`

---

## Summary Statistics

| Category | Number of Skills |
|----------|-----------------|
| Code Reviewer | 8 |
| DevOps Engineer | 6 |
| Product Architect | 5 |
| QA Engineer | 6 |
| Security Engineer | 6 |
| System Architect | 6 |
| General Purpose | 12 |
| Meta Skills | 1 |
| **Total** | **50** |

---

## Usage Notes

1. **Invoking Skills**: Use the `/skill-name` format to invoke a skill (e.g., `/code-review`)
2. **Agent-Specific Skills**: Skills under agent sections are optimized for that agent's workflow
3. **General Purpose Skills**: Can be used by any agent or directly by users
4. **Trigger Keywords**: Keywords help Claude automatically suggest relevant skills
5. **Skill Paths**: Show the location of each skill's SKILL.md file in the repository

## Related Documentation

- [CLAUDE.md](./CLAUDE.md) - Repository overview and development guide
- [README.md](./README.md) - Repository introduction
- Agent definitions in `agents/` directory
- Individual skill documentation in `skills/` directories
