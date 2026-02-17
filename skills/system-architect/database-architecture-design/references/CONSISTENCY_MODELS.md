# Data Consistency Models

## Overview

Consistency models define what guarantees a distributed database provides about the visibility and ordering of updates across multiple nodes. Understanding these models is critical for designing reliable distributed systems.

## The CAP Theorem

**CAP Theorem states**: A distributed system can provide at most TWO of the following three guarantees:

- **Consistency (C)**: Every read receives the most recent write or an error
- **Availability (A)**: Every request receives a response (without guarantee of most recent data)
- **Partition Tolerance (P)**: System continues operating despite network partitions

**In practice**: Partition tolerance is mandatory (networks fail), so you choose between **CP (Consistency + Partition Tolerance)** or **AP (Availability + Partition Tolerance)**.

````
         Network Partition Occurs
                    │
         ┌──────────┴──────────┐
         │                     │
    CP System              AP System
    │                     │
    Choose Consistency    Choose Availability
    │                     │
    Return error          Return potentially stale data
    Wait for partition    Continue serving requests
    to heal               from available nodes
````

### CP Systems (Consistency + Partition Tolerance)

**Behavior**: During a partition, some nodes become unavailable to maintain consistency.

**Use cases**:
- Financial transactions (bank transfers)
- Inventory management (prevent overselling)
- User authentication and authorization
- Booking systems (prevent double-booking)

**Examples**: PostgreSQL, MySQL (single primary), MongoDB (strong consistency), HBase, Consul, etcd

### AP Systems (Availability + Partition Tolerance)

**Behavior**: During a partition, all nodes remain available but may return stale data.

**Use cases**:
- Social media feeds
- Product catalogs
- Analytics and metrics
- Recommendation systems
- Content delivery

**Examples**: Cassandra, DynamoDB (default), Riak, Couchbase

---

## Consistency Models Spectrum

From strongest to weakest:

````
Strongest (Slow, Limited Availability)
│
├─ Linearizability (Atomic Consistency)
├─ Sequential Consistency
├─ Causal Consistency
├─ Session Consistency (Read Your Writes)
├─ Monotonic Reads
├─ Monotonic Writes
├─ Eventual Consistency
│
Weakest (Fast, High Availability)
````

---

## Linearizability (Atomic Consistency)

### Definition

All operations appear to execute atomically in some global order. If operation A completes before operation B starts, then A appears before B in the global order.

### Guarantees

- Strongest consistency model
- Operations appear instantaneous
- All clients see same order of operations
- Real-time guarantee

### Analogy

Like a single-file line at a bank teller. Everyone sees the same sequence of customers being served.

### Implementation

- Synchronous replication to all nodes
- Quorum writes: W = N (all nodes must acknowledge)
- Quorum reads: R = N (read from all nodes)
- Distributed locking (e.g., Paxos, Raft)

### Trade-offs

**Pros**:
- Simplest mental model
- No surprises for developers
- Safe for critical operations

**Cons**:
- Highest latency (must wait for all nodes)
- Lowest availability (fails if any node is down)
- Not partition-tolerant (becomes unavailable during partition)

### Use Cases

- Financial transactions
- Leader election
- Configuration management (etcd, Consul)
- Distributed locking

### Example

````python
# Linearizable counter
counter = 0

# Thread 1
counter = counter + 1  # Completes at time T1
print(counter)         # Prints: 1

# Thread 2 (starts after T1)
print(counter)         # MUST print 1 or higher, never 0
````

### Technologies

- **Google Spanner**: Linearizability via TrueTime (atomic clocks)
- **CockroachDB**: Linearizability via Hybrid Logical Clocks
- **etcd**: Linearizability via Raft consensus
- **Consul**: Linearizability via Raft consensus

---

## Sequential Consistency

### Definition

All operations appear to execute in some sequential order. Same as linearizability, but without real-time guarantee.

### Guarantees

- All clients see same order of operations
- Order matches program order for each client
- No real-time guarantee (can reorder across clients)

### Difference from Linearizability

Operations can be reordered, but all clients see same global order.

````
Thread 1: Write X=1 at T1
Thread 2: Write Y=2 at T2 (T2 > T1)

Linearizable: All nodes must see X=1 before Y=2
Sequential: Nodes may see Y=2 before X=1, but all see same order
````

### Use Cases

- Less common in practice (linearizability or causal consistency more typical)
- Academic interest

