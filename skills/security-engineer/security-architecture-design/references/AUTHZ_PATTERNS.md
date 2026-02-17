# Authorization Architecture Patterns

## Overview

Authorization determines what authenticated users are allowed to do. This document covers RBAC, ABAC, ReBAC, and PBAC patterns.

## Pattern Selection Guide

| Model | Complexity | Flexibility | Best For | Example Use Case |
|-------|------------|-------------|----------|------------------|
| RBAC | Low | Medium | Fixed organizational roles | Corporate applications, admin panels |
| ABAC | High | High | Context-dependent access | Healthcare, financial services |
| ReBAC | Medium | Medium | Social/collaborative apps | Document sharing, social networks |
| PBAC | High | Very High | Complex enterprise needs | Multi-tenant SaaS, regulatory compliance |

## Pattern 1: Role-Based Access Control (RBAC)

**Concept:** Users are assigned roles, roles have permissions.

**Architecture:**
```
User → assigned to → Role → has → Permissions → control access to → Resources
```

**Simple RBAC Example:**
```
Roles:
- Admin: Can read/write/delete all resources
- Editor: Can read/write own resources
- Viewer: Can read public resources

Permissions:
- users:read, users:write, users:delete
- documents:read, documents:write, documents:delete
- reports:read, reports:generate

Role Assignments:
Admin → users:*, documents:*, reports:*
Editor → documents:read, documents:write, reports:read
Viewer → documents:read (public only)
```

**Hierarchical RBAC:**
```
Admin (inherits Manager permissions)
  └── Manager (inherits User permissions)
      └── User (inherits Guest permissions)
          └── Guest
```

**Implementation:**
```python
class RBACAuthorizer:
    def __init__(self):
        self.roles = {
            'admin': ['users:*', 'documents:*', 'reports:*'],
            'editor': ['documents:read', 'documents:write', 'reports:read'],
            'viewer': ['documents:read']
        }
    
    def can_access(self, user_role, resource, action):
        permissions = self.roles.get(user_role, [])
        required_permission = f"{resource}:{action}"
        
        # Check for wildcard permission
        if f"{resource}:*" in permissions:
            return True
        
        # Check for specific permission
        if required_permission in permissions:
            return True
        
        return False
```

**Pros:**
- Simple to understand and implement
- Easy to manage (assign roles, not individual permissions)
- Good for most applications
- Clear separation of duties

