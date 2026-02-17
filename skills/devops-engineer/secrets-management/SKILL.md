---
name: secrets-management
description: |
  Implement production-grade secrets management using HashiCorp Vault, AWS Secrets Manager, Google Secret Manager,
  or Kubernetes secrets. Handles secret rotation, access policies, encryption, audit logging, and secure injection
  into applications without exposing secrets in code or configuration files.

  Use when: managing API keys, passwords, certificates, implementing secret rotation, configuring Vault, setting up
  secrets injection, or when user mentions secrets, credentials, API keys, passwords, certificates, Vault, AWS Secrets Manager,
  secret rotation, secret injection, environment variables, or secure configuration.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Secrets Management

Implement secure secrets management systems that store, rotate, and inject secrets into applications without hardcoding them in source code, configuration files, or environment variables.

## Core Implementation Areas

### 1. Secrets Backend Selection

**Choose based on environment and requirements:**

**HashiCorp Vault:**
- **Best for**: Multi-cloud, complex access policies, dynamic secrets
- **Deployment**: Self-hosted (HA cluster) or HCP Vault (managed)
- **Features**: Dynamic secrets, secret rotation, encryption-as-a-service
- **Cost**: Free (open source) or ~$0.03/hour per cluster (HCP)
- **Learning curve**: Steep, but most flexible

**AWS Secrets Manager:**
- **Best for**: AWS-native applications, automatic RDS rotation
- **Integration**: Native with RDS, Lambda, ECS, EC2
- **Features**: Automatic rotation for RDS/DocumentDB/Redshift
- **Cost**: $0.40/secret/month + $0.05/10,000 API calls
- **Learning curve**: Low for AWS users

**Google Secret Manager:**
- **Best for**: GCP-native applications, GKE integration
- **Integration**: Native with Cloud Run, GKE, Cloud Functions
- **Features**: Automatic versioning, replication
- **Cost**: $0.06/10,000 accesses (first 10,000 free)
- **Learning curve**: Low for GCP users

**Azure Key Vault:**
- **Best for**: Azure-native applications, certificate management
- **Integration**: Native with Azure services
- **Features**: HSM-backed keys (FIPS 140-2)
- **Cost**: $0.03/10,000 operations
- **Learning curve**: Low for Azure users

**Kubernetes Secrets + External Secrets Operator:**
- **Best for**: Kubernetes-only, sync from external backends
- **Integration**: Native Kubernetes resources
- **Features**: Syncs from Vault/AWS/GCP to K8s secrets
- **Cost**: Free (open source)
- **Learning curve**: Low for Kubernetes users

**Decision matrix:**
- Multi-cloud? → Vault
- AWS-only? → AWS Secrets Manager
- GCP-only? → Google Secret Manager
- Azure-only? → Azure Key Vault
- Kubernetes-only? → External Secrets Operator

### 2. Vault Deployment & Configuration

**Deployment options:**

**Development mode** (NOT for production):
```bash
vault server -dev -dev-root-token-id="root"
```

**Production HA cluster:**
- 3-5 Vault servers for high availability
- Integrated Raft storage or Consul backend
- Auto-unseal with cloud KMS
- Load balancer in front

**Example Kubernetes deployment:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: vault-config
data:
  vault.hcl: |
    storage "raft" {
      path = "/vault/data"
    }

    listener "tcp" {
      address = "0.0.0.0:8200"
      tls_cert_file = "/vault/tls/tls.crt"
      tls_key_file = "/vault/tls/tls.key"
    }

    api_addr = "https://vault:8200"
    cluster_addr = "https://vault:8201"

    ui = true
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vault
spec:
  serviceName: vault
  replicas: 3
  template:
    spec:
      containers:
      - name: vault
        image: hashicorp/vault:1.15
        args:
        - server
        - -config=/vault/config/vault.hcl
        ports:
        - containerPort: 8200
          name: http
        - containerPort: 8201
          name: cluster
        volumeMounts:
        - name: config
          mountPath: /vault/config
        - name: data
          mountPath: /vault/data
        - name: tls
          mountPath: /vault/tls
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

