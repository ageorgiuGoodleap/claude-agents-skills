---
name: container-orchestration
description: |
  Create production-grade Docker containers and Kubernetes deployments with multi-stage builds, Helm charts,
  auto-scaling, and resource management. Supports Docker, Kubernetes, Helm, ECS, and container best practices.

  Use when: containerizing applications, creating Dockerfiles, deploying to Kubernetes, writing Helm charts,
  setting up container orchestration, configuring auto-scaling, or when user mentions Docker, Kubernetes, K8s,
  containers, pods, deployments, services, ingress, Helm, containerize, orchestration, or ECS.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Container Orchestration

## Overview

Design and implement container-based deployments using Docker and Kubernetes. This skill covers Dockerfile optimization, Kubernetes manifest creation, Helm chart development, auto-scaling configuration, and production-grade container orchestration.

## Workflow

### 1. Analyze Application Requirements
- **Language/Framework**: Node.js, Python, Go, Java, .NET, Ruby, etc.
- **Runtime Dependencies**: System packages, libraries, tools
- **Build Process**: Compile steps, asset bundling, test execution
- **Entry Point**: Command to start the application
- **Environment Configuration**: Config files, environment variables
- **Persistence Needs**: Volumes for data, logs, uploads
- **Network Requirements**: Ports exposed, inter-service communication
- **Resource Estimates**: CPU, memory, storage requirements

### 2. Create Optimized Dockerfile

**Multi-Stage Build Pattern** (Recommended):
```dockerfile
# Stage 1: Build dependencies (large base image okay)
FROM node:18-alpine AS builder
# Install, build, compile

# Stage 2: Production runtime (minimal base image)
FROM node:18-alpine
# Copy only production artifacts from builder
# Smaller final image, faster deploys
```

**Dockerfile Best Practices:**
- Use specific image tags, never `:latest` (e.g., `node:18.19.0-alpine`)
- Run as non-root user for security
- Use `.dockerignore` to exclude unnecessary files
- Layer caching: Put frequently changing commands last
- Minimize layers: Combine RUN commands with `&&`
- Clean up caches in same layer: `apt-get clean && rm -rf /var/lib/apt/lists/*`

### 3. Test Docker Image Locally
```bash
# Build image
docker build -t myapp:dev .

# Run container
docker run -p 8080:8080 --env-file .env.local myapp:dev

# Verify it works
curl http://localhost:8080/health

# Check image size
docker images myapp:dev

# Scan for vulnerabilities
docker scout cves myapp:dev
# Or: trivy image myapp:dev
```

### 4. Design Kubernetes Manifests

**Required Resources:**
1. **Deployment**: Manages pod replicas, rolling updates
2. **Service**: Exposes pods to network traffic
3. **Ingress** (optional): HTTP routing, SSL termination
4. **ConfigMap**: Non-sensitive configuration
5. **Secret**: Sensitive data (API keys, passwords)

**Deployment Structure:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3  # Start with 3 for high availability
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.2.3
    spec:
      containers:
      - name: myapp
        image: registry.example.com/myapp:v1.2.3
        ports:
        - containerPort: 8080
        resources:
          requests:  # Guaranteed resources
            cpu: 100m
            memory: 128Mi
          limits:    # Maximum resources
            cpu: 500m
            memory: 512Mi
        livenessProbe:   # Restart if unhealthy
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:  # Don't send traffic if not ready
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 5. Configure Service Discovery

**ClusterIP Service** (Internal only):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
```

**LoadBalancer Service** (External, cloud provider):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
```

**Ingress** (HTTP routing, SSL):
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
```

### 6. Implement Auto-Scaling

**Horizontal Pod Autoscaler (HPA)**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Scale up at 70% CPU
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80  # Scale up at 80% memory
```

**Vertical Pod Autoscaler (VPA)** (Optional, for right-sizing):
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  updatePolicy:
    updateMode: "Auto"  # Automatically resize pods
```

### 7. Create Helm Chart (Optional, for Reusability)

**Chart Structure:**
```
myapp/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration
├── values-dev.yaml     # Dev overrides
├── values-prod.yaml    # Prod overrides
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── configmap.yaml
    ├── secret.yaml
    └── hpa.yaml
```

**Chart.yaml:**
```yaml
apiVersion: v2
name: myapp
description: My application Helm chart
type: application
version: 1.0.0
appVersion: "1.2.3"
```

**values.yaml** (Templated Configuration):
```yaml
replicaCount: 3

image:
  repository: registry.example.com/myapp
  tag: "1.2.3"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  host: myapp.example.com
  tls:
    enabled: true

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

**templates/deployment.yaml** (Templated):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ include "myapp.name" . }}
  template:
    metadata:
      labels:
        app: {{ include "myapp.name" . }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: 8080
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
```

### 8. Configure Secrets and ConfigMaps

**ConfigMap** (Non-sensitive config):
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  API_TIMEOUT: "30"
```

**Secret** (Sensitive data):
```bash
# Create secret from literal values
kubectl create secret generic myapp-secrets \
  --from-literal=database-password='secure-password' \
  --from-literal=api-key='secret-api-key'

# Or create secret from file
kubectl create secret generic myapp-secrets \
  --from-file=.env.production
```

**Use in Deployment:**
```yaml
env:
- name: APP_ENV
  valueFrom:
    configMapKeyRef:
      name: myapp-config
      key: APP_ENV
- name: DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: myapp-secrets
      key: database-password
```

### 9. Implement Health Checks

**Liveness Probe** (Restart if failing):
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30  # Wait 30s after start
  periodSeconds: 10        # Check every 10s
  timeoutSeconds: 5        # Timeout after 5s
  failureThreshold: 3      # Restart after 3 failures
```

**Readiness Probe** (Remove from load balancer if failing):
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5   # Wait 5s after start
  periodSeconds: 5         # Check every 5s
  timeoutSeconds: 3        # Timeout after 3s
  failureThreshold: 2      # Mark unready after 2 failures
```

**Health Endpoint Requirements:**
- `/health`: Returns 200 OK if application is alive (not stuck)
- `/ready`: Returns 200 OK if application can accept traffic (dependencies healthy)

### 10. Deploy and Verify

**Deploy to Kubernetes:**
```bash
# Apply manifests directly
kubectl apply -f k8s/

# Or install Helm chart
helm install myapp ./myapp-chart -f values-prod.yaml

# Check deployment status
kubectl rollout status deployment/myapp

# View pods
kubectl get pods -l app=myapp

# View service
kubectl get service myapp

# View ingress
kubectl get ingress myapp
```

**Verify Deployment:**
```bash
# Check pod logs
kubectl logs -l app=myapp --tail=50

# Execute command in pod
kubectl exec -it deployment/myapp -- /bin/sh

# Port forward for local testing
kubectl port-forward deployment/myapp 8080:8080
curl http://localhost:8080/health

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

## Output Format

### Dockerfile (Multi-Stage Node.js)

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Dependencies and build
FROM node:18-alpine AS builder

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install all dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Build application (TypeScript, asset bundling, etc.)
RUN npm run build

# Stage 2: Production runtime
FROM node:18-alpine

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy built application from builder stage
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 8080

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start application
CMD ["node", "dist/main.js"]
```

### Kubernetes Deployment (Complete)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
    version: v1.2.3
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Create 1 extra pod during update
      maxUnavailable: 0  # Never have less than desired replicas
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.2.3
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      # Use node affinity for better distribution
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - myapp
              topologyKey: kubernetes.io/hostname

      containers:
      - name: myapp
        image: registry.example.com/myapp:v1.2.3
        imagePullPolicy: IfNotPresent

        ports:
        - name: http
          containerPort: 8080
          protocol: TCP

        env:
        - name: NODE_ENV
          value: "production"
        - name: PORT
          value: "8080"

        envFrom:
        - configMapRef:
            name: myapp-config
        - secretRef:
            name: myapp-secrets

        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi

        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2

        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/.cache

      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}

      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: http
    protocol: TCP
    name: http

---
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0    # Scale up immediately
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30

---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
```

## Quality Checks

Before deploying containers to production:

- [ ] Dockerfile uses multi-stage builds
- [ ] Base image uses specific tag (not `:latest`)
- [ ] Container runs as non-root user
- [ ] `.dockerignore` configured to exclude unnecessary files
- [ ] Image scanned for vulnerabilities (no critical/high)
- [ ] Deployment has resource requests and limits
- [ ] Liveness and readiness probes configured
- [ ] At least 2 replicas for high availability
- [ ] HPA configured with appropriate min/max
- [ ] Pod anti-affinity configured for distribution
- [ ] Secrets stored in Kubernetes secrets (not environment variables in manifest)
- [ ] Service and Ingress configured for network access
- [ ] Health endpoints return 200 OK when healthy
- [ ] Tested rollout: `kubectl rollout status deployment/myapp`

## Common Patterns

### Pattern: Sidecar Container (Logging, Metrics)

```yaml
spec:
  containers:
  - name: myapp
    image: myapp:latest
    # Main application

  - name: log-forwarder
    image: fluent/fluent-bit:latest
    # Sidecar that forwards logs to centralized logging
    volumeMounts:
    - name: logs
      mountPath: /var/log/myapp

  volumes:
  - name: logs
    emptyDir: {}
```

### Pattern: Init Container (Database Migration)

```yaml
spec:
  initContainers:
  - name: migration
    image: myapp:latest
    command: ["npm", "run", "migrate"]
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: myapp-secrets
          key: database-url

  containers:
  - name: myapp
    image: myapp:latest
    # Starts only after migration completes
```

### Pattern: Blue-Green Deployment

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0.0

---
# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: myapp
        image: myapp:v2.0.0

---
# Service (switch by changing selector)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Change to 'green' to switch traffic
  ports:
  - port: 80
    targetPort: 8080
```

## Anti-Patterns to Avoid

❌ **Using `:latest` tag**: Unpredictable deployments, no rollback
✅ **Use Specific Tags**: `myapp:v1.2.3` or `myapp:abc123`

❌ **Running as Root**: Security vulnerability
✅ **Non-Root User**: Create and use non-root user in Dockerfile

❌ **No Resource Limits**: One pod can consume entire node
✅ **Set Requests/Limits**: Guarantee resources and prevent over-consumption

❌ **No Health Checks**: Kubernetes can't detect unhealthy pods
✅ **Liveness/Readiness Probes**: Auto-restart unhealthy pods, route traffic only to healthy ones

❌ **Single Replica**: No high availability
✅ **Multiple Replicas**: At least 2, ideally 3+

❌ **Hardcoded Config**: Changing config requires image rebuild
✅ **ConfigMaps/Secrets**: Externalize configuration

❌ **Large Image Size**: Slow to pull
✅ **Optimize Image**: Multi-stage builds, Alpine base, remove unnecessary files

❌ **No Anti-Affinity**: All pods on same node
✅ **Pod Anti-Affinity**: Distribute pods across nodes

❌ **Manual Scaling**: Manually adjust replicas based on load
✅ **Auto-Scaling**: HPA automatically scales based on metrics
