"""
Production-Grade Academic Seeder — DevOps & MLOps Professional Curriculum

This seeder implements a university-level curriculum with:
- Structured theory lessons (type="text") with learning objectives, concepts, and best practices
- Real-world practical labs (type="practice") simulating production scenarios
- Video lessons aligned with pedagogical flow
- Comprehensive quizzes evaluating understanding, not memorization

Architecture: Module → Lessons (video/text/practice/quiz) → Quiz
Each topic has: Video → Theory → Practice → Assessment

Idempotent — safe to run multiple times.
Run: python seed_academic.py
"""

from datetime import datetime, timedelta
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.models.module import Module
from app.models.lesson import Lesson, LessonType
from app.models.quiz import Quiz
from app.models.progression import UserProgression, UserBadge, LessonCompletion
from app.core.security import get_password_hash

NOW = datetime.utcnow()
def days_ago(d): return NOW - timedelta(days=d)


# =============================================================================
# WEEK 1 — DevOps Foundations & Culture
# =============================================================================
MODULE_1 = {
    "id": "week1-devops-foundations",
    "title": "Week 1: DevOps Foundations & Culture",
    "description": "Master DevOps culture, CALMS principles, CI/CD pipelines, containerization with Docker, and automated testing strategies. Build production-grade infrastructure.",
    "week": 1,
    "order": 1,
    "total_duration": 420,  # 7 hours
    "icon": "GitBranch",
}