**Initialization (one-time):**
```bash
# Initialize Vault (generates unseal keys and root token)
vault operator init -key-shares=5 -key-threshold=3

# Unseal Vault (requires 3 of 5 keys)
vault operator unseal <key-1>
vault operator unseal <key-2>
vault operator unseal <key-3>

# Configure auto-unseal with AWS KMS (recommended)
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "alias/vault-unseal"
}
```

**IMPORTANT: Store unseal keys securely:**
- Split among 5 trusted custodians
- Store in password manager (1Password, LastPass)
- Never commit to git
- Use auto-unseal in production (AWS KMS, GCP KMS)

### 3. Access Control & Authentication

**Authentication methods:**

**Kubernetes (for pods):**
```hcl
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure Kubernetes auth
vault write auth/kubernetes/config \
    kubernetes_host="https://kubernetes.default.svc:443" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
    token_reviewer_jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token

# Create role for application
vault write auth/kubernetes/role/myapp \
    bound_service_account_names=myapp \
    bound_service_account_namespaces=production \
    policies=myapp-policy \
    ttl=1h
```

**AWS IAM (for EC2, Lambda):**
```hcl
# Enable AWS auth
vault auth enable aws

# Create role for EC2 instances
vault write auth/aws/role/myapp \
    auth_type=iam \
    bound_iam_principal_arn=arn:aws:iam::123456789012:role/myapp-role \
    policies=myapp-policy \
    ttl=1h
```

**Access policies (least privilege):**
```hcl
# Policy for application to read secrets
path "secret/data/myapp/*" {
  capabilities = ["read"]
}

# Policy for CI/CD to write secrets
path "secret/data/myapp/*" {
  capabilities = ["create", "update"]
}

# Policy for dynamic database credentials
path "database/creds/myapp-db" {
  capabilities = ["read"]
}
```

**Apply policies:**
```bash
vault policy write myapp-policy myapp-policy.hcl
```

### 4. Secret Storage & Organization

**Organize secrets hierarchically:**
```
secret/
├── production/
│   ├── myapp/
│   │   ├── database-password
│   │   ├── api-key
│   │   ├── jwt-secret
│   ├── shared/
│   │   └── third-party-api-key
├── staging/
│   └── myapp/
│       └── database-password
└── development/
    └── myapp/
        └── database-password
```

**Writing secrets to Vault:**
```bash
# Write single secret
vault kv put secret/production/myapp/database-password value="supersecret123"

# Write multiple fields
vault kv put secret/production/myapp/api-keys \
    stripe_key="sk_live_..." \
    sendgrid_key="SG...."

# Read secret
vault kv get secret/production/myapp/database-password

# List secrets
vault kv list secret/production/myapp/
```

**Metadata for tracking:**
```bash
vault kv metadata put secret/production/myapp/database-password \
    custom_metadata=owner="platform-team" \
    custom_metadata=rotation_frequency="90days" \
    custom_metadata=created="2024-02-08"
```

**AWS Secrets Manager:**
```bash
# Create secret
aws secretsmanager create-secret \
    --name production/myapp/database-password \
    --secret-string "supersecret123"

# Retrieve secret
aws secretsmanager get-secret-value \
    --secret-id production/myapp/database-password
```

**Google Secret Manager:**
```bash
# Create secret
echo -n "supersecret123" | gcloud secrets create myapp-db-password \
    --data-file=-

# Access secret
gcloud secrets versions access latest --secret="myapp-db-password"
```

### 5. Secret Injection into Applications

**Method 1: Kubernetes Secrets (External Secrets Operator)**

Install External Secrets Operator:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "myapp"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: myapp-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-password
    remoteRef:
      key: production/myapp/database-password
      property: value
