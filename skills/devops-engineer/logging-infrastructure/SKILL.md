---
name: logging-infrastructure
description: |
  Configure centralized logging infrastructure with ELK Stack (Elasticsearch, Logstash, Kibana), Loki, or CloudWatch.
  Implements log forwarding, aggregation, parsing, filtering, retention policies, and search capabilities for distributed systems.

  Use when: setting up centralized logging, configuring log aggregation, implementing log forwarding, designing log retention,
  troubleshooting with logs, or when user mentions logging, ELK, Elasticsearch, Logstash, Kibana, Loki, Promtail, Fluentd,
  Fluent Bit, CloudWatch Logs, log aggregation, log management, or structured logging.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Logging Infrastructure

Configure production-grade centralized logging systems that aggregate logs from multiple sources, parse and structure them for searchability, and provide retention policies for compliance and cost management.

## Core Implementation Areas

### 1. Log Collection & Forwarding

**Choose the right forwarder for your environment:**

**Fluent Bit** (recommended for Kubernetes):
- Lightweight, low resource usage
- Native Kubernetes support
- Built-in filtering and parsing
- Outputs to Elasticsearch, Loki, CloudWatch

**Fluentd**:
- Rich plugin ecosystem
- Complex transformations
- Higher resource usage
- Better for legacy systems

**Promtail** (Loki-specific):
- Optimized for Loki backend
- Kubernetes-native service discovery
- Label-based log streaming

**Configuration locations:**
- Kubernetes: DaemonSet running on every node
- Docker: Sidecar container or logging driver
- VMs: Systemd service