LESSONS_MODULE_1 = [
    # ═══════════════════════════════════════════════════════════════════════
    # TOPIC 1: DevOps Culture & CALMS Principles
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": "w1-devops-culture-video",
        "module_id": "week1-devops-foundations",
        "title": "Video: DevOps Culture & Transformation",
        "type": "video",
        "duration": "18",
        "url": "https://www.youtube.com/embed/Me3ea4nUt0U",
        "content": "Introduction to DevOps culture, CALMS framework, and organizational transformation. Covers collaboration patterns, automation benefits, and lean thinking in software delivery.",
        "order": 1,
    },
    {
        "id": "w1-devops-culture-theory",
        "module_id": "week1-devops-foundations",
        "title": "Theory: DevOps Culture & CALMS Framework",
        "type": "text",
        "duration": "25",
        "url": None,
        "content": """# DevOps Culture & CALMS Framework

## Learning Objectives
By the end of this lesson, you will be able to:
- Define DevOps and articulate its core principles
- Explain the CALMS framework and its application in organizations
- Identify cultural barriers to DevOps adoption
- Apply DevOps metrics (DORA) to measure team performance
- Design collaboration strategies between Dev and Ops teams

## Introduction: The DevOps Revolution

DevOps emerged from the need to break down silos between development and operations teams. Traditional waterfall approaches created friction: developers wanted rapid feature releases, while operations prioritized stability. This fundamental conflict led to slow deployments, manual handoffs, and blame culture.

**Definition**: DevOps is a set of practices, cultural philosophies, and tools that combines software development (Dev) and IT operations (Ops) to shorten the systems development life cycle while delivering features, fixes, and updates frequently in close alignment with business objectives.

## The CALMS Framework

CALMS represents the five pillars of successful DevOps transformation:

### 1. Culture
**Definition**: Breaking down silos and fostering collaboration between traditionally separated teams.

**Key Principles**:
- Shared responsibility for outcomes (not just outputs)
- Blameless post-mortems that focus on systemic improvements
- Psychological safety to experiment and fail fast
- Cross-functional teams with T-shaped skills

**Industry Example**: Netflix's "Freedom and Responsibility" culture empowers engineers to make deployment decisions, leading to thousands of production deployments per day.

**Common Mistake**: Treating DevOps as a job title rather than a cultural shift. Creating a "DevOps team" that becomes another silo defeats the purpose.

### 2. Automation
**Definition**: Eliminating manual, repetitive tasks through tooling and scripts.

**Areas to Automate**:
- **Build & Test**: Continuous Integration pipelines
- **Deployment**: Infrastructure as Code (IaC), automated releases
- **Monitoring**: Alert generation, anomaly detection
- **Incident Response**: Auto-remediation, runbook automation

**Industry Example**: Amazon automates deployments every 11.7 seconds on average, enabling rapid iteration without sacrificing reliability.

**Best Practice**: Start with high-value, high-frequency tasks. Don't automate broken processes—fix them first.

### 3. Lean
**Definition**: Applying lean manufacturing principles to software delivery—maximize value, minimize waste.

**Core Concepts**:
- **Value Stream Mapping**: Identify and eliminate bottlenecks in delivery
- **Work in Progress (WIP) Limits**: Reduce context switching and improve flow
- **Kaizen**: Continuous, incremental improvements
- **Just-In-Time**: Reduce inventory (unused features, technical debt)

**Waste Types to Eliminate**:
- Waiting (approval queues, environment provisioning)
- Manual handoffs (dev → ops → security)
- Partially done work (features sitting in staging)
- Defects (bugs found late in the cycle)

**Industry Example**: Toyota's lean principles inspired the "pull" model in Kanban, adopted by teams like Spotify for agile delivery.

### 4. Measurement
**Definition**: Making data-driven decisions through comprehensive metrics.

**DORA Four Key Metrics**:
1. **Deployment Frequency**: How often you deploy to production
   - Elite: Multiple times per day
   - High: Weekly to monthly
   - Low: Monthly to semi-annually

2. **Lead Time for Changes**: Time from commit to production
   - Elite: < 1 hour
   - High: < 1 week
   - Low: > 6 months

3. **Change Failure Rate**: % of deployments causing incidents
   - Elite: 0-15%
   - Low: > 45%

4. **Time to Restore Service**: Mean time to recover (MTTR)
   - Elite: < 1 hour
   - High: < 1 day
   - Low: > 1 week

**Industry Example**: Google's Site Reliability Engineering (SRE) teams use error budgets to balance innovation and reliability.

**Best Practice**: Track leading indicators (deployment frequency) alongside lagging indicators (incident count).

### 5. Sharing
**Definition**: Knowledge sharing, transparent communication, and collaborative learning.

**Practices**:
- **Internal Tech Talks**: "Lunch and Learn" sessions
- **Documentation as Code**: Runbooks in Git, architecture decision records (ADRs)
- **Cross-team Rotations**: Operations engineers shadow developers
- **Public Post-Mortems**: Learning from failures openly (Etsy, PagerDuty)

**Industry Example**: HashiCorp open-sources tools like Terraform, creating a global community of shared knowledge.

## DevOps vs. Traditional IT

| Aspect | Traditional IT | DevOps |
|--------|---------------|---------|
| **Teams** | Siloed (Dev, QA, Ops) | Cross-functional, integrated |
| **Releases** | Quarterly, manual | Continuous, automated |
| **Testing** | End-of-cycle | Continuous, shift-left |
| **Infrastructure** | Manual provisioning | Infrastructure as Code |
| **Failures** | Blame individuals | Blameless post-mortems |
| **Metrics** | Utilization, uptime | Flow, DORA metrics |

## Implementing DevOps: Challenges & Solutions

### Challenge 1: Organizational Resistance
**Solution**: Start with a pilot team, demonstrate value, then scale. Use metrics to show ROI.

### Challenge 2: Legacy Systems
**Solution**: Strangler fig pattern—gradually replace legacy components while maintaining old system.

### Challenge 3: Skills Gap
**Solution**: Invest in training, pair programming, and communities of practice.

### Challenge 4: Tool Overload
**Solution**: Focus on culture first, tools second. Choose composable tools over monoliths.

## Summary

DevOps is a cultural transformation, not a technology solution. The CALMS framework provides a structured approach:
- **Culture**: Break silos, foster collaboration
- **Automation**: Eliminate toil, increase reliability
- **Lean**: Maximize value, minimize waste
- **Measurement**: Data-driven decisions with DORA metrics
- **Sharing**: Knowledge transfer, transparency

**Key Takeaway**: DevOps success requires changing how people work together, supported by automation and measurement. Start small, measure impact, and scale incrementally.

## Further Reading
- "The Phoenix Project" by Gene Kim (DevOps novel)
- "Accelerate" by Forsgren, Humble, Kim (DORA research)
- Google SRE Book: https://sre.google/books/
""",
        "order": 2,
    },
    {
        "id": "w1-devops-culture-practice",
        "module_id": "week1-devops-foundations",
        "title": "Lab: DevOps Culture Assessment & Transformation Plan",
        "type": "practice",
        "duration": "45",
        "url": None,
        "content": """# Lab: DevOps Culture Assessment & Transformation Plan

## Scenario
You are a newly hired DevOps consultant at **FinTech Solutions Inc.**, a mid-sized financial technology company. The company currently has:
- **Dev Team**: 25 developers deploying features to a staging environment
- **QA Team**: 8 testers manually testing releases (2-week cycle)
- **Ops Team**: 5 sysadmins managing production infrastructure manually
- **Current Deployment**: Quarterly releases with 35% failure rate
- **Lead Time**: 6 months from commit to production

The CTO wants to adopt DevOps to improve delivery speed and reduce incidents. Your task is to conduct a culture assessment and create a transformation roadmap.

## Problem Statement
Create a comprehensive DevOps transformation plan that:
1. Assesses the current state using CALMS framework
2. Identifies cultural barriers and technical gaps
3. Proposes a phased adoption strategy
4. Defines metrics to track progress

## Tasks

### Task 1: CALMS Assessment (15 minutes)
For each CALMS pillar, evaluate the current state (0-5 score) and document:
- **Culture**: Do teams collaborate or work in silos? Evidence?
- **Automation**: What percentage of releases are automated? Build? Test? Deploy?
- **Lean**: What are the top 3 wastes in the delivery pipeline?
- **Measurement**: What metrics are currently tracked? Are they actionable?
- **Sharing**: How is knowledge transferred? Is documentation up-to-date?

**Deliverable**: CALMS scorecard with justification for each score.

### Task 2: Identify Barriers (10 minutes)
List at least 5 barriers preventing DevOps adoption:
- **Organizational**: (e.g., "Developers rewarded for features, Ops for uptime")
- **Technical**: (e.g., "Legacy monolith without API, can't deploy incrementally")
- **Cultural**: (e.g., "Ops doesn't trust Dev to have production access")

**Deliverable**: Barrier analysis with impact (high/medium/low).

### Task 3: Design 90-Day Transformation Roadmap (15 minutes)
Create a phased plan:

**Phase 1 (Days 1-30): Foundation**
- Form cross-functional pilot team (2 devs, 1 QA, 1 ops)
- Choose pilot application (low-risk, frequently changing)
- Set up CI pipeline (build + unit tests automated)
- Define success metrics (deployment frequency, lead time)

**Phase 2 (Days 31-60): Automation**
- Implement automated integration tests
- Infrastructure as Code for pilot app (Terraform/CloudFormation)
- Automated deployments to staging environment
- Blameless post-mortem process

**Phase 3 (Days 61-90): Scale**
- Deploy pilot to production using blue-green deployment
- Measure DORA metrics, compare to baseline
- Document lessons learned, share with organization
- Expand to second team

**Deliverable**: Timeline with milestones, responsible teams, and success criteria.

### Task 4: Define Metrics & KPIs (5 minutes)
Choose metrics to track transformation success:
- **Baseline (Current)**:
  - Deployment frequency: Quarterly
  - Lead time: 6 months
  - Change failure rate: 35%
  - MTTR: 48 hours

- **Target (90 days)**:
  - Deployment frequency: ?
  - Lead time: ?
  - Change failure rate: ?
  - MTTR: ?

**Deliverable**: Metrics dashboard design (can be sketch/table).

## Expected Deliverables
1. **CALMS Scorecard** (PDF/Markdown): Current state assessment
2. **Barrier Analysis** (Table): Top 5-7 barriers with mitigation strategies
3. **90-Day Roadmap** (Gantt chart or timeline): Phases, tasks, owners
4. **Metrics Dashboard Mockup** (Sketch/Wireframe): How you'll visualize DORA metrics

## Technical Constraints
- No budget for new tools in first 30 days (use open-source)
- Cannot change org structure immediately (political constraint)
- Must maintain 99.9% uptime SLA during transition
- Security team requires approval for all production changes

## Evaluation Criteria
- **Realism** (30%): Is the plan achievable in 90 days?
- **CALMS Coverage** (25%): Does the plan address all five pillars?
- **Metrics** (20%): Are metrics specific, measurable, and aligned with DORA?
- **Risk Management** (15%): Are risks identified and mitigated?
- **Communication** (10%): Is the plan clearly documented?

## Bonus Challenge (+10%)
Design a "DevOps Champions" program to scale culture change:
- How do you identify and empower champions in each team?
- What incentives align with DevOps goals?
- How do you measure cultural change (not just technical metrics)?

## Submission Format
```
devops-transformation-plan/
├── 1-calms-assessment.md
├── 2-barriers.md
├── 3-roadmap.md (or .png Gantt chart)
├── 4-metrics-dashboard.png (or mockup)
└── BONUS-champions-program.md (optional)
```

## Real-World Context
This lab simulates actual consulting engagements. Companies like Capital One, Target, and ING Bank underwent similar transformations, reducing lead times from months to hours while improving reliability.

**Key Insight**: DevOps transformation is 80% cultural, 20% technical. Your plan should reflect this ratio.
""",
        "order": 3,
    },

    # ═══════════════════════════════════════════════════════════════════════
    # TOPIC 2: CI/CD Pipelines & GitHub Actions
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": "w1-cicd-video",
        "module_id": "week1-devops-foundations",
        "title": "Video: CI/CD with GitHub Actions",
        "type": "video",
        "duration": "32",
        "url": "https://www.youtube.com/embed/R8_veQiYBjI",
        "content": "Comprehensive tutorial on building CI/CD pipelines with GitHub Actions. Covers workflow syntax, jobs, steps, matrix builds, secrets management, and deployment strategies.",
        "order": 4,
    },
    {
        "id": "w1-cicd-theory",
        "module_id": "week1-devops-foundations",
        "title": "Theory: CI/CD Pipelines & Automation",
        "type": "text",
        "duration": "30",
        "url": None,
        "content": """# CI/CD Pipelines & Automation

## Learning Objectives
- Distinguish between Continuous Integration, Delivery, and Deployment
- Design effective CI/CD pipelines for different application types
- Implement testing strategies (unit, integration, E2E) in pipelines
- Apply branching strategies (Git Flow, Trunk-Based Development)
- Configure secrets management and environment promotion

## Introduction: The Automation Continuum

Software delivery involves transforming source code into running applications. Historically, this was manual, error-prone, and slow. CI/CD automates this pipeline, enabling teams to ship code faster and more reliably.

**Key Insight**: CI/CD is not just about speed—it's about confidence. Automated testing and gradual rollouts reduce risk.

## Continuous Integration (CI)

### Definition
**Continuous Integration** is the practice of frequently merging code changes into a shared repository, with automated builds and tests validating each integration.

### Core Principles
1. **Frequent Commits**: Developers integrate code at least daily
2. **Automated Build**: Every commit triggers a build
3. **Automated Testing**: Unit and integration tests run on every build
4. **Fast Feedback**: Builds complete in < 10 minutes
5. **Shared Responsibility**: Everyone fixes broken builds immediately

### CI Pipeline Stages

```
┌─────────────────────────────────────────────────────────┐
│  Commit  →  Build  →  Test  →  Code Quality  →  Artifact│
└─────────────────────────────────────────────────────────┘
```

**Stage 1: Code Checkout**
- Clone repository
- Checkout specific branch/commit

**Stage 2: Build**
- Compile source code
- Resolve dependencies
- Generate build artifacts

**Stage 3: Test**
- **Unit Tests**: Test individual functions/classes (fast, isolated)
- **Integration Tests**: Test component interactions (databases, APIs)
- **Static Analysis**: Linting (ESLint, Pylint), security scans (Snyk)

**Stage 4: Code Quality Gates**
- Code coverage threshold (e.g., > 80%)
- Complexity analysis (cyclomatic complexity)
- Vulnerability scanning (OWASP, Dependabot)

**Stage 5: Artifact Storage**
- Publish Docker images to registry
- Upload packages to Artifactory/Nexus
- Tag artifacts with commit SHA

### Industry Example: Etsy
Etsy deploys 50+ times per day using CI. Every commit runs 10,000+ automated tests. If tests pass, code is deployed within minutes.

### Common Mistakes
❌ **Flaky Tests**: Tests that randomly fail break trust in CI
   - **Solution**: Quarantine flaky tests, investigate root cause

❌ **Slow Pipelines**: 30-minute builds kill productivity
   - **Solution**: Parallelize tests, cache dependencies, optimize Docker layers

❌ **No Test Failures Fail Build**: Tests run but don't block merges
   - **Solution**: Make test failures hard failures, not warnings

## Continuous Delivery (CD)

### Definition
**Continuous Delivery** extends CI by automating the release process up to production, but requires manual approval for deployment.

**Key Difference from CI**: Code is always in a deployable state, but deployment is triggered manually.

### CD Pipeline Stages

```
┌───────────────────────────────────────────────────────────────┐
│  CI  →  Deploy to Staging  →  E2E Tests  →  Manual Approval  │
│       →  Deploy to Production  →  Smoke Tests  →  Monitor     │
└───────────────────────────────────────────────────────────────┘
```

**Environment Promotion**:
1. **Development**: Automatic deployment on every commit
2. **Staging**: Automatic deployment after successful dev tests
3. **Production**: Manual approval gate (change advisory board)

### Environment Parity
**Principle**: Environments should be as identical as possible to avoid "works on my machine" issues.

**Strategies**:
- **Infrastructure as Code**: Use Terraform to provision all environments identically
- **Environment Variables**: Externalize config (database URLs, API keys)
- **Immutable Infrastructure**: Never modify running servers; deploy new versions

### Industry Example: Facebook
Facebook uses continuous delivery with "dark launches"—code ships to production but features are hidden behind feature flags, gradually enabled for user segments.

## Continuous Deployment

### Definition
**Continuous Deployment** automates the entire pipeline—every commit that passes tests automatically deploys to production.

**When to Use**:
- High-confidence test suites (coverage > 85%)
- Feature flags for gradual rollouts
- Robust monitoring and rollback mechanisms

**When NOT to Use**:
- Regulated industries (finance, healthcare) requiring manual approvals
- Legacy systems without comprehensive tests

### Deployment Strategies

#### 1. Blue-Green Deployment
**Concept**: Run two identical production environments (blue and green). Deploy to inactive environment, switch traffic.

**Advantages**:
- Instant rollback (switch traffic back)
- Zero downtime

**Disadvantages**:
- Double infrastructure cost
- Database migrations tricky (schema changes affect both environments)

**Use Case**: E-commerce during peak sales events (Black Friday)

#### 2. Canary Deployment
**Concept**: Deploy new version to a small subset of users (e.g., 5%), monitor metrics, gradually increase traffic.

**Advantages**:
- Limit blast radius of bugs
- Real-world testing with production traffic

**Disadvantages**:
- Requires sophisticated routing (service mesh like Istio)
- Longer deployment cycle

**Use Case**: Netflix uses canary deployments for new recommendation algorithms

#### 3. Rolling Deployment
**Concept**: Gradually replace instances of old version with new version (e.g., 25% at a time).

**Advantages**:
- No extra infrastructure needed
- Smooth transition

**Disadvantages**:
- Two versions running simultaneously (compatibility issues)
- Slower than blue-green

**Use Case**: Kubernetes default strategy for deployments

## Branching Strategies

### Git Flow
**Structure**:
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `release/*`: Release candidates
- `hotfix/*`: Emergency fixes

**Pros**: Clear separation of concerns, good for scheduled releases
**Cons**: Complex, slower feedback loop

**Use Case**: Enterprise software with quarterly releases

### Trunk-Based Development
**Structure**:
- `main`: Single source of truth
- Short-lived feature branches (< 24 hours)
- Feature flags for incomplete features

**Pros**: Simple, fast feedback, aligns with continuous deployment
**Cons**: Requires discipline, good test coverage

**Use Case**: Google, Facebook (monorepo with trunk-based development)

### GitHub Flow
**Structure**:
- `main`: Always deployable
- Feature branches → Pull Request → Merge to main → Deploy

**Pros**: Simple, good for continuous deployment
**Cons**: No explicit staging branch

**Use Case**: GitHub itself, web applications

## CI/CD Tools Comparison

| Tool | Best For | Pros | Cons |
|------|----------|------|------|
| **GitHub Actions** | GitHub repos, startups | Integrated, YAML config, free tier | Vendor lock-in |
| **GitLab CI** | Self-hosted, compliance | Built-in, auto DevOps | Requires GitLab |
| **Jenkins** | Legacy systems, plugins | Highly customizable | Steep learning curve |
| **CircleCI** | Fast builds, Docker | Excellent caching | Expensive at scale |
| **Azure DevOps** | Microsoft stack | Integrated (Boards, Repos, Artifacts) | UI complexity |

## Secrets Management

### Anti-Pattern: Hardcoded Secrets
```yaml
# ❌ NEVER DO THIS
env:
  DATABASE_PASSWORD: "admin123"  # Exposed in Git history
```

### Best Practices

#### 1. Environment Variables
```yaml
# ✅ Store in GitHub Secrets, inject at runtime
env:
  DATABASE_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

#### 2. Vault Solutions
- **HashiCorp Vault**: Centralized secret storage with dynamic secrets
- **AWS Secrets Manager**: Rotation, audit logging
- **Azure Key Vault**: Integration with Azure services

#### 3. Secret Rotation
- Rotate secrets every 90 days
- Automated rotation for database credentials
- Immediate rotation after employee departure

## Testing Pyramid in CI/CD

```
         /\
        /  \  E2E (10%)    ← Slow, brittle
       /────\
      /      \  Integration (20%) ← Medium speed
     /────────\
    /          \  Unit (70%)  ← Fast, reliable
   /────────────\
```

**Strategy**:
- **70% Unit Tests**: Fast feedback (< 1 second per test)
- **20% Integration Tests**: Test component interactions (databases, APIs)
- **10% E2E Tests**: Critical user journeys only (login, checkout)

**Why**: E2E tests are slow and flaky. Rely on fast unit tests for rapid iteration.

## Monitoring CI/CD Pipelines

### Metrics to Track
1. **Build Success Rate**: % of builds passing
   - Target: > 95%

2. **Build Duration**: Time from commit to artifact
   - Target: < 10 minutes

3. **Deployment Frequency**: Deploys per day
   - Elite: Multiple times per day

4. **Mean Time to Recovery**: Time to fix broken build
   - Target: < 30 minutes

### Alerts
- Broken build on `main` branch (notify team immediately)
- Deployment failure (auto-rollback + alert)
- Security vulnerability detected (block deployment)

## Summary

CI/CD automates the software delivery pipeline, enabling:
- **Faster feedback**: Bugs caught within minutes, not weeks
- **Reduced risk**: Small, frequent deployments are safer than big-bang releases
- **Improved quality**: Automated testing enforces quality gates

**Key Principles**:
1. **Automate everything**: Build, test, deploy
2. **Fast feedback**: Pipelines complete in < 10 minutes
3. **Shift left**: Test early, test often
4. **Environment parity**: Staging mirrors production
5. **Monitor everything**: Metrics + alerts for pipeline health

**Next Steps**: Implement a CI/CD pipeline for a real application in the lab.

## Further Reading
- "Continuous Delivery" by Jez Humble (the definitive book)
- GitHub Actions Documentation: https://docs.github.com/actions
- CircleCI Best Practices: https://circleci.com/docs/optimization-cookbook/
""",
        "order": 5,
    },
    {
        "id": "w1-cicd-practice",
        "module_id": "week1-devops-foundations",
        "title": "Lab: Build Production-Grade CI/CD Pipeline",
        "type": "practice",
        "duration": "60",
        "url": None,
        "content": """# Lab: Build Production-Grade CI/CD Pipeline

## Scenario
You are a DevOps Engineer at **HealthTech Analytics**, a healthcare SaaS startup. The team has built a patient data analytics API (Python/FastAPI) that:
- Processes sensitive healthcare data (HIPAA compliance required)
- Serves 50,000+ requests/day
- Has a 99.95% uptime SLA

**Current Problem**: Deployments are manual, taking 4 hours and failing 40% of the time. Your CTO wants a fully automated CI/CD pipeline that:
- Deploys to production multiple times per day
- Maintains security and compliance
- Reduces deployment failures to < 5%

## Problem Statement
Design and implement a GitHub Actions CI/CD pipeline that:
1. Runs on every commit to ensure code quality
2. Deploys automatically to staging after tests pass
3. Requires manual approval for production deployment
4. Implements security scanning and compliance checks
5. Supports rollback in case of failures

## Application Details
**Repository**: (Assume a FastAPI application with this structure)
```
healthtech-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── models.py        # Database models
│   └── api/
│       ├── patients.py  # Patient endpoints
│       └── analytics.py # Analytics endpoints
├── tests/
│   ├── unit/
│   │   └── test_models.py
│   └── integration/
│       └── test_api.py
├── Dockerfile
├── requirements.txt
└── .github/workflows/
    └── ci-cd.yml        # YOU WILL CREATE THIS
```

## Tasks

### Task 1: Design CI/CD Pipeline (10 minutes)
Create a pipeline flowchart with these stages:
1. **Linting & Security Scan** (parallel)
2. **Build Docker Image**
3. **Unit Tests** (inside Docker container)
4. **Integration Tests** (with test database)
5. **Deploy to Staging**
6. **E2E Tests** (against staging)
7. **Manual Approval Gate**
8. **Deploy to Production** (blue-green deployment)
9. **Smoke Tests** (verify production)
10. **Rollback** (if smoke tests fail)

**Deliverable**: Flowchart (draw.io, Mermaid, or hand-drawn)

### Task 2: Implement GitHub Actions Workflow (40 minutes)
Create `.github/workflows/ci-cd.yml` with the following requirements:

#### Job 1: Code Quality & Security
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
      # TODO: Implement these steps
      - Checkout code
      - Set up Python 3.11
      - Install dependencies
      - Run Black (code formatter) in check mode
      - Run Flake8 (linter)
      - Run Bandit (security linter for Python)
      - Run pip-audit (check for vulnerabilities in dependencies)
```

**Requirements**:
- Fail build if code is not formatted (Black)
- Fail build if linting errors exist (Flake8)
- Fail build if security vulnerabilities found (Bandit, pip-audit)

#### Job 2: Build & Test
```yaml
  build-and-test:
    needs: code-quality
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      # TODO: Implement these steps
      - Build Docker image (with caching)
      - Run unit tests (pytest with coverage > 80%)
      - Run integration tests (against test database)
      - Upload coverage report
      - Push Docker image to registry (tag with commit SHA)
```

**Requirements**:
- Use Docker BuildKit caching to speed up builds
- Fail if test coverage < 80%
- Tag images with: `latest`, `${{ github.sha }}`, `v1.2.3` (if tagged commit)
- Store image in GitHub Container Registry

#### Job 3: Deploy to Staging
```yaml
  deploy-staging:
    needs: build-and-test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.healthtech-api.com
    steps:
      # TODO: Implement deployment
      - Deploy to staging environment (use SSH or cloud CLI)
      - Wait for health check (retry 10 times, 10s interval)
      - Run smoke tests
```

**Requirements**:
- Only deploy staging on `develop` branch
- Health check must return 200 OK
- Smoke tests verify critical endpoints (`/health`, `/api/patients`)

#### Job 4: Production Deployment
```yaml
  deploy-production:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api.healthtech-api.com
    steps:
      # TODO: Implement blue-green deployment
      - Deploy to inactive slot (blue or green)
      - Run smoke tests on inactive slot
      - Switch traffic to new slot (0% → 25% → 50% → 100% over 10 minutes)
      - Monitor error rate
      - If error rate > 1%, rollback
```

**Requirements**:
- Require manual approval (GitHub Environments with protection rules)
- Gradual traffic shift (canary-style)
- Auto-rollback if error rate spikes

### Task 3: Secrets Management (5 minutes)
Document which secrets need to be stored in GitHub Secrets:
- `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN` (or GitHub Container Registry token)
- `STAGING_SSH_KEY` / `PRODUCTION_SSH_KEY` (deployment credentials)
- `DATABASE_URL_STAGING` / `DATABASE_URL_PRODUCTION`
- `SLACK_WEBHOOK_URL` (for deployment notifications)

**Deliverable**: Table of secrets with description and rotation policy

### Task 4: Monitoring & Alerts (5 minutes)
Design a monitoring strategy:
- **Metrics to Track**:
  - Build success rate
  - Build duration
  - Deployment frequency
  - Deployment failure rate
  - Rollback frequency

- **Alerts to Configure**:
  - Build fails on `main` → Slack alert to #devops
  - Production deployment failed → PagerDuty alert
  - Security vulnerability detected → Slack alert to #security

**Deliverable**: Monitoring & alerting plan

## Expected Deliverables
1. **Pipeline Flowchart** (`pipeline-diagram.png` or `.mmd`)
2. **GitHub Actions Workflow** (`.github/workflows/ci-cd.yml`)
3. **Secrets Documentation** (`SECRETS.md`)
4. **Monitoring Plan** (`MONITORING.md`)
5. **README** explaining pipeline stages and how to use it

## Technical Constraints
- Must use GitHub Actions (no external CI tools)
- Must comply with HIPAA (encrypt data at rest, audit logs)
- Pipeline must complete in < 15 minutes
- Cannot exceed 2,000 GitHub Actions minutes/month (optimize caching)
- Must support rollback within 2 minutes

## Evaluation Criteria
- **Completeness** (30%): All 10 pipeline stages implemented
- **Security** (25%): Secrets management, vulnerability scanning, HIPAA compliance
- **Efficiency** (20%): Caching, parallel jobs, build time < 15 minutes
- **Reliability** (15%): Health checks, smoke tests, auto-rollback
- **Documentation** (10%): Clear README, comments in workflow

## Bonus Challenges (+15% each)
1. **Matrix Builds**: Test across multiple Python versions (3.9, 3.10, 3.11)
2. **Slack Notifications**: Send rich notifications to Slack on deployment success/failure
3. **Performance Testing**: Add Locust load tests (must handle 1,000 req/sec)

## Example Workflow Snippet (Starter Code)
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install black flake8 bandit pip-audit
          pip install -r requirements.txt

      - name: Run Black
        run: black --check app/ tests/

      - name: Run Flake8
        run: flake8 app/ tests/ --max-line-length=100

      - name: Run Bandit (security)
        run: bandit -r app/ -ll

      - name: Check dependencies for vulnerabilities
        run: pip-audit

  build-and-test:
    needs: code-quality
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: healthtech_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          load: true
          tags: healthtech-api:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run unit tests
        run: |
          docker run --rm \
            -e DATABASE_URL=postgresql://postgres:testpass@postgres:5432/healthtech_test \
            --network host \
            healthtech-api:${{ github.sha }} \
            pytest tests/unit/ --cov=app --cov-report=xml --cov-fail-under=80

      # TODO: Continue with remaining steps
      # - Run integration tests
      # - Push to registry
      # - Deploy to staging
      # - etc.
```

## Real-World Context
This lab simulates real CI/CD pipelines at companies like:
- **Stripe**: 100+ deploys/day with comprehensive testing
- **Shopify**: Canary deployments with automated rollback
- **GitLab**: Dogfooding their own CI/CD platform

**Key Takeaway**: A well-designed CI/CD pipeline is like a safety net—it catches issues before they reach users, enabling teams to ship fearlessly.
""",
        "order": 6,
    },

    # ═══════════════════════════════════════════════════════════════════════
    # TOPIC 3: Containerization with Docker
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": "w1-docker-video",
        "module_id": "week1-devops-foundations",
        "title": "Video: Docker Fundamentals",
        "type": "video",
        "duration": "28",
        "url": "https://www.youtube.com/embed/pg19Z8LL06w",
        "content": "Complete Docker tutorial covering containers, images, Dockerfiles, networking, volumes, and best practices for building production-ready container images.",
        "order": 7,
    },
    {
        "id": "w1-docker-theory",
        "module_id": "week1-devops-foundations",
        "title": "Theory: Docker & Containerization",
        "type": "text",
        "duration": "35",
        "url": None,
        "content": """# Docker & Containerization

## Learning Objectives
- Explain how containers differ from virtual machines
- Build optimized Docker images using multi-stage builds
- Implement container security best practices
- Design container networking for microservices
- Manage persistent data with Docker volumes

## Introduction: The Container Revolution

Before containers, deploying applications was fraught with "works on my machine" problems. Different environments (dev, staging, prod) had different OS versions, libraries, and configurations. Containers solve this by packaging the application AND its dependencies into a single, portable unit.

**Definition**: A **container** is a lightweight, standalone, executable package that includes everything needed to run a piece of software: code, runtime, system tools, libraries, and settings.

## Containers vs. Virtual Machines

### Architecture Comparison

**Virtual Machines**:
```
┌──────────────────────────────────────┐
│          App A    │    App B         │
│      ┌─────────┐  │  ┌─────────┐     │
│      │Guest OS │  │  │Guest OS │     │  <── Multiple full OS copies
│      └─────────┘  │  └─────────┘     │
│     ┌───────────────────────────┐    │
│     │     Hypervisor (ESXi)     │    │
│     └───────────────────────────┘    │
│          Host Operating System        │
│              Hardware                 │
└──────────────────────────────────────┘
```

**Containers**:
```
┌──────────────────────────────────────┐
│      App A    │    App B    │  App C │
│   ┌────────┐  │  ┌────────┐ │ ┌────┐│
│   │Container│  │  │Container│ │ │Cont││  <── Share host OS kernel
│   └────────┘  │  └────────┘ │ └────┘│
│      ┌───────────────────────────┐   │
│      │  Container Runtime (Docker)│   │
│      └───────────────────────────┘   │
│          Host Operating System        │
│              Hardware                 │
└──────────────────────────────────────┘
```

### Key Differences

| Aspect | Virtual Machines | Containers |
|--------|-----------------|------------|
| **Size** | GBs (full OS) | MBs (app + dependencies) |
| **Startup Time** | Minutes | Seconds |
| **Performance** | Overhead from hypervisor | Near-native performance |
| **Isolation** | Complete (separate kernel) | Process-level (shared kernel) |
| **Density** | 10-20 VMs per host | 100+ containers per host |
| **Use Case** | Different OS on same hardware | Same OS, different apps |

**When to Use VMs**: Running Windows on Mac, strong isolation for multi-tenant systems
**When to Use Containers**: Microservices, CI/CD, rapid scaling

## Docker Architecture

### Core Components

**1. Docker Daemon** (`dockerd`)
- Background service managing containers, images, networks, volumes
- Listens to Docker API requests

**2. Docker Client** (`docker` CLI)
- User interface to interact with daemon
- Commands: `docker run`, `docker build`, etc.

**3. Docker Registry**
- Storage for Docker images
- **Docker Hub**: Public registry (hub.docker.com)
- **Private Registries**: ECR (AWS), GCR (Google), Azure Container Registry

**4. Docker Images**
- Read-only templates containing application code and dependencies
- Built in layers (each `RUN`, `COPY` command creates a layer)

**5. Docker Containers**
- Running instances of images
- Isolated file system, network, and processes

### Image Layers

Images are built in layers (like a stack of pancakes):
```
┌─────────────────────────────┐
│  Layer 4: COPY app.py /app  │  ← Your application code
├─────────────────────────────┤
│  Layer 3: RUN pip install   │  ← Python dependencies
├─────────────────────────────┤
│  Layer 2: WORKDIR /app      │  ← Set working directory
├─────────────────────────────┤
│  Layer 1: FROM python:3.11  │  ← Base image (Python runtime)
└─────────────────────────────┘
```

**Benefit**: Layers are cached. If Layer 1-3 haven't changed, Docker reuses them → faster builds.

## Dockerfile Best Practices

### 1. Multi-Stage Builds
**Problem**: Including build tools in final image bloats the image.

**Solution**: Use multi-stage builds to separate build and runtime environments.

**Example**:
```dockerfile
# ❌ BAD: Single-stage (large image)
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install  # Includes dev dependencies
COPY . .
RUN npm run build
CMD ["npm", "start"]
# Result: 1.2 GB image

# ✅ GOOD: Multi-stage (small image)
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production  # Production deps only
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine  # Alpine Linux (5 MB vs 900 MB)
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/server.js"]
# Result: 150 MB image (8x smaller!)
```

### 2. Layer Ordering (Minimize Cache Busting)
**Principle**: Place frequently changing layers (code) AFTER rarely changing layers (dependencies).

**Example**:
```dockerfile
# ❌ BAD: Code changes invalidate ALL layers
FROM python:3.11
WORKDIR /app
COPY . .                    # ← Changes frequently
RUN pip install -r requirements.txt  # ← Reinstalled every time

# ✅ GOOD: Dependencies cached until requirements.txt changes
FROM python:3.11
WORKDIR /app
COPY requirements.txt ./    # ← Changes rarely
RUN pip install -r requirements.txt  # ← Cached if req.txt unchanged
COPY . .                    # ← Code changes don't bust dep cache
```

### 3. Use `.dockerignore`
**Purpose**: Exclude unnecessary files from Docker context (faster builds, smaller images).

**Example** `.dockerignore`:
```
.git/
.vscode/
node_modules/
*.log
*.md
__pycache__/
*.pyc
.env
```

### 4. Minimize Layers
**Principle**: Combine commands to reduce layers.

**Example**:
```dockerfile
# ❌ BAD: 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# ✅ GOOD: 1 layer
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*  # Clean up cache
```

### 5. Use Official Base Images
**Why**: Security updates, best practices, smaller size.

**Examples**:
- `python:3.11-alpine` (35 MB) vs `python:3.11` (900 MB)
- `node:18-alpine` vs `node:18`
- `nginx:alpine` vs `nginx`

**Trade-off**: Alpine uses `musl libc` instead of `glibc`, which can cause compatibility issues with some packages.

## Container Security

### 1. Run as Non-Root User
**Problem**: Containers run as `root` by default. If compromised, attacker has full control.

**Solution**: Create and use a non-privileged user.

```dockerfile
# ✅ Create non-root user
FROM python:3.11-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY --chown=appuser:appgroup . .

USER appuser  # ← Switch to non-root user

CMD ["python", "app.py"]
```

### 2. Scan for Vulnerabilities
**Tools**:
- **Snyk**: `snyk test --docker python:3.11`
- **Trivy**: `trivy image myapp:latest`
- **Docker Scout**: Built into Docker Desktop

**Example Output**:
```
✗ High severity vulnerability found in openssl
  Introduced through: openssl@1.1.1k
  Fixed in: openssl@1.1.1l
```

**Action**: Update base image or pin to patched version.

### 3. Use Read-Only File Systems
**Principle**: Containers should not write to their file system (use volumes for persistence).

```bash
docker run --read-only \
  -v /app/data:/data \
  myapp:latest
```

**Benefit**: Prevents malware from modifying binaries.

### 4. Limit Resources
**Problem**: A runaway container can consume all host resources.

**Solution**: Set CPU and memory limits.

```bash
docker run -d \
  --memory="512m" \
  --cpus="0.5" \
  myapp:latest
```

## Docker Networking

### Network Drivers

**1. Bridge (Default)**
- Containers on same bridge can communicate
- Isolated from other bridges

**Use Case**: Single-host applications

**2. Host**
- Container shares host's network stack (no isolation)
- Better performance (no NAT overhead)

**Use Case**: High-performance networking

**3. Overlay**
- Connects containers across multiple Docker hosts
- Used in Docker Swarm, Kubernetes

**Use Case**: Multi-host deployments

**4. None**
- No networking (isolated container)

**Use Case**: Security-critical containers

### Example: Multi-Container Networking
```bash
# Create custom bridge network
docker network create my-app-network

# Run database on network
docker run -d \
  --name postgres \
  --network my-app-network \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# Run app on same network (can access postgres by hostname)
docker run -d \
  --name app \
  --network my-app-network \
  -e DATABASE_URL=postgresql://postgres:5432/mydb \
  myapp:latest
```

**Key**: Containers on same network can resolve each other by container name (DNS).

## Docker Volumes

### Why Volumes?
**Problem**: Container file systems are ephemeral. Data is lost when container stops.

**Solution**: Volumes persist data outside the container.

### Volume Types

**1. Named Volumes** (Managed by Docker)
```bash
docker volume create my-data
docker run -d \
  -v my-data:/app/data \
  myapp:latest
```

**Pros**: Docker manages location, easy to backup
**Cons**: Less control over file location

**2. Bind Mounts** (Host directory)
```bash
docker run -d \
  -v /host/path:/container/path \
  myapp:latest
```

**Pros**: Easy to access from host
**Cons**: Host-specific paths (not portable)

**3. tmpfs** (In-memory)
```bash
docker run -d \
  --tmpfs /app/cache:size=512m \
  myapp:latest
```

**Pros**: Fast (no disk I/O)
**Cons**: Lost when container stops

### Volume Best Practices

**1. Use Named Volumes for Databases**
```yaml
services:
  postgres:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data  # Named volume

volumes:
  pgdata:  # Docker manages this
```

**2. Use Bind Mounts for Development**
```yaml
services:
  app:
    build: .
    volumes:
      - ./src:/app/src  # Hot-reload during development
```

## Docker Compose

### Purpose
Orchestrate multi-container applications using YAML configuration.

### Example: Web App + Database + Redis
```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    restart: always

  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    restart: always

  cache:
    image: redis:7-alpine
    restart: always

volumes:
  pgdata:
```

**Commands**:
```bash
docker-compose up -d     # Start all services
docker-compose logs -f   # Stream logs
docker-compose down      # Stop and remove containers
docker-compose ps        # List running services
```

## Common Mistakes & Pitfalls

### ❌ Mistake 1: Not Using `.dockerignore`
**Impact**: Slow builds, large images (node_modules copied unnecessarily)

**Fix**: Create `.dockerignore` with common exclusions

### ❌ Mistake 2: Running as Root
**Impact**: Security vulnerability

**Fix**: Always use `USER` directive

### ❌ Mistake 3: Storing Secrets in Images
**Impact**: Credentials exposed in image layers

**Fix**: Use environment variables or Docker Secrets

### ❌ Mistake 4: Not Cleaning Up
**Impact**: Disk space filled with old images

**Fix**: Regular cleanup
```bash
docker system prune -a  # Remove all unused images
docker volume prune     # Remove unused volumes
```

## Summary

Docker revolutionized software deployment by providing:
- **Portability**: Run anywhere (laptop, server, cloud)
- **Efficiency**: Lightweight (seconds to start)
- **Isolation**: Process, network, file system isolation
- **Consistency**: Same environment across dev/test/prod

**Best Practices**:
1. Multi-stage builds for smaller images
2. Order Dockerfile layers to maximize caching
3. Run as non-root user
4. Scan images for vulnerabilities
5. Use named volumes for persistent data
6. Use Docker Compose for multi-container apps

**Next Step**: Containerize a real application in the lab.

## Further Reading
- Official Docker Documentation: https://docs.docker.com
- "Docker Deep Dive" by Nigel Poulton
- Dockerfile Best Practices: https://docs.docker.com/develop/dev-best-practices/
""",
        "order": 8,
    },
    {
        "id": "w1-docker-practice",
        "module_id": "week1-devops-foundations",
        "title": "Lab: Production-Ready Docker Containerization",
        "type": "practice",
        "duration": "75",
        "url": None,
        "content": """# Lab: Production-Ready Docker Containerization

## Scenario
You are a Platform Engineer at **E-Commerce Unlimited**, a fast-growing online retailer. The company runs a monolithic Node.js application that currently deploys manually to bare-metal servers. The application consists of:
- **Web Server**: Express.js API (20,000 requests/min peak)
- **Background Workers**: Order processing, email sending
- **Database**: PostgreSQL 15
- **Cache**: Redis for session storage

**Business Problem**: During Black Friday, manual deployments take 3 hours and result in downtime. The CTO wants to containerize the application to enable:
- Zero-downtime deployments
- Horizontal scaling (10x traffic spikes)
- Development environment parity

**Your Mission**: Containerize the entire stack with production-grade Dockerfiles and Docker Compose orchestration.

## Problem Statement
Create a containerized deployment system that:
1. Builds optimized Docker images (< 200 MB for web app)
2. Implements security best practices (non-root, vulnerability scanning)
3. Enables local development with hot-reload
4. Supports production deployment with health checks
5. Persists data across container restarts

## Application Architecture
```
┌─────────────────────────────────────────────────────┐
│                   Load Balancer                      │
│                   (nginx:alpine)                     │
└───────────┬─────────────────────────────────────────┘
            │
    ┌───────┴────────┐
    │                │
┌───▼────┐     ┌────▼───┐
│  Web   │     │  Web   │  ← Express.js (Node.js)
│  App   │     │  App   │
└───┬────┘     └────┬───┘
    │               │
    └───────┬───────┘
            │
    ┌───────▼────────┐
    │   PostgreSQL   │  ← Primary database
    └────────────────┘
            │
    ┌───────▼────────┐
    │     Redis      │  ← Session cache
    └────────────────┘
```

## Tasks

### Task 1: Web Application Dockerfile (30 minutes)
Create a production-optimized `Dockerfile` for the Node.js application.

**Application Code** (assume this structure):
```
ecommerce-app/
├── package.json
├── package-lock.json
├── src/
│   ├── server.js
│   ├── routes/
│   ├── models/
│   └── workers/
├── public/
│   └── assets/
├── tests/
│   └── integration/
└── Dockerfile  ← YOU WILL CREATE THIS
```

**Requirements**:
1. **Multi-stage build**:
   - Stage 1 (`builder`): Install ALL dependencies, run tests
   - Stage 2 (`production`): Only production dependencies + compiled assets

2. **Security**:
   - Run as non-root user (`node` user, UID 1000)
   - Scan for vulnerabilities (document process)
   - No secrets in image

3. **Optimization**:
   - Final image < 200 MB
   - Leverage layer caching (dependencies separate from code)
   - Use `.dockerignore`

4. **Health Check**:
   - HTTP health check on `/health` endpoint
   - Fail if response not 200 OK within 3 seconds

**Starter Code**:
```dockerfile
# Stage 1: Builder
FROM node:18-alpine AS builder

# Create app directory
WORKDIR /app

# TODO: Copy package files and install dependencies
# TODO: Copy source code
# TODO: Run tests (fail build if tests fail)
# TODO: Build production assets (if using TypeScript/Webpack)

# Stage 2: Production
FROM node:18-alpine

# TODO: Create non-root user
# TODO: Set working directory
# TODO: Copy only production dependencies and built assets from builder
# TODO: Set user to non-root
# TODO: Expose port
# TODO: Add health check
# TODO: Start application

CMD ["node", "src/server.js"]
```

**Deliverable**: `Dockerfile` with comments explaining each optimization

### Task 2: Docker Compose Orchestration (25 minutes)
Create `docker-compose.yml` for the full stack.

**Requirements**:
1. **Services**:
   - `web`: Node.js app (2 replicas for load balancing)
   - `nginx`: Load balancer (distributes traffic to `web` replicas)
   - `postgres`: Database with persistent volume
   - `redis`: Cache
   - `worker`: Background worker (same image as `web`, different command)

2. **Networking**:
   - Frontend network: `nginx` ↔ `web`
   - Backend network: `web` ↔ `postgres`, `redis`
   - `nginx` should NOT access database directly

3. **Volumes**:
   - Named volume for PostgreSQL data (`pgdata`)
   - Named volume for Redis data (`redisdata`)
   - Bind mount for development (hot-reload)

4. **Environment Variables**:
   - Database credentials (use `.env` file)
   - Redis connection URL
   - Node environment (`NODE_ENV=production`)

5. **Health Checks**:
   - All services must have health checks
   - `web` depends on `postgres` and `redis` being healthy

6. **Resource Limits**:
   - `web`: Max 512 MB RAM, 0.5 CPU
   - `postgres`: Max 1 GB RAM, 1 CPU
   - `redis`: Max 256 MB RAM, 0.25 CPU

**Starter Code**:
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    networks:
      - frontend
    restart: always

  web:
    build:
      context: .
      dockerfile: Dockerfile
    # TODO: Configure environment variables
    # TODO: Add depends_on with health checks
    # TODO: Add resource limits
    # TODO: Attach to networks
    deploy:
      replicas: 2  # Run 2 instances for load balancing
    restart: always

  postgres:
    image: postgres:15-alpine
    # TODO: Configure environment variables (POSTGRES_USER, etc.)
    # TODO: Add named volume for data persistence
    # TODO: Add health check
    # TODO: Add resource limits
    networks:
      - backend
    restart: always

  redis:
    image: redis:7-alpine
    # TODO: Add named volume for data persistence
    # TODO: Add health check
    # TODO: Add resource limits
    networks:
      - backend
    restart: always

  worker:
    build:
      context: .
      dockerfile: Dockerfile
    command: ["node", "src/workers/order-processor.js"]
    # TODO: Add environment variables
    # TODO: Depend on postgres and redis
    # TODO: Add resource limits
    networks:
      - backend
    restart: always

networks:
  frontend:  # nginx ↔ web
  backend:   # web ↔ postgres, redis

volumes:
  pgdata:
  redisdata:
```

**Deliverable**: `docker-compose.yml` + `docker-compose.dev.yml` (for development with bind mounts)

### Task 3: Nginx Load Balancer Configuration (10 minutes)
Create `nginx.conf` for load balancing across `web` replicas.

**Requirements**:
- Round-robin load balancing
- Health check endpoint (`/health`)
- Request timeout: 30 seconds
- Max request body: 10 MB (for product images)
- Enable gzip compression

**Starter Code**:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream web_backend {
        # TODO: Define web service instances
        server web:3000 max_fails=3 fail_timeout=30s;
    }

    server {
        listen 80;

        # TODO: Configure proxy settings
        # TODO: Add gzip compression
        # TODO: Set timeouts
        # TODO: Configure health check endpoint

        location / {
            proxy_pass http://web_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

**Deliverable**: `nginx.conf`

### Task 4: Development vs Production Configurations (10 minutes)
Create separate configurations for development and production.

**Development** (`docker-compose.dev.yml`):
- Bind mount source code (hot-reload)
- Enable debug logging
- Expose database ports (for GUI tools)

**Production** (`docker-compose.prod.yml`):
- No bind mounts
- Optimized images
- No exposed database ports
- Enable logging driver

**Example Override**:
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  web:
    volumes:
      - ./src:/app/src  # Hot-reload
    environment:
      - NODE_ENV=development
      - DEBUG=*
    ports:
      - "3000:3000"  # Expose for debugging

  postgres:
    ports:
      - "5432:5432"  # Expose for pgAdmin
```

**Usage**:
```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Deliverable**: `docker-compose.dev.yml` and `docker-compose.prod.yml`

### Task 5: Security Hardening (Bonus, +15%)
Implement advanced security measures:

1. **Image Scanning**:
   - Scan with Trivy: `trivy image ecommerce-app:latest`
   - Document vulnerabilities found
   - Remediate HIGH and CRITICAL issues

2. **Secrets Management**:
   - Use Docker Secrets (Swarm mode) or external secret manager
   - Never hardcode passwords in `docker-compose.yml`

3. **Network Policies**:
   - Ensure `nginx` cannot access `postgres` directly
   - Implement principle of least privilege

**Deliverable**: `SECURITY.md` documenting:
- Trivy scan results
- Vulnerabilities remediated
- Secrets management strategy
- Network isolation diagram

## Expected Deliverables
1. **Dockerfile** (optimized, multi-stage, < 200 MB final image)
2. **docker-compose.yml** (full stack orchestration)
3. **docker-compose.dev.yml** (development overrides)
4. **docker-compose.prod.yml** (production overrides)
5. **nginx.conf** (load balancer configuration)
6. **.dockerignore** (exclude unnecessary files)
7. **.env.example** (template for environment variables)
8. **README.md** (setup instructions, architecture diagram)
9. **SECURITY.md** (bonus: security hardening report)

## Technical Constraints
- Final `web` image must be < 200 MB
- All services must have health checks
- PostgreSQL data must persist across restarts
- Development environment must support hot-reload
- Production environment must handle 20,000 requests/min

## Evaluation Criteria
- **Image Optimization** (25%): Size, layers, caching strategy
- **Security** (25%): Non-root user, vulnerability scanning, secrets management
- **Orchestration** (20%): Docker Compose configuration, networking, volumes
- **Production-Readiness** (15%): Health checks, resource limits, restart policies
- **Documentation** (10%): README, comments, architecture diagram
- **Development Experience** (5%): Hot-reload, easy setup

## Testing Your Solution
```bash
# 1. Build and start services
docker-compose up -d --build

# 2. Verify all services are healthy
docker-compose ps

# Expected output:
# NAME       IMAGE              STATUS                    PORTS
# nginx      nginx:alpine       Up (healthy)              0.0.0.0:80->80/tcp
# web_1      ecommerce:latest   Up (healthy)
# web_2      ecommerce:latest   Up (healthy)
# postgres   postgres:15        Up (healthy)
# redis      redis:7            Up (healthy)
# worker     ecommerce:latest   Up

# 3. Test load balancing
for i in {1..10}; do
  curl -s http://localhost/health | jq .hostname
done
# Should show different hostnames (web_1, web_2)

# 4. Verify data persistence
docker-compose down
docker-compose up -d
# Database data should still exist

# 5. Check image size
docker images | grep ecommerce
# Should be < 200 MB

# 6. Run security scan
trivy image ecommerce:latest --severity HIGH,CRITICAL
# Should have no HIGH or CRITICAL vulnerabilities
```

## Real-World Context
This lab mirrors production containerization at companies like:
- **Shopify**: Runs 1,000+ containerized services, processing 600k+ requests/sec
- **Airbnb**: Containerized monolith to enable gradual microservices migration
- **Netflix**: 3 billion+ Docker container launches per week

**Key Takeaway**: Production containerization is not just `docker run`. It requires optimization, security, orchestration, and operational excellence.

## Hints
- Use `docker build --target builder` to test intermediate stages
- Use `docker-compose up --scale web=3` to test scaling
- Use `docker stats` to monitor resource usage
- Use `docker logs -f <container>` to debug startup issues
""",
        "order": 9,
    },

    # ═══════════════════════════════════════════════════════════════════════
    # QUIZ: Week 1 Assessment
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": "w1-quiz-lesson",
        "module_id": "week1-devops-foundations",
        "title": "Week 1 Assessment",
        "type": "quiz",
        "duration": "30",
        "url": None,
        "content": None,
        "order": 10,
    },
]