```

Application uses standard Kubernetes secret:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: myapp
    image: myapp:latest
    env:
    - name: DATABASE_PASSWORD
      valueFrom:
        secretKeyRef:
          name: myapp-secrets
          key: database-password
```

**Method 2: Vault Agent Sidecar**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  serviceAccountName: myapp
  containers:
  - name: myapp
    image: myapp:latest
    volumeMounts:
    - name: secrets
      mountPath: /vault/secrets
  - name: vault-agent
    image: hashicorp/vault:1.15
    args:
    - agent
    - -config=/vault/config/agent.hcl
    volumeMounts:
    - name: vault-config
      mountPath: /vault/config
    - name: secrets
      mountPath: /vault/secrets
  volumes:
  - name: secrets
    emptyDir: {}
  - name: vault-config
    configMap:
      name: vault-agent-config
```

**Method 3: Application SDK (direct fetch)**
```python
import hvac

# Initialize Vault client
client = hvac.Client(url='https://vault:8200')

# Authenticate with Kubernetes
with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as f:
    jwt = f.read()

client.auth.kubernetes.login(
    role='myapp',
    jwt=jwt
)

# Read secret
secret = client.secrets.kv.v2.read_secret_version(
    path='production/myapp/database-password'
)
db_password = secret['data']['data']['value']
```

**AWS Secrets Manager SDK:**
```python
import boto3
import json

client = boto3.client('secretsmanager')

response = client.get_secret_value(
    SecretId='production/myapp/database-password'
)

secret = json.loads(response['SecretString'])
db_password = secret['password']
```

### 6. Secret Rotation

**Automatic rotation strategies:**

**Vault dynamic database credentials:**
```hcl
# Configure database backend
vault write database/config/mydb \
    plugin_name=postgresql-database-plugin \
    allowed_roles="myapp-db" \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb" \
    username="vault" \
    password="vaultpass"

# Create role that generates temporary credentials
vault write database/roles/myapp-db \
    db_name=mydb \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

# Application requests credentials (new every hour)
vault read database/creds/myapp-db
```

**AWS Secrets Manager automatic rotation:**
```bash
# Enable automatic rotation for RDS password
aws secretsmanager rotate-secret \
    --secret-id production/myapp/rds-password \
    --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:SecretsManagerRDSRotation \
    --rotation-rules AutomaticallyAfterDays=30
```

**Manual rotation workflow:**
1. Generate new secret value
2. Update application to use new secret (rolling update)
3. Verify application works with new secret
4. Deactivate old secret (wait 7 days before deletion)

**Rotation frequency recommendations:**
- Database passwords: 90 days
- API keys: Annually or on suspected compromise
- TLS certificates: 90 days (Let's Encrypt auto-renews at 60 days)
- SSH keys: Daily (use Vault SSH CA)

### 7. Audit Logging & Compliance

**Enable Vault audit logging:**
```hcl
# File audit device
vault audit enable file file_path=/vault/logs/audit.log

# Syslog audit device
vault audit enable syslog

# Socket audit device (send to log aggregation)
vault audit enable socket address=logstash:9000 socket_type=tcp
```

**Audit log contents:**
- Timestamp, request ID
- Authentication method and identity
- Operation (read, write, delete)
- Path accessed (secret/data/production/myapp/database-password)
- Success or failure
- Client IP address

**Compliance reports:**
- Who accessed which secrets? (monthly report)
- Which secrets haven't been rotated? (quarterly report)
- Unusual access patterns? (real-time alerts)

**Forward audit logs to centralized logging:**
```yaml
# Fluent Bit configuration
[INPUT]
    Name   tail
    Path   /vault/logs/audit.log
    Parser json

[OUTPUT]
    Name   loki
    Match  *
    Host   loki.monitoring.svc
    Port   3100
    Labels job=vault-audit
```

**Compliance requirements:**
- SOC2: Retain audit logs for 7 years
- HIPAA: Retain for 6 years
- PCI-DSS: Retain for 1 year, 3 months readily available

### 8. Disaster Recovery & Backup

**Vault backups (Raft storage):**
```bash
# Take snapshot
vault operator raft snapshot save backup.snap

