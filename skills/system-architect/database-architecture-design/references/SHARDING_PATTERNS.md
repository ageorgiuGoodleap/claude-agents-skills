# Database Sharding Patterns

## Overview

Sharding (horizontal partitioning) is the practice of splitting data across multiple database instances to scale beyond the limits of a single machine. This reference covers sharding strategies, implementation patterns, and migration approaches.

## When to Shard

### Signals You Need Sharding

**Storage Limits**:
- Database size approaching instance storage limit
- Growth projections exceed single-instance capacity
- Historical data overwhelming primary storage

**Performance Degradation**:
- Query latency increasing despite optimization and indexing
- CPU or memory consistently above 80%
- I/O throughput hitting disk limits
- Lock contention increasing

**Scalability Limits**:
- Vertical scaling (bigger instances) becoming cost-prohibitive
- Single instance cannot handle write throughput
- Read replicas cannot handle read throughput
- Need for geographic distribution

### Thresholds (Rough Guidelines)

| Database | Consider Sharding When |
|----------|------------------------|
| PostgreSQL | >1TB data, >10K queries/sec, CPU >80% sustained |
| MySQL | >500GB data, >5K queries/sec, CPU >80% sustained |
| MongoDB | >2TB per replica set, performance degradation |
| Cassandra | Usually pre-sharded (distributed by default) |

### Before Sharding

Try these optimizations first (sharding adds significant complexity):

1. **Indexing**: Add indexes for slow queries
2. **Query optimization**: Rewrite inefficient queries
3. **Caching**: Add Redis/Memcached layer
4. **Read replicas**: Offload reads from primary
5. **Vertical scaling**: Upgrade to larger instance
6. **Archiving**: Move old data to cold storage
7. **Partitioning**: Use table partitioning (single database)

**Only shard when these optimizations are exhausted.**

---

## Sharding Strategies

### 1. Range-Based Sharding

Partition data based on ranges of a key.

````
Shard 1: user_id 1 - 1,000,000
Shard 2: user_id 1,000,001 - 2,000,000
Shard 3: user_id 2,000,001 - 3,000,000
Shard 4: user_id 3,000,001 - 4,000,000
````

**Shard Selection**:
````python
def get_shard(user_id):
    shard_size = 1_000_000
    shard_number = (user_id - 1) // shard_size
    return shards[shard_number]
````

**Advantages**:
- Simple to implement and understand
- Range queries are efficient (scan single shard)
- Ordered data stays together (useful for time-series)
- Easy to add new shards (extend range)

**Disadvantages**:
- Uneven distribution (recent data gets more traffic)
- Hotspots on recent shards (e.g., new users)
- Requires sequential ID generation
- Rebalancing is complex

**Use Cases**:
- Time-series data (log entries, events, metrics)
- Historical data access patterns (recent data more accessed)
- Sequential ID schemes

**Example: E-commerce Orders by Date**
````sql
-- Shard 1: Orders Q1 2024
CREATE TABLE orders_2024_q1 (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ...
) WHERE created_at >= '2024-01-01' AND created_at < '2024-04-01';

-- Shard 2: Orders Q2 2024
CREATE TABLE orders_2024_q2 (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ...
) WHERE created_at >= '2024-04-01' AND created_at < '2024-07-01';
````

### 2. Hash-Based Sharding

Partition data using hash function on key.

````
shard_number = hash(user_id) % num_shards
````

**Shard Selection**:
````python
import hashlib

def get_shard(user_id):
    # Use consistent hashing for stable assignment
    hash_value = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16)
    shard_number = hash_value % len(shards)
    return shards[shard_number]
````

**Advantages**:
- Even distribution across shards
- No hotspots (assuming good hash function)
- Simple to implement
- Predictable shard assignment

**Disadvantages**:
- Range queries require querying all shards
- Rebalancing requires rehashing (moves many rows)
- Adding/removing shards is complex
- Related data may be split across shards

**Use Cases**:
- User data (users, profiles, preferences)
- Lookup-heavy workloads (simple key-value access)
- Avoid hotspots on popular keys

**Example: User Profiles**
````python
# Application code
def get_user(user_id):
    shard = get_shard(user_id)
    return shard.query("SELECT * FROM users WHERE id = ?", user_id)