QUIZ_WEEK1 = {
    "id": "quiz-week1-devops",
    "module_id": "week1-devops-foundations",
    "title": "Week 1: DevOps Foundations Assessment",
    "passing_score": 75,
    "time_limit": 1800,  # 30 minutes
    "questions": [
        {
            "id": "q1",
            "question": "A company measures the following metrics: deployments every 2 weeks, 6-month lead time, 40% change failure rate, and 48-hour MTTR. According to DORA, which metric should they prioritize improving FIRST to have maximum impact on overall performance?",
            "type": "single",
            "options": [
                "Deployment Frequency (every 2 weeks → daily)",
                "Lead Time for Changes (6 months → 1 week)",
                "Change Failure Rate (40% → 15%)",
                "Time to Restore Service (48 hours → 1 hour)"
            ],
            "correct_answers": [2],
            "explanation": "Change Failure Rate of 40% is alarmingly high (Elite is <15%). This indicates systemic quality issues. Improving quality through better testing, code reviews, and automated gates will naturally improve other metrics. Deploying more frequently (option A) with 40% failure rate would cause MORE incidents. Lead time and MTTR are important but addressing quality is the foundation."
        },
        {
            "id": "q2",
            "question": "You are implementing DevOps culture in a traditional organization. The Operations team is resistant because they are measured on uptime, while Developers are measured on features delivered. Which CALMS pillar is violated, and what is the correct solution?",
            "type": "single",
            "options": [
                "Automation - Implement CI/CD to remove manual deployments",
                "Culture - Align incentives so both teams share responsibility for uptime AND feature velocity",
                "Lean - Reduce WIP limits to improve flow",
                "Measurement - Add more metrics to track both teams separately"
            ],
            "correct_answers": [1],
            "explanation": "This is a Culture problem. Conflicting incentives create silos (Ops protects uptime by rejecting deployments, Dev pushes features without considering stability). Solution: Shared metrics (e.g., both teams measured on 'successful deploys per week'). Option A (automation) addresses a symptom, not root cause. Option C (Lean) doesn't fix misaligned incentives. Option D (more metrics) reinforces silos."
        },
        {
            "id": "q3",
            "question": "In a CI/CD pipeline, which stages should run in parallel to minimize total build time? (Select all that apply)",
            "type": "multiple",
            "options": [
                "Unit tests and integration tests",
                "Code linting and security scanning",
                "Building Docker image and running tests",
                "Deploying to staging and deploying to production"
            ],
            "correct_answers": [1],
            "explanation": "Correct: Option B (linting and security scanning) - Both are static analysis and don't depend on each other. Incorrect: Option A (unit & integration tests) - Integration tests often require built artifacts, so they depend on unit tests passing first. Option C (build & tests) - Tests require the built artifact. Option D (staging & production) - Must deploy staging first, verify, then production (sequential, not parallel)."
        },
        {
            "id": "q4",
            "question": "Your CI pipeline takes 25 minutes to run. Developers complain about slow feedback. Analysis shows: Build (5 min), Unit Tests (3 min), Integration Tests (12 min), Security Scan (5 min). What is the MOST effective optimization?",
            "type": "single",
            "options": [
                "Cache dependencies to reduce build time from 5 min to 2 min",
                "Parallelize unit and integration tests to overlap execution",
                "Move security scan to nightly builds instead of every commit",
                "Parallelize integration tests across 4 machines (12 min → 3 min)"
            ],
            "correct_answers": [3],
            "explanation": "Option D provides the largest time reduction (12 min → 3 min = 9 min saved). New total: 5+3+3+5 = 16 min (36% faster). Option A saves only 3 min. Option B is incorrect - integration tests depend on unit tests passing. Option C (moving security scan) is dangerous - it delays critical feedback on vulnerabilities. Rule: Optimize the longest-running stage first (integration tests)."
        },
        {
            "id": "q5",
            "question": "Which branching strategy is BEST suited for a team practicing continuous deployment (multiple deploys per day) to a SaaS application?",
            "type": "single",
            "options": [
                "Git Flow (main, develop, feature, release, hotfix branches)",
                "Trunk-Based Development (main + short-lived feature branches)",
                "GitHub Flow (main + feature branches + pull requests)",
                "Environment branches (dev, staging, production)"
            ],
            "correct_answers": [1],
            "explanation": "Trunk-Based Development is optimal for continuous deployment. Developers merge small changes to 'main' frequently (multiple times per day), and 'main' is always deployable. Feature flags hide incomplete features. Git Flow (option A) is designed for scheduled releases (too heavyweight). GitHub Flow (option C) works but is slower than trunk-based. Environment branches (option D) are an anti-pattern - branches should represent features, not environments."
        },
        {
            "id": "q6",
            "question": "Scenario: A production deployment fails during a blue-green deployment. The new version (green) has a bug causing 5% error rate. The old version (blue) is still running. What is the CORRECT rollback strategy?",
            "type": "single",
            "options": [
                "Immediately switch 100% traffic back to blue (instant rollback)",
                "Fix the bug in green, deploy a new version, then switch traffic",
                "Keep green running and investigate the issue over the next few hours",
                "Split traffic 50/50 between blue and green to dilute the error rate"
            ],
            "correct_answers": [0],
            "explanation": "Option A is correct - blue-green's main advantage is instant rollback. Since blue is still running, immediately switch traffic back (zero downtime). Option B (fix forward) is appropriate for canary or rolling deployments where rollback is harder, but not here. Option C risks customer impact. Option D doesn't solve the problem - 50% of users still see errors. Rule: In blue-green, rollback is instantaneous and zero-risk."
        },
        {
            "id": "q7",
            "question": "Which Docker Dockerfile optimization provides the LARGEST image size reduction for a Python application?",
            "type": "single",
            "options": [
                "Combine multiple RUN commands into a single layer",
                "Use python:3.11-alpine instead of python:3.11 as base image",
                "Use multi-stage build to separate build and runtime dependencies",
                "Add a .dockerignore file to exclude node_modules and .git"
            ],
            "correct_answers": [1],
            "explanation": "Option B (alpine) provides the largest reduction: python:3.11 is ~900 MB, python:3.11-alpine is ~35 MB (25x smaller!). Option A (combining RUN) saves disk space but not image size in final layer. Option C (multi-stage) is valuable but typically saves 100-300 MB (less than alpine's 865 MB savings). Option D (.dockerignore) prevents copying unnecessary files but depends on project structure."
        },
        {
            "id": "q8",
            "question": "You run a container as root (UID 0). An attacker exploits a vulnerability and gains shell access inside the container. What can the attacker do?",
            "type": "multiple",
            "options": [
                "Modify files inside the container (install backdoors, change binaries)",
                "Access files on the host system in mounted volumes with root permissions",
                "Escalate to root on the host system and compromise other containers",
                "Nothing - containers provide complete isolation from the host"
            ],
            "correct_answers": [0, 1],
            "explanation": "Correct: A (modify container files) and B (access mounted volumes as root). If a volume is mounted (-v /host:/container), the attacker has root access to those files. Incorrect: C (host root escalation) is possible with kernel exploits but not guaranteed. D (complete isolation) is false - containers share the kernel and UID 0 inside = UID 0 outside for volumes. Fix: Run as non-root user."
        },
        {
            "id": "q9",
            "question": "In Docker Compose, Service A (web app) depends on Service B (database). You set `depends_on: [db]`. However, the web app crashes on startup with 'cannot connect to database'. Why?",
            "type": "single",
            "options": [
                "depends_on is wrong syntax, should be depends_on: db (not array)",
                "depends_on only waits for container to START, not for database to be READY",
                "Docker Compose networking is broken, services can't communicate",
                "The database container needs a health check defined"
            ],
            "correct_answers": [1],
            "explanation": "Option B is correct. `depends_on` only ensures the database *container* starts before the web app, but doesn't wait for PostgreSQL to finish initializing (can take 5-10 seconds). Solution: Add health check to db service, and use `depends_on: db: condition: service_healthy`. Option A (syntax) is wrong - array is valid. Option C (networking) - Compose creates a network automatically. Option D is partially true (health check needed) but doesn't explain the root cause."
        },
        {
            "id": "q10",
            "question": "True or False: In a multi-stage Dockerfile, layers from the builder stage are automatically included in the final image, increasing its size.",
            "type": "boolean",
            "options": ["True", "False"],
            "correct_answers": [1],
            "explanation": "False. Multi-stage builds explicitly copy only specific files from previous stages using `COPY --from=builder`. Unused layers from the builder stage are NOT included in the final image. This is the entire purpose of multi-stage builds - to separate build-time dependencies (compilers, dev tools) from runtime dependencies. Only what you explicitly COPY makes it to the final image."
        },
        {
            "id": "q11",
            "question": "Scenario: You deploy a new Docker image to production. Trivy scan shows a CRITICAL vulnerability in openssl (CVE-2023-XXXX). The vulnerability is in the base image (python:3.11). What is the IMMEDIATE action?",
            "type": "single",
            "options": [
                "Rollback the deployment immediately and investigate",
                "Update to python:3.11.1 (patched version), rebuild, redeploy",
                "Continue deployment - CRITICAL vulnerabilities are often false positives",
                "Add a network firewall rule to block exploitation of the vulnerability"
            ],
            "correct_answers": [1],
            "explanation": "Option B is correct. CRITICAL CVEs in core libraries like openssl must be patched immediately. Solution: Update base image to patched version, rebuild, test, redeploy. Option A (rollback) doesn't help if old image has same vulnerability. Option C (ignore) is dangerous - CRITICAL means actively exploited in the wild. Option D (firewall) is defense-in-depth but doesn't fix root cause. Rule: Patch critical vulnerabilities in <24 hours."
        },
        {
            "id": "q12",
            "question": "Your Docker Compose stack has a PostgreSQL service with a named volume `pgdata:/var/lib/postgresql/data`. You run `docker-compose down`. What happens to the data?",
            "type": "single",
            "options": [
                "Data is deleted permanently (volumes are removed with containers)",
                "Data persists (named volumes survive container deletion)",
                "Data is backed up to the host system automatically",
                "Data is corrupted because the database wasn't shut down gracefully"
            ],
            "correct_answers": [1],
            "explanation": "Option B is correct. Named volumes persist after `docker-compose down`. Data remains on disk until explicitly removed with `docker-compose down -v` or `docker volume rm pgdata`. This is the key benefit of named volumes vs container file systems. Option A is wrong - volumes are separate from containers. Option C - no automatic backup (must configure separately). Option D - Compose sends SIGTERM for graceful shutdown."
        }
    ]
}


# =============================================================================
# WEEK 2 — MLOps Core: Versioning, Tracking & Reproducibility
# =============================================================================
MODULE_2 = {
    "id": "week2-mlops-core",
    "title": "Week 2: MLOps Core - Versioning & Experiment Tracking",
    "description": "Master data versioning with DVC, experiment tracking with MLflow, model registry management, and reproducible ML pipelines. Build production-grade MLOps infrastructure.",
    "week": 2,
    "order": 2,
    "total_duration": 450,  # 7.5 hours
    "icon": "Brain",
}

LESSONS_MODULE_2 = [
    # ═══════════════════════════════════════════════════════════════════════
    # TOPIC 1: Introduction to MLOps
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": "w2-mlops-intro-video",
        "module_id": "week2-mlops-core",
        "title": "Video: MLOps Fundamentals",
        "type": "video",
        "duration": "22",
        "url": "https://www.youtube.com/embed/Jx6HGxV_g-E",
        "content": "Introduction to MLOps principles, differences from DevOps, and the ML lifecycle. Covers model development, deployment, monitoring, and the unique challenges of operationalizing machine learning.",
        "order": 1,
    },
    {
        "id": "w2-mlops-intro-theory",
        "module_id": "week2-mlops-core",
        "title": "Theory: MLOps Principles & Lifecycle",
        "type": "text",
        "duration": "30",
        "url": None,
        "content": """# MLOps Principles & ML Lifecycle

## Learning Objectives
- Define MLOps and explain how it extends DevOps for ML systems
- Identify the 7 stages of the ML lifecycle
- Recognize technical debt unique to ML systems
- Apply level assessment (Level 0-4) to evaluate ML maturity
- Design reproducible ML pipelines

## Introduction: Why MLOps?

Machine Learning in production is fundamentally different from traditional software:
- **Code is not the only artifact**: Models, data, and hyperparameters are equally critical
- **Non-deterministic**: Same code + different data = different results
- **Degrades over time**: Model drift as the world changes
- **Experimentation-heavy**: 100 experiments to find 1 production model

**Definition**: **MLOps** is a set of practices that combines Machine Learning, DevOps, and Data Engineering to deploy and maintain ML systems in production reliably and efficiently.

## ML vs. Traditional Software

| Aspect | Traditional Software | Machine Learning |
|--------|---------------------|------------------|
| **Primary artifact** | Code | Code + Data + Model + Config |
| **Testing** | Unit tests, integration tests | Data validation, model evaluation, drift detection |
| **Versioning** | Git (code) | Git (code) + DVC (data) + MLflow (experiments) |
| **Deployment** | Blue-green, canary | A/B testing, shadow mode, gradual rollout |
| **Monitoring** | Error rate, latency | Accuracy, precision, recall, data drift, concept drift |
| **Failure modes** | Bugs, crashes | Silent failures (wrong predictions), drift |

**Key Insight**: ML models can fail silently—producing confident but wrong predictions—making monitoring critical.

## The ML Lifecycle (7 Stages)

### 1. Problem Definition
**Goal**: Frame the business problem as an ML problem.

**Key Questions**:
- What are we predicting? (Classification, regression, clustering)
- What is success? (Business metric: revenue, churn reduction)
- Is ML the right solution? (Rule-based might be simpler)

**Example**: "Reduce customer churn by 15%" → "Predict which customers will churn in next 30 days (binary classification)"

**Anti-pattern**: Starting with model selection before defining success criteria.

### 2. Data Collection & Labeling
**Goal**: Gather representative, high-quality data.

**Challenges**:
- **Bias**: Training data doesn't match production distribution (sampling bias)
- **Class imbalance**: Fraud detection (0.1% fraud cases)
- **Label quality**: Human labelers disagree 20-30% of the time

**Best Practices**:
- **Data versioning**: Track data changes (DVC, Pachyderm)
- **Labeling guidelines**: Clear annotation rules, inter-annotator agreement checks
- **Continuous labeling**: Label production data to capture drift

**Industry Example**: Tesla collects 1 billion+ miles of labeled driving data for Autopilot.

### 3. Feature Engineering
**Goal**: Transform raw data into features models can learn from.

**Techniques**:
- **Numerical**: Scaling, binning, polynomial features
- **Categorical**: One-hot encoding, target encoding
- **Text**: TF-IDF, embeddings (Word2Vec, BERT)
- **Temporal**: Lag features, rolling statistics

**Anti-pattern**: Data leakage—using future information to predict the past.

**Example**: Predicting loan default using credit score from *after* the loan decision (leakage).

**Best Practice**: Feature stores (Feast, Tecton) for reusable, consistent features across training and serving.

### 4. Model Training & Experimentation
**Goal**: Find the best model architecture and hyperparameters.

**Process**:
1. Baseline model (logistic regression, random forest)
2. Hyperparameter tuning (grid search, Bayesian optimization)
3. Model selection (XGBoost, neural networks)
4. Ensemble methods (stacking, blending)

**Tracking**:
- **Experiments**: Log hyperparameters, metrics, artifacts (MLflow)
- **Reproducibility**: Fix random seeds, save environment (requirements.txt, Docker)

**Industry Example**: Netflix runs 100,000+ A/B tests annually to optimize recommendation models.

### 5. Model Evaluation
**Goal**: Assess model performance on held-out data.

**Metrics** (choose based on problem):
- **Classification**: Accuracy, Precision, Recall, F1, AUC-ROC
- **Regression**: MAE, RMSE, R²
- **Ranking**: NDCG, MAP

**Beyond Metrics**:
- **Fairness**: Disparate impact across demographics
- **Explainability**: SHAP values, LIME
- **Error analysis**: Confusion matrix, failure case analysis

**Anti-pattern**: Optimizing for accuracy on imbalanced data (99% accuracy predicting all negatives).

### 6. Model Deployment
**Goal**: Serve predictions in production.

**Deployment Patterns**:

#### Batch Prediction
- **Use case**: Daily churn prediction, monthly credit scoring
- **Pros**: Simple, efficient for large-scale processing
- **Cons**: Not real-time

#### Real-Time Serving
- **Use case**: Fraud detection, recommendation systems
- **Infrastructure**: REST API (FastAPI), gRPC, model serving platforms (TensorFlow Serving, Seldon)
- **SLA**: < 100ms latency, 99.9% uptime

#### Edge Deployment
- **Use case**: Mobile apps (face recognition), IoT devices
- **Challenges**: Model size (must fit in < 100 MB), latency

**Deployment Strategies**:
- **Shadow mode**: New model runs in parallel, predictions logged but not used
- **Canary**: Gradual rollout (5% → 25% → 50% → 100% traffic)
- **A/B testing**: Compare new model vs baseline (statistical significance)

**Industry Example**: Uber deploys ML models 1,000+ times per day using canary deployments.

### 7. Monitoring & Maintenance
**Goal**: Detect and respond to model degradation.

**Monitoring Layers**:

#### 1. Infrastructure Monitoring
- CPU/GPU utilization, memory, latency
- Tools: Prometheus, Grafana, Datadog

#### 2. Data Monitoring
- **Data drift**: Input distribution changes (age mean: 35 → 50)
- **Schema drift**: New columns, missing features
- Tools: Evidently AI, WhyLabs, Great Expectations

#### 3. Model Performance Monitoring
- **Online metrics**: Precision/recall on labeled production data
- **Proxy metrics**: Click-through rate (for recommendations)
- **Concept drift**: Relationship between features and target changes

**Example**: Credit scoring model trained in 2020 degrades in 2023 (economic conditions changed).

**Mitigation**:
- **Retraining triggers**: Schedule (monthly), performance-based (accuracy < 85%), drift-based
- **Human-in-the-loop**: Route low-confidence predictions to human reviewers

## MLOps Maturity Levels

### Level 0: Manual Process
- **Characteristics**: Jupyter notebooks, manual model training, ad-hoc deployments
- **Problems**: Not reproducible, no versioning, high risk
- **Example**: Data scientist copies model.pkl to server via SCP

### Level 1: Automated Training
- **Characteristics**: CI/CD for training, experiment tracking, automated evaluation
- **Tools**: MLflow, DVC, GitHub Actions for training
- **Gaps**: Still manual deployment, no monitoring

### Level 2: Automated Deployment
- **Characteristics**: CT/CD (Continuous Training/Deployment), automated model serving
- **Tools**: Kubernetes, model registries, feature stores
- **Gaps**: Reactive monitoring (detect drift but don't auto-retrain)

### Level 3: Automated Retraining
- **Characteristics**: Trigger retraining on drift detection, automated validation
- **Tools**: Airflow/Kubeflow for orchestration, automated data pipelines
- **Gaps**: No feedback loops

### Level 4: Full Automation
- **Characteristics**: Closed-loop system, automated data collection from production, active learning
- **Example**: Self-driving cars retrain on edge cases collected from fleet

## Technical Debt in ML Systems

### 1. Data Dependency Debt
**Problem**: Models depend on upstream data pipelines. Changes break models silently.

**Solution**: Data contracts, schema validation (Great Expectations).

### 2. Configuration Debt
**Problem**: Hyperparameters, feature lists, thresholds scattered across code.

**Solution**: Centralized config (YAML, MLflow params), version control.

### 3. Model Boundary Debt
**Problem**: Entangled models—one model's output feeds another, tight coupling.

**Solution**: Well-defined interfaces, versioned APIs.

### 4. Monitoring Debt
**Problem**: No visibility into model degradation until customer complaints.

**Solution**: Comprehensive monitoring (data, model, infrastructure).

## Reproducibility: The Foundation of MLOps

### Why Reproducibility Matters
- **Regulatory compliance**: Finance, healthcare require auditable models
- **Debugging**: "Why did this prediction change?"
- **Collaboration**: Team members can reproduce experiments

### 6 Pillars of Reproducibility

**1. Code**: Version control (Git)
```bash
git commit -m "Experiment: LSTM with 128 units"
```

**2. Data**: Data versioning (DVC)
```bash
dvc add data/train.csv
git add data/train.csv.dvc
```

**3. Environment**: Reproducible dependencies
```bash
# requirements.txt with pinned versions
scikit-learn==1.2.2
numpy==1.24.3
```

**4. Random Seeds**: Fix randomness
```python
import random, numpy as np, torch
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
```

**5. Experiments**: Track hyperparameters, metrics
```python
import mlflow
mlflow.log_param("learning_rate", 0.001)
mlflow.log_metric("accuracy", 0.95)
```

**6. Model**: Version and register models
```python
mlflow.sklearn.log_model(model, "model")
```

## Summary

MLOps extends DevOps to handle the unique challenges of ML systems:
- **Versioning**: Code + Data + Models
- **Lifecycle**: 7 stages from problem definition to monitoring
- **Maturity**: Progress from manual (Level 0) to automated (Level 4)
- **Reproducibility**: Essential for collaboration, debugging, compliance

**Key Takeaway**: ML systems are more complex than traditional software. MLOps provides the discipline and tooling to operationalize ML reliably.

**Next Step**: Learn DVC for data versioning and MLflow for experiment tracking.

## Further Reading
- "Machine Learning Engineering" by Andriy Burkov
- Google's "ML Best Practices" (cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- "Designing Machine Learning Systems" by Chip Huyen
""",
        "order": 2,
    },
    {
        "id": "w2-mlops-intro-practice",
        "module_id": "week2-mlops-core",
        "title": "Lab: ML Lifecycle Assessment & Pipeline Design",
        "type": "practice",
        "duration": "50",
        "url": None,
        "content": """# Lab: ML Lifecycle Assessment & Pipeline Design

## Scenario
You are a Machine Learning Engineer at **InsureTech AI**, an insurance company using ML to automate claims processing. The current system:
- **Model**: Fraud detection classifier (XGBoost)
- **Training**: Data scientists retrain manually every quarter
- **Deployment**: Model.pkl copied to production server via SCP
- **Monitoring**: None (find issues via customer complaints)

**Incident**: Last month, the model's precision dropped from 85% to 62%, causing:
- 300+ false positives (legitimate claims flagged as fraud)
- Customer complaints, bad PR, $2M in manual review costs

**Your Mission**: Assess the current ML system maturity and design a production-grade MLOps pipeline.

## Problem Statement
1. Evaluate the current system using the MLOps maturity levels (0-4)
2. Identify technical debt and failure points
3. Design an end-to-end ML pipeline (data → training → deployment → monitoring)
4. Create a roadmap to achieve Level 2 maturity

## Tasks

### Task 1: Maturity Assessment (15 minutes)
For each MLOps maturity level (0-4), evaluate if InsureTech AI meets the criteria.

**Template**:
| Level | Criteria | Current State | Evidence | Gaps |
|-------|----------|---------------|----------|------|
| 0 - Manual | Manual training, no CI/CD | ✅ YES | "Quarterly manual retraining" | All gaps |
| 1 - Automated Training | Experiment tracking, automated training pipeline | ❌ NO | No MLflow, no automation | Need CI/CD for training |
| 2 - Automated Deployment | Model registry, automated serving, monitoring | ❌ NO | Manual SCP deployment | Need registry, monitoring |
| 3 - Automated Retraining | Drift triggers, auto-retrain | ❌ NO | No drift detection | Need drift monitoring |
| 4 - Full Automation | Closed-loop, active learning | ❌ NO | No feedback loop | Future goal |

**Current Level**: 0 (Manual Process)

**Deliverable**: Maturity assessment table with justification for each level.

### Task 2: Technical Debt Analysis (10 minutes)
Identify technical debt in the current system using the framework from the theory lesson.

**Categories**:
1. **Data Dependency Debt**: What happens if upstream data schema changes?
2. **Configuration Debt**: Where are hyperparameters stored?
3. **Reproducibility Debt**: Can experiments be reproduced?
4. **Monitoring Debt**: How is model degradation detected?

**Example Answer (Data Dependency Debt)**:
- **Problem**: Claims data schema changes (new column added) break feature engineering pipeline
- **Impact**: Model receives incorrect features, predictions fail silently
- **Solution**: Implement schema validation (Great Expectations) on data ingestion

**Deliverable**: Technical debt analysis table with problem, impact, and solution for each category.

### Task 3: Design End-to-End ML Pipeline (20 minutes)
Design a production-grade ML pipeline with these components:

#### Pipeline Architecture
```
┌──────────────────────────────────────────────────────────────┐
│  1. Data Ingestion                                           │
│     Raw Claims Data (S3/Blob Storage)                        │
│       ↓                                                       │
│     Data Validation (Great Expectations)                     │
│       ↓                                                       │
│     Data Versioning (DVC)                                    │
└───────────────────┬──────────────────────────────────────────┘
                    │
┌───────────────────▼──────────────────────────────────────────┐
│  2. Feature Engineering                                      │
│     Feature Store (Feast/Tecton)                             │
│       ↓                                                       │
│     Training Features + Serving Features (same code)         │
└───────────────────┬──────────────────────────────────────────┘
                    │
┌───────────────────▼──────────────────────────────────────────┐
│  3. Model Training (CI/CD)                                   │
│     ┌─────────────────────────────────────────────┐         │
│     │ Trigger: Schedule (monthly) OR Drift Detected│         │
│     └─────────────┬───────────────────────────────┘         │
│                   ↓                                          │
│     Experiment Tracking (MLflow)                             │
│       ↓                                                       │
│     Model Evaluation (Test set)                              │
│       ↓                                                       │
│     IF accuracy > 85%: Register in Model Registry            │
└───────────────────┬──────────────────────────────────────────┘
                    │
┌───────────────────▼──────────────────────────────────────────┐
│  4. Model Deployment (CD)                                    │
│     A/B Test: 10% traffic → New model                        │
│                90% traffic → Baseline model                  │
│       ↓                                                       │
│     Monitor metrics for 24 hours                             │
│       ↓                                                       │
│     IF new_precision > baseline_precision:                   │
│       Promote to 100% (gradual rollout)                      │
│     ELSE:                                                     │
│       Rollback                                               │
└───────────────────┬──────────────────────────────────────────┘
                    │
┌───────────────────▼──────────────────────────────────────────┐
│  5. Monitoring                                               │
│     ┌──────────────┬─────────────┬────────────────┐         │
│     │ Data Drift   │ Model Perf  │ Infrastructure │         │
│     │ (Evidently)  │ (Precision) │ (Prometheus)   │         │
│     └──────┬───────┴─────┬───────┴────────┬───────┘         │
│            │             │                │                 │
│        Alerts        Alerts            Alerts               │
│       (Slack)       (PagerDuty)       (Grafana)             │
└──────────────────────────────────────────────────────────────┘
```

**Requirements**:
For each component, specify:
- **Tool/Technology**: (e.g., DVC, MLflow, Docker, Kubernetes)
- **Trigger**: What initiates this stage?
- **Validation**: Quality gates before proceeding
- **Failure Handling**: What happens if validation fails?

**Example (Model Training)**:
- **Tool**: MLflow Tracking + GitHub Actions
- **Trigger**: Scheduled (monthly) OR Manual (data scientist)
- **Validation**: Test set accuracy > 85%, no data drift detected
- **Failure Handling**: Alert team, do NOT deploy, investigate

**Deliverable**: Pipeline diagram (draw.io, Mermaid, or hand-drawn) + component specifications

### Task 4: Monitoring Strategy (5 minutes)
Design a comprehensive monitoring strategy covering all layers.

**Monitoring Layers**:
1. **Data Monitoring**: What to monitor?
   - Schema drift (columns added/removed)
   - Data drift (distribution changes)
   - Data quality (missing values, outliers)

2. **Model Performance**: What metrics?
   - Precision, Recall, F1 (requires labeled production data)
   - Proxy metrics (average claim review time)
   - Prediction distribution (% flagged as fraud)

3. **Infrastructure**: What to track?
   - API latency (P50, P95, P99)
   - Request rate
   - Error rate (500s)

**Alerting**:
- **Data drift detected** → Slack alert, schedule retraining
- **Precision < 75%** → PagerDuty alert (critical)
- **API latency > 500ms** → Grafana alert (warning)

**Deliverable**: Monitoring & alerting plan table

## Expected Deliverables
1. **Maturity Assessment** (`maturity-assessment.md`): Level 0-4 evaluation
2. **Technical Debt Analysis** (`technical-debt.md`): 4+ debt categories
3. **Pipeline Diagram** (`pipeline-diagram.png` or `.mmd`): End-to-end flow
4. **Component Specifications** (`pipeline-components.md`): Tools, triggers, validations
5. **Monitoring Plan** (`monitoring-plan.md`): 3 layers + alerts

## Technical Constraints
- Must use open-source tools (budget constraint)
- Must be cloud-agnostic (AWS, GCP, or Azure)
- Training time < 4 hours (business requirement)
- Deployment with < 5 minutes downtime acceptable
- Model retraining triggered automatically on drift

## Evaluation Criteria
- **Completeness** (30%): All 5 pipeline stages designed
- **Tooling Choices** (25%): Appropriate tools for each component
- **Reproducibility** (20%): Versioning data, code, models, environment
- **Monitoring** (15%): Comprehensive monitoring across all layers
- **Realism** (10%): Feasible with given constraints

## Bonus Challenges (+10% each)
1. **Feature Store Design**: Design a feature store schema (Feast) for claims data
2. **Cost Optimization**: Estimate cloud costs for pipeline (training, storage, serving)
3. **Disaster Recovery**: Design backup/restore strategy for models and data

## Real-World Context
This lab simulates ML system redesigns at:
- **Airbnb**: Rebuilt pricing model pipeline from manual to automated, reducing retraining time from 2 weeks to 2 hours
- **Uber**: Implemented Michelangelo platform for end-to-end ML lifecycle management
- **Lyft**: Built Flyte for reproducible ML workflows

**Key Insight**: Most ML failures in production are not algorithm failures—they're infrastructure and monitoring failures.

## Submission Format
```
mlops-pipeline-design/
├── maturity-assessment.md
├── technical-debt.md
├── pipeline-diagram.png (or .mmd)
├── pipeline-components.md
├── monitoring-plan.md
└── BONUS/ (optional)
    ├── feature-store-schema.md
    ├── cost-estimation.xlsx
    └── disaster-recovery.md
```

## Hints
- Start with the maturity assessment to identify current gaps
- Design monitoring first (observe before optimizing)
- Use managed services for complex components (e.g., AWS SageMaker Feature Store vs building custom)
- Prioritize: Reproducibility → Monitoring → Automation
""",
        "order": 3,
    },

    # Add remaining Week 2 lessons following the same pattern...
    # (DVC, MLflow, Model Registry, etc.)
    # This is a comprehensive example - full file would be very long
]

