---
name: system-architecture-design
description: |
  Design system architectures with C4 diagrams, component specifications, and technology selection.
  Use when user asks to design system architecture, create architecture diagrams, select architectural
  patterns, define system components, choose technologies, design microservices or monoliths, create
  high-level design, document system structure, evaluate architectural trade-offs, or plan component interactions.
allowed-tools: Read, Write, Edit, Bash
---

# System Architecture Design

Design comprehensive system architectures with C4 model diagrams, component specifications, and justified technology selections.

## Workflow

### 1. Extract Requirements
Read requirements documents to identify:
- Functional requirements (features, use cases)
- Non-functional requirements (performance, scalability, availability, security, compliance)
- Constraints (budget, timeline, team skills, existing systems)
- Traffic projections (DAU, QPS, data volume, growth rate)
- Latency requirements and SLAs

### 2. Select Architectural Pattern

**Monolithic**: Small team (<5), simple domain, <1000 concurrent users, fast time-to-market

**Microservices**: Large team (>10), complex domain, different scaling per component, independent deployment

**Serverless**: Sporadic traffic, event-driven, minimal ops overhead, stateless workloads

**Event-Driven**: Loose coupling needed, async acceptable, audit trail required, eventual consistency

**CQRS**: Read/write patterns differ significantly, complex queries, event sourcing

### 3. Define Components

For each component document:
- Responsibility (single purpose)
- Exposed interfaces (REST, gRPC, events)
- Dependencies
- Data owned
- Technology choice with justification

Component boundaries: high cohesion, low coupling, domain-aligned, independently deployable.

### 4. Create C4 Diagrams

Generate Mermaid diagrams for three levels:

**Level 1 (Context)**: Show system and external dependencies (users, external systems)

**Level 2 (Container)**: Show major containers (web app, API, services, databases, caches)

**Level 3 (Component)**: Show components within key containers (for critical services only)

### 5. Document Critical Flows

Create sequence diagrams for key user journeys (authentication, checkout, data sync).

Document for each flow:
- Synchronous calls (REST, gRPC)
- Asynchronous events (pub/sub, queues)
- Error handling and retry logic
- Circuit breakers and fallbacks

### 6. Select and Justify Technologies

For each layer (frontend, backend, database, infrastructure), select technologies and document:
- Options considered (2-3 alternatives)
- Comparison (pros, cons, cost, complexity)
- Decision rationale (why this option fits requirements)

Use comparison tables:
| Option | Pros | Cons | Cost | Complexity | Verdict |
|--------|------|------|------|------------|---------|
| [Tech A] | - [Pro] | - [Con] | $ | Low | ✅ |
| [Tech B] | - [Pro] | - [Con] | $$ | Med | ❌ |

### 7. Validate Design

Before finalizing, verify:
- All functional requirements mapped to components
- Non-functional requirements (performance, scale, security) addressed
- Technology choices match team capabilities
- Component boundaries have high cohesion, low coupling
- No single points of failure (or mitigated)
- Error handling at all boundaries
- Security considerations covered

## Output Structure

Generate a markdown document with:

### Executive Summary
- Architectural pattern with rationale
- Key technologies (frontend, backend, database, infrastructure) with justification
- Scale projections (users, QPS, data growth)

### Architecture Diagrams
- C4 Level 1: Context diagram
- C4 Level 2: Container diagram
- C4 Level 3: Component diagrams for key containers

### Component Specifications
For each component: responsibility, technology, APIs, dependencies, data owned, scaling strategy

### Critical Flows
Sequence diagrams for key flows with error handling documented

### Technology Rationale
Comparison tables showing alternatives considered, decision, and reasoning

### Security & Monitoring
Authentication/authorization approach, encryption strategy, monitoring stack

### Implementation Considerations
Prerequisites, risks with mitigations, dependencies

Link to related ADRs if applicable.

## Key Patterns

**API Gateway + Microservices**: Multiple services, unified auth, independent scaling

**Modular Monolith**: Single deployment, module boundaries, simpler ops

**Event-Driven**: Loose coupling, async processing, event bus for communication

**CQRS**: Separate read/write models, optimized for different access patterns

**Legacy Integration**: Strangler fig pattern or anti-corruption layer to isolate legacy

## Critical Anti-Patterns to Avoid

**Distributed Monolith**: Microservices with tight coupling defeats the purpose

**Premature Microservices**: Small teams (<5) with simple domains start monolithic

**Shared Database**: Services sharing tables creates tight coupling; each service owns its data