def update_user(user_id, data):
    shard = get_shard(user_id)
    shard.execute("UPDATE users SET name = ? WHERE id = ?", data['name'], user_id)
````

### 3. Geographic Sharding

Partition data based on geographic location.

````
Shard US: Users in North America
Shard EU: Users in Europe
Shard ASIA: Users in Asia-Pacific
````

**Shard Selection**:
````python
def get_shard(user_id):
    user = lookup_user_metadata(user_id)  # Lightweight lookup
    region = user['region']

    region_mapping = {
        'US': shards['us'],
        'EU': shards['eu'],
        'ASIA': shards['asia']
    }

    return region_mapping.get(region, shards['us'])  # Default to US
````

**Advantages**:
- Data residency compliance (GDPR, data sovereignty)
- Reduced latency (data close to users)
- Natural isolation for regional failures
- Easier to reason about data location

**Disadvantages**:
- Uneven distribution (population imbalance)
- Cross-region queries are slow
- Difficult to handle users moving regions
- Requires geographic metadata

**Use Cases**:
- Regulatory compliance (GDPR, data residency)
- Global applications with regional user bases
- Latency-sensitive applications

**Example: Multi-Region SaaS**
````yaml
# US Region
database:
  host: us-west-2.rds.amazonaws.com
  region: us
  users: US, Canada, Latin America

# EU Region
database:
  host: eu-central-1.rds.amazonaws.com
  region: eu
  users: EU, UK, Middle East, Africa

# Asia Region
database:
  host: ap-southeast-1.rds.amazonaws.com
  region: asia
  users: Asia-Pacific, Australia
````

### 4. Directory-Based Sharding

Use a lookup table to map keys to shards.

````
Lookup Table (metadata database):
user_123 → shard_2
user_456 → shard_1
user_789 → shard_3
````

**Shard Selection**:
````python
def get_shard(user_id):
    # Query lookup table (cached for performance)
    shard_id = cache.get(f"shard:{user_id}")

    if not shard_id:
        shard_id = metadata_db.query(
            "SELECT shard_id FROM user_shards WHERE user_id = ?",
            user_id
        )
        cache.set(f"shard:{user_id}", shard_id, ttl=3600)

    return shards[shard_id]
````

**Advantages**:
- Maximum flexibility (arbitrary assignment)
- Easy to rebalance (update lookup table)
- Can group related data on same shard
- Supports custom sharding logic

**Disadvantages**:
- Additional lookup latency
- Metadata database is single point of failure
- Caching complexity
- Metadata can become large

**Use Cases**:
- Tenant-based sharding (multi-tenant SaaS)
- Situations requiring frequent rebalancing
- Custom sharding logic (by customer size, etc.)

