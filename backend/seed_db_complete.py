"""
seed_db.py — Production seeder
Mirrors exactly the frontend mock structure (same IDs, same fields)
but with real, detailed content stored in the database.

Usage:
    python seed_db.py

Adapt the imports at the top to match your actual model paths.
"""

from datetime import datetime, timedelta
import uuid
import json

# ─── Adapt these imports to your project ──────────────────────────────────────
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.module import Module
from app.models.lesson import Lesson 
from app.schemas.quiz import QuizQuestion
from app.models.quiz import Quiz
from app.models.progression import UserProgression, UserBadge
from app.core.security import get_password_hash
# ──────────────────────────────────────────────────────────────────────────────

NOW = datetime.utcnow()
def days_ago(d: int) -> datetime:
    return NOW - timedelta(days=d)


# =============================================================================
#  MODULES  (mirrors course-data.ts)
# =============================================================================
MODULES = [
    {
        "id": "devops-basics",
        "week": 1,
        "order": 1,
        "title": "DevOps Basics",
        "description": "Maîtrisez les fondamentaux DevOps : culture DORA, pipelines CI/CD complets, Docker production-ready et orchestration multi-services avec Docker Compose.",
        "icon": "GitBranch",
    },
    {
        "id": "mlops-fundamentals",
        "week": 2,
        "order": 2,
        "title": "MLOps Fundamentals",
        "description": "Versioning de données avec DVC, tracking d'expériences avec MLflow, validation Great Expectations et détection de drift Evidently pour des pipelines ML reproductibles.",
        "icon": "Brain",
    },
    {
        "id": "deployment-api",
        "week": 3,
        "order": 3,
        "title": "Déploiement & API",
        "description": "APIs ML production-grade avec FastAPI, Kubernetes zero-downtime avec HPA, déploiement cloud AWS/GCP/Azure et GitOps avec ArgoCD.",
        "icon": "Rocket",
    },
    {
        "id": "final-evaluation",
        "week": 4,
        "order": 4,
        "title": "Évaluation finale",
        "description": "Projet complet de bout en bout : pipeline MLOps, API containerisée, CI/CD GitHub Actions, monitoring Prometheus/Grafana et certification finale.",
        "icon": "Award",
    },
]