---

## Causal Consistency

### Definition

Operations that are causally related are seen in the same order by all nodes. Concurrent operations may be seen in different orders.

### Guarantees

- If operation A causally affects operation B, all nodes see A before B
- Concurrent operations (no causal relationship) can appear in any order
- Preserves happens-before relationships

### Analogy

Like email threads. Everyone sees the same email conversation flow, but unrelated emails can arrive in any order.

### Implementation

- Vector clocks
- Lamport timestamps
- Hybrid logical clocks
- Causal histories

### Example

````
User A posts: "What's for lunch?"        [Event 1]
User B replies: "Pizza!"                 [Event 2, caused by Event 1]
User C posts: "Meeting at 3pm"           [Event 3, concurrent with 1 and 2]

Causal consistency guarantees:
- All users see Event 2 after Event 1 (causal relationship)
- Event 3 can appear before, between, or after Events 1 and 2 (concurrent)
````

### Use Cases

- Chat applications
- Collaborative editing
- Social media (comments on posts)
- Distributed caching

### Technologies

- **MongoDB** (with causal consistency setting)
- **Cassandra** (with SERIAL consistency)
- **Riak** (with dotted version vectors)
- **COPS** (research system)

---

## Session Consistency (Read Your Writes)

### Definition

A client always sees their own writes. Other clients may see eventual consistency.

### Guarantees

- Read-your-writes: Client sees effects of their own writes
- Monotonic reads: Client never sees older data after seeing newer data
- No guarantee about seeing other clients' writes immediately

### Implementation

- Sticky sessions (route user to same replica)
- Client-side version tracking
- Write-to-primary, read-from-same-replica

### Example

````
User updates profile picture:
1. User uploads new picture → Write to database
2. User refreshes profile page → MUST see new picture
3. Other users may still see old picture (eventually updated)
````

### Use Cases

- User profile updates
- Shopping cart updates
- User preferences
- Personalized dashboards

### Technologies

- **DynamoDB** (consistent reads from same region)
- **Cosmos DB** (session consistency level)
- **Cassandra** (with LOCAL_QUORUM)

---

## Monotonic Reads

### Definition

If a client reads value V1, subsequent reads will return V1 or later values, never earlier values.

### Guarantees

- No "going back in time"
- Client sees monotonically increasing versions

### Implementation

- Session affinity to replica
- Version vectors
- Read from replicas ahead of client's last-seen version

### Example

````
Social media feed:
1. User sees posts 1, 2, 3, 4, 5
2. User scrolls down
3. User sees posts 6, 7, 8 (OK)
4. User must NOT see posts 1, 2, 3 again (violates monotonic reads)
````

### Use Cases

- Social media feeds
- News feeds
- Activity logs
- Timelines

---

## Monotonic Writes

### Definition

Writes from a single client are seen by all nodes in the order they were issued.

### Guarantees

- Writes from same client are ordered
- Other clients' writes may interleave

### Example

````
Blog post system:
1. Author creates draft post      [Write 1]
2. Author updates draft           [Write 2]
3. Author publishes post          [Write 3]

All replicas must see Write 1 before Write 2 before Write 3
(Cannot publish before creating draft)
````

---

## Eventual Consistency

### Definition

If no new updates are made, eventually all replicas will converge to the same value.

### Guarantees

- Weakest consistency model
- Replicas may be temporarily inconsistent
- No guarantee on convergence time
- All replicas eventually converge

### Analogy

Like gossip spreading through a town. Eventually everyone hears the news, but timing varies.

### Implementation

- Asynchronous replication
- Anti-entropy (background sync)
- Read repair
- Hinted handoff

### Conflicts

When concurrent writes occur, conflicts must be resolved:

**Last-Write-Wins (LWW)**:
````
Node A: Write X=1 at timestamp T1
Node B: Write X=2 at timestamp T2
Result: X=2 (if T2 > T1)
````
- Simple but loses data
- Relies on clock synchronization

**Vector Clocks**:
````
Node A: Write X=1, version [A:1, B:0]
Node B: Write X=2, version [A:0, B:1]
Result: Conflict detected, both versions retained
````
- Application resolves conflict
- Preserves all writes

**CRDTs (Conflict-Free Replicated Data Types)**:
````
Counter: Increment-only counters (add operation is commutative)
Set: Add and remove with unique identifiers
````
- Automatic conflict resolution
- Mathematically proven convergence

