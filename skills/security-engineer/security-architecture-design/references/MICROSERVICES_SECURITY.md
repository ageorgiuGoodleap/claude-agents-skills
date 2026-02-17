# Microservices Security Architecture Patterns

## Zero-Trust Principles for Microservices

1. **Never trust, always verify** - Authenticate every request, even internal
2. **Least privilege** - Each service has minimal permissions
3. **Assume breach** - Limit blast radius with segmentation
4. **Encrypt everything** - TLS for all communication
5. **Monitor and audit** - Complete visibility into all access

## Service Mesh with mTLS

**Architecture:**
```
Service A [App + Sidecar Proxy] --mTLS--> [Sidecar Proxy + App] Service B
```

**Benefits:**
- Automatic encryption (TLS for all traffic)
- Mutual authentication (both ends verify)
- Service identity (certificate-based)
- Traffic control (routing, retries, timeouts)
- Observability (metrics, tracing, logs)

**Popular Service Mesh Solutions:**
- Istio
- Linkerd
- Consul Connect
- AWS App Mesh

**mTLS Certificate Lifecycle:**
1. Service starts
2. Sidecar requests certificate from CA (SPIFFE/SPIRE)
3. CA issues short-lived certificate (24 hours)
4. Sidecar automatically rotates certificate before expiration
5. All service-to-service traffic uses mTLS

**No changes to application code required!**

## Service Identity with SPIFFE/SPIRE

**SPIFFE (Secure Production Identity Framework for Everyone):**
- Standard for service identity
- Identity format: `spiffe://trust-domain/path/to/service`
- Example: `spiffe://prod.example.com/users/api`

**SPIRE (SPIFFE Runtime Environment):**
- Implements SPIFFE specification
- Issues and rotates X.509 certificates
- Automatic workload attestation
- Zero-touch certificate management

**Benefits:**
- No long-lived secrets
- Automatic rotation
- Strong cryptographic identity
- Platform-agnostic

## Service-to-Service Authorization

### Pattern 1: JWT with Service Scopes

**Flow:**
```
1. Service A obtains JWT (from auth service or issuer)
2. JWT contains service identity and allowed actions
3. Service A calls Service B with JWT in Authorization header
4. Service B validates JWT signature and checks scopes
5. If authorized, Service B processes request
```

**JWT Structure:**
```json
{
  "iss": "https://auth.example.com",
  "sub": "service:users-api",
  "aud": "service:orders-api",
  "exp": 1625097600,
  "scope": "read:orders write:orders"
}
```

**Validation in Service B:**
```python
def authorize_request(jwt, required_scope):
    # 1. Verify JWT signature
    payload = verify_jwt_signature(jwt)
    
    # 2. Check expiration
    if payload['exp'] < time.time():
        raise Unauthorized("Token expired")
    
    # 3. Check audience (is this token for me?)
    if payload['aud'] != 'service:orders-api':
        raise Unauthorized("Invalid audience")
    
    # 4. Check scope
    if required_scope not in payload['scope']:
        raise Forbidden("Insufficient scope")
    
    return True
```

### Pattern 2: Service Mesh Policy Enforcement

**Istio Authorization Policy Example:**
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: orders-api-policy
spec:
  selector:
    matchLabels:
      app: orders-api
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/users-api"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/orders/*"]
```

**Benefits:**
- Policy as code (version controlled)
- Centralized policy management
- Enforced at proxy level (no app changes)
- Deny-by-default

## Network Segmentation

**Kubernetes Network Policies:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: orders-api-policy
spec:
  podSelector:
    matchLabels:
      app: orders-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: users-api
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

**Effect:**
- orders-api can ONLY receive traffic from users-api
- orders-api can ONLY send traffic to database
- All other traffic is denied

## Secrets Management

**Anti-Pattern:**
```yaml
# DON'T hardcode secrets in config!
env:
- name: DATABASE_PASSWORD
  value: "super_secret_password"
