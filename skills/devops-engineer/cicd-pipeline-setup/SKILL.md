---
name: cicd-pipeline-setup
description: |
  Create production-grade CI/CD pipelines with automated testing, multi-stage builds, and environment-specific
  deployments. Supports GitHub Actions, GitLab CI, Jenkins, CircleCI, and Travis CI.

  Use when: setting up automated deployments, creating build pipelines, implementing continuous integration,
  configuring automated testing, or when user mentions CI/CD, GitHub Actions, GitLab CI, Jenkins, automated
  deployment, build pipeline, continuous integration, continuous deployment, deployment automation, or
  release automation.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# CI/CD Pipeline Setup

## Overview

Set up production-grade CI/CD pipelines that automate building, testing, and deploying applications. This skill covers pipeline architecture, multi-stage builds, environment-specific deployments, deployment gates, and rollback automation.

## Workflow

### 1. Analyze Repository Structure
- Identify project type (Node.js, Python, Go, Java, React, Next.js, etc.)
- Locate build configuration files (`package.json`, `requirements.txt`, `pom.xml`, `go.mod`)
- Check for existing CI/CD configurations (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`)
- Identify test frameworks and test directories
- Note deployment targets (AWS, GCP, Azure, Vercel, Netlify, Heroku)

### 2. Determine CI/CD Platform
**GitHub Actions** if:
- Repository hosted on GitHub
- Need tight integration with GitHub features (pull requests, issues, releases)
- Want marketplace actions for common tasks
- Prefer YAML-based configuration

**GitLab CI** if:
- Repository hosted on GitLab
- Need built-in container registry
- Want Auto DevOps features
- Prefer `.gitlab-ci.yml` configuration

**Jenkins** if:
- Self-hosted infrastructure required
- Need complex pipeline orchestration
- Want plugin ecosystem for integrations
- Prefer Groovy-based Jenkinsfile

**CircleCI** if:
- Need fast builds with caching
- Want Docker layer caching
- Prefer cloud-based solution with GitHub/Bitbucket
- Need SSH debugging into build containers

### 3. Design Pipeline Stages

**Standard Pipeline Structure:**
```
Install → Lint → Test → Build → Deploy → Verify → Notify
```

**Stage Definitions:**
- **Install**: Install dependencies (npm install, pip install, go mod download)
- **Lint**: Code quality checks (ESLint, Pylint, golangci-lint)
- **Test**: Run unit tests, integration tests, coverage reports
- **Build**: Compile code, build Docker images, generate artifacts
- **Deploy**: Deploy to target environment (dev, staging, production)
- **Verify**: Health checks, smoke tests, rollback on failure
- **Notify**: Send deployment notifications (Slack, email, webhooks)

### 4. Configure Environment-Specific Deployments

**Environment Strategy:**
- **Development**: Auto-deploy on push to `develop` branch
- **Staging**: Auto-deploy on push to `main` branch
- **Production**: Manual approval or deploy on tag creation (`v*`)

**Environment Variables:**
- Store secrets in CI/CD platform secrets (GitHub Secrets, GitLab CI/CD Variables)
- Use environment-specific variable groups
- Never commit secrets to repository

### 5. Implement Caching Strategy

**Cache Dependencies:**
- Node.js: Cache `node_modules/` based on `package-lock.json` hash
- Python: Cache pip packages based on `requirements.txt` hash
- Go: Cache Go modules based on `go.sum` hash
- Docker: Use layer caching and multi-stage builds

**Cache Locations:**
- GitHub Actions: `actions/cache@v3`
- GitLab CI: `cache:` key with `paths:`
- Jenkins: Use workspace caching plugins

### 6. Configure Automated Testing

**Test Stages:**
1. **Unit Tests**: Fast, isolated tests (< 1 minute)
2. **Integration Tests**: API tests, database tests (< 5 minutes)
3. **E2E Tests**: Full user workflows (< 15 minutes, run on staging only)

**Test Commands:**
- Node.js: `npm test`, `npm run test:coverage`
- Python: `pytest --cov`, `coverage report`
- Go: `go test ./...`, `go test -race -coverprofile=coverage.out`

**Test Reporting:**
- Generate JUnit XML for test results
- Upload coverage reports to Codecov/Coveralls
- Fail pipeline if coverage drops below threshold (e.g., 80%)

### 7. Set Up Deployment Gates

**Quality Gates:**
- All tests must pass (unit, integration, E2E)
- Code coverage must meet threshold (e.g., >= 80%)
- No critical security vulnerabilities (npm audit, Snyk, Trivy)
- Linter must pass with no errors

**Approval Gates (Production Only):**
- Require manual approval from designated approvers
- Add deployment checklist (database migrations ready, rollback plan documented)
- Implement deployment windows (only deploy during business hours)

### 8. Implement Rollback Strategy

**Automated Rollback Triggers:**
- Health check failures after deployment
- Error rate spike (> 5% errors in first 5 minutes)
- Response time degradation (> 2x baseline)

**Manual Rollback:**
- Provide rollback command/button
- Redeploy previous successful version
- Document rollback procedure in runbook

### 9. Configure Notifications

**Notification Triggers:**
- Pipeline start (optional, can be noisy)
- Pipeline failure (always notify)
- Pipeline success (notify for production deployments)
- Deployment started (production only)
- Deployment completed (production only)

**Notification Channels:**
- Slack webhook to `#deployments` channel
- Email to team distribution list
- GitHub commit status checks
- Custom webhook to monitoring system

### 10. Add Deployment Metadata

**Tag Deployments:**
- Git commit SHA
- Build number
- Deployment timestamp
- Deployer (user or bot)
- Environment name

**Track Deployments:**
- Log to deployment tracking system
- Update Sentry/DataDog release tracking
- Create GitHub deployment record
- Update service version label in Kubernetes

## Output Format

### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [develop, main]
    tags: ['v*']
  pull_request:
    branches: [develop, main]

env:
  NODE_VERSION: '18'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha,prefix={{branch}}-

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Deploy to staging
        run: |
          echo "Deploying to staging..."
          # Add deployment commands here

  deploy-production:
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Add deployment commands here

      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Deployment to production completed: ${{ github.ref_name }}"
            }
```

### GitLab CI Configuration

```yaml
# .gitlab-ci.yml
stages:
  - install
  - lint
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "18"

cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
    - .npm/

install:
  stage: install
  image: node:${NODE_VERSION}
  script:
    - npm ci --cache .npm --prefer-offline
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 hour

lint:
  stage: lint
  image: node:${NODE_VERSION}
  dependencies:
    - install
  script:
    - npm run lint

test:
  stage: test
  image: node:${NODE_VERSION}
  dependencies:
    - install
  script:
    - npm test -- --coverage
  coverage: '/Statements\s*:\s*([^%]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  dependencies:
    - install
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
    - tags

deploy:staging:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
  script:
    - echo "Deploying to staging..."
    - curl -X POST $STAGING_DEPLOY_WEBHOOK
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - main

deploy:production:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
  script:
    - echo "Deploying to production..."
    - curl -X POST $PRODUCTION_DEPLOY_WEBHOOK
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - tags
```

### Jenkins Pipeline (Jenkinsfile)

```groovy
pipeline {
    agent any

    environment {
        NODE_VERSION = '18'
        REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'myapp'
    }

    stages {
        stage('Install') {
            steps {
                sh "npm ci"
            }
        }

        stage('Lint') {
            steps {
                sh "npm run lint"
            }
        }

        stage('Test') {
            steps {
                sh "npm test -- --coverage"
            }
            post {
                always {
                    junit 'test-results/**/*.xml'
                    publishCoverage adapters: [coberturaAdapter('coverage/cobertura-coverage.xml')]
                }
            }
        }

        stage('Build') {
            when {
                anyOf {
                    branch 'main'
                    tag pattern: 'v\\d+\\.\\d+\\.\\d+', comparator: 'REGEXP'
                }
            }
            steps {
                script {
                    def imageTag = env.BRANCH_NAME == 'main' ? 'latest' : env.TAG_NAME
                    sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:${imageTag} ."
                    sh "docker push ${REGISTRY}/${IMAGE_NAME}:${imageTag}"
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh "kubectl set image deployment/myapp myapp=${REGISTRY}/${IMAGE_NAME}:latest -n staging"
            }
        }

        stage('Deploy to Production') {
            when {
                tag pattern: 'v\\d+\\.\\d+\\.\\d+', comparator: 'REGEXP'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                sh "kubectl set image deployment/myapp myapp=${REGISTRY}/${IMAGE_NAME}:${TAG_NAME} -n production"
            }
        }
    }

    post {
        success {
            slackSend color: 'good', message: "Pipeline succeeded: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        failure {
            slackSend color: 'danger', message: "Pipeline failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
    }
}
```

## Quality Checks

Before finalizing CI/CD pipeline configuration:

- [ ] All stages defined (install, lint, test, build, deploy)
- [ ] Caching configured for dependencies
- [ ] Test reports uploaded (JUnit XML, coverage)
- [ ] Docker images tagged with commit SHA and version
- [ ] Environment-specific deployments configured (dev, staging, prod)
- [ ] Secrets stored securely (never in code)
- [ ] Deployment gates enforced (tests pass, coverage threshold met)
- [ ] Manual approval required for production
- [ ] Notifications configured (Slack, email)
- [ ] Rollback procedure documented

## Common Patterns

### Pattern: Monorepo with Multiple Services

```yaml
# Only build/deploy services that changed
jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      service-a: ${{ steps.changes.outputs.service-a }}
      service-b: ${{ steps.changes.outputs.service-b }}
    steps:
      - uses: actions/checkout@v3
      - uses: dorny/paths-filter@v2
        id: changes
        with:
          filters: |
            service-a:
              - 'services/service-a/**'
            service-b:
              - 'services/service-b/**'

  build-service-a:
    needs: detect-changes
    if: needs.detect-changes.outputs.service-a == 'true'
    # Build service A
```

### Pattern: Database Migrations Before Deployment

```yaml
deploy:
  steps:
    - name: Run database migrations
      run: |
        npm run migrate

    - name: Deploy application
      run: |
        kubectl rollout restart deployment/myapp

    - name: Wait for rollout
      run: |
        kubectl rollout status deployment/myapp --timeout=5m

    - name: Verify health
      run: |
        curl -f https://myapp.example.com/health || exit 1
```

### Pattern: Progressive Canary Deployment

```yaml
deploy:
  steps:
    - name: Deploy canary (10%)
      run: kubectl apply -f k8s/canary-10.yaml

    - name: Wait 5 minutes
      run: sleep 300

    - name: Check error rate
      run: |
        ERROR_RATE=$(curl -s https://metrics.example.com/error-rate)
        if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
          echo "Error rate too high: $ERROR_RATE"
          kubectl delete -f k8s/canary-10.yaml
          exit 1
        fi

    - name: Deploy canary (50%)
      run: kubectl apply -f k8s/canary-50.yaml

    - name: Wait 5 minutes
      run: sleep 300

    - name: Full deployment
      run: kubectl apply -f k8s/deployment.yaml
```

## Anti-Patterns to Avoid

❌ **Secrets in Code**: Never commit API keys, passwords, or tokens to repository
✅ **Use Secrets Manager**: Store secrets in CI/CD platform secrets or external vault

❌ **Deploy Without Tests**: Skipping tests to deploy faster
✅ **Always Run Tests**: Make tests fast, not optional

❌ **Manual Deployments**: SSH into servers to deploy manually
✅ **Automate Everything**: CI/CD pipeline handles all deployments

❌ **No Rollback Plan**: Deploy and hope it works
✅ **Test Rollback**: Regularly test rollback procedures

❌ **Single Stage Pipeline**: One giant script that does everything
✅ **Multi-Stage Pipeline**: Separate stages for clarity and failure isolation

❌ **No Caching**: Install dependencies from scratch every build
✅ **Cache Aggressively**: Cache dependencies and build artifacts

❌ **Deploy to Production on Main**: Auto-deploy to prod on every merge
✅ **Manual Gate for Prod**: Require explicit approval for production deployments

❌ **No Health Checks**: Deploy and assume it's working
✅ **Verify After Deploy**: Health checks, smoke tests, metric validation