# Restore snapshot
vault operator raft snapshot restore backup.snap

# Automate with cron
0 2 * * * /usr/local/bin/vault operator raft snapshot save /backups/vault-$(date +\%Y\%m\%d).snap
```

**AWS Secrets Manager:**
- Automatic replication to multiple regions
- Point-in-time recovery via secret versions

**Kubernetes etcd backup (for K8s secrets):**
```bash
# Backup etcd
ETCDCTL_API=3 etcdctl snapshot save etcd-backup.db \
    --endpoints=https://127.0.0.1:2379 \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key

# Restore etcd
ETCDCTL_API=3 etcdctl snapshot restore etcd-backup.db --data-dir=/var/lib/etcd-restore
```

**Recovery testing:**
- Test restore procedure quarterly
- Document RTO (< 4 hours) and RPO (< 24 hours)
- Practice in staging environment

### 9. Encryption & Security Hardening

**Encryption layers:**

**In transit:**
- TLS 1.3 for all Vault communication
- Mutual TLS (mTLS) for service-to-service

**At rest:**
- Vault: Auto-unseal with KMS, encrypted Raft storage
- AWS: Server-side encryption with KMS
- Kubernetes: Enable etcd encryption at rest

**Enable etcd encryption (Kubernetes):**
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-encoded-32-byte-key>
      - identity: {}
```

**Security hardening checklist:**
- [ ] Network policies restrict access to secrets backend
- [ ] Firewall rules whitelist only necessary IPs
- [ ] Rate limiting prevents brute force attacks
- [ ] Secret scanning enabled in CI/CD (TruffleHog, GitGuardian)
- [ ] Root credentials never used by applications
- [ ] Regular security audits (quarterly)

### 10. Migration from Existing Secret Storage

**Migration workflow:**

**Phase 1: Inventory**
```bash
# Scan codebase for hardcoded secrets
trufflehog git file://. --only-verified

# Find environment variables with secrets
grep -r "API_KEY\|PASSWORD\|SECRET" .env* docker-compose.yml
```

**Phase 2: Create secrets in new backend**
```bash
# Vault
vault kv put secret/production/myapp/api-key value="existing-key"

# AWS
aws secretsmanager create-secret \
    --name production/myapp/api-key \
    --secret-string "existing-key"
```

**Phase 3: Update application code**
```python
# Before (hardcoded)
API_KEY = "sk_live_abc123"

# After (fetch from Vault)
import hvac
client = hvac.Client()
secret = client.secrets.kv.v2.read_secret_version(path='production/myapp/api-key')
API_KEY = secret['data']['data']['value']
```

**Phase 4: Test in staging, deploy to production**
- Gradual rollout (one service at a time)
- Monitor for errors
- Keep old secrets active during transition

