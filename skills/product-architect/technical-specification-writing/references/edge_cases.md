# Edge Case Catalog

Comprehensive edge case patterns and solutions for technical specifications.

## Table of Contents
- [Concurrent Operations](#concurrent-operations)
- [Token and Session Management](#token-and-session-management)
- [System State Conflicts](#system-state-conflicts)
- [Network and Connection Issues](#network-and-connection-issues)
- [Race Conditions](#race-conditions)

---

## Concurrent Operations

### 1. Concurrent Registrations with Same Email

**Problem:** Two requests to register the same email arrive simultaneously

**Without Solution:**
- Both requests check if email exists (both see "no")
- Both attempt to create user
- One succeeds, one fails with database constraint error
- Second user sees cryptic database error

**Solution:**
- Rely on database unique constraint on email
- Catch constraint violation exception
- Return 409 Conflict with clear message: "An account with this email already exists"
- Transaction ensures atomic check-and-create

**Implementation:**
```sql
-- Database constraint prevents duplicates
CREATE UNIQUE INDEX idx_users_email ON users(LOWER(email));
```

### 2. Duplicate Session Creation (Double Login)

**Problem:** User clicks login button twice quickly

**Without Solution:**
- Two sessions created
- Wastes resources
- Cleanup complexity

**Solution:**
- Use idempotency key (client-generated UUID)
- Cache processed keys in Redis (1-minute TTL)
- Return existing session if key already processed
- Frontend disables button after first click

---

## Token and Session Management

### 3. Email Verification Link Clicked Multiple Times

**Problem:** User clicks verification link multiple times (forwards email, clicks again by mistake)

**Without Solution:**
- First click consumes token
- Second click fails with "token not found"
- User confused

**Solution:**
- Check if email already verified
  - If yes: Return success with message "Email already verified"
  - If no: Verify email and return success
- Mark token as used but keep in database for audit trail
- Expired tokens return clear message: "Verification link expired. Request a new one."

### 4. Session Expiry During Active Request

**Problem:** User's session expires while they're in the middle of an operation

**Without Solution:**
- Request fails mid-flight
- Partial data might be saved
- User confused about state

**Solution:**
- Validate session at request start
- Use database transactions for multi-step operations
- If session expires mid-request, transaction rolls back
- Return 401 with message: "Session expired. Please log in again."
- Frontend refreshes token or redirects to login

### 5. Password Reset Token Used After Password Changed

**Problem:** User requests password reset, then changes password through account settings, then uses stale reset link

**Without Solution:**
- Reset link still works
- Could allow unintended password change

**Solution:**
- Include password hash version in reset token
- When password changes, increment version
- Validate version when processing reset token
- If version mismatch: Return error "This reset link is no longer valid"

### 6. Clock Skew Between Server and Client

**Problem:** JWT validation fails because server and client clocks are out of sync

**Without Solution:**
- Valid tokens rejected as expired
- Users can't log in

**Solution:**
- Add 5-minute leeway to JWT validation
- Accept tokens that expired up to 5 minutes ago
- Accept tokens with `nbf` (not before) up to 5 minutes in future
- Log warnings when leeway is used (indicates clock drift)

**Implementation:**
```javascript
jwt.verify(token, secret, {
  clockTolerance: 300  // 5 minutes in seconds
});
```

---

## System State Conflicts

### 7. User Deletes Account While Logged In on Other Devices

**Problem:** User deletes account on web, but still has active sessions on mobile

**Without Solution:**
- Mobile sessions still work
- User can still access "deleted" account

**Solution:**
- ON DELETE CASCADE on sessions table
- When user deleted, all sessions deleted automatically
- Active requests return 401 "User not found"
- Frontend detects and redirects to login

**Schema:**
```sql
CREATE TABLE sessions (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    ...
);
```

### 8. Race Condition on Profile Update

**Problem:** User updates profile from two devices simultaneously

**Without Solution:**
- Last write wins
- One update silently lost

**Solution:**
- Optimistic locking with version field
- Include version in update condition
- Return 409 Conflict if version mismatch
- Client fetches latest and prompts user to retry

**Schema:**
```sql
ALTER TABLE profiles ADD COLUMN version INTEGER DEFAULT 1;

-- Update query
UPDATE profiles
SET name = ?, bio = ?, version = version + 1
WHERE id = ? AND version = ?;

-- If rowcount = 0, conflict occurred
```

---

## Network and Connection Issues

### 9. Partial Email Service Failure

**Problem:** Email sent successfully but database update to mark it sent fails

**Without Solution:**
- User receives multiple verification emails
- Confusion and poor UX

**Solution:**
- Use idempotency key for email sending
- Store sent email records in database first (pending state)
- Send email
- Update record to sent state
- If sending fails, background job retries
- SendGrid deduplicates based on idempotency key

**Flow:**
```
1. INSERT INTO email_log (id, user_id, type, status) VALUES (..., 'pending')
2. Send email with idempotency_key = email_log.id
3. UPDATE email_log SET status = 'sent' WHERE id = ...
```

### 10. Database Connection Lost Mid-Transaction

**Problem:** Connection to database drops while writing data

**Without Solution:**
- Partial data written
- Inconsistent state

**Solution:**
- Wrap all multi-step operations in database transactions
- Set transaction timeout (10 seconds)
- On connection loss, transaction automatically rolls back
- Return 500 error to client
- Client retries with idempotency key

**Implementation:**
```python
with db.transaction():
    user = create_user(email, password)
    profile = create_profile(user.id, name)
    send_verification_email(user.email)
# Automatic rollback if any step fails
```

---

## Edge Case Checklist

When documenting edge cases in specifications:

- [ ] Identify the problem with concrete scenario
- [ ] Describe failure mode without solution
- [ ] Provide specific solution with code/schema
- [ ] Include implementation notes where relevant
- [ ] Consider both technical and user impact
- [ ] Document prevention strategies
- [ ] Add monitoring/alerting requirements if needed