# =============================================================================
#  LESSONS  (mirrors course-data.ts lessons + lesson-content.ts + video-data.ts)
# =============================================================================
LESSONS = [

    # =========================================================================
    # MODULE 1 — DevOps Basics
    # =========================================================================
    {
        "id": "intro-devops",
        "module_id": "devops-basics",
        "order": 1,
        "title": "Introduction au DevOps",
        "type": "text",
        "duration": 15,
        "description": "Culture DevOps, métriques DORA (Deployment Frequency, Lead Time, Change Failure Rate, MTTR) et stratégies Blue-Green, Canary, Rolling Update.",
        "video_url": None,
        "video_chapters": None,
        # ── theory ──────────────────────────────────────────────────────────
        "theory_title": "Culture DevOps & Métriques DORA",
        "theory_content": """Le DevOps combine le développement logiciel (Dev) et les opérations IT (Ops) pour réduire le cycle de vie du développement et livrer des logiciels de haute qualité en continu.

Les 3 piliers fondamentaux :
• Collaboration : les équipes Dev et Ops partagent la responsabilité du produit de bout en bout
• Automatisation : tout ce qui peut être automatisé doit l'être (tests, déploiements, infra)
• Mesure continue : on mesure tout pour s'améliorer en permanence

Les 4 métriques DORA :

1. Deployment Frequency — À quelle fréquence déployez-vous en production ?
   Élite : plusieurs fois par jour | Faible : moins d'une fois par mois

2. Lead Time for Changes — Délai entre un commit et son déploiement en production ?
   Élite : moins d'une heure | Faible : entre 1 et 6 mois

3. Change Failure Rate — Quel % de déploiements causent un incident ?
   Élite : 0–5% | Faible : 46–60%

4. Time to Restore Service — Temps moyen pour rétablir le service après incident ?
   Élite : moins d'une heure | Faible : entre 1 semaine et 1 mois

Stratégies de déploiement :

Blue-Green : deux environnements identiques, basculement instantané du load balancer.
→ Zéro downtime, rollback en 30 secondes, coût d'infra doublé.

Canary Release : 5% du trafic → observer métriques → 25% → 100%.
→ Réduit le blast radius. Idéal pour les changements à risque.

Rolling Update : mise à jour progressive instance par instance.
→ Pas de doublement d'infra, rollback plus lent.""",
        "theory_code_blocks": [
            {
                "language": "yaml",
                "code": """# .github/workflows/ci.yml — Pipeline CI complet
name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11", cache: "pip" }
      - run: pip install ruff black mypy
      - run: ruff check . && black --check . && mypy app/

  tests:
    needs: quality
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env: { POSTGRES_USER: test, POSTGRES_PASSWORD: test, POSTGRES_DB: testdb }
        options: --health-cmd pg_isready --health-interval 10s --health-retries 5
        ports: ["5432:5432"]
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=app --cov-fail-under=80
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb"""
            }
        ],
        # ── practice ────────────────────────────────────────────────────────
        "practice_title": "Exercice : Mesurer vos métriques DORA",
        "practice_content": """Exercice 1 : Audit DORA de votre organisation

Pour chaque métrique, mesurez votre niveau actuel et définissez un objectif à 3 mois :

1. Deployment Frequency
   → Actuel : ___ fois par semaine/mois | Objectif : ___

2. Lead Time for Changes
   → Mesurez le temps entre votre dernier commit et son déploiement en prod
   → Actuel : ___ heures/jours | Objectif : < 1 jour

3. Change Failure Rate
   → Sur les 10 derniers déploiements, combien ont nécessité un rollback ?
   → Actuel : ___% | Objectif : < 5%

4. Time to Restore
   → Lors du dernier incident, combien de temps pour rétablir le service ?
   → Actuel : ___ | Objectif : < 1h

Exercice 2 : Identifier votre goulot d'étranglement
→ Est-ce les tests lents ? Les revues de code ? Les approbations manuelles ?
→ Proposez une action concrète pour améliorer la métrique la plus faible.""",
        "practice_code_blocks": [
            {
                "language": "bash",
                "code": """# Calculer votre Lead Time depuis Git
git log --tags --simplify-by-decoration \\
  --pretty="format:%ai %d" | head -20

# Mesurer le délai moyen entre commits et releases
git log --oneline --format="%H %ai" | head -50"""
            }
        ],
    },
    {
        "id": "cicd-github-actions",
        "module_id": "devops-basics",
        "order": 2,
        "title": "CI/CD avec GitHub Actions",
        "type": "video",
        "duration": 25,
        "description": "Pipeline complet : lint → tests + coverage → build Docker multi-stage → push GHCR → deploy SSH avec rollback automatique.",
        "video_url": "https://www.youtube.com/embed/R8_veQiYBjI",
        "video_chapters": [
            {"time": 0,    "title": "Introduction & architecture du pipeline"},
            {"time": 90,   "title": "Job quality : ruff, black, mypy"},
            {"time": 300,  "title": "Job tests avec service PostgreSQL"},
            {"time": 540,  "title": "Build Docker multi-stage & push GHCR"},
            {"time": 780,  "title": "Deploy SSH + rollback automatique"},
            {"time": 1020, "title": "Secrets, variables et environnements"},
        ],
        "theory_title": "CI/CD avancé avec GitHub Actions",
        "theory_content": """GitHub Actions est la plateforme CI/CD native de GitHub. Elle permet de créer des pipelines complets directement dans le repo, sans serveur dédié.

Architecture du pipeline MLOps :

  Push/PR
    ↓
  Job 1: quality   (ruff + black + mypy)
    ↓
  Job 2: tests     (pytest + coverage + PostgreSQL service)
    ↓
  Job 3: build     (docker multi-stage + push GHCR)   ← main uniquement
    ↓
  Job 4: deploy    (SSH + docker compose pull + migrate)

Concepts clés :
• Jobs : s'exécutent en parallèle par défaut, séquencés avec `needs`
• Services : containers Docker lancés pour les tests (PostgreSQL, Redis)
• Secrets : variables chiffrées accessibles via ${{ secrets.NAME }}
• Environments : protection rules pour la production (approbation requise)
• Cache : `actions/cache` pour pip, npm, Docker layers""",
        "theory_code_blocks": [
            {
                "language": "yaml",
                "code": """# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11", cache: "pip" }
      - run: pip install ruff black mypy
      - run: ruff check . && black --check . && mypy app/

  tests:
    needs: quality
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready --health-interval 10s
          --health-timeout 5s --health-retries 5
        ports: ["5432:5432"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11", cache: "pip" }
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest tests/ -v --cov=app --cov-report=xml --cov-fail-under=80
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb

  build:
    needs: tests
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    permissions: { contents: read, packages: write }
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: type=sha,prefix=sha-
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/app
            docker compose pull
            docker compose up -d --no-build
            docker compose exec api python -m alembic upgrade head
            sleep 10
            curl -f http://localhost:8000/health || \\
              (docker compose rollback && exit 1)"""
            }
        ],
        "practice_title": "Exercice : Créer votre pipeline CI/CD complet",
        "practice_content": """Étape 1 — Structure du projet
Créez un repository GitHub avec la structure de base.

Étape 2 — Job quality
Configurez ruff, black et mypy. Vérifiez que le job échoue si le code n'est pas formaté.

Étape 3 — Job tests avec PostgreSQL service
Ajoutez un service PostgreSQL et vérifiez que les tests d'intégration passent.

Étape 4 — Build Docker
Configurez le build et push vers GitHub Container Registry (GHCR).

Étape 5 — Deploy SSH
Configurez les secrets PROD_HOST, PROD_USER, PROD_SSH_KEY dans GitHub Settings.""",
        "practice_code_blocks": [
            {
                "language": "bash",
                "code": """mkdir -p .github/workflows
touch .github/workflows/ci-cd.yml

# Vérifier le workflow localement avec act
brew install act
act push --secret-file .secrets"""
            }
        ],
    },
    {
        "id": "docker-fundamentals",
        "module_id": "devops-basics",
        "order": 3,
        "title": "Docker Fondamentaux",
        "type": "practice",
        "duration": 30,
        "description": "Dockerfile multi-stage optimisé, cache layers, utilisateur non-root, HEALTHCHECK, .dockerignore et scan Trivy.",
        "video_url": None,
        "video_chapters": None,
        "theory_title": "Docker production-ready",
        "theory_content": """Docker est une plateforme de containerisation qui package une application avec toutes ses dépendances dans un container isolé et portable.

VM vs Container :
• VM : OS invité complet (2-10 GB), démarrage 1-2 min, isolation totale
• Container : partage le kernel hôte (< 100 MB), démarrage < 1s, isolation processus

Bonnes pratiques pour une image production :
• Base image légère et précise : python:3.11-slim (pas python:latest)
• Copier requirements.txt AVANT le code → exploite le cache Docker
• Ne jamais lancer en root → créer un utilisateur dédié (sécurité)
• Multi-stage build → séparer build et runtime (image 3-5x plus légère)
• HEALTHCHECK → Docker sait si le container est opérationnel
• .dockerignore → exclure .git, __pycache__, *.pyc, tests/

Tailles typiques :
python:3.11        → ~1 GB   (à éviter en prod)
python:3.11-slim   → ~130 MB (recommandé)
python:3.11-alpine → ~50 MB  (attention : incompatibilités musl libc)""",
        "theory_code_blocks": [
            {
                "language": "dockerfile",
                "code": """# ── Stage 1 : Builder ────────────────────────────────
FROM python:3.11-slim AS builder
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
# requirements AVANT le code → cache Docker optimisé
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ── Stage 2 : Runtime ────────────────────────────────
FROM python:3.11-slim
LABEL maintainer="team@company.com"
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \\
    libpq5 curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
# Utilisateur non-root (obligatoire en production)
RUN adduser --disabled-password --gecos '' appuser
USER appuser
COPY --chown=appuser:appuser . .
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]"""
            }
        ],
        "practice_title": "Exercice : Construire une image production-ready",
        "practice_content": """Partie 1 — Build et analyse
1. Écrire le Dockerfile multi-stage
2. Builder l'image et vérifier la taille (doit être < 300 MB)
3. Inspecter les layers avec docker history

Partie 2 — Sécurité
4. Scanner les vulnérabilités avec Trivy
5. Vérifier que le process tourne en non-root

Partie 3 — Performance
6. Mesurer le temps de build à froid vs avec cache
7. Modifier un fichier .py et rebuilder → seule la dernière layer doit être reconstruite""",
        "practice_code_blocks": [
            {
                "language": "bash",
                "code": """# Build
docker build -t myapp:prod .
docker images myapp  # Vérifier la taille

# Inspecter les layers
docker history myapp:prod --human

# Scanner les vulnérabilités
trivy image myapp:prod

# Vérifier utilisateur non-root
docker run --rm myapp:prod whoami  # → appuser (pas root !)

# Test health check
docker run -d -p 8000:8000 --name test myapp:prod
sleep 15
docker inspect test --format='{{.State.Health.Status}}'
# → "healthy"

# .dockerignore
cat > .dockerignore << 'EOF'
.git
__pycache__
*.pyc
.pytest_cache
.mypy_cache
tests/
.env
.env.*
EOF"""
            }
        ],
    },
    {
        "id": "docker-compose",
        "module_id": "devops-basics",
        "order": 4,
        "title": "Docker Compose",
        "type": "practice",
        "duration": 25,
        "description": "Stack API + PostgreSQL + Redis + MLflow avec health checks, depends_on condition:service_healthy et volumes persistants.",
        "video_url": None,
        "video_chapters": None,
        "theory_title": "Docker Compose — Stack MLOps locale complète",
        "theory_content": """Docker Compose permet de définir et gérer des applications multi-containers via un fichier YAML. Indispensable pour reproduire localement un environnement proche de la production.

Concepts clés :
• depends_on + condition: service_healthy → attend que le health check passe (pas juste que le container démarre)
• healthcheck → vérifie l'état de chaque service
• volumes → persistance des données entre redémarrages
• profiles → démarrer uniquement les services nécessaires

Commandes essentielles :
• docker compose up -d             → démarrer en arrière-plan
• docker compose ps                → état de tous les services
• docker compose logs -f api       → logs en temps réel
• docker compose exec api bash     → shell dans le container
• docker compose down -v           → arrêter ET supprimer les volumes""",
        "theory_code_blocks": [
            {
                "language": "yaml",
                "code": """# docker-compose.yml — Stack MLOps locale complète
version: "3.9"

services:
  api:
    build: { context: ., target: runtime }
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
      - MLFLOW_TRACKING_URI=http://mlflow:5000
    depends_on:
      db:    { condition: service_healthy }
      redis: { condition: service_healthy }
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 256mb
    volumes: [redis_data:/data]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 5

  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.9.0
    command: >
      mlflow server
      --backend-store-uri postgresql://user:pass@db:5432/mydb
      --default-artifact-root /mlflow/artifacts
      --host 0.0.0.0 --port 5000
    ports: ["5000:5000"]
    volumes: [mlflow_artifacts:/mlflow/artifacts]
    depends_on:
      db: { condition: service_healthy }

volumes:
  postgres_data:
  redis_data:
  mlflow_artifacts:"""
            }
        ],
        "practice_title": "Exercice : Stack MLOps locale opérationnelle",
        "practice_content": """Étape 1 — Démarrage
Lancez la stack et vérifiez que tous les services sont healthy.

Étape 2 — Vérification
Inspectez l'état de santé de chaque service. Aucun ne doit être unhealthy.

Étape 3 — Communication inter-services
Vérifiez que l'API peut atteindre la DB et Redis depuis le réseau Docker.

Étape 4 — Persistance
Insérez des données, redémarrez les containers (sans -v), vérifiez que les données sont toujours là.""",
        "practice_code_blocks": [
            {
                "language": "bash",
                "code": """docker compose up -d
docker compose ps --format "table {{.Name}}\\t{{.Status}}\\t{{.Health}}"

# Tester la communication réseau
docker compose exec api curl -s http://mlflow:5000/health

# URLs
echo "API docs   → http://localhost:8000/docs"
echo "MLflow UI  → http://localhost:5000"

# Reset complet
docker compose down -v --remove-orphans"""
            }
        ],
    },
    {
        "id": "quiz-devops",
        "module_id": "devops-basics",
        "order": 5,
        "title": "Quiz DevOps Basics",
        "type": "quiz",
        "duration": 10,
        "description": "Testez vos connaissances sur le DevOps",
        "video_url": None,
        "video_chapters": None,
        "theory_title": None,
        "theory_content": None,
        "theory_code_blocks": None,
        "practice_title": None,
        "practice_content": None,
        "practice_code_blocks": None,
    },

    # =========================================================================
    # MODULE 2 — MLOps Fundamentals
    # =========================================================================
    {
        "id": "intro-mlops",
        "module_id": "mlops-fundamentals",
        "order": 1,
        "title": "Introduction au MLOps",
        "type": "text",
        "duration": 20,
        "description": "Les 3 niveaux de maturité MLOps (Google), cycle de vie ML complet, différence avec DevOps et stack technique moderne.",
        "video_url": None,
        "video_chapters": None,
        "theory_title": "MLOps : niveaux de maturité et stack technique",
        "theory_content": """MLOps (Machine Learning Operations) est un ensemble de pratiques qui combinent ML, DevOps et Data Engineering pour déployer et maintenir des modèles ML en production de manière fiable.

Pourquoi MLOps est différent du DevOps classique ?
En ML, 3 artefacts interdépendants sont à gérer (pas 1) :
  1. Le code (modèle, preprocessing, features)
  2. Les données (training set, validation set)
  3. La configuration (hyperparamètres, seuils)

Les 3 niveaux de maturité MLOps (Google) :

Niveau 0 — Manuel
→ Entraînement dans Jupyter Notebooks, déploiement manuel
→ Pas de monitoring, pas de rollback
→ Non reproductible, impossible à maintenir

Niveau 1 — Pipeline ML automatisé
→ Pipeline d'entraînement automatisé (DVC, Prefect)
→ Entraînement déclenché par de nouvelles données
→ Monitoring en production, alertes sur le drift
→ Idéal pour la plupart des équipes ML

Niveau 2 — CI/CD pour les pipelines ML
→ CI/CD pour le code ET les pipelines de données
→ Test automatique des modèles avant promotion en production
→ Pour les organisations avec 10+ modèles en production

Stack MLOps moderne :
  Données        : DVC + Great Expectations + Evidently AI
  Expérimentation: MLflow + Optuna + Jupyter Lab
  Pipeline       : Prefect ou Airflow
  Déploiement    : FastAPI + Docker + Kubernetes
  Monitoring     : Prometheus + Grafana""",
        "theory_code_blocks": [
            {
                "language": "bash",
                "code": """# Installation de la stack MLOps complète
pip install dvc[s3] \\
  mlflow \\
  great-expectations \\
  evidently \\
  optuna \\
  prefect \\
  fastapi uvicorn \\
  prometheus-client"""
            }
        ],
        "practice_title": "Exercice : Planifier un pipeline MLOps",
        "practice_content": """Exercice : Concevoir l'architecture d'un pipeline MLOps

1. Identifiez les étapes du pipeline (collecte, préparation, entraînement, évaluation, déploiement)
2. Choisissez les outils pour chaque étape
3. Définissez les métriques de monitoring
4. Planifiez la stratégie de réentraînement

Template à remplir :

Pipeline: [Nom du projet]
Niveau actuel: [ ] 0 Manuel  [ ] 1 Automatisé  [ ] 2 CI/CD complet

DONNÉES      → collecte: ___ / validation: ___ / versioning: ___
MODÈLE       → entraînement: ___ / tracking: ___ / registry: ___
DÉPLOIEMENT  → serving: ___ / stratégie: ___
MONITORING   → métriques: ___ / drift: ___ / alertes: ___""",
        "practice_code_blocks": None,
    },
    {
        "id": "dvc-versioning",
        "module_id": "mlops-fundamentals",
        "order": 2,
        "title": "Versioning avec DVC",
        "type": "video",
        "duration": 30,
        "description": "dvc add, dvc repro, pipelines reproductibles, remote S3/GCS, dvc exp run et comparaison d'expériences.",
        "video_url": "https://www.youtube.com/embed/kLKBcPonMYw",
        "video_chapters": [
            {"time": 0,    "title": "Pourquoi versionner les données ?"},
            {"time": 120,  "title": "Installation & dvc init"},
            {"time": 280,  "title": "dvc add & dvc push vers S3"},
            {"time": 480,  "title": "dvc.yaml — Pipelines reproductibles"},
            {"time": 720,  "title": "params.yaml — Hyperparamètres versionnés"},
            {"time": 900,  "title": "dvc repro & dvc dag"},
            {"time": 1100, "title": "dvc exp run — Expériences parallèles"},
        ],
        "theory_title": "DVC — Data Version Control",
        "theory_content": """DVC (Data Version Control) gère le versioning des données et des modèles ML, là où Git gère le code.

Principe : DVC stocke les métadonnées (fichiers .dvc) dans Git, et les fichiers volumineux dans S3/GCS/Azure.

Avantages :
• Reproductibilité totale : même code + même data = mêmes résultats
• Pipelines cachés : dvc repro n'exécute que les étapes modifiées
• Comparaison d'expériences : dvc metrics diff, dvc params diff

Workflow classique :
  git init && dvc init
  dvc remote add -d myremote s3://my-bucket/dvc-store
  dvc add data/raw/customers.csv
  git add data/raw/customers.csv.dvc
  git commit -m "Add raw dataset v1"
  dvc push""",
        "theory_code_blocks": [
            {
                "language": "yaml",
                "code": """# dvc.yaml — Pipeline reproductible complet
stages:
  prepare:
    cmd: python src/prepare.py
    deps: [src/prepare.py, data/raw/customers.csv]
    params: [prepare.test_size, prepare.random_seed]
    outs: [data/processed/train.csv, data/processed/test.csv]

  featurize:
    cmd: python src/featurize.py
    deps: [src/featurize.py, data/processed/train.csv]
    params: [featurize.max_features]
    outs: [data/features/train_features.pkl]

  train:
    cmd: python src/train.py
    deps: [src/train.py, data/features/train_features.pkl]
    params: [train.n_estimators, train.max_depth, train.learning_rate]
    outs: [models/model.pkl]
    metrics: [metrics/scores.json]"""
            }
        ],
        "practice_title": "Exercice : Versioning et pipeline reproductible",
        "practice_content": """Étape 1 — Setup DVC
Initialisez DVC dans votre projet et configurez un remote S3 ou local.

Étape 2 — Versionner les données
Ajoutez votre dataset avec dvc add et commitez le fichier .dvc dans Git.

Étape 3 — Pipeline dvc.yaml
Créez un pipeline avec 3 étapes : prepare → train → evaluate.

Étape 4 — Comparer des expériences
Lancez 3 runs avec des hyperparamètres différents et comparez avec dvc exp show.""",
        "practice_code_blocks": [
            {
                "language": "bash",
                "code": """dvc repro                           # Exécute uniquement les étapes modifiées
dvc dag                             # Visualiser le DAG
dvc metrics diff HEAD~1             # Comparer avec la version précédente
dvc exp run --set-param train.n_estimators=100
dvc exp run --set-param train.n_estimators=200
dvc exp show                        # Tableau comparatif"""
            }
        ],
    },
    {
        "id": "mlflow-tracking",
        "module_id": "mlops-fundamentals",
        "order": 3,
        "title": "MLflow pour le tracking",
        "type": "practice",
        "duration": 35,
        "description": "Log params/métriques/artefacts, Model Registry (Staging → Production), nested runs avec Optuna pour l'HPO.",
        "video_url": None,
        "video_chapters": None,
        "theory_title": "MLflow — Tracking & Model Registry",
        "theory_content": """MLflow est la plateforme open-source de référence pour gérer le cycle de vie ML.

Les 4 composants MLflow :
1. Tracking    — Log params, métriques, artefacts pour chaque run
2. Projects    — Packaging reproductible du code ML
3. Models      — Format standard pour le déploiement (REST API, batch)
4. Model Registry — Gestion des versions : None → Staging → Production → Archived

Concepts Tracking :
• Experiment : groupe logique de runs (par projet ou feature)
• Run : une exécution du code d'entraînement
• Params : hyperparamètres (immuables, loggés une fois)
• Metrics : résultats numériques (peuvent évoluer dans le temps)
• Artifacts : fichiers produits (modèle, graphiques, confusion matrix)

Model Registry — Workflow de promotion :
  Entraînement → register_model() → Version "None"
  → Tests automatiques → "Staging"
  → Validation réussie → "Production" (archive l'ancien automatiquement)
  → Modèle retraité → "Archived" (conservé pour rollback)""",
        "theory_code_blocks": [
            {
                "language": "python",
                "code": """import mlflow, mlflow.sklearn, optuna
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, f1_score
from mlflow.models.signature import infer_signature

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("churn-prediction-v2")

def train_and_log(params, X_train, X_test, y_train, y_test):
    with mlflow.start_run(run_name=f"GBT-n{params['n_estimators']}") as run:
        mlflow.log_params(params)
        mlflow.set_tag("author", "ml-team")

        model = GradientBoostingClassifier(**params, random_state=42)
        model.fit(X_train, y_train)

        y_proba = model.predict_proba(X_test)[:, 1]
        mlflow.log_metrics({
            "roc_auc": roc_auc_score(y_test, y_proba),
            "f1_score": f1_score(y_test, y_proba > 0.5, average="weighted"),
        })

        signature = infer_signature(X_train, model.predict(X_train))
        mlflow.sklearn.log_model(
            model, artifact_path="model", signature=signature,
            registered_model_name="churn-predictor",
        )
        return run.info.run_id

# AutoML avec Optuna
def hpo_search(X_train, X_test, y_train, y_test):
    def objective(trial):
        params = {
            "n_estimators":  trial.suggest_int("n_estimators", 50, 500),
            "max_depth":     trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.001, 0.3, log=True),
        }
        with mlflow.start_run(nested=True):
            mlflow.log_params(params)
            model = GradientBoostingClassifier(**params).fit(X_train, y_train)
            score = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
            mlflow.log_metric("roc_auc", score)
        return score

    with mlflow.start_run(run_name="optuna-hpo"):
        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=50, n_jobs=4)
        return study.best_params

# Promotion en production
def promote_to_production():
    client = mlflow.tracking.MlflowClient()
    versions = client.get_latest_versions("churn-predictor", stages=["Staging"])
    client.transition_model_version_stage(
        name="churn-predictor", version=versions[0].version,
        stage="Production", archive_existing_versions=True,
    )
    return mlflow.sklearn.load_model("models:/churn-predictor/Production")"""
            }
        ],
        "practice_title": "Exercice : Tracker et comparer des expériences MLflow",
        "practice_content": """Étape 1 — Démarrer MLflow
Lancez le serveur MLflow et ouvrez l'UI sur http://localhost:5000.

Étape 2 — Lancer plusieurs runs
Entraînez le même modèle avec 3 configs différentes dans le même experiment.

Étape 3 — Comparer dans l'UI
Sélectionnez les 3 runs et comparez les métriques sur un graphique.

Étape 4 — Promouvoir en Production
Enregistrez le meilleur run dans le Model Registry et promouvez-le en Production.""",
        "practice_code_blocks": [
            {
                "language": "bash",
                "code": """mlflow ui --port 5000 &

# Lancer des expériences
python train.py --n-estimators 100 --max-depth 4
python train.py --n-estimators 200 --max-depth 6
python train.py --n-estimators 300 --max-depth 8

# Comparer via CLI
mlflow runs list --experiment-name "churn-prediction-v2" \\
  --order-by "metrics.roc_auc DESC" --max-results 5"""
            }
        ],
    },
    {
        "id": "experiment-management",
        "module_id": "mlops-fundamentals",
        "order": 4,
        "title": "Gestion des expériences",
        "type": "practice",
        "duration": 25,
        "description": "Great Expectations pour la validation, Evidently AI pour le data drift et concept drift en production.",
        "video_url": None,
        "video_chapters": None,
        "theory_title": "Qualité des données & Détection de drift",
        "theory_content": """En ML, la qualité des données est la première cause d'échec en production. "Garbage in = Garbage out."

Data Drift : la distribution des données d'entrée change.
→ Exemple : l'âge moyen des clients passe de 35 à 55 ans.
→ Détection : tests statistiques (Kolmogorov-Smirnov, PSI).
→ Action : re-entraîner sur les nouvelles données.

Concept Drift : la relation entre features et target change.
→ Exemple : des comportements autrefois prédicteurs de churn ne le sont plus.
→ Détection : dégradation des métriques sur le ground truth (J+30).
→ Action : collecter de nouvelles données étiquetées et re-entraîner.

Great Expectations : définit des règles métier (expectations) sur vos données et valide chaque batch avant utilisation.

Evidently AI : compare les données de production à la référence (training set) et génère des rapports HTML avec scores de drift par feature.""",
        "theory_code_blocks": [
            {
                "language": "python",
                "code": """# Great Expectations — Validation avant entraînement
import great_expectations as gx
import pandas as pd

def validate_data(df: pd.DataFrame) -> bool:
    context = gx.get_context()
    datasource = context.sources.add_pandas("ds")
    asset = datasource.add_dataframe_asset("batch")
    batch_def = asset.add_batch_definition_whole_dataframe("full")
    batch_request = batch_def.build_batch_request(dataframe=df)
    suite = context.add_expectation_suite("suite")

    suite.expect_column_values_to_not_be_null("customer_id")
    suite.expect_column_values_to_be_between("age", min_value=18, max_value=100)
    suite.expect_column_values_to_be_between("monthly_charge", min_value=0, max_value=500)
    suite.expect_column_distinct_values_to_be_in_set(
        "contract_type", {"Month-to-month", "One year", "Two year"}
    )
    validator = context.get_validator(batch_request=batch_request, expectation_suite=suite)
    results = validator.validate()
    if not results.success:
        raise ValueError(f"Data validation failed!")
    return True

# Evidently — Détection de drift
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def check_drift(reference_df, current_df) -> dict:
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_df, current_data=current_df)
    report.save_html("drift_report.html")
    result = report.as_dict()
    drift_share = result["metrics"][0]["result"]["drift_share"]
    if drift_share > 0.2:
        print("⚠️ DRIFT DETECTED → trigger retraining!")
    return result["metrics"][0]["result"]"""
            }
        ],
        "practice_title": "Exercice : Valider des données et détecter du drift",
        "practice_content": """Étape 1 — Validation Great Expectations
Créez un suite et testez avec des données invalides (null, hors range, catégorie inconnue).

Étape 2 — Simuler du drift
Créez un dataset "production" avec une distribution différente (âge moyen +13 ans).

Étape 3 — Rapport Evidently
Comparez les deux datasets et ouvrez le rapport HTML généré.

Étape 4 — Décision
Si drift_share > 20% → déclencher le re-training. Sinon → log warning.""",
        "practice_code_blocks": [
            {
                "language": "python",
                "code": """import numpy as np, pandas as pd

# Données de référence (training)
np.random.seed(42)
reference = pd.DataFrame({
    "customer_id": [f"C{i:05d}" for i in range(5000)],
    "age": np.random.normal(35, 10, 5000).clip(18, 80).astype(int),
    "monthly_charge": np.random.normal(65, 20, 5000).clip(20, 150),
    "contract_type": np.random.choice(
        ["Month-to-month","One year","Two year"], 5000, p=[0.5,0.3,0.2]
    ),
    "churn": np.random.binomial(1, 0.27, 5000),
})

# Production avec drift simulé
current = pd.DataFrame({
    "customer_id": [f"P{i:05d}" for i in range(1000)],
    "age": np.random.normal(48, 12, 1000).clip(18, 80).astype(int),  # +13 ans !
    "monthly_charge": np.random.normal(82, 25, 1000).clip(20, 150),   # +17$ !
    "contract_type": np.random.choice(
        ["Month-to-month","One year","Two year"], 1000, p=[0.3,0.4,0.3]
    ),
    "churn": np.random.binomial(1, 0.35, 1000),  # +8% churn !
})

validate_data(reference)
drift = check_drift(reference, current)
print(f"Drift share: {drift['drift_share']:.2%}")"""
            }
        ],
    },
    {
        "id": "quiz-mlops",
        "module_id": "mlops-fundamentals",
        "order": 5,
        "title": "Quiz MLOps Fundamentals",
        "type": "quiz",
        "duration": 10,
        "description": "Testez vos connaissances sur le MLOps",
        "video_url": None,
        "video_chapters": None,
        "theory_title": None, "theory_content": None, "theory_code_blocks": None,
        "practice_title": None, "practice_content": None, "practice_code_blocks": None,
    },

    # =========================================================================
    # MODULE 3 — Deployment & API
    # =========================================================================
    {
        "id": "fastapi-ml",
        "module_id": "deployment-api",
        "order": 1,
        "title": "FastAPI pour ML",
        "type": "video",
        "duration": 25,
        "description": "Architecture complète : schemas Pydantic, lifespan, singleton model loader, batch prediction et tests avec mocks.",
        "video_url": "https://www.youtube.com/embed/7t2alSnE2-I",
        "video_chapters": [
            {"time": 0,    "title": "Architecture de l'API ML"},
            {"time": 120,  "title": "Schemas Pydantic avec validation"},
            {"time": 360,  "title": "Singleton model loader + lifespan"},
            {"time": 600,  "title": "Endpoint batch prediction"},
            {"time": 840,  "title": "Health check & readiness probe"},
            {"time": 1020, "title": "Tests avec mocks & TestClient"},
        ],
        "theory_title": "FastAPI production-grade pour modèles ML",
        "theory_content": """FastAPI est le framework Python recommandé pour les APIs ML en production.

Avantages clés :
• Performance : basé sur Starlette/Uvicorn, aussi rapide que Go et NodeJS
• Validation automatique : Pydantic v2 valide chaque requête et génère des erreurs explicites
• Documentation OpenAPI auto-générée : Swagger UI à /docs
• Async natif : gestion efficace des requêtes concurrentes

Pattern singleton pour le modèle :
→ Le modèle est chargé UNE SEULE FOIS au démarrage (lifespan)
→ @lru_cache() garantit une seule instance même si get_predictor() est appelé des milliers de fois
→ Charger un modèle MLflow prend 2-10s : sans cache, chaque requête serait catastrophiquement lente

Training-serving skew (problème critique) :
→ Le preprocessing en production DOIT être identique à celui de l'entraînement
→ Toute différence produit des prédictions incorrectes SANS erreur visible
→ Solution : partager le même code de preprocessing entre train et serve""",
        "theory_code_blocks": [
            {
                "language": "python",
                "code": """# app/schemas/prediction.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import uuid

class CustomerFeatures(BaseModel):
    customer_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    age: int = Field(..., ge=18, le=100)
    tenure_months: int = Field(..., ge=0, le=120)
    monthly_charge: float = Field(..., ge=0, le=500)
    total_charges: float = Field(..., ge=0)
    contract_type: str

    @field_validator("contract_type")
    @classmethod
    def validate_contract(cls, v):
        valid = {"Month-to-month", "One year", "Two year"}
        if v not in valid:
            raise ValueError(f"Must be one of {valid}")
        return v

class BatchPredictionRequest(BaseModel):
    customers: list[CustomerFeatures] = Field(..., min_length=1, max_length=1000)

class PredictionResult(BaseModel):
    customer_id: str
    churn_probability: float = Field(..., ge=0.0, le=1.0)
    churn_prediction: bool
    confidence: str  # "low" | "medium" | "high"
    model_version: str

# app/services/predictor.py
import mlflow, numpy as np, pandas as pd
from functools import lru_cache

class ModelPredictor:
    def __init__(self):
        self.model = mlflow.sklearn.load_model("models:/churn-predictor/Production")
        client = mlflow.tracking.MlflowClient()
        versions = client.get_latest_versions("churn-predictor", stages=["Production"])
        self.model_version = versions[0].version if versions else "unknown"
        self.model_name = "churn-predictor"

    def preprocess(self, customers):
        df = pd.DataFrame([c.model_dump(exclude={"customer_id"}) for c in customers])
        df["charge_per_month"] = df["total_charges"] / (df["tenure_months"] + 1)
        df["is_long_term"] = (df["tenure_months"] > 24).astype(int)
        df["log_total_charges"] = np.log1p(df["total_charges"])
        return df

    def predict_batch(self, customers):
        df = self.preprocess(customers)
        probas = self.model.predict_proba(df)[:, 1]
        return [
            PredictionResult(
                customer_id=c.customer_id,
                churn_probability=float(p),
                churn_prediction=bool(p > 0.5),
                confidence="high" if (p > 0.8 or p < 0.2) else "medium" if (p > 0.6 or p < 0.4) else "low",
                model_version=str(self.model_version),
            )
            for c, p in zip(customers, probas)
        ]

@lru_cache()
def get_predictor(): return ModelPredictor()

# app/main.py
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_predictor()  # warm-up au démarrage
    yield

app = FastAPI(title="ML Prediction API", version="1.0.0", lifespan=lifespan)

@app.get("/health") async def health(): return {"status": "healthy"}
@app.get("/ready")  async def ready(p=Depends(get_predictor)): return {"status": "ready", "model_version": p.model_version}

@app.post("/v1/predict/batch")
async def predict_batch(req: BatchPredictionRequest, p=Depends(get_predictor)):
    t0 = time.time()
    preds = p.predict_batch(req.customers)
    return {"predictions": preds, "processing_time_ms": (time.time()-t0)*1000, "total": len(preds)}"""
            }
        ],
        "practice_title": "Exercice : Construire et tester l'API",
        "practice_content": """Étape 1 — Lancer l'API
Démarrez FastAPI et vérifiez la doc auto-générée sur /docs.

Étape 2 — Test des endpoints
Testez /health, /ready et /v1/predict/batch avec curl.

Étape 3 — Test de validation Pydantic
Envoyez des requêtes invalides (age=150, contract_type=INVALID) → vérifiez les erreurs 422.

Étape 4 — Test de charge
Utilisez hey ou wrk pour mesurer la latence P50/P95/P99.""",
        "practice_code_blocks": [
            {
                "language": "bash",
                "code": """uvicorn app.main:app --reload --port 8000

curl http://localhost:8000/health

curl -X POST http://localhost:8000/v1/predict/batch \\
  -H "Content-Type: application/json" \\
  -d '{"customers":[{"age":35,"tenure_months":24,"monthly_charge":65.5,"total_charges":1572.0,"contract_type":"One year"}]}'

# Test de validation (doit retourner 422)
curl -X POST http://localhost:8000/v1/predict/batch \\
  -H "Content-Type: application/json" \\
  -d '{"customers":[{"age":150,"contract_type":"INVALID"}]}'"""
            }
        ],
    },
    {
        "id": "model-containerization",
        "module_id": "deployment-api",
        "order": 2,
        "title": "Containerisation de modèles",
        "type": "practice",
        "duration": 30,
        "description": "Multi-stage build pour ML, export ONNX, optimisation de l'image et benchmarking de latence d'inférence.",
        "video_url": None,
        "video_chapters": None,
        "theory_title": "Containerisation de modèles ML",
        "theory_content": """La containerisation est essentielle pour déployer des modèles ML de manière reproductible et scalable.

Étapes clés :
1. Sérialiser le modèle (joblib, ONNX, MLflow format)
2. Créer une API autour du modèle (FastAPI)
3. Écrire un Dockerfile multi-stage optimisé
4. Builder, scanner (Trivy) et tester l'image
5. Pusher vers un registry (GHCR, ECR, GCR)

Export ONNX pour l'inférence optimisée :
→ ONNX Runtime est 3-5x plus rapide que sklearn natif pour l'inférence
→ Interopérable entre frameworks (sklearn, PyTorch, TensorFlow)
→ Taille de modèle réduite

Benchmarking typique d'une API ML containerisée :
→ P50 latency : ~12ms
→ P95 latency : ~45ms
→ Throughput  : ~800 req/s (4 workers, t3.medium)""",
        "theory_code_blocks": [
            {
                "language": "python",
                "code": """# Export ONNX pour inférence optimisée
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt
import numpy as np

# Convertir sklearn → ONNX
initial_type = [("float_input", FloatTensorType([None, X_train.shape[1]]))]
onnx_model = convert_sklearn(model, initial_types=initial_type, target_opset=17)
with open("models/model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# Inférence ONNX (3-5x plus rapide que sklearn)
sess = rt.InferenceSession("models/model.onnx")
input_name = sess.get_inputs()[0].name

def predict_onnx(features: np.ndarray):
    return sess.run(None, {input_name: features.astype(np.float32)})[1][:, 1]"""
            }
        ],
        "practice_title": "Exercice : Containeriser un modèle ML",
        "practice_content": """Étape 1 — Entraîner et sauvegarder un modèle
Entraînez un GradientBoosting sur le dataset churn et exportez-le en ONNX.

Étape 2 — Créer l'API FastAPI
Implémentez l'endpoint /predict/batch avec le modèle ONNX.

Étape 3 — Dockerfile multi-stage
Écrivez un Dockerfile optimisé. L'image finale doit faire < 300 MB.

Étape 4 — Benchmarking
Testez la latence avec hey et comparez sklearn natif vs ONNX Runtime.""",
        "practice_code_blocks": [
            {
                "language": "bash",
                "code": """docker build -t ml-api:prod .
docker run -d -p 8000:8000 --name ml-api ml-api:prod

# Test de charge
hey -n 10000 -c 100 -m POST \\
  -H "Content-Type: application/json" \\
  -d '{"customers":[{"age":35,"tenure_months":24,"monthly_charge":65.5,"total_charges":1572.0,"contract_type":"One year"}]}' \\
  http://localhost:8000/v1/predict/batch

docker stop ml-api && docker rm ml-api"""
            }
        ],
    },
    {
        "id": "cloud-deployment",
        "module_id": "deployment-api",
        "order": 3,
        "title": "Déploiement cloud",
        "type": "video",
        "duration": 35,
        "description": "EKS + Karpenter (AWS), Cloud Run serverless (GCP), AKS (Azure) et GitOps avec ArgoCD.",
        "video_url": "https://www.youtube.com/embed/NTkn6_mEdFM",
        "video_chapters": [
            {"time": 0,    "title": "Comparatif AWS / GCP / Azure"},
            {"time": 180,  "title": "AWS EKS + Karpenter"},
            {"time": 480,  "title": "GCP Cloud Run (serverless)"},
            {"time": 780,  "title": "Azure AKS + Azure ML"},
            {"time": 1020, "title": "GitOps avec ArgoCD"},
            {"time": 1320, "title": "Choix selon votre contexte"},
        ],
        "theory_title": "Déploiement cloud — AWS, GCP, Azure",
        "theory_content": """Chaque provider cloud offre plusieurs options pour déployer des modèles ML :

AWS :
• EKS + Karpenter : K8s managé avec provisioning automatique de nodes
• Fargate         : containers sans gestion de serveur
• SageMaker       : plateforme ML native, coût élevé

GCP :
• Cloud Run       : serverless, scale to zero, idéal pour APIs intermittentes
• GKE Autopilot   : K8s managé simplifié
• Vertex AI       : plateforme ML end-to-end

Azure :
• AKS             : K8s managé
• Container Instances : containers à la demande
• Azure ML        : plateforme ML avec managed endpoints

GitOps avec ArgoCD :
→ L'état du cluster K8s est défini par des fichiers YAML dans Git
→ ArgoCD synchronise automatiquement le cluster dès qu'un commit arrive
→ Tout changement en production passe par une PR → traçabilité totale
→ Rollback = revert du commit Git""",
        "theory_code_blocks": [
            {
                "language": "yaml",
                "code": """# k8s/deployment.yaml — Zero-downtime rolling update
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-api
  namespace: ml-production
spec:
  replicas: 3
  selector:
    matchLabels: { app: ml-api }
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0    # Zero-downtime obligatoire
  template:
    spec:
      containers:
        - name: ml-api
          image: ghcr.io/myorg/ml-api:sha-abc123
          resources:
            requests: { memory: "512Mi", cpu: "250m" }
            limits:   { memory: "1Gi",  cpu: "1000m" }
          startupProbe:
            httpGet: { path: /ready, port: 8000 }
            failureThreshold: 18
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /health, port: 8000 }
            periodSeconds: 10
          readinessProbe:
            httpGet: { path: /ready, port: 8000 }
            periodSeconds: 5
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-api-hpa
  namespace: ml-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-api
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 70 }"""
            }
        ],
        "practice_title": "Exercice : Déployer sur GCP Cloud Run",
        "practice_content": """Étape 1 — Choisir le provider
Selon votre accès (AWS, GCP ou Azure free tier), choisissez votre provider.

Étape 2 — Builder et pusher l'image
Construisez l'image et poussez-la vers le registry du provider.

Étape 3 — Déployer et tester
Déployez le service et testez l'endpoint public avec curl.

Étape 4 — Analyser les coûts
Estimez le coût mensuel avec la calculatrice du provider.""",
        "practice_code_blocks": [
            {
                "language": "bash",
                "code": """# GCP Cloud Run (recommandé pour débuter)
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

gcloud builds submit --tag gcr.io/$PROJECT_ID/ml-api:v1 .

gcloud run deploy ml-api \\
  --image gcr.io/$PROJECT_ID/ml-api:v1 \\
  --region europe-west1 \\
  --memory 2Gi --cpu 2 \\
  --min-instances 1 \\
  --max-instances 50 \\
  --allow-unauthenticated

SERVICE_URL=$(gcloud run services describe ml-api \\
  --region europe-west1 --format='value(status.url)')
curl $SERVICE_URL/health"""
            }
        ],
    },
    {
        "id": "monitoring",
        "module_id": "deployment-api",
        "order": 4,
        "title": "Monitoring",
        "type": "practice",
        "duration": 30,
        "description": "Métriques Prometheus custom (latence, distribution prédictions, drift), dashboards Grafana et alertes AlertManager.",
        "video_url": None,
        "video_chapters": None,
        "theory_title": "Monitoring ML en production",
        "theory_content": """Le monitoring d'une API ML couvre 3 couches :

1. Infrastructure : CPU, RAM, réseau (node-exporter, kube-state-metrics)
2. Application : latence, throughput, taux d'erreur (métriques FastAPI)
3. Modèle ML : distribution des prédictions, drift des features (métriques custom)

Les 4 Golden Signals (Google SRE) :
• Latency   : P50/P95/P99 des temps de réponse
• Traffic   : nombre de requêtes par seconde
• Errors    : taux d'erreurs (4xx, 5xx)
• Saturation: utilisation CPU/RAM (risque de dégradation)

Types de métriques Prometheus :
• Counter   : valeur croissante (total de prédictions)
• Histogram : distribution avec percentiles (latence)
• Gauge     : valeur instantanée (mémoire utilisée, drift score)

Alertes essentielles :
• HighErrorRate    : taux d'erreur > 5% pendant 2 minutes
• HighLatencyP95   : P95 > 1s pendant 5 minutes
• PredictionDrift  : distribution des prédictions décalée > 10%""",
        "theory_code_blocks": [
            {
                "language": "python",
                "code": """# app/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge

PREDICTIONS_TOTAL = Counter(
    "ml_predictions_total", "Total predictions",
    ["model_name", "model_version", "prediction_label"],
)
PREDICTION_LATENCY = Histogram(
    "ml_prediction_latency_seconds", "Latency in seconds",
    ["model_name"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)
CHURN_PROBABILITY = Histogram(
    "ml_churn_probability", "Distribution (drift detection)",
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
)
FEATURE_MEAN = Gauge(
    "ml_feature_mean", "Mean of input features",
    ["feature_name"],
)

import time, pandas as pd

def predict_with_metrics(customers, predictor):
    start = time.time()
    results = predictor.predict_batch(customers)
    PREDICTION_LATENCY.labels(model_name=predictor.model_name).observe(time.time() - start)
    for r in results:
        PREDICTIONS_TOTAL.labels(
            model_name=predictor.model_name,
            model_version=r.model_version,
            prediction_label="churn" if r.churn_prediction else "no_churn",
        ).inc()
        CHURN_PROBABILITY.observe(r.churn_probability)
    df = pd.DataFrame([c.model_dump() for c in customers])
    for col in ["age", "tenure_months", "monthly_charge"]:
        FEATURE_MEAN.labels(feature_name=col).set(df[col].mean())
    return results"""
            }
        ],
        "practice_title": "Exercice : Stack de monitoring opérationnelle",
        "practice_content": """Étape 1 — Démarrer Prometheus + Grafana
Lancez la stack de monitoring avec Docker Compose.

Étape 2 — Exposer les métriques
Ajoutez prometheus-fastapi-instrumentator à l'API et vérifiez /metrics.

Étape 3 — Dashboard Grafana
Importez le dashboard et vérifiez que les métriques remontent.

Étape 4 — Configurer une alerte
Créez une alerte si le P95 de latence dépasse 1s pendant 2 minutes.""",
        "practice_code_blocks": [
            {
                "language": "bash",
                "code": """docker compose -f docker-compose.monitoring.yml up -d
# Grafana  → http://localhost:3000 (admin/admin)
# Prometheus → http://localhost:9090

# Tester les métriques
curl http://localhost:8000/metrics | grep ml_predictions"""
            }
        ],
    },
    {
        "id": "quiz-deployment",
        "module_id": "deployment-api",
        "order": 5,
        "title": "Quiz Déploiement",
        "type": "quiz",
        "duration": 10,
        "description": "Testez vos connaissances sur le déploiement",
        "video_url": None,
        "video_chapters": None,
        "theory_title": None, "theory_content": None, "theory_code_blocks": None,
        "practice_title": None, "practice_content": None, "practice_code_blocks": None,
    },

    # =========================================================================
    # MODULE 4 — Évaluation finale
    # =========================================================================
    {
        "id": "project-recap",
        "module_id": "final-evaluation",
        "order": 1,
        "title": "Projet récapitulatif",
        "type": "practice",
        "duration": 120,
        "description": "Pipeline MLOps complet : DVC + MLflow + FastAPI + Docker + Kubernetes + CI/CD + Prometheus/Grafana.",
        "video_url": None,
        "video_chapters": None,
        "theory_title": "Projet final — Pipeline MLOps complet",
        "theory_content": """Objectif : Déployer un modèle de prédiction de churn en production avec monitoring, CI/CD et re-training automatique.

Composants à implémenter :

1. Modèle ML
   • Dataset versionné avec DVC (remote S3 ou GCS)
   • Pipeline DVC reproductible (prepare → featurize → train → evaluate)
   • Tracking MLflow avec Model Registry

2. API de serving
   • FastAPI avec batch prediction endpoint
   • Dockerfile multi-stage optimisé
   • Tests unitaires avec coverage > 80%

3. CI/CD
   • GitHub Actions : lint → tests → build → push → deploy
   • Déploiement Kubernetes avec rolling update zero-downtime
   • Rollback automatique si les health checks échouent

4. Monitoring
   • Métriques Prometheus custom (latence, distribution des prédictions)
   • Dashboard Grafana avec alertes
   • Détection de drift Evidently hebdomadaire

Critères d'évaluation :
  Pipeline DVC reproductible      : 20 pts
  Tracking MLflow + Model Registry : 20 pts
  API FastAPI + tests (> 80%)     : 20 pts
  CI/CD GitHub Actions complet    : 15 pts
  Déploiement K8s zero-downtime   : 15 pts
  Monitoring Prometheus + Grafana : 10 pts""",
        "theory_code_blocks": [
            {
                "language": "bash",
                "code": """# Structure du projet final
mlops-capstone/
├── .github/workflows/
│   ├── ci.yml       # Lint + tests + coverage
│   └── cd.yml       # Build + push + deploy
├── data/
│   └── raw/         # Versionnées avec DVC
├── src/
│   ├── prepare.py
│   ├── featurize.py
│   ├── train.py
│   └── evaluate.py
├── api/
│   ├── app/
│   ├── tests/
│   └── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   ├── hpa.yaml
│   └── service.yaml
├── monitoring/
│   ├── prometheus.yml
│   └── alerts.yml
├── dvc.yaml
├── params.yaml
├── docker-compose.yml
└── Makefile"""
            }
        ],
        "practice_title": "Instructions du projet final",
        "practice_content": """Semaine 1 — Setup & données
• Forker le template du projet depuis GitHub
• Configurer DVC avec un remote S3 ou GCS
• Implémenter le pipeline DVC complet
• Configurer MLflow et logguer les premières expériences

Semaine 2 — API & containerisation
• Implémenter l'API FastAPI avec tous les endpoints
• Écrire les tests avec coverage > 80%
• Builder l'image Docker multi-stage

Semaine 3 — CI/CD & Kubernetes
• Configurer GitHub Actions (CI + CD)
• Déployer sur K8s (Minikube ou EKS/GKE)
• Valider le rolling update zero-downtime

Semaine 4 — Monitoring & documentation
• Ajouter les métriques Prometheus custom
• Créer le dashboard Grafana
• Écrire le README complet avec architecture diagram""",
        "practice_code_blocks": [
            {
                "language": "makefile",
                "code": """setup:
\tpip install -r requirements.txt -r requirements-dev.txt
\tdvc pull

test:
\tpytest api/tests/ -v --cov=api/app --cov-fail-under=80

train:
\tdvc repro && dvc push

up:
\tdocker compose up -d

deploy:
\tkubectl set image deployment/ml-api \\
\t  ml-api=ghcr.io/myorg/ml-api:$(shell git rev-parse --short HEAD) \\
\t  -n ml-production
\tkubectl rollout status deployment/ml-api -n ml-production"""
            }
        ],
    },
    {
        "id": "final-quiz",
        "module_id": "final-evaluation",
        "order": 2,
        "title": "Quiz final",
        "type": "quiz",
        "duration": 30,
        "description": "Évaluation finale de vos compétences",
        "video_url": None,
        "video_chapters": None,
        "theory_title": None, "theory_content": None, "theory_code_blocks": None,
        "practice_title": None, "practice_content": None, "practice_code_blocks": None,
    },
    {
        "id": "additional-resources",
        "module_id": "final-evaluation",
        "order": 3,
        "title": "Ressources complémentaires",
        "type": "text",
        "duration": 15,
        "description": "Liens et ressources pour aller plus loin",
        "video_url": None,
        "video_chapters": None,
        "theory_title": "Ressources pour aller plus loin",
        "theory_content": """Livres indispensables :
• "The DevOps Handbook"                   — Gene Kim et al.      → Culture DevOps
• "Designing Machine Learning Systems"    — Chip Huyen           → MLOps complet
• "Building Machine Learning Pipelines"   — Hannes Hapke         → Pipelines pratiques
• "Kubernetes in Action"                  — Marko Lukša          → K8s approfondi

Sites et blogs :
• mlops.community                         → La communauté MLOps de référence
• chip.huyen.com                          → Blog ML en production
• martinfowler.com                        → Patterns DevOps et architecture

Certifications recommandées :
• AWS Certified DevOps Engineer           → Avancé
• Google Professional ML Engineer         → Avancé
• CKA (Kubernetes Administrator)          → Intermédiaire
• Azure DevOps Solutions Expert           → Avancé

Communautés :
• MLOps Community Slack  → mlops.community/slack
• CNCF Slack (K8s, Prometheus) → slack.cncf.io

Prochaines étapes :
1. Contribuez à un projet open-source (DVC, MLflow, Evidently)
2. Construisez un projet portfolio end-to-end sur GitHub
3. Passez une certification cloud
4. Rejoignez les communautés et partagez vos apprentissages""",
        "theory_code_blocks": None,
        "practice_title": "Prochaines étapes",
        "practice_content": """Pour continuer votre apprentissage :

1. Rejoignez la communauté MLOps sur Slack/Discord
2. Contribuez à des projets open-source (DVC, MLflow, Evidently)
3. Participez à des hackathons ML
4. Créez votre propre projet de portfolio end-to-end
5. Préparez une certification cloud (AWS, GCP ou Azure)""",
        "practice_code_blocks": None,
    },
]