### Use Cases

- DNS (domain name system)
- CDN caching
- Analytics and metrics
- Product catalogs
- Social media feeds

### Technologies

- **DynamoDB** (default)
- **Cassandra** (default)
- **Riak** (default)
- **Couchbase**
- **S3** (eventual consistency for overwrite operations)

---

## Choosing a Consistency Model

### Decision Framework

````
Can data loss cause financial impact or safety issues?
│
├─ YES → Linearizability or Sequential Consistency
│        Examples: Bank transfers, inventory, booking systems
│
└─ NO → Do users need to see their own writes immediately?
         │
         ├─ YES → Session Consistency (Read Your Writes)
         │        Examples: User profiles, settings, personalized data
         │
         └─ NO → Are writes causally related?
                  │
                  ├─ YES → Causal Consistency
                  │        Examples: Chat, comments, collaborative editing
                  │
                  └─ NO → Eventual Consistency
                           Examples: Analytics, catalogs, feeds
````

### By Use Case

| Use Case | Recommended Model | Rationale |
|----------|-------------------|-----------|
| Bank transfers | Linearizability | Cannot double-spend or lose money |
| Shopping cart | Session consistency | User must see their items |
| Product catalog | Eventual consistency | Stale data acceptable for seconds |
| Social media posts | Causal consistency | Comments after post, not vice versa |
| Inventory | Linearizability | Prevent overselling |
| User settings | Session consistency | User sees their changes |
| Analytics dashboard | Eventual consistency | Slight delay acceptable |
| Collaborative doc | Causal consistency | Preserve edit order |
| DNS | Eventual consistency | Propagation delay acceptable |
| Leader election | Linearizability | Only one leader allowed |

---

## Tunable Consistency (Quorum Systems)

Many databases allow tuning consistency vs. performance via quorum settings.

### Quorum Formula

````
R + W > N → Strong consistency
R + W ≤ N → Eventual consistency

Where:
R = Read quorum (nodes that must respond to read)
W = Write quorum (nodes that must acknowledge write)
N = Total number of replicas
````

### Common Configurations

| R | W | N | Consistency | Use Case |
|---|---|---|-------------|----------|
| 1 | N | 3 | Linearizable | Critical writes, fast reads |
| N | 1 | 3 | Linearizable | Critical reads, fast writes |
| 2 | 2 | 3 | Strong | Balanced |
| 1 | 1 | 3 | Eventual | High performance |
| 1 | 2 | 3 | Eventual | Fast reads, durable writes |

### Example: Cassandra Consistency Levels

````sql
-- Linearizable read (read from all replicas)
SELECT * FROM users WHERE id = 123 USING CONSISTENCY ALL;

-- Strong consistency (quorum)
SELECT * FROM users WHERE id = 123 USING CONSISTENCY QUORUM;

-- Eventual consistency (any replica)
SELECT * FROM users WHERE id = 123 USING CONSISTENCY ONE;

-- Read from local datacenter (lower latency)
SELECT * FROM users WHERE id = 123 USING CONSISTENCY LOCAL_QUORUM;
````

### Availability vs. Consistency Trade-off

````
High Availability          Balanced           Strong Consistency
(R=1, W=1)                 (R=2, W=2)         (R=N, W=N)
│                          │                  │
Fast reads/writes          Moderate latency   Slow reads/writes
Stale reads possible       Strong consistency  Always fresh data
High availability          Moderate availability Low availability
````

---

## Handling Network Partitions

### Split-Brain Problem

When network partition occurs, both sides may accept writes, leading to divergent state.

````
         Primary                    Replica
         (Region A)                 (Region B)
             │                          │
             │   Network Partition      │
             │ ════════════════════════ │
             │                          │
        Write X=1                   Write X=2
             │                          │
        Clients in A                Clients in B
        see X=1                     see X=2

        When partition heals: Conflict!
````

### Strategies

**1. Quorum-Based (CP)**:
````
Require W = N/2 + 1 (majority) to accept writes
- Only one side of partition can form quorum
- Other side rejects writes (maintains consistency)
- Trades availability for consistency
````

**2. Last-Write-Wins (AP)**:
````
Accept writes on both sides
- When partition heals, latest timestamp wins
- Risk of data loss
- Trades consistency for availability
````

**3. Vector Clocks + Application Resolution (AP)**:
````
Accept writes on both sides with version vectors
- When partition heals, conflicts are detected
- Application resolves conflicts
- No data loss, but complexity in application
````

