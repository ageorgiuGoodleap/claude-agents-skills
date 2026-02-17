---
name: performance-review
description: |
  Performance impact analysis for algorithmic complexity, query efficiency, and resource usage.

  WHAT: Analyzes code for performance concerns: algorithmic complexity (O(n²) loops, nested iterations), database query efficiency (N+1 problems, missing indexes, sequential queries), unnecessary computations (redundant loops, premature optimization), memory usage patterns (large allocations, potential leaks, inefficient copying). Estimates performance impact as High (10x+ degradation), Medium (2-10x), or Low (under 2x). Suggests concrete optimizations with code examples.

  WHEN: Use for performance-sensitive code reviews, optimization analysis, or bottleneck identification. Trigger on: "performance review", "code performance", "optimization review", "efficiency review", "algorithmic complexity", "slow code", "performance impact", "bottleneck", "N+1 query", "inefficient loop", "memory usage".
allowed-tools: Read, Grep, Glob
---

# Performance Review Skill

## Overview

This skill analyzes code changes for performance impact, identifying algorithmic complexity issues, inefficient database queries, unnecessary computations, and memory usage patterns. It provides concrete optimization recommendations with before/after code examples and estimated performance improvements.

## Workflow

### 1. Identify Performance-Sensitive Code

Scan for code areas most likely to impact performance:

- **Database operations:** Queries, ORM method calls, raw SQL
- **Loops and iterations:** Especially nested loops, large dataset processing
- **Network operations:** API calls, HTTP requests, external service integrations
- **File I/O:** Reading/writing files, especially large files
- **Recursive functions:** Deep recursion, memoization opportunities
- **Data structure operations:** Sorting, searching, filtering large collections

### 2. Analyze Algorithmic Complexity

Determine time complexity for each operation:

- **O(1):** Constant time - hash table lookups, array access by index
- **O(log n):** Logarithmic - binary search, balanced tree operations
- **O(n):** Linear - single loop over dataset, simple list operations
- **O(n log n):** Log-linear - efficient sorting (merge sort, quicksort)
- **O(n²):** Quadratic - nested loops, comparing every item with every other item
- **O(2^n):** Exponential - recursive algorithms without memoization

**Red flags:**
- Nested loops over the same or related datasets → Often O(n²)
- Multiple sequential database queries in a loop → N+1 problem
- Recursion without memoization → Exponential complexity

### 3. Detect N+1 Query Problems

The N+1 query problem occurs when code executes one query to fetch a list, then executes N additional queries (one per item) to fetch related data.

**Patterns to identify:**

```python
# Python/Django example
for user in User.objects.all():  # 1 query
    posts = user.posts.all()     # N queries (one per user)

# Ruby/Rails example
User.all.each do |user|          # 1 query
  posts = user.posts             # N queries
end

# JavaScript/TypeORM example
const users = await userRepository.find();  // 1 query
for (const user of users) {
  const posts = await postRepository.find({ userId: user.id });  // N queries
}
```

**Solutions:**
- Django: Use `.select_related()` (1-to-1, foreign keys) or `.prefetch_related()` (many-to-many, reverse foreign keys)
- Rails: Use `.includes()` or `.eager_load()`
- TypeORM: Use `relations` option or `leftJoinAndSelect()`

### 4. Review Database Query Efficiency

Check for common inefficiencies:

- **SELECT * instead of specific columns:** Fetches unnecessary data
- **Missing WHERE clause indexes:** Full table scans instead of index lookups
- **Inefficient JOINs:** Multiple tables, Cartesian products, large result sets
- **No pagination:** Loading thousands of rows when only 20 needed
- **Sequential queries:** Multiple queries that could be combined

**Optimization strategies:**
- Add indexes to frequently queried columns
- Select only needed columns: `SELECT id, name` not `SELECT *`
- Use pagination: `LIMIT 20 OFFSET 0`
- Combine related queries with JOINs

### 5. Check for Redundant Computations

Identify calculations performed repeatedly:

```python
# Bad: Computation inside loop
for item in items:
    total += item.price * (1 + tax_rate / 100)  # tax_rate calculated each iteration

# Good: Compute once outside loop
tax_multiplier = 1 + tax_rate / 100
for item in items:
    total += item.price * tax_multiplier
```

**Common patterns:**
- Same database query executed multiple times → Cache result
- Expensive function called repeatedly with same arguments → Memoization
- Sorting/filtering same data multiple times → Store intermediate result

### 6. Analyze Memory Usage

Look for memory inefficiencies:

- **Large allocations in loops:** Growing lists without size limit
- **Loading entire files into memory:** Should use streaming/line-by-line processing
- **Caching without eviction:** Unbounded cache growth
- **Deep copying large structures:** Unnecessary data duplication
- **Keeping references to large objects:** Prevents garbage collection

**Memory-efficient patterns:**

```python
# Bad: Load entire file
content = open('large_file.csv').read()  # 1GB in memory

# Good: Stream line-by-line
for line in open('large_file.csv'):
    process_line(line)  # Constant memory

# Bad: Grow list indefinitely
results = []
for item in infinite_stream():
    results.append(process(item))  # Memory grows unbounded

# Good: Process and discard
for item in infinite_stream():
    result = process(item)
    save_to_database(result)  # Discard after saving
```

### 7. Identify Parallelization Opportunities

Find operations that could run concurrently:

- **Sequential API calls:** Could use async/await or threading
- **Independent loop iterations:** Could use multiprocessing
- **Blocking I/O operations:** Could use async I/O

**Example optimization:**

```python
# Sequential (slow)
for user_id in user_ids:
    response = requests.get(f"/api/users/{user_id}")  # 200ms each
    users.append(response.json())
# Total: 10 users × 200ms = 2000ms

# Parallel (fast)
import asyncio
import aiohttp

async def fetch_user(session, user_id):
    async with session.get(f"/api/users/{user_id}") as response:
        return await response.json()

async def fetch_all_users(user_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_user(session, uid) for uid in user_ids]
        return await asyncio.gather(*tasks)
# Total: ~200ms (all parallel)
```

### 8. Check Caching Usage

Identify expensive operations that could benefit from caching:

- Repeated database queries with same parameters
- Expensive computations with deterministic results
- External API calls with slowly changing data

**Caching strategies:**

```python
# Python: functools.lru_cache
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_user_permissions(user_id):
    return expensive_database_query(user_id)

# Redis caching
import redis
cache = redis.Redis()

def get_user_data(user_id):
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    data = database.query(user_id)
    cache.setex(f"user:{user_id}", 3600, json.dumps(data))  # 1 hour TTL
    return data
```

### 9. Review Data Structure Choices

Ensure appropriate data structures for operations:

| Operation | Inefficient | Efficient | Complexity |
|-----------|-------------|-----------|------------|
| Membership test | List (`item in list`) | Set (`item in set`) | O(n) → O(1) |
| Frequent lookups | List with iteration | Dict with key lookup | O(n) → O(1) |
| FIFO queue | List with `pop(0)` | `collections.deque` | O(n) → O(1) |
| Sorted data | Maintain sorted list | `heapq` or `bisect` | O(n log n) → O(log n) |

### 10. Estimate Performance Impact

Categorize findings by severity:

**High Impact (>10x degradation):**
- O(n²) or worse complexity on large datasets (n > 1000)
- N+1 query problem with many items (N > 100)
- Loading multi-GB files entirely into memory
- Synchronous blocking calls in hot paths

**Medium Impact (2-10x degradation):**
- Inefficient sorting algorithms on medium datasets
- Multiple sequential API calls (could be parallel)
- Missing database indexes on frequently queried columns
- Redundant computations in moderately tight loops

**Low Impact (<2x degradation):**
- Minor redundant calculations
- Suboptimal but acceptable data structure choices
- Small inefficiencies with limited execution frequency

## Output Format

Present findings in this structured format:

```markdown
# Performance Review

## Summary
**Status:** [NO CONCERNS / MINOR ISSUES / SIGNIFICANT ISSUES / BLOCKING ISSUES]
**High Impact Issues:** [count]
**Medium Impact Issues:** [count]
**Low Impact Issues:** [count]

---

## High Impact Issues (>10x Performance Degradation)

### [Issue Number]. [Issue Type] in `file.py:line`
- **Location:** `function_name()`
- **Current Approach:**
  ```[language]
  [current code]
  ```
- **Issue:** [Clear explanation of the problem]
- **Impact:** [Quantified impact with concrete numbers]
- **Complexity:** [Big-O notation]
- **Fix:**
  ```[language]
  [optimized code]
  ```
- **Improvement:** [Quantified improvement]

---

## Medium Impact Issues (2-10x Performance Degradation)

[Same structure as High Impact]

---

## Low Impact Issues (<2x Performance Degradation)

[Same structure as High Impact]

---

## Memory Usage Issues

### [Issue Number]. [Issue Type] in `file.py:line`
- **Location:** `function_name()`
- **Current Approach:** [Description]
- **Issue:** [Memory problem]
- **Impact:** [Memory usage numbers]
- **Fix:** [Solution]
- **Improvement:** [Memory savings]

---

## Optimization Opportunities

[Additional improvements that aren't critical but recommended]

---

## Recommendations

### High Priority (Fix Now)
1. [Most critical performance fixes]

### Medium Priority (Should Address)
1. [Important but not blocking]

### Low Priority (Consider)
1. [Nice-to-have improvements]

---

## Performance Metrics Summary

**Estimated Improvements:**
- **Total Queries:** [before] → [after] ([X]% reduction)
- **Time Complexity:** [before] → [after] ([X]x improvement)
- **Execution Time:** [before] → [after] ([X]x faster)
- **Memory Usage:** [before] → [after]
```

## Quality Checklist

Before completing the review, verify:

- [ ] Algorithmic complexity analyzed and stated (O(n), O(n²), etc.)
- [ ] Performance impact estimated with concrete numbers
- [ ] All N+1 queries identified with fix examples
- [ ] Memory usage issues flagged with streaming alternatives
- [ ] Parallelization opportunities suggested where applicable
- [ ] Before/after code examples provided for each issue
- [ ] Time/memory savings estimated quantitatively
- [ ] Recommendations prioritized by impact

## Common Performance Anti-Patterns

### N+1 Query Problem

**Django:**
```python
# Bad
for user in User.objects.all():
    posts = user.posts.all()  # N queries

# Good
for user in User.objects.prefetch_related('posts'):
    posts = user.posts.all()  # 2 queries total
```

**Rails:**
```ruby
# Bad
User.all.each do |user|
  posts = user.posts  # N queries
end

# Good
User.includes(:posts).each do |user|
  posts = user.posts  # 2 queries total
end
```

### Nested Loops (O(n²) → O(n))

```python
# Bad: O(n²)
duplicates = []
for i, item in enumerate(items):
    for j, other in enumerate(items):
        if i != j and item == other:
            duplicates.append(item)

# Good: O(n)
seen = set()
duplicates = []
for item in items:
    if item in seen:
        duplicates.append(item)
    seen.add(item)
```

### Sequential API Calls

```python
# Bad: Sequential
results = []
for id in ids:
    response = requests.get(f"/api/resource/{id}")
    results.append(response.json())

# Good: Parallel
import asyncio
import aiohttp

async def fetch_all(ids):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(f"/api/resource/{id}") for id in ids]
        responses = await asyncio.gather(*tasks)
        return [await r.json() for r in responses]
```

### Loading Large Files

```python
# Bad: Load entire file
content = open('large.csv').read()
process(content)

# Good: Stream line-by-line
for line in open('large.csv'):
    process_line(line)
```

## Tips

- **Always provide concrete numbers:** "100 queries" not "many queries"
- **Show before/after complexity:** O(n²) → O(n) with dataset size impact
- **Include working code examples:** Reviewers should be able to copy/paste fixes
- **Estimate real-world impact:** "2 seconds → 200ms on production dataset of 1000 items"
- **Prioritize by impact × likelihood:** High-impact issues in hot paths first
- **Consider data size:** O(n²) is fine for n=10, terrible for n=10,000
- **Profile when uncertain:** Don't optimize prematurely, measure first
