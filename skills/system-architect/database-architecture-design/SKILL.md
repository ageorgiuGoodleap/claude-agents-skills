---
name: database-architecture-design
description: |
  Design data architecture with database selection, data modeling, scaling, and operational strategies.
  Use when user asks to design data architecture, select databases, create data models, plan database
  scaling, design persistence layer, choose SQL vs NoSQL, plan sharding or replication, design caching
  strategies, create ER diagrams, plan backup and recovery, or design multi-database architectures.
allowed-tools: Read, Write, Edit
---

# Database Architecture Design

Design comprehensive data architectures with database selection, data modeling, scaling strategies, and operational considerations.

## Workflow

### 1. Analyze Data Requirements

Extract:
- **Entities and relationships** (users, orders, products; 1:1, 1:N, M:N)
- **Access patterns** (read/write ratio, query types, frequency, QPS)
- **Data volume** (current size, growth rate, retention)
- **Consistency needs** (strong for financials, eventual for feeds)
- **Compliance** (GDPR, HIPAA, data residency)

### 2. Select Database Technology

**Relational (SQL)**: Complex relationships, ACID transactions, ad-hoc queries, structured schema
- PostgreSQL (feature-rich), MySQL (widely supported)

**Document Store (NoSQL)**: Flexible schema, nested data, high writes, horizontal scaling
- MongoDB (general purpose), DynamoDB (AWS-native)

**Key-Value**: Simple lookups, sessions, caching, extreme throughput
- Redis (in-memory), DynamoDB (persistent)

**Wide-Column**: Time-series, massive scale, sparse data, write-heavy
- Cassandra (open source), ScyllaDB (performance)

**Graph**: Complex relationships, traversal queries, pattern matching
- Neo4j (mature), Amazon Neptune (managed)

**Time-Series**: Metrics, logs, IoT, temporal queries
- InfluxDB, TimescaleDB (PostgreSQL-based)

**Vector**: ML embeddings, semantic search, similarity matching
- Pinecone (managed), pgvector (PostgreSQL extension)

**Polyglot Persistence**: Use multiple database types for different data patterns.

### 3. Design Data Model

**For SQL**:
- Normalize to 3NF (denormalize selectively for performance)
- Define tables, primary keys, foreign keys
- Create indexes for query patterns (single-column, composite, covering, partial, full-text)
- Document denormalization decisions

**For NoSQL**:
- Design document structure optimized for access patterns
- **Embed** when: data accessed together, limited growth, strong ownership
- **Reference** when: data is large, shared across documents, independent lifecycle

### 4. Design Caching Strategy

**Layers**:
1. CDN Cache (CloudFront, Fastly) - static assets, API responses, hours-days TTL
2. Application Cache (Redis, Memcached) - sessions, computed data, minutes-hours TTL
3. Database Query Cache - complex aggregations

**Patterns**:
- **Cache-Aside**: Check cache → miss → query DB → store in cache
- **Write-Through**: Update DB → update cache immediately
- **Write-Behind**: Update cache → async DB update

**Invalidation**: TTL-based (simple, stale data), event-based (complex, always fresh), versioned (no invalidation)

### 5. Plan Partitioning and Sharding

**When to Shard**: Instance capacity reached, query performance degrades, vertical limits, regulatory requirements

**Strategies**:
- **Range-Based**: user_id 1-1M, 1M-2M (simple, but hotspots)
- **Hash-Based**: hash(user_id) % num_shards (even distribution, hard to rebalance)
- **Geographic**: by region (data residency, reduced latency, uneven sizes)
- **Directory-Based**: lookup table (flexible, but additional latency)

**Considerations**: Choose high-cardinality shard key, avoid cross-shard transactions, plan rebalancing

### 6. Design Replication Strategy

**Primary-Replica**: Read-heavy workloads (90%+ reads), eventual consistency, replica lag <1s
- Primary: writes + critical reads
- Replicas: non-critical reads

**Multi-Primary**: Multi-region with local writes, requires conflict resolution (last-write-wins, CRDTs)