**Example: Multi-Tenant SaaS**
````sql
-- Metadata database
CREATE TABLE tenant_shards (
    tenant_id INTEGER PRIMARY KEY,
    shard_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Application code
def get_tenant_shard(tenant_id):
    shard_id = metadata_db.query(
        "SELECT shard_id FROM tenant_shards WHERE tenant_id = ?",
        tenant_id
    )
    return shards[shard_id]
````

### 5. Consistent Hashing

Advanced hash-based approach that minimizes data movement when shards are added/removed.

````
Hash Ring:
     0°
     ○ ──────── Node A (120°)
     │
Node D (300°)     Node B (180°)
     │
     ○ ──────── Node C (240°)
````

**Shard Selection**:
````python
import hashlib

class ConsistentHashing:
    def __init__(self, nodes, virtual_nodes=150):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.nodes = nodes

        for node in nodes:
            self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_value = self._hash(virtual_key)
            self.ring[hash_value] = node

    def get_node(self, key):
        if not self.ring:
            return None

        hash_value = self._hash(key)

        # Find first node clockwise from hash_value
        for ring_key in sorted(self.ring.keys()):
            if hash_value <= ring_key:
                return self.ring[ring_key]

        # Wrap around to first node
        return self.ring[min(self.ring.keys())]

# Usage
ch = ConsistentHashing(['shard1', 'shard2', 'shard3'])
shard = ch.get_node(user_id)
````

**Advantages**:
- Minimal data movement when adding/removing shards
- Even distribution with virtual nodes
- No lookup table needed
- Supports dynamic shard membership

**Disadvantages**:
- More complex to implement
- Range queries span all shards
- Virtual nodes add memory overhead

**Use Cases**:
- Caching layers (Redis, Memcached clusters)
- Distributed systems with dynamic membership
- Situations requiring frequent shard additions

---

## Shard Key Selection

### Characteristics of a Good Shard Key

1. **High Cardinality**: Many distinct values (not just 0/1)
2. **Even Distribution**: Balanced data across shards
3. **Stable**: Doesn't change frequently
4. **Query Alignment**: Used in most queries (avoids scatter-gather)

### Examples

**Good Shard Keys**:
- `user_id` (high cardinality, stable, query-aligned)
- `tenant_id` (multi-tenant systems)
- `email_hash` (even distribution)
- `order_date` (time-series data)
- `country_code` + `user_id` (geographic + unique)

**Bad Shard Keys**:
- `status` (low cardinality: active/inactive)
- `is_premium` (boolean, uneven distribution)
- `created_at` (monotonically increasing, creates hotspots)
- `country` alone (uneven distribution, US >> others)

### Compound Shard Keys

Combine multiple columns for better distribution:

````python
# Geographic + hash
shard_key = f"{country_code}:{hash(user_id) % 100}"

# Tenant + entity
shard_key = f"{tenant_id}:{resource_type}"
````

---

## Cross-Shard Operations

### Challenge

Sharding breaks operations that require data from multiple shards.

### Strategies

#### 1. Denormalization (Preferred)

Duplicate data so queries hit single shard.

````sql
-- Without denormalization (requires cross-shard join)
-- Shard A: users table
-- Shard B: orders table
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.id = 123;

-- With denormalization (single shard)
-- Shard A: users table
-- Shard A: orders table includes user_name
SELECT user_name, total
FROM orders
WHERE user_id = 123;
````

**Trade-off**: Storage overhead and update complexity vs. query simplicity

#### 2. Application-Level Joins

Query each shard and join in application.

````python
def get_user_orders(user_id):
    # Query user shard
    user_shard = get_shard(user_id)
    user = user_shard.query("SELECT * FROM users WHERE id = ?", user_id)

    # Query order shard(s)
    orders = []
    for shard in shards:
        shard_orders = shard.query(
            "SELECT * FROM orders WHERE user_id = ?",
            user_id
        )
        orders.extend(shard_orders)

    return {'user': user, 'orders': orders}
````

**Trade-off**: Multiple queries, higher latency

#### 3. Scatter-Gather

Query all shards and aggregate results.

````python
def search_users(name_pattern):
    results = []

    # Query all shards in parallel
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(shard.query, "SELECT * FROM users WHERE name LIKE ?", name_pattern)
            for shard in shards
        ]

        for future in futures:
            results.extend(future.result())

    return results
````

**Trade-off**: Expensive (queries all shards), but supports global queries

#### 4. Distributed Transactions (Avoid When Possible)

Use two-phase commit (2PC) or Saga pattern for cross-shard transactions.

````python
# Two-Phase Commit (simplified)
def transfer_balance(from_user_id, to_user_id, amount):
    from_shard = get_shard(from_user_id)
    to_shard = get_shard(to_user_id)

    # Phase 1: Prepare
    tx1 = from_shard.prepare_transaction()
    tx1.execute("UPDATE users SET balance = balance - ? WHERE id = ?", amount, from_user_id)

    tx2 = to_shard.prepare_transaction()
    tx2.execute("UPDATE users SET balance = balance + ? WHERE id = ?", amount, to_user_id)

    # Phase 2: Commit
    try:
        tx1.commit()
        tx2.commit()
    except Exception:
        tx1.rollback()
        tx2.rollback()
        raise
````

**Trade-off**: Complex, slower, potential for distributed deadlocks

---

## Rebalancing Strategies

### When to Rebalance

- Shard becomes too large (approaching instance limits)
- Uneven distribution causing performance issues
- Hot shard (one shard getting disproportionate traffic)
- Adding new shards to increase capacity

### Rebalancing Approaches

#### 1. Add New Shard and Redirect New Data

Simplest approach: new data goes to new shard, old data stays in place.

````python
# Before
shards = ['shard1', 'shard2', 'shard3']

# After adding shard4
shards = ['shard1', 'shard2', 'shard3', 'shard4']

