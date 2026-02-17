---
name: scalability-planning
description: |
  Analyze bottlenecks and design horizontal/vertical scaling strategies for system growth.
  Use when user asks about scalability planning, capacity planning, performance architecture, scaling
  strategies, bottleneck analysis, load distribution, horizontal/vertical scaling, auto-scaling design,
  capacity forecasting, handling growth, eliminating single points of failure, or database/cache scaling.
---

# Scalability Planning

Analyze bottlenecks, design scaling strategies, and plan capacity for projected growth.

## Workflow

### 1. Establish Current Baseline
Document:
- Traffic metrics (concurrent users, QPS by endpoint, peak vs average)
- Database QPS (read vs write)
- Data volume (storage size, growth rate)
- Response times (p50, p95, p99)
- Resource utilization (CPU, memory, network, disk I/O at average and peak)
- Current infrastructure (instance types, counts, database config, cache config)

### 2. Project Growth Targets
Define projections:
- User growth (monthly/annual DAU)
- Traffic growth (QPS, data volume)
- Performance SLAs (response time targets, availability targets)

Example: Current 10K DAU, 500 QPS, 100GB → 6mo: 30K DAU (3x), 1.5K QPS, 300GB → 12mo: 100K DAU (10x), 5K QPS, 1TB

### 3. Identify Bottlenecks

**Common Categories**:
- **Application**: CPU-bound ops, memory leaks, inefficient algorithms, blocking I/O, thread pool exhaustion
- **Database**: Slow queries (missing indexes), connection pool exhaustion, single primary writes, locks, replication lag
- **Network**: Bandwidth saturation, high latency (distance), DNS delays, load balancer limits
- **Storage**: IOPS limits, disk space exhaustion, slow storage (HDD vs SSD)

For each bottleneck document: Current limit, projected breach date, impact, severity, affected components.

### 4. Design Horizontal Scaling

**Application Servers**:
- Stateless design (sessions in Redis)
- Load balancer in front (round robin, least connections, IP hash, weighted)
- Auto-scaling: Min 2, max based on capacity, target CPU 70%, step scaling at 80/90%

**Database Read Scaling**: Add read replicas, route reads to replicas (writes to primary), accept eventual consistency (~1s lag)

**Database Write Scaling (Sharding)**: Partition data across instances, select shard key (user_id, region), implement routing, plan rebalancing.

### 5. Design Vertical Scaling

Upgrade instance size: t3.large (2 vCPU, 8GB) → t3.xlarge (4 vCPU, 16GB) → t3.2xlarge (8 vCPU, 32GB)

**When to Use**: Single-threaded workloads, resource-intensive per request, high IOPS database, simpler than horizontal initially

**Limitations**: Max instance size, downtime for resize (unless blue-green), cost increases linearly, single point of failure.

### 6. Design Caching Strategy

**Layers**:
1. **CDN** (CloudFront, Fastly): Static assets, API responses, hours-days TTL
2. **Application** (Redis, Memcached): Sessions, frequent data, computed aggregations, minutes-hours TTL
3. **Database Query Cache**: Complex aggregations

**Patterns**: Cache-Aside (check → miss → DB → store), Write-Through (DB → cache immediately), Write-Behind (cache → async DB)

**Cache Sizing**: Calculate working set (1M users × 1KB = 1GB) + 20-30% buffer

**Eviction**: LRU (least recently used), LFU (least frequently used), TTL (time to live)

### 7. Design Database Scaling

**Read Scaling**: Primary + read replicas (2-4), route analytics/reporting to replicas, replication lag <1s

**Write Scaling**: Vertical scale first, then consider sharding (range-based, hash-based, geographic, directory-based)

**Connection Pooling**: Min 10, max 50, idle timeout 300s, max lifetime 3600s

### 8. Design Content Delivery

**CDN Benefits**: Reduced latency (edge caching), reduced origin load (80-95% hit ratio), lower bandwidth costs, DDoS protection

**Configuration**: Origin (S3/ALB), cache TTLs (images 24hr, CSS/JS 1hr, API 5min), compression (gzip/brotli), edge locations based on users

### 9. Eliminate Single Points of Failure

- **Application**: Auto-scaling group with min 2 instances across AZs
- **Database**: Multi-AZ with automatic failover
- **Load Balancer**: Multi-AZ (managed service handles)
- **Cache**: Redis cluster with replication
- **Message Queue**: Cluster with mirrored queues
- **External Dependencies**: Fallback provider, circuit breaker, graceful degradation

### 10. Define Scaling Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| CPU | 70% | 85% | Scale up |
| Memory | 75% | 90% | Scale up |
| DB Connections | 70% | 90% | Increase pool or scale DB |
| Replication Lag | 5s | 30s | Add replica |
| Cache Hit Rate | <80% | <60% | Increase cache |
| API p95 Time | 500ms | 1000ms | Investigate + scale |
| Error Rate | 0.5% | 2% | Alert + investigate |
| Disk Usage | 75% | 90% | Add storage |

### 11. Create Capacity Forecast

For each component, document: Current (instances, capacity, load), 6-month projection (expected load, required capacity, recommended resources), 12-month projection.

### 12. Document Scaling Plan

Include: Baseline metrics, growth projections (6mo, 12mo), bottlenecks with severity, horizontal/vertical strategies, auto-scaling policies, database scaling (replicas/sharding), caching strategy, CDN config, SPOF mitigations, cost implications, implementation timeline.

## Key Patterns

**Application Auto-Scaling + Read Replicas**: Read-heavy apps with variable traffic (2-20 instances, primary + 2-4 replicas)

**Aggressive Caching + CDN**: Content-heavy apps (90%+ cache hit rate target)

**Database Sharding**: High write volume exceeding single DB (hash-based sharding, shard router)

**Multi-Region**: Global apps requiring low latency (deploy in multiple regions, global load balancer, cross-region replication)

## Critical Anti-Patterns

**Reactive Scaling**: Proactive scaling based on projections; maintain 2x headroom

**Premature Sharding**: Vertical scale → read replicas → caching → only then shard if writes exhausted

**Over-Provisioning 24/7**: Use auto-scaling to match demand

**Ignoring SPOF**: Implement multi-AZ deployments early

**No Load Testing**: Test after every change, simulate expected patterns