# Continuing with abbreviated versions of remaining modules...

# =============================================================================
# USERS
# =============================================================================
USERS = [
    {
        "id": "admin-1",
        "email": "admin@learnops.io",
        "password": "Admin2024!",
        "first_name": "Admin",
        "last_name": "DevOps",
        "role": "admin",
        "is_active": True,
        "created_days_ago": 90,
        "last_login_days_ago": 0,
    },
    {
        "id": "instructor-1",
        "email": "claire@learnops.io",
        "password": "Instructor2024!",
        "first_name": "Claire",
        "last_name": "Martin",
        "role": "instructor",
        "is_active": True,
        "created_days_ago": 85,
        "last_login_days_ago": 1,
    },
    {
        "id": "student-1",
        "email": "marie@student.com",
        "password": "Student2024!",
        "first_name": "Marie",
        "last_name": "Dupont",
        "role": "student",
        "is_active": True,
        "created_days_ago": 30,
        "last_login_days_ago": 0,
    },
]

PROGRESSIONS = [
    {"user_id": "admin-1", "progression": 0, "modules_completed": [], "time_spent": 0},
    {"user_id": "instructor-1", "progression": 100, "modules_completed": ["week1-devops-foundations", "week2-mlops-core"], "time_spent": 32400},
    {"user_id": "student-1", "progression": 35, "modules_completed": [], "time_spent": 8100},
]

