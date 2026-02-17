---
name: monitoring-and-alerting
description: |
  Configure production-grade monitoring with Prometheus metrics collection, Grafana dashboards, alerting rules,
  and health checks. Implements SLO/SLI tracking, smart alert thresholds, and observability best practices.

  Use when: setting up monitoring, creating Grafana dashboards, configuring Prometheus, setting up alerts,
  implementing health checks, tracking SLOs, or when user mentions monitoring, alerting, Prometheus, Grafana,
  metrics, observability, health checks, dashboards, SLO, SLI, or APM.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Monitoring and Alerting

## Overview

Implement comprehensive monitoring and alerting infrastructure using Prometheus for metrics collection, Grafana for visualization, and Alertmanager for alert routing. This skill covers metric instrumentation, dashboard design, alert rule configuration, and SLO/SLI tracking.

## Workflow

### 1. Identify Monitoring Requirements
- **Application Metrics**: Request rate, error rate, latency (RED method)
- **Infrastructure Metrics**: CPU, memory, disk, network
- **Business Metrics**: User signups, transactions, revenue
- **SLO/SLI Targets**: Availability (99.9%), latency (p95 < 200ms), error rate (< 0.1%)
- **Alert Recipients**: On-call engineers, team channels, escalation paths

### 2. Instrument Application with Metrics

**Four Golden Signals (Google SRE):**
1. **Latency**: How long requests take
2. **Traffic**: How many requests received
3. **Errors**: Rate of failed requests
4. **Saturation**: How "full" the service is (CPU, memory, connections)

**Prometheus Client Libraries:**
- **Node.js**: `prom-client`
- **Python**: `prometheus_client`
- **Go**: `prometheus/client_golang`
- **Java**: `micrometer` or `prometheus/client_java`

**Key Metric Types:**
- **Counter**: Monotonically increasing (requests, errors)
- **Gauge**: Can go up/down (active connections, memory usage)
- **Histogram**: Distribution of values (request duration)
- **Summary**: Similar to histogram with quantiles (p50, p95, p99)

### 3. Deploy Prometheus

**Prometheus Configuration** (`prometheus.yml`):
```yaml
global:
  scrape_interval: 15s      # Scrape metrics every 15 seconds
  evaluation_interval: 15s  # Evaluate alert rules every 15 seconds
  external_labels:
    cluster: 'production'
    region: 'us-east-1'

# Scrape targets
scrape_configs:
  - job_name: 'myapp'
    kubernetes_sd_configs:
    - role: pod
      namespaces:
        names:
        - production
    relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
      action: replace
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
      target_label: __address__

# Alert rules
rule_files:
  - '/etc/prometheus/rules/*.yml'

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - alertmanager:9093
```

### 4. Create Grafana Dashboards

**Dashboard Design Principles:**
- **Top Row**: High-level overview (uptime, request rate, error rate, latency)
- **Middle Rows**: Detailed metrics (per-endpoint metrics, resource usage)
- **Bottom Rows**: Debugging info (logs links, trace links)

**Panel Types:**
- **Graph**: Time-series data (request rate over time)
- **Gauge**: Current value with thresholds (CPU usage)
- **Stat**: Single number (total requests)
- **Heatmap**: Distribution over time (latency heatmap)
- **Table**: List of values (top endpoints by traffic)

**PromQL Queries Examples:**
```promql
# Request rate (requests per second)
rate(http_requests_total[5m])

# Error rate (percentage)
sum(rate(http_requests_total{status=~"5.."}[5m]))
/ sum(rate(http_requests_total[5m])) * 100

# P95 latency (milliseconds)
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# CPU usage percentage
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage percentage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Pod count
count(kube_pod_info{namespace="production"})
```

### 5. Configure Alert Rules

**Alert Rule File** (`alerts.yml`):
```yaml
groups:
- name: application_alerts
  interval: 30s
  rules:
  # High error rate
  - alert: HighErrorRate
    expr: |
      sum(rate(http_requests_total{status=~"5.."}[5m]))
      / sum(rate(http_requests_total[5m])) * 100 > 1
    for: 5m
    labels:
      severity: critical
      service: myapp
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value | humanizePercentage }} (threshold: 1%)"
      runbook: "https://runbooks.example.com/high-error-rate"

  # High latency
  - alert: HighLatency
    expr: |
      histogram_quantile(0.95,
        sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
      ) > 0.5
    for: 5m
    labels:
      severity: warning
      service: myapp
    annotations:
      summary: "High latency detected"
      description: "P95 latency is {{ $value }}s (threshold: 0.5s)"

  # Service down
  - alert: ServiceDown
    expr: up{job="myapp"} == 0
    for: 1m
    labels:
      severity: critical
      service: myapp
    annotations:
      summary: "Service {{ $labels.instance }} is down"
      description: "Instance has been down for more than 1 minute"

  # High memory usage
  - alert: HighMemoryUsage
    expr: |
      (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High memory usage on {{ $labels.instance }}"
      description: "Memory usage is {{ $value | humanizePercentage }}"

  # Disk space low
  - alert: DiskSpaceLow
    expr: |
      (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 15
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Low disk space on {{ $labels.instance }}"
      description: "Only {{ $value | humanizePercentage }} disk space remaining"

- name: kubernetes_alerts
  interval: 30s
  rules:
  # Pod crash looping
  - alert: PodCrashLooping
    expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
      description: "Pod restarted {{ $value }} times in the last 15 minutes"

  # Pod not ready
  - alert: PodNotReady
    expr: |
      kube_pod_status_phase{phase!~"Running|Succeeded"} > 0
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} not ready"
      description: "Pod has been in {{ $labels.phase }} state for more than 10 minutes"
```

### 6. Configure Alertmanager

**Alertmanager Configuration** (`alertmanager.yml`):
```yaml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

# Alert routing
route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s        # Wait 10s before sending first notification
  group_interval: 10s    # Wait 10s between subsequent notifications
  repeat_interval: 12h   # Repeat notification every 12h if not resolved
  receiver: 'team-slack'

  routes:
  # Critical alerts go to on-call immediately
  - match:
      severity: critical
    receiver: 'oncall-pagerduty'
    continue: true  # Also send to Slack

  # Warning alerts only go to Slack
  - match:
      severity: warning
    receiver: 'team-slack'

# Alert receivers
receivers:
- name: 'team-slack'
  slack_configs:
  - channel: '#alerts'
    title: '{{ template "slack.default.title" . }}'
    text: '{{ template "slack.default.text" . }}'
    color: '{{ if eq .Status "firing" }}danger{{ else }}good{{ end }}'

- name: 'oncall-pagerduty'
  pagerduty_configs:
  - service_key: 'YOUR_PAGERDUTY_SERVICE_KEY'
    description: '{{ template "pagerduty.default.description" . }}'

# Inhibition rules (suppress alerts based on other alerts)
inhibit_rules:
- source_match:
    severity: 'critical'
  target_match:
    severity: 'warning'
  equal: ['alertname', 'cluster', 'service']
```

### 7. Implement Health Check Endpoints

**Health Check Requirements:**
- **`/health` (Liveness)**: Application is alive (not deadlocked)
- **`/ready` (Readiness)**: Application can handle traffic (dependencies healthy)

**Example Health Endpoint (Node.js/Express):**
```javascript
app.get('/health', (req, res) => {
  // Simple health check - just return OK if app is running
  res.status(200).json({ status: 'ok' });
});

app.get('/ready', async (req, res) => {
  const checks = {
    database: false,
    redis: false,
    external_api: false
  };

  // Check database connection
  try {
    await db.ping();
    checks.database = true;
  } catch (error) {
    console.error('Database health check failed:', error);
  }

  // Check Redis connection
  try {
    await redis.ping();
    checks.redis = true;
  } catch (error) {
    console.error('Redis health check failed:', error);
  }

  // Check external API
  try {
    const response = await fetch('https://api.example.com/health', { timeout: 2000 });
    checks.external_api = response.ok;
  } catch (error) {
    console.error('External API health check failed:', error);
  }

  // Return 200 if all checks pass, 503 otherwise
  const allHealthy = Object.values(checks).every(v => v === true);
  const statusCode = allHealthy ? 200 : 503;

  res.status(statusCode).json({
    status: allHealthy ? 'ready' : 'not_ready',
    checks: checks
  });
});
```