**4. CRDTs (AP)**:
````
Use data structures with commutative operations
- Automatic conflict resolution
- Eventually consistent with provable convergence
- Limited to specific data types (counters, sets, maps)
````

---

## Practical Implementation Patterns

### Pattern 1: Strong Primary, Eventual Replicas

````python
def write_user(user_id, data):
    # Write to primary (synchronous, strong consistency)
    primary_db.write(user_id, data)

    # Replicate to replicas (asynchronous, eventual consistency)
    for replica in replicas:
        replica.write_async(user_id, data)

def read_user(user_id, strong_consistency=False):
    if strong_consistency:
        # Read from primary
        return primary_db.read(user_id)
    else:
        # Read from any replica (may be stale)
        return random.choice(replicas).read(user_id)
````

**Use case**: Read-heavy workload where most reads can tolerate slight staleness.

### Pattern 2: Session Affinity

````python
def get_replica_for_user(user_id):
    # Route user to same replica for session
    replica_index = hash(user_id) % len(replicas)
    return replicas[replica_index]

def write_user(user_id, data):
    primary_db.write(user_id, data)

def read_user(user_id):
    # Always read from same replica for this user
    replica = get_replica_for_user(user_id)
    return replica.read(user_id)
````

**Use case**: User must see their own writes (session consistency).

### Pattern 3: Version Tracking

````python
def write_user(user_id, data):
    version = primary_db.write(user_id, data)
    return version  # Return version to client

def read_user(user_id, min_version=None):
    # Keep trying replicas until finding one with sufficient version
    for replica in replicas:
        user, version = replica.read(user_id)
        if min_version is None or version >= min_version:
            return user

    # Fallback to primary if no replica is up-to-date
    return primary_db.read(user_id)
````

**Use case**: Client tracks version and ensures reads are causally consistent with previous writes.

### Pattern 4: Hybrid (Critical + Non-Critical Data)

````python
def transfer_money(from_account, to_account, amount):
    # Financial transaction requires strong consistency
    with linearizable_db.transaction():
        from_balance = linearizable_db.read(from_account)
        to_balance = linearizable_db.read(to_account)

        linearizable_db.write(from_account, from_balance - amount)
        linearizable_db.write(to_account, to_balance + amount)

def get_account_activity(account_id):
    # Activity feed can use eventual consistency
    return eventual_db.read_activity(account_id)
````

**Use case**: Mix strong consistency for critical operations with eventual consistency for non-critical data.

---

## Testing Consistency Models

### Jepsen Testing

Jepsen is a framework for testing distributed systems under network partitions.

````bash
# Example: Test Cassandra consistency
lein run test --nodes n1,n2,n3,n4,n5 \
              --time-limit 300 \
              --test-count 10 \
              --cassandra-version 4.0.0 \
              --consistency quorum
````

### Manual Testing Scenarios

**Test 1: Replication Lag**:
````python
# Write to primary
primary.write("key1", "value1")

# Immediately read from replica
value = replica.read("key1")

# Check: Is value == "value1" or stale?
````

**Test 2: Split-Brain**:
````python
# Partition network between nodes
network.partition([node1, node2], [node3, node4, node5])

# Write to both sides
side_a.write("key1", "valueA")
side_b.write("key1", "valueB")

# Heal partition
network.heal()

# Check: How is conflict resolved?
final_value = db.read("key1")
````

**Test 3: Session Consistency**:
````python
# Write as user1
session = Session(user_id=1)
session.write("profile", "new_picture.jpg")

# Read as same user
value = session.read("profile")

# Check: Is value == "new_picture.jpg"?
````

---

## Summary Table

| Model | Latency | Availability | Complexity | Use Case |
|-------|---------|--------------|------------|----------|
| Linearizability | Highest | Lowest | Low | Financial, locking |
| Sequential | High | Low | Low | Rarely used |
| Causal | Medium | Medium | Medium | Chat, collaboration |
| Session | Low | High | Medium | User profiles |
| Monotonic Reads | Low | High | Low | Feeds, timelines |
| Monotonic Writes | Low | High | Low | Logs, audit trails |
| Eventual | Lowest | Highest | High (conflicts) | Catalogs, analytics |

---

This reference provides comprehensive coverage of consistency models. Use it when designing systems that require specific consistency guarantees or when troubleshooting consistency-related issues.