def get_shard(user_id):
    # Old users stay on old shards, new users go to all shards
    if user_id < 3_000_000:
        return shards[hash(user_id) % 3]  # Old sharding logic
    else:
        return shards[hash(user_id) % 4]  # New sharding logic
````

**Pros**: No data movement, immediate
**Cons**: Complexity in shard logic, doesn't fix existing imbalance

#### 2. Live Migration

Move data from overloaded shard to new shard while serving traffic.

````python
# Phase 1: Dual-write (writes go to both shards)
def write_user(user_id, data):
    old_shard = get_old_shard(user_id)
    new_shard = get_new_shard(user_id)

    old_shard.write(user_id, data)
    new_shard.write(user_id, data)  # Duplicate write

# Phase 2: Backfill (copy old data to new shard)
def backfill():
    for user_id in old_shard.all_user_ids():
        user = old_shard.read(user_id)
        new_shard.write(user_id, user)

# Phase 3: Switch reads to new shard
def read_user(user_id):
    new_shard = get_new_shard(user_id)
    return new_shard.read(user_id)

# Phase 4: Remove data from old shard
def cleanup():
    for user_id in migrated_users:
        old_shard.delete(user_id)
````

**Pros**: No downtime, safe rollback
**Cons**: Complex, temporary storage overhead

#### 3. Offline Migration

Take shard offline, move data, bring back online.

````bash
# Step 1: Stop writes to old shard
app.config.read_only_mode = true

# Step 2: Dump data
pg_dump -h old_shard -d database -t users > users.sql

# Step 3: Load data into new shard
psql -h new_shard -d database < users.sql

# Step 4: Update routing configuration
app.config.shards['users'] = new_shard

# Step 5: Resume writes
app.config.read_only_mode = false
````

**Pros**: Simpler, no dual-write complexity
**Cons**: Downtime required

#### 4. Consistent Hashing (Automatic Rebalancing)

With consistent hashing, adding nodes automatically rebalances minimal data.

````
# Before: 3 nodes
Node A: 33% of keys
Node B: 33% of keys
Node C: 33% of keys

# After adding Node D: only ~8% of keys move
Node A: 25% of keys (lost 8%)
Node B: 25% of keys (lost 8%)
Node C: 25% of keys (lost 8%)
Node D: 25% of keys (gained 25%)
````

**Pros**: Minimal data movement, automatic
**Cons**: Requires consistent hashing from start

---

## Sharding Patterns by Use Case

### Multi-Tenant SaaS

**Strategy**: Directory-based sharding by `tenant_id`

````python
# Group small tenants on shared shards, large tenants on dedicated shards
def get_tenant_shard(tenant_id):
    tenant_metadata = get_tenant_metadata(tenant_id)

    if tenant_metadata['size'] == 'large':
        # Dedicated shard for large tenant
        return dedicated_shards[tenant_id]
    else:
        # Shared shard for small tenants
        return shared_shards[hash(tenant_id) % num_shared_shards]
````

**Benefits**:
- Isolate large tenants (performance isolation)
- Efficient use of resources (small tenants share)
- Easy to move tenants between shards

### Social Network

**Strategy**: Hash-based sharding by `user_id`

````python
# Shard users
shard = hash(user_id) % num_shards

# Co-locate related data
# Posts: shard by author_id (same shard as user)
# Followers: shard by follower_id
# Following: shard by followee_id (may require scatter-gather)
````

**Benefits**:
- Even distribution
- User's posts on same shard (efficient queries)
- Scalable writes

**Challenge**: Following/Followers may require cross-shard queries

### E-commerce

**Strategy**: Hybrid (hash-based for users, range-based for orders)

````python
# Users: hash by user_id
user_shard = hash(user_id) % num_user_shards

# Orders: range by order_date (time-series)
order_shard = order_date.year + "_" + order_date.quarter

# Products: hash by product_id
product_shard = hash(product_id) % num_product_shards
````

**Benefits**:
- Users evenly distributed
- Recent orders on fast shards (SSD)
- Old orders archived to slow storage (HDD, S3)

### Time-Series / Logs

**Strategy**: Range-based sharding by timestamp

````python
# Shard by day/week/month depending on volume
shard = f"logs_{timestamp.year}_{timestamp.month}_{timestamp.day}"