**Cons:**
- Role explosion (too many roles)
- Difficult to handle exceptions
- Context-insensitive (doesn't consider time, location, etc.)
- Rigid for dynamic scenarios

## Pattern 2: Attribute-Based Access Control (ABAC)

**Concept:** Access decisions based on attributes of user, resource, action, and environment.

**Architecture:**
```
Policy Engine evaluates:
- User attributes (role, department, clearance level)
- Resource attributes (classification, owner, sensitivity)
- Action attributes (read, write, delete)
- Environmental attributes (time, location, IP)
→ Grant or Deny
```

**ABAC Policy Example:**
```json
{
  "policy": "Allow access to medical records",
  "rules": [
    {
      "effect": "allow",
      "conditions": {
        "user.department": "healthcare",
        "user.clearance": ["doctor", "nurse"],
        "resource.type": "medical_record",
        "resource.patient_id": "user.assigned_patients",
        "environment.location": "hospital_network",
        "environment.time": "working_hours"
      }
    }
  ]
}
```

**Implementation with Open Policy Agent (OPA):**
```rego
# Allow doctors to read medical records of their assigned patients
allow {
    input.user.role == "doctor"
    input.action == "read"
    input.resource.type == "medical_record"
    input.resource.patient_id in input.user.assigned_patients
    is_working_hours(input.environment.time)
}

# Allow admins to do anything
allow {
    input.user.role == "admin"
}
```

**Attribute Categories:**
- **User:** role, department, clearance, groups
- **Resource:** type, owner, sensitivity, classification
- **Action:** read, write, delete, execute
- **Environment:** time, location, IP, device, risk score

**Pros:**
- Highly flexible and dynamic
- Context-aware (time, location, etc.)
- Handles complex scenarios
- Fine-grained control

**Cons:**
- Complex to implement and maintain
- Performance overhead (policy evaluation)
- Difficult to audit ("why was access denied?")
- Requires mature policy management

## Pattern 3: Relationship-Based Access Control (ReBAC)

**Concept:** Access based on relationships between users and resources.

**Architecture:**
```
User → has relationship → Resource
Examples:
- User "owns" Document
- User "is member of" Team
- Team "has access to" Project
```

**ReBAC Graph Example:**
```
User: Alice
  → owns → Document A
  → member_of → Team Engineering
  
Team: Engineering
  → can_read → Project X
  → can_write → Repository Y
  
Result: Alice can read Project X (through team membership)
```

**Implementation with Zanzibar-style:**
```
# Define relationships
User:alice#member@Team:engineering
Team:engineering#viewer@Document:123
User:alice#owner@Document:456

# Check permission
Can User:alice view Document:123?
→ YES (because alice is member of engineering, engineering is viewer of doc 123)

Can User:alice edit Document:123?
→ NO (viewer relation doesn't grant edit)

Can User:alice edit Document:456?
→ YES (alice is owner of doc 456)
```

**Common Relations:**
- **owner** - Full control
- **editor** - Can modify
- **viewer** - Can read
- **member** - Belongs to group
- **admin** - Group administrator

**Pros:**
- Natural for collaborative apps
- Flexible relationship modeling
- Supports transitive permissions (group membership)
- Easy to understand ("alice owns this")

**Cons:**
- Relationship graph can grow complex
- Performance concerns with deep hierarchies
- Requires relationship management UI
- Can be confusing with circular relationships

## Pattern 4: Policy-Based Access Control (PBAC)

**Concept:** Access controlled by explicitly defined policies, often using policy languages.

**Architecture:**
```
Policy Repository → Policy Decision Point (PDP) → Policy Enforcement Point (PEP)
```

**XACML Policy Example:**
```xml
<Policy PolicyId="FinancialDataAccess">
  <Target>
    <Resources>
      <Resource>financial_data</Resource>
    </Resources>
  </Target>
  
  <Rule RuleId="AllowFinanceTeam" Effect="Permit">
    <Condition>
      <Apply FunctionId="string-equal">
        <AttributeValue>finance</AttributeValue>
        <AttributeDesignator AttributeId="user.department"/>
      </Apply>
    </Condition>
  </Rule>
  
  <Rule RuleId="DenyOutsideBusinessHours" Effect="Deny">
    <Condition>
      <Apply FunctionId="time-in-range">
        <AttributeDesignator AttributeId="current.time"/>
        <AttributeValue>09:00:00</AttributeValue>
        <AttributeValue>17:00:00</AttributeValue>
      </Apply>
    </Condition>
  </Rule>
</Policy>
```

**OPA (Open Policy Agent) Example:**
```rego
package authz

default allow = false

# Allow if user is in finance department during business hours
allow {
    input.user.department == "finance"
    input.resource.type == "financial_data"
    is_business_hours(input.time)
    is_trusted_network(input.ip)
}

# Allow admins anytime from any network
allow {
    input.user.role == "admin"
}

# Deny if risk score is too high
deny {
    input.risk_score > 80
}

# Final decision: allow if not explicitly denied
final_decision = allow {
    not deny
}
```

**Pros:**
- Maximum flexibility
- Centralized policy management
- Auditable (policies are explicit)
- Supports complex business rules

**Cons:**
- Most complex to implement
- Requires policy language expertise
- Performance overhead
- Difficult to debug policies

## Authorization Enforcement Points

### API Gateway (Centralized)

**Architecture:**
```
Client → API Gateway (enforce authz) → Backend Service (optional additional checks)
```

**Pros:**
- Centralized policy enforcement
- Consistent across all services
- Reduces backend code

**Cons:**
- Single point of failure
- Gateway needs all context
- May not have resource-specific context

**Example (Kong + OPA):**
```
GET /api/documents/123
→ API Gateway extracts JWT
→ Gateway calls OPA with: user, resource, action
→ OPA evaluates policy
→ If allowed, forward to backend
→ If denied, return 403 Forbidden
```

### Application Layer (Distributed)

**Architecture:**
```
Client → Backend Service → Check authz → Access database
```

**Pros:**
- Full context available (resource state)
- Fine-grained control
- Can make complex decisions

**Cons:**
- Decentralized (harder to audit)
- Duplicated logic across services
- Performance overhead

**Example (Python decorator):**
```python
@require_permission("documents:read")
def get_document(document_id):
    document = db.get_document(document_id)
    
    # Additional resource-based check
    if not current_user.can_access(document):
        raise Forbidden("You don't have access to this document")
    
    return document
```

### Hybrid (Gateway + Application)

**Architecture:**
```
Client → API Gateway (basic checks) → Backend (detailed checks)
```

**Best Practice:**
- Gateway: Authentication, rate limiting, basic authorization (role checks)
- Application: Resource-specific authorization (owner checks, complex policies)

## Authorization Patterns by Use Case

### Multi-Tenancy

**Pattern:** Tenant isolation + RBAC within tenant

```
User → belongs to → Tenant → has → Roles → have → Permissions
```

**Implementation:**
```python
def authorize_request(user, tenant_id, resource, action):
    # 1. Verify user belongs to tenant
    if user.tenant_id != tenant_id:
        return False
    
    # 2. Check role-based permissions within tenant
    user_role = user.get_role_in_tenant(tenant_id)
    required_permission = f"{resource}:{action}"
    
    return user_role.has_permission(required_permission)
```

### Document Sharing (Google Docs-style)

**Pattern:** Ownership + Share links + Granular permissions

```
User: alice@example.com
  → owner → Document 123
  → editor → Document 456 (shared by bob)
  
Document 123:
  → owner: alice@example.com
  → editors: [bob@example.com]
  → viewers: [charlie@example.com]
  → link: anyone_with_link (viewer)
```

### Hierarchical Organizations

**Pattern:** Organizational hierarchy + Inheritance

```
CEO → can access all
  └── VP Engineering → can access engineering resources
      └── Engineering Manager → can access team resources
          └── Engineer → can access own resources
```

## Best Practices

### 1. Principle of Least Privilege

- Grant minimum necessary permissions
- Default deny (explicit allow)
- Regular access reviews
- Time-bound access for elevated privileges

### 2. Separation of Duties

- Split sensitive operations across multiple roles
- Require approval for critical actions
- Prevent conflicts of interest
- Audit privileged operations

### 3. Defense in Depth

- Multiple authorization checks (gateway + application)
- Verify at every layer
- Don't trust client-side checks
- Re-authorize for sensitive operations

### 4. Fail Securely

- Default deny on error
- Log authorization failures
- Graceful degradation
- Clear error messages (without leaking info)

### 5. Audit and Monitor

- Log all authorization decisions
- Monitor for anomalies (unusual access patterns)
- Regular access reviews
- Alert on policy violations

## Anti-Patterns to Avoid

**DON'T:**
- ❌ Rely on client-side authorization checks
- ❌ Use user input directly in authorization decisions
- ❌ Forget to authorize at backend
- ❌ Grant overly broad permissions
- ❌ Hardcode authorization logic in code
- ❌ Ignore authorization for internal APIs
- ❌ Allow privilege escalation through parameter manipulation

**DO:**
- ✅ Enforce authorization server-side
- ✅ Use indirect references (not user-supplied IDs)
- ✅ Centralize authorization logic
- ✅ Follow least privilege principle
- ✅ Use policy engines for complex scenarios
- ✅ Audit all authorization decisions
- ✅ Test authorization thoroughly