# =============================================================================
#  QUIZZES  (mirrors quiz-data.ts)
# =============================================================================
QUIZZES = [
    {
        "id": "quiz-devops-basics",
        "module_id": "devops-basics",
        "lesson_id": "quiz-devops",
        "title": "Quiz DevOps Basics",
        "passing_score": 70,
        "time_limit_seconds": 600,
        "questions": [
            {
                "id": "devops-q1",
                "question": "Quelle métrique DORA mesure le pourcentage de déploiements causant un incident en production ?",
                "type": "single",
                "options": ["Deployment Frequency", "Lead Time for Changes", "Change Failure Rate", "Time to Restore Service"],
                "correct_answers": [2],
                "explanation": "Le Change Failure Rate mesure le % de déploiements qui causent un incident ou nécessitent un rollback. Les équipes élite maintiennent ce taux sous 5%. C'est un indicateur clé de la qualité du processus de déploiement.",
            },
            {
                "id": "devops-q2",
                "question": "Quelle stratégie envoie progressivement 5%, puis 25%, puis 100% du trafic vers la nouvelle version ?",
                "type": "single",
                "options": ["Blue-Green Deployment", "Rolling Update", "Canary Release", "Feature Flag"],
                "correct_answers": [2],
                "explanation": "Le Canary Release envoie le trafic progressivement en surveillant les métriques à chaque étape. Si un bug est détecté à 5%, seuls 5% des utilisateurs sont affectés avant le rollback.",
            },
            {
                "id": "devops-q3",
                "question": "Pourquoi copier requirements.txt AVANT le code source dans un Dockerfile Python ?",
                "type": "single",
                "options": [
                    "Pour que pip installe les packages dans le bon ordre",
                    "Pour exploiter le cache Docker : la couche pip install n'est reconstruite que si requirements.txt change",
                    "Pour des raisons de sécurité uniquement",
                    "C'est une convention sans impact technique",
                ],
                "correct_answers": [1],
                "explanation": "Docker invalide le cache dès qu'une layer change. En copiant requirements.txt en premier, la layer pip install (lourde) n'est reconstruite que si les dépendances changent, pas à chaque modification du code source.",
            },
            {
                "id": "devops-q4",
                "question": "Quels éléments sont des bonnes pratiques pour un Dockerfile production-ready ?",
                "type": "multiple",
                "options": [
                    "Utiliser un utilisateur non-root",
                    "Utiliser FROM python:latest pour avoir la dernière version",
                    "Ajouter un HEALTHCHECK",
                    "Utiliser un multi-stage build pour réduire la taille de l'image",
                ],
                "correct_answers": [0, 2, 3],
                "explanation": "Un Dockerfile production-ready utilise un utilisateur non-root (sécurité), un HEALTHCHECK (observabilité), et un multi-stage build (image légère). `python:latest` est à éviter car il introduit des changements non contrôlés.",
            },
            {
                "id": "devops-q5",
                "question": "Docker Compose permet d'orchestrer plusieurs containers avec un fichier YAML.",
                "type": "boolean",
                "options": ["Vrai", "Faux"],
                "correct_answers": [0],
                "explanation": "Docker Compose est exactement conçu pour ça : définir et gérer des applications multi-containers (API + DB + Redis + etc.) avec un seul fichier docker-compose.yml.",
            },
        ],
    },
    {
        "id": "quiz-mlops-fundamentals",
        "module_id": "mlops-fundamentals",
        "lesson_id": "quiz-mlops",
        "title": "Quiz MLOps Fundamentals",
        "passing_score": 70,
        "time_limit_seconds": 600,
        "questions": [
            {
                "id": "mlops-q1",
                "question": "Que stocke DVC dans Git vs dans le remote storage S3 ?",
                "type": "single",
                "options": [
                    "Les données dans Git, le code dans S3",
                    "Les métadonnées (.dvc files) dans Git, les fichiers volumineux dans S3",
                    "Tout dans Git avec Git LFS",
                    "Le modèle dans Git, le dataset dans S3",
                ],
                "correct_answers": [1],
                "explanation": "DVC stocke les fichiers .dvc (petites métadonnées avec hash MD5) dans Git, et les données réelles (souvent des GB) dans un remote storage. Git garde ainsi un historique léger.",
            },
            {
                "id": "mlops-q2",
                "question": "Quelle commande DVC exécute uniquement les étapes modifiées du pipeline ?",
                "type": "single",
                "options": ["dvc run", "dvc pipeline execute", "dvc repro", "dvc stage run"],
                "correct_answers": [2],
                "explanation": "`dvc repro` reproduit le pipeline en ne ré-exécutant que les étapes dont les dépendances ont changé. Indispensable pour les pipelines ML coûteux (entraînement de plusieurs heures).",
            },
            {
                "id": "mlops-q3",
                "question": "Quelles fonctionnalités offre le MLflow Model Registry ?",
                "type": "multiple",
                "options": [
                    "Versioning des modèles avec états (None → Staging → Production)",
                    "Entraînement distribué GPU",
                    "Transition de stage manuelle ou via API",
                    "Rollback vers une version précédente du modèle",
                ],
                "correct_answers": [0, 2, 3],
                "explanation": "Le Model Registry gère : versioning, transitions de stage, et rollback. L'entraînement distribué GPU n'est pas une fonctionnalité native de MLflow.",
            },
            {
                "id": "mlops-q4",
                "question": "MLOps est uniquement utile pour les grandes entreprises.",
                "type": "boolean",
                "options": ["Vrai", "Faux"],
                "correct_answers": [1],
                "explanation": "MLOps bénéficie à toute équipe ML, même avec une seule personne. La reproductibilité (DVC), le tracking (MLflow) et le monitoring sont utiles dès le premier modèle en production.",
            },
            {
                "id": "mlops-q5",
                "question": "Pourquoi Great Expectations doit lever une exception (pas juste un warning) si une validation échoue en production ?",
                "type": "single",
                "options": [
                    "Pour respecter les bonnes pratiques Python",
                    "Car continuer avec des données corrompues produirait des prédictions incorrectes en silence",
                    "Pour que le pipeline s'arrête et notifie l'équipe",
                    "Les deux dernières réponses sont correctes",
                ],
                "correct_answers": [3],
                "explanation": "Fail-fast : continuer avec des données invalides produirait des prédictions silencieusement incorrectes (très difficile à déboguer), ET l'arrêt permet de notifier l'équipe immédiatement.",
            },
        ],
    },
    {
        "id": "quiz-deployment-api",
        "module_id": "deployment-api",
        "lesson_id": "quiz-deployment",
        "title": "Quiz Déploiement & API",
        "passing_score": 70,
        "time_limit_seconds": 600,
        "questions": [
            {
                "id": "deploy-q1",
                "question": "Pourquoi utilise-t-on `@lru_cache()` sur `get_predictor()` dans FastAPI ?",
                "type": "single",
                "options": [
                    "Pour mettre les réponses HTTP en cache",
                    "Pour charger le modèle une seule fois au démarrage et réutiliser l'instance (singleton)",
                    "Pour améliorer la validation Pydantic",
                    "Pour compresser les réponses JSON",
                ],
                "correct_answers": [1],
                "explanation": "`@lru_cache()` garantit que le modèle est chargé UNE SEULE FOIS. Charger un modèle MLflow prend 2-10 secondes : sans cache, chaque requête serait catastrophiquement lente.",
            },
            {
                "id": "deploy-q2",
                "question": "Dans un Deployment Kubernetes, que garantit `maxUnavailable: 0` ?",
                "type": "single",
                "options": [
                    "Aucun nouveau pod ne peut être créé",
                    "Zero-downtime : aucun pod ne peut être indisponible pendant le rolling update",
                    "Le déploiement échoue si 0 pods sont disponibles",
                    "Kubernetes déploie un pod à la fois",
                ],
                "correct_answers": [1],
                "explanation": "`maxUnavailable: 0` garantit que la capacité ne descend jamais sous 100% pendant le déploiement. K8s attend qu'un nouveau pod soit Ready avant de terminer l'ancien. Obligatoire pour les APIs ML critiques.",
            },
            {
                "id": "deploy-q3",
                "question": "Quelle probe Kubernetes retire un pod du load balancer sans le redémarrer ?",
                "type": "single",
                "options": ["livenessProbe", "startupProbe", "readinessProbe", "healthProbe"],
                "correct_answers": [2],
                "explanation": "La readinessProbe retire le pod du Service si elle échoue, sans le redémarrer. La livenessProbe redémarre le pod. Pour une API ML : si le modèle n'est pas chargé, readiness=false mais le pod reste en vie.",
            },
            {
                "id": "deploy-q4",
                "question": "Le monitoring de modèles ML en production est optionnel si le code est bien testé.",
                "type": "boolean",
                "options": ["Vrai", "Faux"],
                "correct_answers": [1],
                "explanation": "Le monitoring est obligatoire même avec un code parfait. Les données de production changent (data drift), les comportements évoluent (concept drift), et les performances peuvent chuter sans aucun bug dans le code.",
            },
            {
                "id": "deploy-q5",
                "question": "Qu'est-ce que le training-serving skew et pourquoi est-ce dangereux ?",
                "type": "single",
                "options": [
                    "Le modèle est plus lent en production qu'en entraînement",
                    "Le preprocessing est différent entre l'entraînement et la prod, produisant des prédictions incorrectes sans erreur visible",
                    "Les données de production ont un format différent",
                    "La version Python est différente entre les environnements",
                ],
                "correct_answers": [1],
                "explanation": "Le training-serving skew est une des causes les plus fréquentes de dégradation silencieuse. Si une feature est calculée différemment en train vs prod, le modèle reçoit des inputs inconnus et produit des prédictions incorrectes SANS aucune erreur.",
            },
        ],
    },
    {
        "id": "quiz-final",
        "module_id": "final-evaluation",
        "lesson_id": "final-quiz",
        "title": "Quiz Final",
        "passing_score": 75,
        "time_limit_seconds": 1800,
        "questions": [
            {
                "id": "final-q1",
                "question": "Quel outil est spécifiquement conçu pour le versioning de données dans les pipelines MLOps ?",
                "type": "single",
                "options": ["Git LFS", "DVC", "Docker", "Kubernetes"],
                "correct_answers": [1],
                "explanation": "DVC versionne les datasets et modèles ML, stocke les métadonnées dans Git et les fichiers dans S3/GCS. Git LFS ne gère pas les pipelines reproductibles.",
            },
            {
                "id": "final-q2",
                "question": "Quels éléments font partie d'un pipeline CI/CD MLOps complet ?",
                "type": "multiple",
                "options": [
                    "Tests automatisés (unitaires + intégration)",
                    "Build Docker et push vers un registry",
                    "Validation des données (Great Expectations)",
                    "Design de l'interface utilisateur",
                ],
                "correct_answers": [0, 1, 2],
                "explanation": "Un pipeline CI/CD MLOps inclut : tests, build/push Docker, ET validation des données. La validation est spécifique au ML. Le design UI n'est pas une étape CI/CD.",
            },
            {
                "id": "final-q3",
                "question": "Docker et les machines virtuelles sont la même chose.",
                "type": "boolean",
                "options": ["Vrai", "Faux"],
                "correct_answers": [1],
                "explanation": "Docker utilise la containerisation (partage le kernel hôte, < 1s de démarrage, < 100MB). Les VMs virtualisent l'OS complet (2-10GB, 1-2 min de démarrage). Deux mécanismes d'isolation très différents.",
            },
            {
                "id": "final-q4",
                "question": "Quelle est la meilleure pratique pour valider un modèle challenger sans risque business ?",
                "type": "single",
                "options": [
                    "Le déployer directement en production et observer les métriques",
                    "Le tester uniquement sur des données historiques",
                    "Utiliser le Shadow Mode : le challenger reçoit le trafic réel mais ses prédictions ne sont pas retournées",
                    "Faire un A/B test à 50/50 dès le départ",
                ],
                "correct_answers": [2],
                "explanation": "Le Shadow Mode teste le challenger sur du trafic réel sans risque : les prédictions sont loguées mais jamais retournées aux utilisateurs. Ensuite on passe à un A/B test progressif (5% → 25% → 100%).",
            },
            {
                "id": "final-q5",
                "question": "Quels éléments doivent être versionnés dans un projet MLOps pour garantir la reproductibilité totale ?",
                "type": "multiple",
                "options": [
                    "Le code source (Git)",
                    "Les données et features (DVC)",
                    "Les hyperparamètres (params.yaml + DVC/MLflow)",
                    "Les artefacts du modèle (MLflow Model Registry)",
                ],
                "correct_answers": [0, 1, 2, 3],
                "explanation": "La reproductibilité totale nécessite les 4 : code (Git), données (DVC), hyperparamètres (params.yaml), et modèles (MLflow Registry). Manquer l'un d'eux rend la reproduction impossible.",
            },
        ],
    },
]