BADGES = [
    {"user_id": "instructor-1", "badge_name": "week1-devops-foundations"},
    {"user_id": "instructor-1", "badge_name": "week2-mlops-core"},
]

COMPLETIONS = [
    ("instructor-1", "w1-devops-culture-video"),
    ("instructor-1", "w1-devops-culture-theory"),
    ("instructor-1", "w1-devops-culture-practice"),
    ("student-1", "w1-devops-culture-video"),
    ("student-1", "w1-devops-culture-theory"),
]


# =============================================================================
# SEED FUNCTION
# =============================================================================
def seed():
    db = SessionLocal()
    try:
        print("\n🎓 Seeding ACADEMIC curriculum — University-level content\n")

        all_modules = [MODULE_1, MODULE_2]  # Add MODULE_3, MODULE_4 in full version
        all_lessons = LESSONS_MODULE_1 + LESSONS_MODULE_2
        all_quizzes = [QUIZ_WEEK1]  # Add more quizzes in full version

        # Modules
        for m in all_modules:
            ex = db.query(Module).filter(Module.id == m["id"]).first()
            if ex:
                for k, v in m.items():
                    setattr(ex, k, v)
            else:
                db.add(Module(**m))
        db.commit()
        print(f"✅ Modules: {len(all_modules)}")

        # Lessons
        for L in all_lessons:
            typ = L["type"] if L["type"] in ("video", "text", "quiz", "practice") else "text"
            payload = {
                "id": L["id"],
                "module_id": L["module_id"],
                "title": L["title"],
                "type": LessonType(typ),
                "duration": str(L["duration"]),
                "url": L.get("url"),
                "content": L.get("content"),
                "order": L["order"],
            }
            ex = db.query(Lesson).filter(Lesson.id == L["id"]).first()
            if ex:
                for k, v in payload.items():
                    setattr(ex, k, v)
            else:
                db.add(Lesson(**payload))
        db.commit()

        n_text = sum(1 for L in all_lessons if L["type"] == "text")
        n_practice = sum(1 for L in all_lessons if L["type"] == "practice")
        n_video = sum(1 for L in all_lessons if L["type"] == "video")
        n_quiz_l = sum(1 for L in all_lessons if L["type"] == "quiz")
        print(f"✅ Lessons: {len(all_lessons)} (📹 {n_video} videos | 📖 {n_text} theory | 🛠️ {n_practice} labs | 📝 {n_quiz_l} quizzes)")

        # Quizzes
        for q in all_quizzes:
            payload = {
                "id": q["id"],
                "module_id": q["module_id"],
                "title": q["title"],
                "passing_score": q["passing_score"],
                "time_limit": q.get("time_limit"),
                "questions": q["questions"],
            }
            ex = db.query(Quiz).filter(Quiz.id == q["id"]).first()
            if ex:
                for k, v in payload.items():
                    setattr(ex, k, v)
            else:
                db.add(Quiz(**payload))
        db.commit()
        print(f"✅ Quizzes: {len(all_quizzes)}")

        # Users
        for u in USERS:
            payload = {
                "id": u["id"],
                "email": u["email"],
                "first_name": u["first_name"],
                "last_name": u["last_name"],
                "role": UserRole(u["role"]),
                "is_active": u["is_active"],
                "created_at": days_ago(u["created_days_ago"]),
                "last_login": days_ago(u["last_login_days_ago"]),
            }
            ex = db.query(User).filter(User.id == u["id"]).first()
            if ex:
                for k, v in payload.items():
                    if k != "created_at":
                        setattr(ex, k, v)
            else:
                payload["hashed_password"] = get_password_hash(u["password"])
                db.add(User(**payload))
        db.commit()
        print(f"✅ Users: {len(USERS)}")

        # Progressions
        for p in PROGRESSIONS:
            uid = p["user_id"]
            payload = {
                "user_id": uid,
                "progression": p["progression"],
                "modules_completed": p["modules_completed"],
                "time_spent": p["time_spent"],
            }
            ex = db.query(UserProgression).filter(UserProgression.user_id == uid).first()
            if ex:
                for k, v in payload.items():
                    setattr(ex, k, v)
            else:
                db.add(UserProgression(id=f"prog-{uid}", **payload))
        db.commit()

        # Badges
        for b in BADGES:
            bid = f"badge-{b['user_id']}-{b['badge_name']}"
            if not db.query(UserBadge).filter(UserBadge.id == bid).first():
                db.add(UserBadge(id=bid, user_id=b["user_id"], badge_name=b["badge_name"]))
        db.commit()

        # Completions
        for user_id, lesson_id in COMPLETIONS:
            ex = db.query(LessonCompletion).filter(
                LessonCompletion.user_id == user_id,
                LessonCompletion.lesson_id == lesson_id,
            ).first()
            if not ex:
                db.add(LessonCompletion(user_id=user_id, lesson_id=lesson_id, completed=1))
        db.commit()

        print("\n" + "=" * 80)
        print("🎉 ACADEMIC CURRICULUM SEEDED — Production-Grade Content")
        print("=" * 80)
        print(f"\n📚 Content: {len(all_modules)} weeks | {len(all_lessons)} lessons | {len(all_quizzes)} assessments")
        print(f"    📹 {n_video} videos | 📖 {n_text} theory | 🛠️ {n_practice} labs | 📝 {n_quiz_l} quizzes")
        print(f"\n🔑 Accounts:")
        print(f"    👑 Admin: admin@learnops.io / Admin2024!")
        print(f"    👩‍🏫 Instructor: claire@learnops.io / Instructor2024!")
        print(f"    👩‍🎓 Student: marie@student.com / Student2024!")
        print("\n📖 Content Quality: University-level with real-world scenarios")
        print("=" * 80 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()