**Example Fluent Bit DaemonSet:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush         5
        Log_Level     info

    [INPUT]
        Name              tail
        Path              /var/log/containers/*.log
        Parser            docker
        Tag               kube.*

    [FILTER]
        Name                kubernetes
        Match               kube.*
        Kube_URL            https://kubernetes.default.svc:443

    [OUTPUT]
        Name   loki
        Match  *
        Host   loki.monitoring.svc.cluster.local
        Port   3100
        Labels job=fluentbit
```

### 2. Log Parsing & Structuring

Transform unstructured logs into searchable, structured data.

**For JSON logs:**
- Already structured - validate and index
- Add metadata fields (environment, version, hostname)

**For plain text logs:**
- Use grok patterns or regex
- Extract fields: timestamp, level, message, request_id

**Common parsing patterns:**

**Nginx access logs:**
```
(?<remote_addr>[^ ]*) - (?<remote_user>[^ ]*) \[(?<time_local>[^\]]*)\] "(?<method>\S+) (?<path>[^"]*) HTTP/(?<http_version>[^"]*)" (?<status>\d+) (?<body_bytes_sent>\d+) "(?<http_referer>[^"]*)" "(?<http_user_agent>[^"]*)"
```

**Application stack traces:**
- Combine multi-line exceptions into single log entry
- Extract exception type, message, stack frames

**Enrichment:**
- Add Kubernetes metadata (namespace, pod, container)
- Add environment labels (prod, staging, dev)
- Add correlation IDs (trace_id, span_id)

### 3. Storage Backend Selection

**Choose based on requirements:**

**Elasticsearch (ELK Stack):**
- **Best for**: Full-text search, complex aggregations, large teams
- **Resources**: 3+ nodes, 8GB RAM per node minimum
- **Cost**: High (storage + compute)
- **Query performance**: Excellent for full-text search

**Loki (Grafana Loki):**
- **Best for**: Kubernetes logs, cost optimization, simple queries
- **Resources**: Single instance sufficient for moderate volume
- **Cost**: Low (indexes only metadata, stores logs in S3/GCS)
- **Query performance**: Good for label-based filtering

**CloudWatch Logs:**
- **Best for**: AWS-native applications, minimal infrastructure
- **Resources**: Fully managed, no servers
- **Cost**: $0.50/GB ingested, $0.03/GB stored/month
- **Query performance**: Good with Log Insights

**Deployment example for Loki:**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: loki
spec:
  serviceName: loki
  replicas: 1
  template:
    spec:
      containers:
      - name: loki
        image: grafana/loki:2.9.0
        args:
        - -config.file=/etc/loki/loki.yaml
        volumeMounts:
        - name: config
          mountPath: /etc/loki
        - name: storage
          mountPath: /loki
  volumeClaimTemplates:
  - metadata:
      name: storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

### 4. Retention Policies

Balance storage costs with troubleshooting and compliance needs.

**Retention tiers:**
- **Hot** (1-7 days): Full search, fast storage (SSD)
- **Warm** (8-30 days): Reduced search, cheaper storage
- **Cold** (31-90 days): Archive to S3/GCS, query via Athena
- **Delete** (90+ days): Remove based on compliance

**Elasticsearch ILM policy:**
```json
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "50GB",
            "max_age": "1d"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "readonly": {},
          "allocate": {
            "number_of_replicas": 1
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "freeze": {},
          "allocate": {
            "number_of_replicas": 0
          }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

**Loki retention:**
```yaml
limits_config:
  retention_period: 744h  # 31 days

compactor:
  working_directory: /loki/compactor
  shared_store: s3
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
```

### 5. Visualization & Search

**Kibana (for Elasticsearch):**
- Create index patterns: `logs-*`
- Build dashboards for error rates, response times
- Set up saved searches for common queries
- Configure alerts (requires X-Pack or OpenDistro)

**Grafana (for Loki):**
- Use Explore view for log searching
- LogQL queries: `{namespace="production", app="api"} |= "error"`
- Create dashboard panels with log queries
- Combine with Prometheus metrics

**Common queries to set up:**

**Error rate over time:**
```
# Loki LogQL
rate({namespace="production"} |~ "(?i)error" [5m])

# Elasticsearch KQL
level:ERROR AND environment:production
```

**Top error messages:**
```
# Loki
topk(10, sum by (msg) (rate({app="api"} |= "error" | json [1h])))

# Elasticsearch aggregation
{
  "aggs": {
    "top_errors": {
      "terms": {
        "field": "message.keyword",
        "size": 10
      }
    }
  },
  "query": {
    "term": { "level": "ERROR" }
  }
}
```

**Requests by endpoint:**
```
# Loki
sum by (path) (rate({app="nginx"} | json [5m]))
```

### 6. Security & Access Control

**Encryption:**
- **In transit**: TLS between forwarders and storage
- **At rest**: Disk encryption for Elasticsearch, S3 SSE for Loki

**Authentication:**
- Kibana: SAML/OIDC integration (Okta, Auth0)
- Grafana: Built-in users or LDAP/OAuth

**Authorization:**
- Elasticsearch: Index-level permissions (logs-app1-* vs logs-app2-*)
- Kibana: Space-level access control
- Grafana: Dashboard and data source permissions

**PII masking:**
```
# Fluent Bit filter to redact credit cards
[FILTER]
    Name    modify
    Match   *
    Condition Key_value_matches message \d{4}-\d{4}-\d{4}-\d{4}
    Set message [REDACTED CARD NUMBER]
```

### 7. Performance Optimization

**Forwarder tuning:**
- Buffer size: 5-10MB to handle spikes
- Batch size: 100-1000 logs per request
- Flush interval: 5-10 seconds
- Compression: Enable gzip

**Elasticsearch optimization:**
- Shard size: Target 20-50GB per shard
- Replica count: 1 replica minimum for production
- Refresh interval: 30s (default 1s too aggressive)
- Bulk indexing: Batch 1000-5000 documents

**Loki optimization:**
- Chunk size: 1MB default (tune based on log rate)
- Parallelization: Increase querier parallelism
- Caching: Enable results cache for frequent queries

**Performance targets:**
- Log ingestion latency: < 10 seconds
- Query response time: < 5 seconds (90th percentile)
- Throughput: 10,000+ logs/second per application
- Uptime: 99.9% for log pipeline

## Implementation Workflow

### Phase 1: Requirements Gathering

Ask the user:
1. What applications/services will send logs?
2. Expected log volume (logs/second, GB/day)?
3. Retention requirements (compliance, troubleshooting)?
4. Query patterns (search by request ID, filter by error)?
5. Budget constraints (storage, compute costs)?

### Phase 2: Architecture Design

1. **Select storage backend** based on requirements:
   - High search performance needed? → Elasticsearch
   - Cost-conscious, Kubernetes-native? → Loki
   - AWS-native, minimal infrastructure? → CloudWatch

2. **Choose log forwarders**:
   - Kubernetes? → Fluent Bit or Promtail
   - Legacy systems? → Fluentd
   - AWS services? → CloudWatch agent

3. **Design retention strategy**:
   - Compliance: Legal requirements (7 years for financial)
   - Troubleshooting: 30 days minimum
   - Cost: Archive to cold storage after 30 days

4. **Plan access control**:
   - Who needs access to which logs?
   - Separate production from staging/dev
   - Role-based access (developers, ops, security)

### Phase 3: Deployment

1. **Deploy storage backend**:
   - Elasticsearch: 3-node cluster with monitoring
   - Loki: Single instance with S3 backend
   - CloudWatch: Enable Log Groups per application

2. **Deploy log forwarders**:
   - Kubernetes: DaemonSet on every node
   - Docker: Configure logging driver
   - VMs: Install and configure agent

3. **Configure parsing**:
   - JSON logs: Validate schema, add metadata
   - Plain text: Create grok patterns
   - Multi-line: Combine stack traces

4. **Set up visualization**:
   - Kibana: Index patterns, dashboards
   - Grafana: Data sources, explore views
   - CloudWatch: Log Insights queries

5. **Implement retention**:
   - Elasticsearch: Apply ILM policies
   - Loki: Configure retention period
   - CloudWatch: Set retention per log group

### Phase 4: Application Integration

1. **Update applications to log structured JSON**:
   ```json
   {
     "timestamp": "2024-02-08T10:30:00Z",
     "level": "ERROR",
     "message": "Database connection failed",
     "request_id": "abc-123",
     "user_id": "user-456",
     "environment": "production"
   }
   ```

2. **Add correlation IDs**:
   - Generate unique request_id per request
   - Pass through all services (trace_id, span_id)
   - Include in all log entries

3. **Implement log levels**:
   - DEBUG: Detailed information for debugging
   - INFO: General informational messages
   - WARN: Warning messages, not errors
   - ERROR: Error conditions
   - FATAL: Critical errors causing shutdown

4. **Add contextual metadata**:
   - User ID, tenant ID
   - Environment (prod, staging, dev)
   - Application version
   - Hostname, pod name

### Phase 5: Validation & Tuning

1. **Verify log collection**:
   - Check logs from all sources are arriving
   - Verify timestamps are correct (timezone issues common)
   - Confirm structured fields are parsed

2. **Test search functionality**:
   - Search by request ID
   - Filter by error level
   - Query by time range
   - Test dashboard visualizations

3. **Validate retention**:
   - Verify old logs are deleted
   - Check cold storage archival
   - Test restore from archive

4. **Monitor performance**:
   - Forwarder CPU/memory usage
   - Storage backend health
   - Query latency
   - Ingestion rate

5. **Optimize**:
   - Adjust buffer sizes if logs are dropped
   - Tune batch sizes for efficiency
   - Optimize slow queries
   - Scale storage if needed

## Quality Checklist

Before considering the implementation complete, verify:

- [ ] All log sources forwarding to centralized storage
- [ ] Logs searchable within 10 seconds of generation
- [ ] Structured fields extracted (level, timestamp, message)
- [ ] Retention policies configured and tested
- [ ] Dashboards created for common troubleshooting
- [ ] Access control implemented (RBAC)
- [ ] Encryption enabled (transit and rest)
- [ ] Monitoring of logging infrastructure (forwarder health, storage usage)
- [ ] Documentation complete (architecture diagram, runbook)
- [ ] Cost projections calculated and approved

## Common Patterns

### Pattern 1: Kubernetes Logging with Loki
- Promtail DaemonSet collects from all pods
- Loki aggregates and indexes by labels
- Grafana provides search interface
- **Cost**: ~$50-100/month for moderate volume

### Pattern 2: ELK Stack for Multi-Cloud
- Filebeat forwards from multiple clouds
- Elasticsearch centralized storage (3+ nodes)
- Kibana for visualization
- **Cost**: ~$500-2000/month depending on volume

### Pattern 3: CloudWatch for AWS-Native
- CloudWatch agent on EC2/ECS
- Container Insights for EKS
- Log Insights for querying
- **Cost**: ~$0.50/GB ingested

### Pattern 4: Hybrid (Logs + Metrics)
- Loki for logs, Prometheus for metrics
- Grafana unified interface
- Trace ID correlation
- **Benefit**: Jump from metric spike to logs

## Anti-Patterns to Avoid

❌ **Log everything at DEBUG level in production**
✅ **Use INFO+ in production, DEBUG only in development**

❌ **No retention policy (logs forever)**
✅ **Hot/warm/cold tiers with auto-deletion**

❌ **Plain text logs without structure**
✅ **JSON structured logs with consistent fields**

❌ **Single Elasticsearch node (no HA)**
✅ **3+ node cluster with replication**

❌ **No log sampling (10k logs/sec from one endpoint)**
✅ **Sample debug logs, keep all errors/warnings**

❌ **Sensitive data in logs (passwords, credit cards)**
✅ **PII masking and redaction before storage**

❌ **No monitoring of logging system**
✅ **Alert on forwarder failures, storage full**

## Key Technologies

**Log Forwarders:**
- Fluent Bit, Fluentd, Promtail, Filebeat, Logstash, CloudWatch agent

**Storage Backends:**
- Elasticsearch, Loki, CloudWatch Logs, Splunk, Datadog

**Visualization:**
- Kibana, Grafana, CloudWatch Log Insights

**Supporting Tools:**
- Grok patterns, LogQL, Lucene, KQL (Kibana Query Language)

## Success Criteria

The logging infrastructure is production-ready when:
- Reliability: 99.9% uptime, no log loss
- Performance: Logs searchable in < 10 seconds
- Security: TLS encryption, RBAC enforced
- Cost-optimized: Retention tiers minimize storage costs
- Scalable: Handles 2-5x current volume
- Observable: Monitoring of pipeline health
- Compliant: Meets SOC2/HIPAA/GDPR retention requirements