### 8. Configure SLO/SLI Tracking

**Define SLOs (Service Level Objectives):**
- **Availability**: 99.9% uptime (43 minutes downtime/month allowed)
- **Latency**: P95 latency < 200ms
- **Error Rate**: < 0.1% of requests fail

**SLI (Service Level Indicators) - Prometheus Recording Rules:**
```yaml
groups:
- name: sli_recording_rules
  interval: 30s
  rules:
  # Availability SLI (percentage of successful requests)
  - record: sli:availability:ratio
    expr: |
      sum(rate(http_requests_total{status!~"5.."}[5m]))
      / sum(rate(http_requests_total[5m]))

  # Latency SLI (percentage of requests faster than 200ms)
  - record: sli:latency:ratio
    expr: |
      sum(rate(http_request_duration_seconds_bucket{le="0.2"}[5m]))
      / sum(rate(http_request_duration_seconds_count[5m]))

  # Error budget burn rate (how fast we're consuming error budget)
  - record: sli:error_budget_burn_rate:5m
    expr: 1 - sli:availability:ratio
```

**SLO Dashboard Panels:**
- Current availability vs. SLO target (99.9%)
- Error budget remaining (percentage and time)
- Error budget burn rate (how fast we're consuming it)
- Latency vs. SLO target (P95 < 200ms)

### 9. Set Up Monitoring Dashboard Structure

**Recommended Dashboard Hierarchy:**
1. **Overview Dashboard**: All services, high-level health
2. **Service Dashboard**: Individual service metrics (myapp dashboard)
3. **Infrastructure Dashboard**: Node metrics, cluster health
4. **SLO Dashboard**: SLO/SLI tracking, error budget

### 10. Test and Validate Monitoring

**Validation Checklist:**
```bash
# Test Prometheus targets are being scraped
curl http://prometheus:9090/api/v1/targets | jq '.data.activeTargets'

# Test Prometheus rules are loaded
curl http://prometheus:9090/api/v1/rules | jq '.data.groups'

# Test Alertmanager is receiving alerts
curl http://alertmanager:9093/api/v2/alerts

# Trigger a test alert
curl -X POST http://alertmanager:9093/api/v1/alerts \
  -H 'Content-Type: application/json' \
  -d '[{
    "labels": {"alertname": "TestAlert", "severity": "warning"},
    "annotations": {"summary": "Test alert"}
  }]'

# Check Grafana datasource
curl -H "Authorization: Bearer $GRAFANA_API_KEY" \
  http://grafana:3000/api/datasources

# Test application /metrics endpoint
curl http://myapp:8080/metrics

# Test health endpoints
curl http://myapp:8080/health
curl http://myapp:8080/ready
```

## Output Format

### Application Metrics Instrumentation (Node.js)

```javascript
// metrics.js
const promClient = require('prom-client');

// Create metrics registry
const register = new promClient.Registry();

// Add default metrics (CPU, memory, event loop lag)
promClient.collectDefaultMetrics({ register });

// HTTP request duration histogram
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
});
register.registerMetric(httpRequestDuration);

// HTTP request counter
const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});
register.registerMetric(httpRequestsTotal);

// Active connections gauge
const activeConnections = new promClient.Gauge({
  name: 'http_active_connections',
  help: 'Number of active HTTP connections'
});
register.registerMetric(activeConnections);

// Database query duration
const dbQueryDuration = new promClient.Histogram({
  name: 'db_query_duration_seconds',
  help: 'Duration of database queries in seconds',
  labelNames: ['operation', 'table'],
  buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]
});
register.registerMetric(dbQueryDuration);

// Middleware to record metrics
const metricsMiddleware = (req, res, next) => {
  const start = Date.now();
  activeConnections.inc();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const route = req.route ? req.route.path : req.path;
    const labels = {
      method: req.method,
      route: route,
      status_code: res.statusCode
    };

    httpRequestDuration.observe(labels, duration);
    httpRequestsTotal.inc(labels);
    activeConnections.dec();
  });

  next();
};

// Metrics endpoint
const metricsEndpoint = async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
};

module.exports = {
  register,
  metricsMiddleware,
  metricsEndpoint,
  httpRequestDuration,
  httpRequestsTotal,
  activeConnections,
  dbQueryDuration
};

// Usage in app.js:
// const { metricsMiddleware, metricsEndpoint } = require('./metrics');
// app.use(metricsMiddleware);
// app.get('/metrics', metricsEndpoint);
```

### Grafana Dashboard JSON (Overview)

```json
{
  "dashboard": {
    "title": "MyApp Overview",
    "tags": ["myapp", "production"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m]))",
            "legendFormat": "Requests/s"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status_code=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100",
            "legendFormat": "Error %"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "alert": {
          "conditions": [
            {
              "evaluator": {"params": [1], "type": "gt"},
              "operator": {"type": "and"},
              "query": {"params": ["A", "5m", "now"]},
              "reducer": {"params": [], "type": "avg"},
              "type": "query"
            }
          ]
        }
      },
      {
        "id": 3,
        "title": "P95 Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "P95"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
      },
      {
        "id": 4,
        "title": "Active Pods",
        "type": "stat",
        "targets": [
          {
            "expr": "count(up{job=\"myapp\"} == 1)",
            "legendFormat": "Active Pods"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
      }
    ]
  }
}
```

## Quality Checks

Before deploying monitoring to production:

- [ ] Prometheus successfully scraping all targets
- [ ] Application `/metrics` endpoint returning metrics
- [ ] Health check endpoints (`/health`, `/ready`) returning correct status
- [ ] Grafana dashboards created for all services
- [ ] Alert rules configured and tested
- [ ] Alertmanager routing to correct receivers (Slack, PagerDuty)
- [ ] Test alerts sent and received successfully
- [ ] SLO/SLI tracking configured
- [ ] Runbooks documented for each alert
- [ ] Metric retention configured (default: 15 days)
- [ ] Prometheus storage sized appropriately
- [ ] Dashboards show last 24h by default, allow extending to 7d/30d

## Common Patterns

### Pattern: Multi-Environment Monitoring

```yaml
# Different Prometheus instances for each environment
# Or use `external_labels` to distinguish

global:
  external_labels:
    environment: 'production'
    cluster: 'us-east-1'

# Route production alerts differently
route:
  routes:
  - match:
      environment: production
    receiver: 'oncall'
  - match:
      environment: staging
    receiver: 'team-slack'
```

### Pattern: Silence Alerts During Maintenance

```bash
# Create silence for 2 hours
amtool silence add \
  --alertmanager.url=http://alertmanager:9093 \
  --author="ops@example.com" \
  --comment="Scheduled maintenance" \
  --duration=2h \
  alertname="HighErrorRate" \
  service="myapp"
```

### Pattern: Dynamic Alert Thresholds

```yaml
# Alert if error rate exceeds 3x the weekly average
- alert: ErrorRateAnomaly
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    / sum(rate(http_requests_total[5m]))
    > 3 * avg_over_time(
      (sum(rate(http_requests_total{status=~"5.."}[5m]))
      / sum(rate(http_requests_total[5m])))[7d:5m]
    )
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Error rate anomaly detected"
```

## Anti-Patterns to Avoid

❌ **Alert on Everything**: Too many alerts cause alert fatigue
✅ **Alert on Symptoms**: Focus on user-impacting issues

❌ **No Runbooks**: Alerts with no resolution steps
✅ **Document Runbooks**: Every alert links to troubleshooting guide

❌ **Alerting Too Early**: Alert after 10 seconds of high CPU
✅ **Wait for Sustained Issues**: Use `for: 5m` to avoid flapping alerts

❌ **Single Notification Channel**: All alerts go to Slack
✅ **Severity-Based Routing**: Critical → PagerDuty, Warning → Slack

❌ **No Alert Grouping**: 100 pods failing = 100 separate alerts
✅ **Group Alerts**: `group_by: ['alertname', 'service']`

❌ **Monitoring Without SLOs**: Track everything, no clear goals
✅ **Define SLOs**: Set targets and track error budget

❌ **No Alert Testing**: Deploy and hope alerts work
✅ **Test Regularly**: Send test alerts, verify routing

❌ **Static Thresholds**: Alert at 80% CPU always
✅ **Context-Aware Thresholds**: Consider baseline and trends