**Phase 5: Cleanup**
```bash
# Remove secrets from environment files
rm .env.production

# Clean git history (if secrets were committed)
bfg --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

## Implementation Workflow

### Phase 1: Assessment

Ask the user:
1. What secrets need to be managed? (API keys, passwords, certificates)
2. Where are secrets currently stored? (code, .env files, environment variables)
3. What is the deployment environment? (Kubernetes, AWS, GCP, Azure)
4. Compliance requirements? (SOC2, HIPAA, PCI-DSS)
5. Team size and access patterns?

### Phase 2: Design

1. Select secrets backend based on environment
2. Design secret organization structure (environment/app/secret-name)
3. Define access policies (who/what can access which secrets)
4. Plan rotation strategy (frequency per secret type)
5. Choose injection method (sidecar, CSI, SDK)

### Phase 3: Deployment

1. Deploy secrets backend (Vault cluster, enable AWS/GCP services)
2. Configure authentication methods (Kubernetes, IAM, service accounts)
3. Create access policies (least privilege)
4. Enable audit logging
5. Set up backup and disaster recovery

### Phase 4: Integration

1. Migrate secrets from old storage to new backend
2. Update applications to fetch secrets (External Secrets, SDK)
3. Test in development/staging
4. Gradual rollout to production (one service at a time)
5. Verify no secrets remain in code/config files

### Phase 5: Operationalization

1. Set up monitoring and alerting (failed authentications, rotation failures)
2. Document rotation procedures
3. Schedule regular audits (quarterly)
4. Train team on best practices
5. Test disaster recovery (restore from backup)

## Quality Checklist

Before considering the implementation complete, verify:

- [ ] No hardcoded secrets in code or configuration files
- [ ] All secrets encrypted at rest and in transit (TLS)
- [ ] Least-privilege access policies enforced
- [ ] Audit logging enabled and forwarded to centralized logging
- [ ] Rotation policies configured (database passwords quarterly, certificates annually)
- [ ] Backup and restore procedures documented and tested
- [ ] Monitoring and alerting configured (unusual access, rotation failures)
- [ ] Team trained on secrets management best practices
- [ ] Code scanned for secrets (TruffleHog, GitGuardian clean)
- [ ] Disaster recovery tested (restore from backup works)

## Common Patterns

### Pattern 1: Kubernetes + External Secrets Operator + Vault
- Vault stores secrets
- External Secrets Operator syncs to Kubernetes secrets
- Applications use standard K8s secret mounting
- **Benefit**: No application code changes

### Pattern 2: AWS ECS + Secrets Manager
- Secrets stored in AWS Secrets Manager
- ECS task definition references secrets
- Secrets injected as environment variables
- Automatic rotation with Lambda

### Pattern 3: Vault Dynamic Database Credentials
- Vault generates temporary database credentials
- Credentials expire after TTL (1 hour)
- No shared passwords
- Automatic revocation on pod termination

### Pattern 4: Multi-Cloud with Vault
- Vault as central secrets backend
- AWS, GCP, Azure services authenticate to Vault
- Consistent secrets management across clouds
- **Benefit**: Cloud-agnostic

## Anti-Patterns to Avoid

❌ **Hardcoded secrets in source code**
✅ **Fetch from secrets backend (Vault, AWS, GCP)**

❌ **Secrets in environment variables** (visible in `ps`, logs, crash dumps)
✅ **Mount as files with restricted permissions**

❌ **Shared database password across all apps**
✅ **Unique credentials per application (dynamic credentials preferred)**

❌ **Never rotating secrets** (same password for years)
✅ **Automatic rotation (quarterly for passwords, annually for keys)**

❌ **No audit logging** (can't determine who accessed secrets)
✅ **Comprehensive audit logs forwarded to centralized logging**

❌ **Using root token in applications**
✅ **Scoped tokens with minimal permissions**

❌ **Base64-encoded K8s secrets without encryption**
✅ **Enable etcd encryption or use External Secrets Operator**

## Key Technologies

**Secrets Backends:**
- HashiCorp Vault (open source + enterprise)
- AWS Secrets Manager, Systems Manager Parameter Store
- Google Secret Manager
- Azure Key Vault

**Integration Tools:**
- External Secrets Operator
- Vault Agent, Vault CSI Driver
- Sealed Secrets (Bitnami)
- SOPS (Mozilla)

**Secret Scanning:**
- TruffleHog, GitGuardian, Gitleaks
- GitHub secret scanning
- AWS Secrets Manager secret detection

## Success Criteria

The secrets management system is production-ready when:
- Security: No secrets in code, all encrypted at rest/transit
- Access control: Least-privilege policies enforced
- Auditability: All access logged and retained per compliance
- Rotation: Automated rotation for all secrets
- Reliability: Backup tested, disaster recovery documented
- Observability: Monitoring and alerting configured
- Compliance: Meets SOC2/HIPAA/PCI-DSS requirements
- Team readiness: Trained on best practices