# Automatically create new shard daily
def get_shard(timestamp):
    shard_name = f"logs_{timestamp.strftime('%Y_%m_%d')}"

    if shard_name not in shards:
        create_shard(shard_name)

    return shards[shard_name]
````

**Benefits**:
- Automatic time-based partitioning
- Easy to archive/delete old shards
- Efficient range queries

---

## Monitoring Sharded Databases

### Key Metrics Per Shard

| Metric | Why Important | Alert Threshold |
|--------|---------------|-----------------|
| Row count | Detect imbalance | >20% difference between shards |
| Query latency | Performance degradation | p99 >200ms |
| CPU usage | Overloaded shard | >80% sustained |
| Storage usage | Approaching limits | >80% of capacity |
| Write throughput | Hotspot detection | >3x average |
| Read throughput | Hotspot detection | >3x average |
| Error rate | Shard failure | >1% error rate |

### Rebalancing Triggers

- Any shard exceeds 80% storage capacity
- Latency p99 >2x other shards
- CPU usage >80% on one shard while others <50%
- Row count skew >30% between shards

### Monitoring Tools

````python
# Example: Prometheus metrics for shard monitoring
from prometheus_client import Gauge, Histogram

shard_row_count = Gauge('shard_row_count', 'Number of rows per shard', ['shard'])
shard_query_latency = Histogram('shard_query_latency_seconds', 'Query latency per shard', ['shard'])

def monitor_shards():
    for shard in shards:
        # Row count
        count = shard.query("SELECT COUNT(*) FROM users")
        shard_row_count.labels(shard=shard.name).set(count)

        # Query latency
        start = time.time()
        shard.query("SELECT * FROM users WHERE id = ?", random_user_id)
        latency = time.time() - start
        shard_query_latency.labels(shard=shard.name).observe(latency)
````

---

## Anti-Patterns

### ❌ Sharding Too Early

````
Problem: "We might scale to millions of users, let's shard from day 1"
Solution: Start with single database, shard when metrics demand it
Rationale: Premature optimization adds complexity without benefit
````

### ❌ Wrong Shard Key

````
Problem: Shard by 'status' (active/inactive) → uneven distribution
Solution: Choose high-cardinality, stable keys (user_id, tenant_id)
Rationale: Low-cardinality keys create hotspots
````

### ❌ Cross-Shard Transactions

````
Problem: Frequent distributed transactions across shards
Solution: Denormalize data or redesign schema to avoid
Rationale: Distributed transactions are slow and complex
````

### ❌ Ignoring Rebalancing

````
Problem: Shards grow unevenly, never rebalanced
Solution: Monitor metrics, rebalance proactively
Rationale: Unbalanced shards cause performance degradation
````

### ❌ No Rollback Plan

````
Problem: Migrate to sharded architecture without rollback plan
Solution: Always have ability to rollback (dual-write, data retention)
Rationale: Sharding is risky, rollback may be necessary
````

---

## Migration Checklist

### Pre-Migration

- [ ] Measure current database metrics (baseline)
- [ ] Identify shard key and validate cardinality
- [ ] Test sharding logic in staging environment
- [ ] Benchmark query performance on sharded schema
- [ ] Prepare rollback plan
- [ ] Set up monitoring for sharded environment
- [ ] Update application code to support sharding
- [ ] Test cross-shard queries and transactions
- [ ] Document shard routing logic

### Migration

- [ ] Enable dual-write mode (write to both old and new)
- [ ] Backfill data to new shards
- [ ] Verify data consistency between old and new
- [ ] Gradually shift reads to new shards
- [ ] Monitor error rates and latency
- [ ] Validate application behavior
- [ ] Full cutover (all reads from new shards)
- [ ] Disable dual-write mode
- [ ] Archive old database

### Post-Migration

- [ ] Monitor shard distribution (row counts, size)
- [ ] Monitor query latency per shard
- [ ] Identify hotspots or imbalances
- [ ] Set up automated rebalancing (if applicable)
- [ ] Document operational runbook
- [ ] Train team on shard management
- [ ] Prepare for next rebalancing cycle

---

This reference provides comprehensive coverage of sharding strategies. Use it when designing sharded architectures or planning migrations to sharded systems.