**Replication Modes**:
- Synchronous: strong consistency, higher latency
- Asynchronous: eventual consistency, lower latency
- Semi-synchronous: wait for one replica (balanced)

### 7. Plan Backup and Disaster Recovery

**Backup Strategy**:
- Full: Daily, 30-day retention, cross-region replication, encrypted
- Incremental: Hourly, 7-day retention
- Point-in-Time Recovery: Transaction logs every 15 min, 7-day retention

**Recovery Metrics**:
- RTO (Recovery Time Objective): Max acceptable downtime
- RPO (Recovery Point Objective): Max acceptable data loss

### 8. Select Consistency Model

**Strong Consistency**: Every read sees latest write (financial, inventory, auth) - higher latency, lower availability

**Eventual Consistency**: Reads may be stale temporarily (feeds, analytics, catalogs) - lower latency, higher availability

**Causal**: Related operations maintain order (chat, collaboration)

**Session (Read Your Writes)**: User sees own writes (personalized apps) - sticky sessions

### 9. Design Index Strategy

**Types**:
- Primary key (automatic)
- Single-column (equality searches)
- Composite (multi-column queries, order matters)
- Covering (includes all query columns, no table lookup)
- Partial (filtered index for common subsets)
- Full-text (search queries)

**Guidelines**: Index WHERE clauses, JOINs, ORDER BY; avoid over-indexing (slows writes); monitor and remove unused

### 10. Estimate Storage and Costs

**Storage**: Rows × Avg Row Size × (1 + Index Overhead) × (1 + Growth Factor)

**Growth Projection**: Current Size × (1 + Annual Growth Rate) ^ Years

**IOPS**: (Reads/sec + Writes/sec) × 1.2 buffer

**Cost Components**: Instance/compute, storage (primary + backup), IOPS, data transfer, replicas

## Output Structure

Generate markdown document with:

### Executive Summary
- Primary database with justification
- Secondary stores if any
- Caching, replication, sharding strategies
- Storage projections and monthly cost
- RTO/RPO

### Requirements Analysis
- Entities, relationships, access patterns, volume, consistency needs, compliance

### Database Selection
- Comparison table of options with verdict and rationale

### Data Model
- ER diagram, schema definition (DDL for SQL or document examples for NoSQL), indexes

### Caching Architecture
- Cache layers with TTLs and invalidation strategy

### Partitioning and Sharding
- Strategy, shard key, distribution, cross-shard handling, rebalancing plan

### Replication Strategy
- Topology diagram, mode (sync/async), replica placement, failover, consistency level

### Backup and Disaster Recovery
- Backup schedule (full, incremental, PITR), RTO/RPO, recovery procedures, testing schedule

### Capacity Planning
- Storage projections (current, 6mo, 1yr, 2yr), scaling triggers, cost breakdown

### Monitoring and Alerting
- Key metrics (latency, throughput, resources, replication lag, errors), alert thresholds

### Migration Plan
- If replacing existing system: strategy, steps, validation, rollback

### Security
- Encryption (at rest, in transit), access control, network isolation, audit logging, secrets management

## Key Patterns

**Start with SQL**: Unless requirements clearly demand NoSQL (flexible schema, massive scale, specific access patterns)

**Polyglot Persistence**: SQL for transactions, Redis for cache, Elasticsearch for search, S3 for files

**Progressive Scaling**: Single instance → read replicas → caching → vertical scale → sharding (only when necessary)

**Denormalize Selectively**: Only for proven performance bottlenecks, document justification

## Critical Anti-Patterns

**Premature Sharding**: Shard only when vertical scaling and replicas exhausted

**NoSQL for Everything**: SQL has decades of tooling and expertise; use where it fits

**Over-Indexing**: Every index slows writes; add reactively based on query patterns

**Ignoring Consistency**: Strong consistency for money/inventory; eventual acceptable elsewhere

**No Cache Invalidation**: Stale data breaks UX; use TTL or event-based invalidation

**Single Region for Global Users**: Multi-region with geo-sharding or replicas reduces latency
