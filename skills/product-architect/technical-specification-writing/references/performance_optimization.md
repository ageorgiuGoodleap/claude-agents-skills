# Performance Optimization Guide

Detailed performance patterns, targets, and optimization strategies.

## Latency Targets (95th Percentile, Normal Load)

| Endpoint | Target | Measurement |
|----------|--------|-------------|
| POST /auth/register | < 500ms | Time to return 201 |
| POST /auth/login | < 200ms | Time to return session token |
| GET /auth/me | < 100ms | Time to return user profile |
| POST /auth/logout | < 100ms | Time to delete session |
| PUT /users/profile | < 150ms | Time to update and return |

**Load Definition:**
- Normal: 100 concurrent users, 1000 req/min
- Peak: 500 concurrent users, 5000 req/min
- Spike: 1000 concurrent users, 10,000 req/min

---

## Throughput Targets

| Operation | Sustained | Peak | Notes |
|-----------|-----------|------|-------|
| Registration | 100 req/min | 500 req/min | Batch email sending |
| Login | 1000 req/min | 5000 req/min | High frequency |
| Session validation | 10,000 req/min | 50,000 req/min | Every API call |
| Profile updates | 200 req/min | 1000 req/min | Less frequent |

---

## Database Query Performance

### Query SLAs

- User lookup by email: < 10ms (indexed)
- Session validation by token: < 5ms (indexed)
- Profile fetch with user: < 10ms (single join)
- List user sessions: < 15ms (indexed on user_id)

### Optimization Strategies

```sql
-- Use EXPLAIN ANALYZE to verify index usage
EXPLAIN ANALYZE
SELECT u.*, p.*
FROM users u
LEFT JOIN profiles p ON p.user_id = u.id
WHERE u.email = 'user@example.com';

-- Expected: Index Scan using idx_users_email
-- Actual rows: 1
-- Execution time: < 10ms
```

### Connection Pooling

- Pool size: 20 connections (2x CPU cores)
- Max wait time: 5 seconds
- Idle timeout: 10 minutes
- Validation query: `SELECT 1`

---

## Caching Strategy

### Cache Architecture

```
┌─────────┐    ┌───────┐    ┌──────────┐
│  Client │───▶│ Redis │───▶│ Database │
└─────────┘    └───────┘    └──────────┘
            Cache Miss
```

### What to Cache

| Data | Cache Key | TTL | Invalidation |
|------|-----------|-----|--------------|
| Session validation | `session:{token}` | Session expiry | On logout |
| User profile | `user:profile:{user_id}` | 5 minutes | On profile update |
| Email verification status | `email:verified:{email}` | 1 hour | On verification |
| Rate limit counters | `rate_limit:{ip}:{endpoint}` | 1 hour | TTL expiry |

### Cache Implementation

```python
def get_user_profile(user_id):
    cache_key = f"user:profile:{user_id}"
    cached = redis.get(cache_key)

    if cached:
        return json.loads(cached)

    # Cache miss - fetch from database
    profile = db.query("SELECT * FROM users WHERE id = ?", user_id)
    redis.setex(cache_key, 300, json.dumps(profile))  # 5-minute TTL
    return profile

def invalidate_user_profile_cache(user_id):
    cache_key = f"user:profile:{user_id}"
    redis.delete(cache_key)
```

### Cache Invalidation Strategy

- Write-through: Update database then invalidate cache
- Never use write-back (risk of data loss)
- TTL as fallback: Even if invalidation fails, cache expires eventually

---

## Scalability Plan

### Horizontal Scaling

- Load balancer: AWS ALB with round-robin distribution
- Auto-scaling: 2-10 API server instances based on CPU (target: 70%)
- Session affinity: Not required (stateless API)

### Database Scaling

- Read replicas: 2 replicas for session validation
- Write operations: Primary only
- Connection routing:
  - Writes → Primary
  - Session validation → Replicas (eventual consistency acceptable)
  - User profile reads → Replicas

### Cache Scaling

- Redis cluster: 3 nodes with replication
- High availability: Automatic failover
- Eviction policy: LRU (least recently used)

---

## Resource Optimization

### API Server

- Runtime: Node.js 20 LTS with async/await
- CPU: 2 vCPUs per instance
- Memory: 4 GB per instance
- Expected: 1000 req/min per instance

### Database

- Instance: AWS RDS PostgreSQL (db.t3.medium)
- CPU: 2 vCPUs
- Memory: 4 GB
- Storage: 100 GB SSD (provisioned IOPS)
- Expected: 5000 queries/min

### Cache

- Instance: AWS ElastiCache Redis (cache.t3.medium)
- Memory: 3.09 GB
- Expected: 50,000 operations/min

---

## Performance Testing Plan

### Load Testing Scenarios

**1. Baseline Test**
- 100 concurrent users, 5-minute duration
- Verify all endpoints meet latency targets

**2. Peak Load Test**
- 500 concurrent users, 10-minute duration
- Verify throughput targets
- Monitor error rate (< 0.1%)

**3. Spike Test**
- Ramp from 100 to 1000 users in 1 minute
- Verify auto-scaling triggers
- Verify graceful degradation (no 500 errors)

**4. Soak Test**
- 100 concurrent users, 24-hour duration
- Verify no memory leaks
- Verify no connection pool exhaustion

### Performance Monitoring

**Metrics:** Response time (p50, p95, p99), throughput, error rate

**Alerts:**
- p95 latency > 2x target for 5 minutes
- Error rate > 1% for 5 minutes
- Database CPU > 80% for 5 minutes
- Cache eviction rate > 100/min

---

## Optimization Patterns

### Pattern 1: N+1 Query Problem

**Problem:**
```python
# Fetches users, then queries database for each user's profile
users = db.query("SELECT * FROM users")
for user in users:
    profile = db.query("SELECT * FROM profiles WHERE user_id = ?", user.id)
```

**Solution:**
```python
# Single query with JOIN
results = db.query("""
    SELECT u.*, p.*
    FROM users u
    LEFT JOIN profiles p ON p.user_id = u.id
""")
```

### Pattern 2: Eager Loading

**Problem:** Loading all data when only subset needed

**Solution:**
```python
# Only select fields actually used
db.query("SELECT id, email, name FROM users")

# Not this
db.query("SELECT * FROM users")  # Fetches all columns
```

### Pattern 3: Pagination

**Problem:** Loading thousands of records at once

**Solution:**
```python
# Cursor-based pagination for performance
def get_users(cursor=None, limit=20):
    query = "SELECT * FROM users WHERE id > ? ORDER BY id LIMIT ?"
    return db.query(query, cursor or 0, limit)
```

### Pattern 4: Database Indexing

**Problem:** Slow queries on unindexed columns

**Solution:**
```sql
-- Index columns used in WHERE, JOIN, ORDER BY
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

### Pattern 5: Batch Operations

**Problem:** Individual database writes in loop

**Solution:**
```python
# Batch insert instead of loop
db.execute_many(
    "INSERT INTO users (email, name) VALUES (?, ?)",
    [(email, name) for email, name in users_to_create]
)
```

---

## Performance Checklist

- [ ] All database queries have appropriate indexes
- [ ] N+1 queries eliminated
- [ ] Caching strategy defined with TTLs
- [ ] Connection pooling configured
- [ ] Pagination implemented for list endpoints
- [ ] Load testing plan documented
- [ ] Performance targets measurable
- [ ] Monitoring and alerts configured
- [ ] Resource sizing justified
- [ ] Scalability strategy defined