```

**Best Practice - External Secrets:**
```yaml
# Kubernetes External Secrets
env:
- name: DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: database-credentials
      key: password
```

**Secret Management Solutions:**
- HashiCorp Vault
- AWS Secrets Manager
- Google Secret Manager
- Azure Key Vault
- Kubernetes External Secrets Operator

**Best Practices:**
- Rotate secrets regularly (90 days)
- Use dynamic secrets (Vault database credentials)
- Encrypt secrets at rest
- Audit secret access
- Principle of least privilege (service-specific secrets)

## Distributed Tracing for Security

**Purpose:** Track requests across microservices for security investigation.

**Key Information:**
- Trace ID (unique per request)
- Span ID (unique per service call)
- Service name
- Timestamp
- User ID / Service identity
- Request/response data

**Example (Jaeger/OpenTelemetry):**
```
Trace ID: 7a8e9f0b1c2d3e4f
├─ Span: api-gateway (duration: 245ms)
│  ├─ User: alice@example.com
│  └─ Action: POST /api/orders
├─ Span: users-api (duration: 50ms)
│  └─ Action: GET /api/users/123
├─ Span: orders-api (duration: 120ms)
│  ├─ Action: POST /api/orders
│  └─ Database query: INSERT INTO orders
└─ Span: notifications-api (duration: 75ms)
   └─ Action: POST /api/notifications
```

**Security Use Cases:**
- Investigate suspicious activity across services
- Trace unauthorized access attempts
- Identify compromised services
- Audit user actions end-to-end

## API Gateway for Microservices

**Responsibilities:**
- External authentication (user-facing)
- Rate limiting (prevent abuse)
- Request validation
- Routing to backend services
- Response aggregation
- TLS termination

**Pattern:**
```
External Client → [API Gateway] → [Service Mesh] → Backend Services
                   ↓
              [User Auth]
              [Rate Limit]
              [Validation]
```

**Security Controls:**
1. Gateway validates user JWT
2. Gateway adds service identity for internal calls
3. Gateway enforces rate limits
4. Internal services use mTLS
5. Service mesh enforces authorization policies

## Monitoring and Alerting

**What to Monitor:**
- Failed authentication attempts
- Authorization denials
- Unusual traffic patterns
- Certificate expiration
- Service health (crashes, errors)
- Resource exhaustion

**Example Alerts:**
```
Alert: High authentication failure rate
Condition: > 100 auth failures per minute from single IP
Action: Block IP, investigate

Alert: Service calling unauthorized endpoint
Condition: Service A calls endpoint it shouldn't access
Action: Alert security team, block traffic

Alert: Certificate expiration
Condition: Certificate expires in < 7 days
Action: Alert ops team, trigger rotation
```

## Best Practices Checklist

**Service-to-Service Communication:**
- [ ] mTLS for all internal traffic
- [ ] Service identity (SPIFFE)
- [ ] JWT-based authorization
- [ ] Network policies (deny-by-default)
- [ ] Distributed tracing enabled

**Secrets Management:**
- [ ] External secret store (Vault, etc.)
- [ ] No hardcoded secrets
- [ ] Secret rotation (90 days)
- [ ] Audit secret access
- [ ] Principle of least privilege

**Network Security:**
- [ ] Service mesh deployed
- [ ] Network segmentation
- [ ] Ingress/egress policies
- [ ] Zero-trust architecture
- [ ] Private subnets for internal services

**Monitoring:**
- [ ] Centralized logging (ELK, Splunk)
- [ ] Distributed tracing (Jaeger, Zipkin)
- [ ] SIEM integration
- [ ] Alerting configured
- [ ] Security dashboards

**Incident Response:**
- [ ] Runbooks for common incidents
- [ ] Automated rollback capability
- [ ] Circuit breakers configured
- [ ] Graceful degradation
- [ ] Post-incident review process