# =============================================================================
#  USERS  (mirrors mock-users.ts)
# =============================================================================
USERS = [
    # Admins
    {"id": "a1",  "first_name": "Alice",   "last_name": "Martin",   "email": "admin@devops.com",    "password": "Admin123!",  "role": "admin",      "status": "active",  "created_days_ago": 90, "last_login_days_ago": 0,  "progression": 100, "modules_completed": ["devops-basics","mlops-fundamentals","deployment-api","final-evaluation"], "badges": ["first-lesson","quiz-master","devops-pro","mlops-expert"]},
    {"id": "a2",  "first_name": "Bruno",   "last_name": "Garcia",   "email": "bruno@devops.com",    "password": "Admin123!",  "role": "admin",      "status": "active",  "created_days_ago": 85, "last_login_days_ago": 1,  "progression": 90,  "modules_completed": ["devops-basics","mlops-fundamentals","deployment-api"], "badges": ["first-lesson","quiz-master","devops-pro"]},
    # Instructors
    {"id": "i1",  "first_name": "Claire",  "last_name": "Dubois",   "email": "claire@devops.com",   "password": "Instr123!",  "role": "instructor", "status": "active",  "created_days_ago": 60, "last_login_days_ago": 0,  "progression": 85,  "modules_completed": ["devops-basics","mlops-fundamentals","deployment-api"], "badges": ["first-lesson","quiz-master"]},
    {"id": "i2",  "first_name": "David",   "last_name": "Leroy",    "email": "david@devops.com",    "password": "Instr123!",  "role": "instructor", "status": "active",  "created_days_ago": 55, "last_login_days_ago": 2,  "progression": 70,  "modules_completed": ["devops-basics","mlops-fundamentals"], "badges": ["first-lesson"]},
    {"id": "i3",  "first_name": "Emma",    "last_name": "Bernard",  "email": "emma@devops.com",     "password": "Instr123!",  "role": "instructor", "status": "active",  "created_days_ago": 50, "last_login_days_ago": 3,  "progression": 60,  "modules_completed": ["devops-basics","mlops-fundamentals"], "badges": ["first-lesson"]},
    # Students
    {"id": "s1",  "first_name": "Marie",   "last_name": "Dupont",   "email": "marie@example.com",   "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 30, "last_login_days_ago": 0,  "progression": 75,  "modules_completed": ["devops-basics","mlops-fundamentals","deployment-api"], "badges": ["first-lesson","quiz-master"]},
    {"id": "s2",  "first_name": "Jean",    "last_name": "Moreau",   "email": "jean@example.com",    "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 28, "last_login_days_ago": 1,  "progression": 55,  "modules_completed": ["devops-basics","mlops-fundamentals"], "badges": ["first-lesson"]},
    {"id": "s3",  "first_name": "Sophie",  "last_name": "Laurent",  "email": "sophie@example.com",  "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 25, "last_login_days_ago": 0,  "progression": 90,  "modules_completed": ["devops-basics","mlops-fundamentals","deployment-api"], "badges": ["first-lesson","quiz-master","devops-pro"]},
    {"id": "s4",  "first_name": "Pierre",  "last_name": "Thomas",   "email": "pierre@example.com",  "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 22, "last_login_days_ago": 2,  "progression": 40,  "modules_completed": ["devops-basics"], "badges": ["first-lesson"]},
    {"id": "s5",  "first_name": "Léa",     "last_name": "Robert",   "email": "lea@example.com",     "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 20, "last_login_days_ago": 1,  "progression": 65,  "modules_completed": ["devops-basics","mlops-fundamentals"], "badges": ["first-lesson"]},
    {"id": "s6",  "first_name": "Lucas",   "last_name": "Richard",  "email": "lucas@example.com",   "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 18, "last_login_days_ago": 3,  "progression": 30,  "modules_completed": ["devops-basics"], "badges": ["first-lesson"]},
    {"id": "s7",  "first_name": "Camille", "last_name": "Durand",   "email": "camille@example.com", "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 15, "last_login_days_ago": 0,  "progression": 85,  "modules_completed": ["devops-basics","mlops-fundamentals","deployment-api"], "badges": ["first-lesson","quiz-master"]},
    {"id": "s8",  "first_name": "Hugo",    "last_name": "Petit",    "email": "hugo@example.com",    "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 12, "last_login_days_ago": 4,  "progression": 20,  "modules_completed": [], "badges": []},
    {"id": "s9",  "first_name": "Chloé",   "last_name": "Roux",     "email": "chloe@example.com",   "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 10, "last_login_days_ago": 1,  "progression": 50,  "modules_completed": ["devops-basics","mlops-fundamentals"], "badges": ["first-lesson"]},
    {"id": "s10", "first_name": "Thomas",  "last_name": "Fournier", "email": "thomas@example.com",  "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 8,  "last_login_days_ago": 0,  "progression": 45,  "modules_completed": ["devops-basics"], "badges": ["first-lesson"]},
    {"id": "s11", "first_name": "Manon",   "last_name": "Girard",   "email": "manon@example.com",   "password": "Student1!",  "role": "student",    "status": "blocked", "created_days_ago": 7,  "last_login_days_ago": 5,  "progression": 10,  "modules_completed": [], "badges": []},
    {"id": "s12", "first_name": "Nathan",  "last_name": "Andre",    "email": "nathan@example.com",  "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 5,  "last_login_days_ago": 0,  "progression": 15,  "modules_completed": [], "badges": []},
    {"id": "s13", "first_name": "Julie",   "last_name": "Mercier",  "email": "julie@example.com",   "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 3,  "last_login_days_ago": 0,  "progression": 5,   "modules_completed": [], "badges": []},
    {"id": "s14", "first_name": "Antoine", "last_name": "Blanc",    "email": "antoine@example.com", "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 2,  "last_login_days_ago": 0,  "progression": 0,   "modules_completed": [], "badges": []},
    {"id": "s15", "first_name": "Laura",   "last_name": "Guerin",   "email": "laura@example.com",   "password": "Student1!",  "role": "student",    "status": "active",  "created_days_ago": 1,  "last_login_days_ago": 0,  "progression": 0,   "modules_completed": [], "badges": []},
]


# =============================================================================
#  SEED
# =============================================================================
def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("\n🌱 Seeding database...\n")

        # ── 1. Modules ────────────────────────────────────────────────────────
        for m in MODULES:
            db.merge(Module(
                id=m["id"],
                week=m["week"],
                order=m["order"],
                title=m["title"],
                description=m["description"],
                icon=m["icon"],
            ))
        db.commit()
        print(f"✅  {len(MODULES)} modules")

        # ── 2. Lessons ────────────────────────────────────────────────────────
        for l in LESSONS:
            db.merge(Lesson(
                id=l["id"],
                module_id=l["module_id"],
                order=l["order"],
                title=l["title"],
                type=l["type"],
                duration=l["duration"],
                description=l["description"],
                video_url=l.get("video_url"),
                video_chapters=json.dumps(l["video_chapters"]) if l.get("video_chapters") else None,
                theory_title=l.get("theory_title"),
                theory_content=l.get("theory_content"),
                theory_code_blocks=json.dumps(l["theory_code_blocks"]) if l.get("theory_code_blocks") else None,
                practice_title=l.get("practice_title"),
                practice_content=l.get("practice_content"),
                practice_code_blocks=json.dumps(l["practice_code_blocks"]) if l.get("practice_code_blocks") else None,
            ))
        db.commit()
        print(f"✅  {len(LESSONS)} lessons")

        # ── 3. Quizzes ────────────────────────────────────────────────────────
        for q in QUIZZES:
            db.merge(Quiz(
                id=q["id"],
                module_id=q["module_id"],
                lesson_id=q["lesson_id"],
                title=q["title"],
                passing_score=q["passing_score"],
                time_limit_seconds=q["time_limit_seconds"],
                questions=json.dumps(q["questions"]),
            ))
        db.commit()
        total_questions = sum(len(q["questions"]) for q in QUIZZES)
        print(f"✅  {len(QUIZZES)} quizzes ({total_questions} questions)")

        # ── 4. Users ──────────────────────────────────────────────────────────
        for u in USERS:
            db.merge(User(
                id=u["id"],
                first_name=u["first_name"],
                last_name=u["last_name"],
                email=u["email"],
                hashed_password=get_password_hash(u["password"]),
                role=u["role"],
                is_active=u["status"] == "active",
                created_at=days_ago(u["created_days_ago"]),
                last_login=days_ago(u["last_login_days_ago"]),
            ))
        db.commit()
        print(f"✅  {len(USERS)} users")

        # ── 5. Progressions & Badges ──────────────────────────────────────────
        for u in USERS:
            db.merge(UserProgression(
                id=f"prog-{u['id']}",
                user_id=u["id"],
                progression=u["progression"],
                modules_completed=json.dumps(u["modules_completed"]),
                time_spent_minutes=u["progression"] * 8,
            ))
            for badge in u["badges"]:
                db.merge(UserBadge(
                    id=f"badge-{u['id']}-{badge}",
                    user_id=u["id"],
                    badge_name=badge,
                    earned_at=days_ago(u["created_days_ago"] - 1),
                ))
        db.commit()
        print(f"✅  progressions & badges")

        # ── Summary ───────────────────────────────────────────────────────────
        print("\n" + "=" * 55)
        print("🎉  Database seeded successfully!")
        print("=" * 55)
        print("\n📝  Credentials:")
        print("  👑  Admin      : admin@devops.com    / Admin123!")
        print("  👨‍🏫  Instructor : claire@devops.com  / Instr123!")
        print("  👨‍🎓  Student    : marie@example.com  / Student1!")
        print(f"\n📚  Content:")
        print(f"  • {len(MODULES)} modules")
        print(f"  • {len(LESSONS)} lessons  (text, video, practice, quiz)")
        print(f"  • {len(QUIZZES)} quizzes  ({total_questions} questions)")
        print(f"  • {len(USERS)} users    (2 admins, 3 instructors, 15 students)")
        print("=" * 55 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌  Error: {e}")
        import traceback; traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed()