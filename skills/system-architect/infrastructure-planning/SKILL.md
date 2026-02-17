---
name: infrastructure-planning
description: |
  Plan cloud infrastructure with compute, storage, networking, cost optimization, and IaC templates.
  Use when user asks to design cloud infrastructure, plan infrastructure, select cloud resources, estimate
  infrastructure costs, create IaC templates, design network architecture, plan deployment infrastructure,
  select compute instances, design storage strategy, plan high availability, or optimize infrastructure costs.
allowed-tools: Read, Write, Edit, Bash
---

# Infrastructure Planning

Design cloud infrastructure with compute, storage, network resources, IaC templates, and cost optimization.

## Workflow

### 1. Gather Requirements

Extract:
- **Traffic**: Concurrent users, QPS, peak vs average, growth projections (12-24 months)
- **Geography**: User locations, data residency (GDPR), latency requirements
- **Availability**: Uptime SLA (99.9%, 99.99%), RTO, RPO, disaster recovery scope
- **Compliance**: Regulations (GDPR, HIPAA, SOC2, PCI-DSS), encryption, audit logging
- **Operational**: Team expertise (managed vs self-managed), budget, existing infrastructure

### 2. Select Cloud Platform

**AWS**: Broadest services (200+), global presence (33+ regions), mature marketplace, team has AWS expertise

**GCP**: Strong data analytics/ML (BigQuery, Vertex AI), Kubernetes-native (GKE), Google network, 10-25% cheaper

**Azure**: Microsoft ecosystem (.NET, AD, Office 365), hybrid cloud, government/healthcare compliance

**Multi-Cloud**: Vendor lock-in mitigation, geographic gaps coverage, best-of-breed services - adds 30-40% operational overhead

### 3. Design Compute Architecture

**Selection Decision Tree**:
- **Long-running stateful with OS control** → VMs/EC2 (t3, m5, c5)
- **Microservices with portability** → Managed Kubernetes (EKS, GKE, AKS)
- **Stateless containers, no cluster management** → Serverless Containers (Fargate, Cloud Run, Container Instances)
- **Event-driven, <15min tasks** → Serverless Functions (Lambda, Cloud Functions, Azure Functions)

**Instance Sizing**: Profile CPU/memory/network/IOPS needs, select family (general purpose, compute, memory, storage, GPU), target 60-70% avg utilization for headroom.

**Auto-Scaling**:
- Min: 2 instances (HA)
- Max: Based on capacity planning
- Desired: Handles typical load + buffer
- Policies: Target tracking (CPU 70%), step scaling (add 2 at 80%), scheduled (peak times)

### 4. Design Storage Architecture

| Type | Use Case | Cost | Latency | Services |
|------|----------|------|---------|----------|
| **Object** | Static assets, backups, archives | $0.02-0.03/GB/mo | ms | S3, Cloud Storage, Blob |
| **Block** | Database volumes, low-latency | $0.10-0.20/GB/mo | μs | EBS, Persistent Disk, Managed Disks |
| **File** | Shared file systems, NFS | $0.30/GB/mo | ms | EFS, Filestore, Azure Files |

**Storage Tiers**: Hot (frequent access), Cool (30+ days, retrieval fees), Cold (90+ days, higher retrieval), Intelligent-Tiering (automatic)

**Optimization**: Lifecycle policies (auto-tier), compression, retention policies, CDN for static content, versioning only where needed

### 5. Design Network Architecture

**Standard Three-Tier**:
```
Internet → CDN → Load Balancer → Public Subnet (Web) → Private Subnet (App) → Private Subnet (DB)
```

**VPC/VNet Configuration**:
- CIDR: 10.0.0.0/16 (65K IPs)
- Subnets per AZ: Public (10.0.1.0/24), Private App (10.0.11.0/24), Private DB (10.0.21.0/24)
- NAT Gateway in public subnets (for private subnet outbound)
- Internet Gateway for public subnets

**Load Balancer**: ALB (Layer 7, HTTP/HTTPS), NLB (Layer 4, TCP/UDP, ultra-low latency, static IP), multi-AZ, health checks

**CDN**: Origin (S3/ALB), caching rules (static assets hours-days, API minutes-hours), compression (gzip/brotli), edge locations based on user distribution

**Security Groups**: Least privilege, ALB allows 80/443 from internet, web tier allows from ALB only, app tier from web tier only, DB from app tier only.

### 6. Design Multi-Region Strategy (if required)

**Single-Region**: Default, one region handles all traffic

**Active-Passive**: Primary serves traffic, secondary on standby, RTO 15-60min, RPO 5-15min, cost 1.3-1.5x

**Active-Active**: Both regions serve traffic, geo-routing, RTO near-zero, RPO 1-5min, cost 2x

Choose Active-Passive if RTO <1hr acceptable and cost-sensitive; Active-Active if RTO <5min required.

### 7. Design Database Infrastructure

**Managed Service** (RDS, Cloud SQL): Less ops overhead, automatic backups, multi-AZ failover, read replicas

**Self-Managed** (EC2 + PostgreSQL): Full control, complex ops

**Configuration**: Instance class, storage type (io2 for IOPS, gp3 for general), size, IOPS, multi-AZ, read replicas (same-region for offload, cross-region for DR), backup (automated 30-day retention, point-in-time recovery)

### 8. Estimate Costs

Calculate monthly cost for:
- **Compute**: Instance type × hourly rate × 730 hours × quantity
- **Database**: Instance type × hourly rate × 730 × multi-AZ factor (2x)
- **Storage**: Volume in GB × rate/GB
- **Data Transfer**: GB/month × rate/GB (outbound typically $0.09/GB)
- **Load Balancer**: Hourly cost + LCU/hour
- **NAT Gateway**: Hourly cost + data processed

**Optimization Strategies**:
1. **Reserved Instances (30-72% savings)**: 1-year (30-40%), 3-year (50-72%) for baseline capacity
2. **Spot Instances (50-90% savings)**: Fault-tolerant, stateless workloads (batch, CI/CD)
3. **Right-Sizing**: Monitor utilization, downgrade over-provisioned, use burstable (t3) for variable
4. **Auto-Scaling**: Scale down off-hours, match capacity to demand
5. **Storage**: Lifecycle policies, delete unused volumes/snapshots, S3 Intelligent-Tiering
6. **Data Transfer**: Minimize cross-region, use CDN, compress data

### 9. Generate Infrastructure as Code

Use Terraform (cloud-agnostic) or CloudFormation (AWS-native).

**Structure**: Provider config, VPC/subnets, security groups, compute (ASG with launch template), database (RDS), load balancer, outputs.

Save complete templates to infrastructure output folder.

### 10. Document Architecture

Create markdown with:
- Executive summary (platform, regions, monthly cost, HA approach)
- Network architecture (diagram, VPC config, subnets, load balancer)
- Compute architecture (instance types, auto-scaling, justification)
- Storage architecture (types, sizes, tiers, lifecycle)
- Database infrastructure (engine, instance specs, HA, backup)
- Security configuration (security groups, encryption, access control, compliance)
- Cost analysis (breakdown by service, optimization opportunities, Reserved Instance recommendations)
- Deployment procedures (initial deployment, updates, DR runbook)

## Key Patterns

**Stateless Web Application**: ALB → Auto Scaling Group → RDS Multi-AZ (~$1,500/mo with RI)

**Microservices on Kubernetes**: ALB → EKS Cluster → RDS/DynamoDB (~$2,500/mo)

**Serverless Application**: API Gateway → Lambda → DynamoDB (~$200-500/mo, variable)

## Critical Anti-Patterns

**Single-AZ Production**: Always Multi-AZ for availability

**Oversized "Just in Case"**: Start conservative, scale based on metrics

**No Auto-Scaling**: Manual scaling doesn't respond to spikes fast enough

**Ignoring Data Transfer Costs**: Cross-region and outbound add up (20% of bill)

**Public Databases**: Always private subnets for data tier

**Untested Backups**: Test restore quarterly

**Shared Security Groups**: Specific per tier for least privilege

**No Monitoring/Alerting**: CloudWatch alarms for CPU, memory, disk, errors essential

**Ignoring Reserved Instance Opportunities**: Baseline should use RI for 30-70% savings
