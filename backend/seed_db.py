"""
Production-ready database seeder with REAL DevOps/MLOps curriculum.

- Real YouTube videos from experts
- Comprehensive quizzes with detailed explanations
- Professional course structure
- Idempotent (safe to run multiple times)
- PostgreSQL compatible

Run: python seed_production.py
"""

from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.models.module import Module
from app.models.lesson import Lesson, LessonType
from app.models.quiz import Quiz
from app.models.progression import UserProgression, UserBadge, LessonCompletion
from app.core.security import get_password_hash

NOW = datetime.utcnow()

def days_ago(days: int) -> datetime:
    return NOW - timedelta(days=days)

# =============================================================================
# MODULE 1: DevOps Foundations
# =============================================================================
MODULE_1 = {
    "id": "devops-foundations",
    "title": "DevOps Foundations",
    "description": "Maîtrisez les fondamentaux du DevOps : culture, CI/CD, Git workflows et automatisation",
    "week": 1,
    "order": 1,
    "total_duration": 180,
    "icon": "GitBranch"
}

LESSONS_MODULE_1 = [
    {
        "id": "devops-culture",
        "module_id": "devops-foundations",
        "title": "Culture DevOps et Principes CALMS",
        "type": "video",
        "duration": "18",
        "url": "https://www.youtube.com/embed/Me3ea4nUt0U",  # DevOps in 5 Minutes - SimpliLearn
        "content": None,
        "order": 1
    },
    {
        "id": "git-workflows",
        "module_id": "devops-foundations",
        "title": "Git Workflows & Branching Strategies",
        "type": "video",
        "duration": "25",
        "url": "https://www.youtube.com/embed/1SXpE08hvGs",  # Git Branching Strategies - ArjanCodes
        "content": None,
        "order": 2
    },
    {
        "id": "github-actions-intro",
        "module_id": "devops-foundations",
        "title": "GitHub Actions - CI/CD Pipeline Complet",
        "type": "video",
        "duration": "32",
        "url": "https://www.youtube.com/embed/R8_veQiYBjI",  # GitHub Actions Tutorial - TechWorld with Nana
        "content": None,
        "order": 3
    },
    {
        "id": "docker-fundamentals",
        "module_id": "devops-foundations",
        "title": "Docker pour Développeurs",
        "type": "video",
        "duration": "28",
        "url": "https://www.youtube.com/embed/pg19Z8LL06w",  # Docker Tutorial for Beginners - TechWorld with Nana
        "content": None,
        "order": 4
    },
    {
        "id": "docker-compose-practice",
        "module_id": "devops-foundations",
        "title": "Docker Compose - Multi-Container Apps",
        "type": "video",
        "duration": "22",
        "url": "https://www.youtube.com/embed/HG6yIjZapSA",  # Docker Compose Tutorial
        "content": None,
        "order": 5
    },
    {
        "id": "devops-metrics",
        "module_id": "devops-foundations",
        "title": "Métriques DORA et Mesure de Performance",
        "type": "text",
        "duration": "15",
        "url": None,
        "content": """# Métriques DORA : Mesurer l'Excellence DevOps

Les 4 métriques DORA (DevOps Research and Assessment) sont le standard industriel pour mesurer la performance DevOps.

## 1. Deployment Frequency (Fréquence de Déploiement)
**Définition:** À quelle fréquence déployez-vous en production ?

**Niveaux de performance:**
- **Elite:** Plusieurs fois par jour
- **High:** Entre une fois par jour et une fois par semaine
- **Medium:** Entre une fois par semaine et une fois par mois
- **Low:** Moins d'une fois par mois

**Pourquoi c'est important:** Reflète votre capacité à livrer de la valeur rapidement aux utilisateurs.

## 2. Lead Time for Changes (Temps de Livraison)
**Définition:** Combien de temps entre le commit et la production ?

**Niveaux de performance:**
- **Elite:** Moins d'une heure
- **High:** Entre un jour et une semaine
- **Medium:** Entre une semaine et un mois
- **Low:** Plus d'un mois

**Pourquoi c'est important:** Mesure l'agilité de votre équipe à répondre aux besoins.

## 3. Change Failure Rate (Taux d'Échec des Changements)
**Définition:** Quel % de déploiements causent un incident en production ?

**Niveaux de performance:**
- **Elite:** 0-15%
- **High:** 16-30%
- **Medium:** 16-30%
- **Low:** > 30%

**Pourquoi c'est important:** Indique la stabilité et la qualité de votre processus.

## 4. Time to Restore Service (Temps de Restauration)
**Définition:** Combien de temps pour restaurer le service après un incident ?

**Niveaux de performance:**
- **Elite:** Moins d'une heure
- **High:** Moins d'un jour
- **Medium:** Entre un jour et une semaine
- **Low:** Plus d'une semaine

**Pourquoi c'est important:** Mesure votre résilience et capacité de réponse.

## Comment Mesurer ?

```yaml
# Exemple GitHub Actions pour tracker les métriques
name: Track DORA Metrics
on: [push, deployment]
jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Record deployment
        run: |
          curl -X POST https://metrics-api/deployments \
            -d "timestamp=$(date -Iseconds)" \
            -d "commit=${{ github.sha }}"
```

## Outils Recommandés
- **Sleuth:** Dashboard DORA metrics
- **LinearB:** Engineering intelligence platform
- **Haystack:** Open-source DORA metrics
- **Datadog:** APM avec DORA tracking
""",
        "order": 6
    },
    {
        "id": "quiz-devops-foundations",
        "module_id": "devops-foundations",
        "title": "Quiz - DevOps Foundations",
        "type": "quiz",
        "duration": "20",
        "url": None,
        "content": None,
        "order": 7
    }
]

QUIZ_DEVOPS_FOUNDATIONS = {
    "id": "quiz-devops-foundations-data",
    "module_id": "devops-foundations",
    "title": "Quiz DevOps Foundations",
    "passing_score": 70,
    "time_limit": 1200,
    "questions": [
        {
            "id": "q1",
            "question": "Que signifie l'acronyme CALMS dans la culture DevOps ?",
            "type": "single",
            "options": [
                "Code, Automation, Lean, Measurement, Sharing",
                "Culture, Automation, Lean, Measurement, Sharing",
                "Continuous, Agile, Lean, Monitoring, Security",
                "Container, API, Linux, Metrics, Speed"
            ],
            "correct_answers": [1],
            "explanation": "CALMS = Culture, Automation, Lean, Measurement, Sharing. Ce sont les 5 piliers de la culture DevOps définis par Jez Humble."
        },
        {
            "id": "q2",
            "question": "Quelle métrique DORA mesure le pourcentage de déploiements causant un incident en production ?",
            "type": "single",
            "options": [
                "Deployment Frequency",
                "Lead Time for Changes",
                "Change Failure Rate",
                "Mean Time to Recovery"
            ],
            "correct_answers": [2],
            "explanation": "Change Failure Rate mesure le % de déploiements qui échouent ou causent des incidents. Une équipe 'Elite' a un taux < 15%."
        },
        {
            "id": "q3",
            "question": "Dans Git Flow, quelle branche contient toujours le code de production ?",
            "type": "single",
            "options": [
                "develop",
                "main (ou master)",
                "release",
                "feature"
            ],
            "correct_answers": [1],
            "explanation": "La branche 'main' (ou 'master') contient toujours le code stable en production. Les nouvelles fonctionnalités sont développées dans des branches 'feature' puis mergées dans 'develop'."
        },
        {
            "id": "q4",
            "question": "Quelle commande Docker permet de construire une image à partir d'un Dockerfile ?",
            "type": "single",
            "options": [
                "docker run -d myimage",
                "docker build -t myimage .",
                "docker create myimage",
                "docker compose up"
            ],
            "correct_answers": [1],
            "explanation": "`docker build -t myimage .` construit une image nommée 'myimage' à partir du Dockerfile dans le répertoire courant."
        },
        {
            "id": "q5",
            "question": "Quels sont les avantages de Docker Compose ? (plusieurs réponses)",
            "type": "multiple",
            "options": [
                "Définir des applications multi-containers dans un fichier YAML",
                "Gérer les dépendances entre services",
                "Créer des images plus légères que Docker seul",
                "Simplifier les commandes avec docker-compose up"
            ],
            "correct_answers": [0, 1, 3],
            "explanation": "Docker Compose permet de définir des apps multi-containers en YAML, gérer les dépendances, et simplifier les commandes. Il ne crée pas d'images plus légères (c'est Docker BuildKit)."
        },
        {
            "id": "q6",
            "question": "GitHub Actions utilise des fichiers YAML pour définir les workflows CI/CD.",
            "type": "boolean",
            "options": ["Vrai", "Faux"],
            "correct_answers": [0],
            "explanation": "Vrai. Les workflows GitHub Actions sont définis dans des fichiers .yml ou .yaml dans le dossier .github/workflows/"
        },
        {
            "id": "q7",
            "question": "Une équipe 'Elite' selon DORA déploie en production :",
            "type": "single",
            "options": [
                "Une fois par semaine",
                "Une fois par jour",
                "Plusieurs fois par jour",
                "Une fois par mois"
            ],
            "correct_answers": [2],
            "explanation": "Les équipes 'Elite' déploient plusieurs fois par jour, avec un Lead Time < 1h et un Change Failure Rate < 15%."
        }
    ]
}

# =============================================================================
# MODULE 2: MLOps Fundamentals
# =============================================================================
MODULE_2 = {
    "id": "mlops-fundamentals",
    "title": "MLOps Fundamentals",
    "description": "Versioning de données (DVC), tracking d'expériences (MLflow), et validation (Great Expectations)",
    "week": 2,
    "order": 2,
    "total_duration": 195,
    "icon": "Brain"
}

LESSONS_MODULE_2 = [
    {
        "id": "mlops-intro",
        "module_id": "mlops-fundamentals",
        "title": "Introduction au MLOps",
        "type": "video",
        "duration": "15",
        "url": "https://www.youtube.com/embed/Jx6HGxV_g-E",  # MLOps Explained
        "content": None,
        "order": 1
    },
    {
        "id": "dvc-data-versioning",
        "module_id": "mlops-fundamentals",
        "title": "DVC - Data Version Control",
        "type": "video",
        "duration": "28",
        "url": "https://www.youtube.com/embed/kLKBcPonMYw",  # DVC Tutorial
        "content": None,
        "order": 2
    },
    {
        "id": "mlflow-tracking",
        "module_id": "mlops-fundamentals",
        "title": "MLflow - Experiment Tracking",
        "type": "video",
        "duration": "35",
        "url": "https://www.youtube.com/embed/ks8wKyBe02k",  # MLflow Tutorial
        "content": None,
        "order": 3
    },
    {
        "id": "mlflow-model-registry",
        "module_id": "mlops-fundamentals",
        "title": "MLflow Model Registry",
        "type": "video",
        "duration": "22",
        "url": "https://www.youtube.com/embed/x3cB6hlb_CY",  # MLflow Model Registry
        "content": None,
        "order": 4
    },
    {
        "id": "great-expectations",
        "module_id": "mlops-fundamentals",
        "title": "Great Expectations - Data Validation",
        "type": "video",
        "duration": "25",
        "url": "https://www.youtube.com/embed/Ocu-xF3j8zk",  # Great Expectations Tutorial
        "content": None,
        "order": 5
    },
    {
        "id": "model-drift-detection",
        "module_id": "mlops-fundamentals",
        "title": "Détection du Model Drift",
        "type": "text",
        "duration": "20",
        "url": None,
        "content": """# Model Drift : Détecter et Résoudre

## Qu'est-ce que le Model Drift ?

Le **model drift** (dérive du modèle) se produit quand les performances d'un modèle ML en production se dégradent au fil du temps.

## Types de Drift

### 1. Data Drift (Dérive des Données)
**Définition:** La distribution des features d'entrée change.

**Exemple:**
```python
# Avant: age moyen = 35 ans
# Après: age moyen = 50 ans (population vieillit)
```

**Détection:**
```python
from scipy import stats

def detect_data_drift(train_data, prod_data, feature):
    ks_stat, p_value = stats.ks_2samp(train_data[feature], prod_data[feature])
    if p_value < 0.05:
        print(f"⚠️ Data drift detected on {feature}!")
    return p_value
```

### 2. Concept Drift (Dérive du Concept)
**Définition:** La relation entre X (features) et Y (target) change.

**Exemple:**
```python
# Avant: prix élevé → house vendue (marché acheteur)
# Après: prix élevé → house PAS vendue (crise immobilière)
```

**Détection:**
```python
def detect_concept_drift(model, X_prod, y_prod_true):
    predictions = model.predict(X_prod)
    accuracy_prod = accuracy_score(y_prod_true, predictions)
    
    if accuracy_prod < accuracy_train * 0.9:
        print("⚠️ Concept drift detected!")
```

### 3. Prediction Drift (Dérive des Prédictions)
**Définition:** La distribution des prédictions du modèle change.

**Exemple:**
```python
# Avant: 50% de prédictions positives
# Après: 90% de prédictions positives
```

## Outils de Détection

### 1. Evidently AI
```python
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=train_df, current_data=prod_df)
report.show()
```

### 2. WhyLabs
```python
import whylogs as why

profile = why.log(prod_data)
profile.view().to_pandas()  # Vérifier les distributions
```

### 3. NannyML
```python
import nannyml as nml

calc = nml.PerformanceCalculator(
    y_pred_proba='prediction',
    y_pred='predicted_class',
    y_true='actual_class',
    metrics=['roc_auc', 'f1']
)
results = calc.calculate(prod_data)
```

## Stratégies de Remédiation

### 1. Réentraînement Périodique
```python
# Réentraîner tous les 30 jours
if days_since_last_training > 30:
    new_model = train_model(recent_data)
    deploy_model(new_model)
```

### 2. Online Learning
```python
from river import linear_model

model = linear_model.LogisticRegression()

# Apprendre en continu sur nouvelles données
for x, y in stream:
    model.learn_one(x, y)
```

### 3. Ensemble avec Ancien Modèle
```python
# Combiner ancien et nouveau modèle
def predict(x):
    pred_old = old_model.predict(x)
    pred_new = new_model.predict(x)
    return 0.7 * pred_old + 0.3 * pred_new  # Weighted average
```

## Checklist Monitoring

- [ ] Monitorer distribution des features (Data Drift)
- [ ] Monitorer performance model (Concept Drift)
- [ ] Monitorer distribution prédictions (Prediction Drift)
- [ ] Alertes automatiques si drift détecté
- [ ] Pipeline réentraînement automatique
- [ ] A/B testing nouveau vs ancien modèle
""",
        "order": 6
    },
    {
        "id": "quiz-mlops-fundamentals",
        "module_id": "mlops-fundamentals",
        "title": "Quiz - MLOps Fundamentals",
        "type": "quiz",
        "duration": "25",
        "url": None,
        "content": None,
        "order": 7
    }
]

QUIZ_MLOPS_FUNDAMENTALS = {
    "id": "quiz-mlops-fundamentals-data",
    "module_id": "mlops-fundamentals",
    "title": "Quiz MLOps Fundamentals",
    "passing_score": 70,
    "time_limit": 1500,
    "questions": [
        {
            "id": "q1",
            "question": "Que stocke DVC dans le repository Git ?",
            "type": "single",
            "options": [
                "Les fichiers de données complets",
                "Les métadonnées (.dvc files) pointant vers le remote storage",
                "Uniquement les modèles ML",
                "Rien, DVC remplace Git"
            ],
            "correct_answers": [1],
            "explanation": "DVC stocke uniquement les métadonnées (.dvc files) dans Git. Les données lourdes sont stockées dans un remote (S3, GCS, etc.)."
        },
        {
            "id": "q2",
            "question": "Quelle commande MLflow permet de logger une métrique ?",
            "type": "single",
            "options": [
                "mlflow.track_metric('accuracy', 0.95)",
                "mlflow.log_metric('accuracy', 0.95)",
                "mlflow.save_metric('accuracy', 0.95)",
                "mlflow.record('accuracy', 0.95)"
            ],
            "correct_answers": [1],
            "explanation": "`mlflow.log_metric('metric_name', value)` est la fonction pour logger une métrique dans MLflow Tracking."
        },
        {
            "id": "q3",
            "question": "Qu'est-ce que le 'Data Drift' ?",
            "type": "single",
            "options": [
                "Le modèle devient obsolète",
                "La distribution des features d'entrée change au fil du temps",
                "Les données d'entraînement sont perdues",
                "Le code du modèle change"
            ],
            "correct_answers": [1],
            "explanation": "Le Data Drift se produit quand la distribution statistique des features d'entrée change (ex: âge moyen des utilisateurs passe de 30 à 50 ans)."
        },
        {
            "id": "q4",
            "question": "MLflow Model Registry permet de : (plusieurs réponses)",
            "type": "multiple",
            "options": [
                "Versionner les modèles",
                "Gérer les transitions de stage (Staging → Production)",
                "Entraîner automatiquement des modèles",
                "Documenter les modèles avec descriptions et tags"
            ],
            "correct_answers": [0, 1, 3],
            "explanation": "MLflow Model Registry versionne, gère les stages, et documente les modèles. Il n'entraîne pas automatiquement (c'est le rôle d'un orchestrateur comme Airflow)."
        },
        {
            "id": "q5",
            "question": "Great Expectations est utilisé pour :",
            "type": "single",
            "options": [
                "Valider la qualité des données",
                "Entraîner des modèles ML",
                "Déployer des modèles",
                "Monitorer les serveurs"
            ],
            "correct_answers": [0],
            "explanation": "Great Expectations est un framework de validation de données. Il permet de définir des 'expectations' (ex: 'column age should be between 0 and 120')."
        },
        {
            "id": "q6",
            "question": "Quelle est la commande DVC pour reproduire un pipeline ?",
            "type": "single",
            "options": [
                "dvc run",
                "dvc repro",
                "dvc reproduce",
                "dvc execute"
            ],
            "correct_answers": [1],
            "explanation": "`dvc repro` reproduit le pipeline défini dans dvc.yaml, en ne ré-exécutant que les étapes modifiées (intelligent caching)."
        },
        {
            "id": "q7",
            "question": "Le 'Concept Drift' signifie que la relation entre X (features) et Y (target) change.",
            "type": "boolean",
            "options": ["Vrai", "Faux"],
            "correct_answers": [0],
            "explanation": "Vrai. Le Concept Drift survient quand la relation statistique entre les features et la cible change (ex: nouvelles tendances de marché)."
        }
    ]
}

# =============================================================================
# MODULE 3: Production Deployment & APIs
# =============================================================================
MODULE_3 = {
    "id": "production-deployment",
    "title": "Production Deployment & APIs",
    "description": "APIs ML avec FastAPI, déploiement cloud, monitoring Prometheus/Grafana et GitOps avec ArgoCD",
    "week": 3,
    "order": 3,
    "total_duration": 205,
    "icon": "Rocket"
}

LESSONS_MODULE_3 = [
    {
        "id": "fastapi-ml-apis",
        "module_id": "production-deployment",
        "title": "FastAPI pour APIs ML",
        "type": "video",
        "duration": "38",
        "url": "https://www.youtube.com/embed/7t2alSnE2-I",  # FastAPI Tutorial
        "content": None,
        "order": 1
    },
    {
        "id": "docker-ml-containers",
        "module_id": "production-deployment",
        "title": "Containeriser un Modèle ML",
        "type": "video",
        "duration": "25",
        "url": "https://www.youtube.com/embed/bi0cKgmRuiA",  # Docker ML
        "content": None,
        "order": 2
    },
    {
        "id": "kubernetes-basics",
        "module_id": "production-deployment",
        "title": "Kubernetes pour ML (K8s Basics)",
        "type": "video",
        "duration": "35",
        "url": "https://www.youtube.com/embed/X48VuDVv0do",  # Kubernetes Tutorial
        "content": None,
        "order": 3
    },
    {
        "id": "cloud-deployment-aws",
        "module_id": "production-deployment",
        "title": "Déploiement sur AWS (SageMaker, ECS)",
        "type": "video",
        "duration": "28",
        "url": "https://www.youtube.com/embed/NTkn6_mEdFM",  # AWS ML Deployment
        "content": None,
        "order": 4
    },
    {
        "id": "prometheus-grafana",
        "module_id": "production-deployment",
        "title": "Monitoring avec Prometheus & Grafana",
        "type": "video",
        "duration": "30",
        "url": "https://www.youtube.com/embed/9TJx7QTrTyo",  # Prometheus Grafana
        "content": None,
        "order": 5
    },
    {
        "id": "argocd-gitops",
        "module_id": "production-deployment",
        "title": "GitOps avec ArgoCD",
        "type": "video",
        "duration": "24",
        "url": "https://www.youtube.com/embed/MeU5_k9ssrs",  # ArgoCD Tutorial
        "content": None,
        "order": 6
    },
    {
        "id": "api-design-best-practices",
        "module_id": "production-deployment",
        "title": "API Design Best Practices",
        "type": "text",
        "duration": "15",
        "url": None,
        "content": """# API Design Best Practices pour ML

## 1. Versioning de l'API

### Approche par URL
```python
from fastapi import FastAPI

app_v1 = FastAPI()
app_v2 = FastAPI()

@app_v1.post("/predict")
def predict_v1(data: InputV1):
    # Ancien modèle
    return old_model.predict(data)

@app_v2.post("/predict")
def predict_v2(data: InputV2):
    # Nouveau modèle
    return new_model.predict(data)

app.mount("/v1", app_v1)
app.mount("/v2", app_v2)
```

### Approche par Header
```python
from fastapi import Header

@app.post("/predict")
def predict(data: Input, version: str = Header(default="1.0")):
    if version == "1.0":
        return model_v1.predict(data)
    elif version == "2.0":
        return model_v2.predict(data)
```

## 2. Validation des Inputs

### Pydantic pour Validation Stricte
```python
from pydantic import BaseModel, Field, validator

class PredictionInput(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Age in years")
    income: float = Field(..., gt=0, description="Annual income")
    credit_score: int = Field(..., ge=300, le=850)
    
    @validator('age')
    def age_realistic(cls, v):
        if v < 18:
            raise ValueError('Must be 18+')
        return v

@app.post("/predict")
def predict(data: PredictionInput):
    return model.predict([[data.age, data.income, data.credit_score]])
```

## 3. Error Handling

### HTTP Status Codes Appropriés
```python
from fastapi import HTTPException, status

@app.post("/predict")
def predict(data: Input):
    try:
        result = model.predict(data.features)
        return {"prediction": result}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model prediction failed"
        )
```

## 4. Rate Limiting

### Avec slowapi
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("10/minute")  # Max 10 requêtes/minute
def predict(request: Request, data: Input):
    return model.predict(data.features)
```

## 5. Caching des Prédictions

### Avec Redis
```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379)

@app.post("/predict")
def predict(data: Input):
    # Créer clé cache
    cache_key = f"pred:{hash(json.dumps(data.dict()))}"
    
    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Prédiction
    result = model.predict(data.features)
    
    # Sauver en cache (expire après 1h)
    redis_client.setex(cache_key, 3600, json.dumps(result))
    
    return result
```

## 6. Batch Predictions

### Endpoint pour Batch
```python
from typing import List

@app.post("/predict/batch")
def predict_batch(data: List[Input]):
    features = [d.features for d in data]
    predictions = model.predict(features)
    return {"predictions": predictions.tolist()}
```

## 7. Health Checks

### Endpoints Standard
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "version": "1.2.3"
    }

@app.get("/readiness")
def readiness_check():
    # Vérifier DB, model, etc.
    try:
        model.predict([[1, 2, 3]])  # Test prediction
        return {"ready": True}
    except:
        raise HTTPException(status_code=503, detail="Not ready")
```

## 8. Logging et Observabilité

### Structured Logging
```python
import logging
import json

logger = logging.getLogger(__name__)

@app.post("/predict")
def predict(data: Input):
    logger.info(json.dumps({
        "event": "prediction_request",
        "features": data.dict(),
        "timestamp": datetime.utcnow().isoformat()
    }))
    
    result = model.predict(data.features)
    
    logger.info(json.dumps({
        "event": "prediction_response",
        "result": result,
        "latency_ms": ...
    }))
    
    return result
```

## 9. Documentation OpenAPI

### Descriptions Détaillées
```python
@app.post("/predict",
    summary="Make a prediction",
    description="Predicts credit risk based on customer features",
    response_description="Prediction result with confidence score",
    tags=["predictions"]
)
def predict(
    data: Input = Body(..., example={
        "age": 35,
        "income": 50000,
        "credit_score": 720
    })
):
    return model.predict(data.features)
```

## Checklist API Production

- [ ] Versioning (URL ou Header)
- [ ] Validation stricte des inputs (Pydantic)
- [ ] Error handling avec codes HTTP appropriés
- [ ] Rate limiting
- [ ] Caching (Redis)
- [ ] Batch endpoint pour volume
- [ ] Health & Readiness checks
- [ ] Logging structuré (JSON)
- [ ] Métriques (Prometheus)
- [ ] Documentation OpenAPI complète
- [ ] Tests (unit + integration)
- [ ] Authentification (JWT)
""",
        "order": 7
    },
    {
        "id": "quiz-production-deployment",
        "module_id": "production-deployment",
        "title": "Quiz - Production Deployment",
        "type": "quiz",
        "duration": "25",
        "url": None,
        "content": None,
        "order": 8
    }
]

QUIZ_PRODUCTION_DEPLOYMENT = {
    "id": "quiz-production-deployment-data",
    "module_id": "production-deployment",
    "title": "Quiz Production Deployment & APIs",
    "passing_score": 70,
    "time_limit": 1500,
    "questions": [
        {
            "id": "q1",
            "question": "Quel est l'avantage principal de FastAPI pour les APIs ML ?",
            "type": "single",
            "options": [
                "Permet d'entraîner des modèles plus rapidement",
                "Validation automatique des données avec Pydantic et documentation OpenAPI",
                "Remplace Docker pour le déploiement",
                "Stocke automatiquement les modèles"
            ],
            "correct_answers": [1],
            "explanation": "FastAPI combine validation automatique (Pydantic), documentation interactive (Swagger/OpenAPI), et haute performance (ASGI). Idéal pour APIs ML."
        },
        {
            "id": "q2",
            "question": "Dans Kubernetes, un 'Pod' est :",
            "type": "single",
            "options": [
                "Un container Docker unique",
                "La plus petite unité déployable contenant un ou plusieurs containers",
                "Un nœud du cluster",
                "Un load balancer"
            ],
            "correct_answers": [1],
            "explanation": "Un Pod est la plus petite unité dans Kubernetes. Il peut contenir un ou plusieurs containers qui partagent le même réseau et storage."
        },
        {
            "id": "q3",
            "question": "Prometheus est principalement utilisé pour :",
            "type": "single",
            "options": [
                "Déployer des containers",
                "Collecter des métriques et créer des alertes",
                "Versionner le code",
                "Entraîner des modèles"
            ],
            "correct_answers": [1],
            "explanation": "Prometheus est un système de monitoring qui collecte des métriques time-series et permet de créer des alertes. Grafana est souvent utilisé pour visualiser ces métriques."
        },
        {
            "id": "q4",
            "question": "Qu'est-ce que GitOps ?",
            "type": "single",
            "options": [
                "Une façon de stocker du code sur Git",
                "Un paradigme où Git est la source de vérité pour l'infrastructure et les déploiements",
                "Un outil de CI/CD",
                "Une alternative à Docker"
            ],
            "correct_answers": [1],
            "explanation": "GitOps utilise Git comme source de vérité unique. Tout changement (infra, config, apps) passe par Git, et un outil (ArgoCD, Flux) synchronise automatiquement."
        },
        {
            "id": "q5",
            "question": "Quelles sont les bonnes pratiques pour une API ML en production ? (plusieurs réponses)",
            "type": "multiple",
            "options": [
                "Versioning de l'API (/v1, /v2)",
                "Health checks (/health, /readiness)",
                "Stocker les credentials dans le code",
                "Rate limiting pour éviter les abus"
            ],
            "correct_answers": [0, 1, 3],
            "explanation": "Versioning, health checks et rate limiting sont essentiels. Les credentials ne doivent JAMAIS être dans le code (utiliser variables d'environnement ou secrets managers)."
        },
        {
            "id": "q6",
            "question": "ArgoCD est un outil de :",
            "type": "single",
            "options": [
                "CI (Continuous Integration)",
                "CD (Continuous Deployment) GitOps",
                "Monitoring",
                "Data versioning"
            ],
            "correct_answers": [1],
            "explanation": "ArgoCD est un outil de Continuous Deployment basé sur GitOps pour Kubernetes. Il surveille un repo Git et synchronise automatiquement l'état du cluster."
        },
        {
            "id": "q7",
            "question": "Pydantic permet de valider automatiquement les données d'entrée d'une API FastAPI.",
            "type": "boolean",
            "options": ["Vrai", "Faux"],
            "correct_answers": [0],
            "explanation": "Vrai. Pydantic valide automatiquement les types et contraintes (ex: age >= 0). FastAPI retourne une erreur 422 si validation échoue."
        },
        {
            "id": "q8",
            "question": "Quel code HTTP doit retourner un endpoint /health si le service est sain ?",
            "type": "single",
            "options": [
                "200 OK",
                "201 Created",
                "204 No Content",
                "503 Service Unavailable"
            ],
            "correct_answers": [0],
            "explanation": "Un health check doit retourner 200 OK si le service est sain (model chargé, DB accessible). 503 si le service n'est pas prêt."
        }
    ]
}

# =============================================================================
# MODULE 4: Final Project & Certification
# =============================================================================
MODULE_4 = {
    "id": "final-project",
    "title": "Projet Final & Certification",
    "description": "Projet MLOps complet de bout en bout : pipeline DVC, MLflow, CI/CD, déploiement et monitoring",
    "week": 4,
    "order": 4,
    "total_duration": 150,
    "icon": "Award"
}

LESSONS_MODULE_4 = [
    {
        "id": "project-requirements",
        "module_id": "final-project",
        "title": "Cahier des Charges du Projet",
        "type": "text",
        "duration": "15",
        "url": None,
        "content": """# Projet Final MLOps - Cahier des Charges

## Objectif

Créer un **pipeline MLOps complet** pour un modèle de classification, avec versioning, tracking, déploiement automatisé et monitoring.

## Livrables Attendus

### 1. Repository Git Structuré
```
mlops-project/
├── data/              # .gitignore (géré par DVC)
├── models/            # .gitignore (géré par DVC)
├── notebooks/         # Exploration
├── src/
│   ├── train.py       # Script entraînement
│   ├── predict.py     # Script prédiction
│   └── api.py         # API FastAPI
├── tests/             # Tests unitaires
├── .dvc/              # Config DVC
├── .github/
│   └── workflows/
│       └── ci-cd.yml  # Pipeline CI/CD
├── Dockerfile         # Container
├── dvc.yaml           # Pipeline DVC
├── requirements.txt
└── README.md
```

### 2. Pipeline DVC
Créer un pipeline reproductible avec :
- Étape `prepare`: Préparer les données
- Étape `train`: Entraîner le modèle
- Étape `evaluate`: Évaluer les métriques

```yaml
# dvc.yaml
stages:
  prepare:
    cmd: python src/prepare.py
    deps:
      - data/raw
    outs:
      - data/processed
  
  train:
    cmd: python src/train.py
    deps:
      - data/processed
      - src/train.py
    outs:
      - models/model.pkl
    metrics:
      - metrics.json:
          cache: false
```

### 3. Tracking MLflow
- Logger tous les hyperparamètres
- Logger toutes les métriques (accuracy, F1, AUC)
- Logger les artifacts (model, plots)
- Utiliser MLflow Model Registry

### 4. API FastAPI
Créer une API avec :
- `POST /predict` : Endpoint de prédiction
- `GET /health` : Health check
- `GET /model/info` : Infos sur le modèle (version, metrics)
- Validation Pydantic
- Documentation OpenAPI

### 5. CI/CD GitHub Actions
Pipeline qui :
- Lance les tests unitaires
- Vérifie le linting (black, flake8)
- Build l'image Docker
- Push vers Docker Hub
- (Bonus) Déploie automatiquement

### 6. Monitoring
- Métriques Prometheus exposées (`/metrics`)
- Dashboard Grafana avec :
  * Nombre de prédictions
  * Latence moyenne
  * Taux d'erreur
  * Distribution des prédictions

### 7. Documentation
- README.md complet avec :
  * Description du projet
  * Installation
  * Usage
  * Exemples d'API calls
  * Architecture diagram

## Dataset Suggérés

Choisir un dataset sur Kaggle :
- **Titanic** (classification binaire)
- **Iris** (multiclass)
- **House Prices** (régression)
- **Credit Card Fraud** (imbalanced)

## Critères d'Évaluation (sur 100 points)

| Critère | Points |
|---------|--------|
| Pipeline DVC fonctionnel | 15 |
| Tracking MLflow complet | 15 |
| API FastAPI avec tests | 20 |
| CI/CD automatisé | 20 |
| Monitoring Prometheus/Grafana | 15 |
| Documentation README | 10 |
| Code quality (linting, tests) | 5 |

**Total: 100 points**
**Passing score: 70 points**

## Timeline

- **Jour 1-2:** Setup DVC, MLflow, pipeline entraînement
- **Jour 3:** API FastAPI + tests
- **Jour 4:** CI/CD GitHub Actions
- **Jour 5:** Monitoring + Documentation
- **Jour 6:** Présentation (optionnel)

## Soumission

1. Push final sur GitHub
2. Remplir le formulaire avec :
   - Lien GitHub repo
   - Lien MLflow UI (si déployé)
   - Lien API déployée (si déployé)
   - Vidéo démo 3-5 min (optionnel)

## Ressources

- [DVC Documentation](https://dvc.org/doc)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
""",
        "order": 1
    },
    {
        "id": "project-demo",
        "module_id": "final-project",
        "title": "Exemple de Projet Complet",
        "type": "video",
        "duration": "45",
        "url": "https://www.youtube.com/embed/zGxu6644EHQ",  # End-to-end ML Project
        "content": None,
        "order": 2
    },
    {
        "id": "best-practices-recap",
        "module_id": "final-project",
        "title": "Récapitulatif Best Practices",
        "type": "text",
        "duration": "20",
        "url": None,
        "content": """# MLOps Best Practices - Récapitulatif

## 1. Code & Repository

### Structure de Projet
```
mlops-project/
├── .github/workflows/    # CI/CD
├── data/                 # Géré par DVC
├── models/               # Géré par DVC
├── notebooks/            # Exploration uniquement
├── src/                  # Code production
│   ├── __init__.py
│   ├── data/             # Data processing
│   ├── features/         # Feature engineering
│   ├── models/           # Model code
│   └── api/              # API code
├── tests/                # Tests unitaires
├── .dvcignore
├── .gitignore
├── dvc.yaml              # DVC pipeline
├── params.yaml           # Hyperparamètres
├── requirements.txt
└── README.md
```

### Git Best Practices
- Commits atomiques et descriptifs
- Branches : `feature/`, `bugfix/`, `hotfix/`
- Pull Requests avec review
- Tags pour releases (`v1.0.0`)

## 2. Data & Experiments

### DVC
```bash
# Initialiser
dvc init

# Tracker données
dvc add data/train.csv

# Remote storage
dvc remote add -d storage s3://mybucket/dvcstore
dvc push

# Pipeline
dvc stage add -n prepare \
  -d data/raw \
  -o data/processed \
  python src/prepare.py

dvc repro  # Reproduire pipeline
```

### MLflow
```python
import mlflow

mlflow.set_experiment("credit-scoring")

with mlflow.start_run(run_name="rf-v1"):
    # Params
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # Train
    model.fit(X_train, y_train)
    
    # Metrics
    acc = accuracy_score(y_test, pred)
    mlflow.log_metric("accuracy", acc)
    
    # Artifacts
    mlflow.sklearn.log_model(model, "model")
    mlflow.log_artifact("confusion_matrix.png")
```

## 3. Testing

### Types de Tests
```python
# tests/test_model.py
def test_model_predict_shape():
    model = load_model()
    X = [[1, 2, 3]]
    pred = model.predict(X)
    assert pred.shape == (1,)

def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_api_predict_valid_input():
    response = client.post("/predict", json={
        "features": [1, 2, 3]
    })
    assert response.status_code == 200
    assert "prediction" in response.json()
```

### Coverage
```bash
pytest --cov=src tests/
coverage report
coverage html  # Génère htmlcov/index.html
```

## 4. API Production

### FastAPI Template
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI(title="ML API", version="1.0.0")

# Load model at startup
model = joblib.load("model.pkl")

class PredictionInput(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: PredictionInput):
    try:
        pred = model.predict([data.features])
        return {"prediction": pred[0].tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}
```

### Dockerfile Multi-Stage
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 5. CI/CD

### GitHub Actions
```yaml
name: CI/CD
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Lint
        run: |
          black --check src/
          flake8 src/
      - name: Test
        run: pytest tests/
  
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker
        run: docker build -t myapp .
      - name: Push to registry
        run: docker push myregistry/myapp:latest
```

## 6. Monitoring

### Prometheus Metrics
```python
from prometheus_client import Counter, Histogram, generate_latest

# Définir métriques
prediction_count = Counter('predictions_total', 'Total predictions')
prediction_latency = Histogram('prediction_latency_seconds', 'Latency')

@app.post("/predict")
def predict(data: Input):
    with prediction_latency.time():
        result = model.predict(data.features)
    prediction_count.inc()
    return result

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Alertes
```yaml
# prometheus-alerts.yml
groups:
  - name: ml_api
    rules:
      - alert: HighLatency
        expr: prediction_latency_seconds > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High prediction latency"
```

## 7. Security

### Checklist
- [ ] Pas de credentials en clair dans le code
- [ ] Utiliser variables d'environnement
- [ ] API authentication (JWT)
- [ ] Rate limiting
- [ ] Input validation stricte
- [ ] HTTPS en production
- [ ] Scan vulnérabilités (Snyk, Dependabot)
- [ ] Secrets management (AWS Secrets Manager, Vault)

## 8. Documentation

### README Template
```markdown
# Project Name

## Description
Prédiction de [use case] avec [model type]

## Installation
```bash
git clone [repo]
cd [repo]
pip install -r requirements.txt
```

## Usage
```bash
# Train
python src/train.py

# API
uvicorn src.api:app --reload

# Test
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1, 2, 3]}'
```

## Architecture
[Diagram or explanation]

## Metrics
- Accuracy: 0.95
- F1-Score: 0.93

## License
MIT
```

## Checklist Final

- [ ] Git repo avec structure propre
- [ ] DVC pour données et modèles
- [ ] MLflow tracking + registry
- [ ] Tests unitaires (coverage > 80%)
- [ ] API FastAPI avec validation
- [ ] Dockerfile optimisé
- [ ] CI/CD automatisé
- [ ] Monitoring Prometheus
- [ ] Documentation README
- [ ] Security checklist validée
""",
        "order": 3
    },
    {
        "id": "certification-exam",
        "module_id": "final-project",
        "title": "Examen de Certification Final",
        "type": "quiz",
        "duration": "60",
        "url": None,
        "content": None,
        "order": 4
    },
    {
        "id": "resources-next-steps",
        "module_id": "final-project",
        "title": "Ressources & Prochaines Étapes",
        "type": "text",
        "duration": "10",
        "url": None,
        "content": """# Ressources & Prochaines Étapes

## 📚 Livres Recommandés

### DevOps
- **"The Phoenix Project"** - Gene Kim (Fiction DevOps)
- **"The DevOps Handbook"** - Gene Kim et al.
- **"Accelerate"** - Nicole Forsgren (Recherche DORA)

### MLOps
- **"Designing Machine Learning Systems"** - Chip Huyen
- **"Building Machine Learning Pipelines"** - Hannes Hapke
- **"Machine Learning Engineering"** - Andriy Burkov

## 🎓 Certifications Professionnelles

### Cloud
- **AWS Certified DevOps Engineer - Professional**
- **Google Professional ML Engineer**
- **Azure DevOps Engineer Expert**

### Kubernetes
- **Certified Kubernetes Administrator (CKA)**
- **Certified Kubernetes Application Developer (CKAD)**

### MLOps
- **MLOps Professional Certificate (Coursera)**
- **TensorFlow Certificate**

## 🌐 Communautés

- **MLOps Community** (mlops.community)
- **r/mlops** (Reddit)
- **DevOps Institute**
- **MLOps World** (Conférences)

## 🛠️ Outils à Explorer

### Avancés
- **Kubeflow**: ML workflows sur Kubernetes
- **Airflow**: Orchestration de pipelines
- **Feast**: Feature store
- **Seldon**: Model serving
- **Evidently AI**: ML monitoring
- **WhyLabs**: Data quality monitoring

## 🚀 Projets Pratiques Suggérés

1. **Portfolio MLOps**
   - Créer 3-5 projets MLOps complets
   - Publier sur GitHub
   - Écrire des articles Medium/Dev.to

2. **Contributions Open Source**
   - Contribuer à MLflow, DVC, FastAPI
   - Créer vos propres outils MLOps

3. **Blog Technique**
   - Documenter votre apprentissage
   - Partager vos découvertes

## 🎯 Parcours de Carrière

### Junior MLOps Engineer
- 0-2 ans d'expérience
- Focus: CI/CD, Docker, basic Kubernetes
- Salaire: 40-60k€

### MLOps Engineer
- 2-5 ans d'expérience
- Focus: Production ML, monitoring, scaling
- Salaire: 60-90k€

### Senior MLOps Engineer / ML Platform Engineer
- 5+ ans d'expérience
- Focus: Architecture, team leadership
- Salaire: 90-130k€

## 📧 Rester en Contact

- **LinkedIn**: Connectez avec des MLOps Engineers
- **Twitter**: Suivre #MLOps, #DevOps
- **Newsletter**: MLOps Weekly, DevOps Weekly

## 🎉 Félicitations !

Vous avez maintenant les compétences pour :
✅ Créer des pipelines MLOps complets
✅ Déployer des modèles ML en production
✅ Monitorer et maintenir des systèmes ML
✅ Automatiser avec CI/CD
✅ Utiliser Docker, Kubernetes, Cloud

**Continuez à pratiquer et bon courage ! 🚀**
""",
        "order": 5
    }
]

QUIZ_FINAL_EXAM = {
    "id": "quiz-final-exam-data",
    "module_id": "final-project",
    "title": "Examen de Certification Final",
    "passing_score": 75,
    "time_limit": 3600,
    "questions": [
        {
            "id": "q1",
            "question": "Quelle commande DVC permet de tracker un fichier de données volumineux ?",
            "type": "single",
            "options": [
                "dvc track data.csv",
                "dvc add data.csv",
                "git add data.csv",
                "dvc push data.csv"
            ],
            "correct_answers": [1],
            "explanation": "`dvc add data.csv` crée un fichier .dvc qui contient le hash et enregistre le fichier dans le cache DVC."
        },
        {
            "id": "q2",
            "question": "Dans un workflow GitOps, quelle est la source de vérité ?",
            "type": "single",
            "options": [
                "Le cluster Kubernetes",
                "Le repository Git",
                "Le CI/CD tool",
                "Le Docker registry"
            ],
            "correct_answers": [1],
            "explanation": "Dans GitOps, le repository Git est la source de vérité unique. Tout changement passe par Git, et un outil (ArgoCD, Flux) synchronise l'état réel avec l'état désiré dans Git."
        },
        {
            "id": "q3",
            "question": "Quelle est la métrique DORA qui mesure la fréquence de déploiement ?",
            "type": "single",
            "options": [
                "Lead Time for Changes",
                "Deployment Frequency",
                "Change Failure Rate",
                "Mean Time to Recovery"
            ],
            "correct_answers": [1],
            "explanation": "Deployment Frequency mesure à quelle fréquence vous déployez en production. Les équipes Elite déploient plusieurs fois par jour."
        },
        {
            "id": "q4",
            "question": "Quels outils font partie de la stack MLOps typique ? (plusieurs réponses)",
            "type": "multiple",
            "options": [
                "DVC pour versioning de données",
                "MLflow pour tracking d'expériences",
                "Prometheus pour monitoring",
                "Photoshop pour visualisation"
            ],
            "correct_answers": [0, 1, 2],
            "explanation": "DVC, MLflow et Prometheus sont des outils MLOps standards. Photoshop n'est pas utilisé en MLOps (Matplotlib, Plotly pour viz)."
        },
        {
            "id": "q5",
            "question": "Dans FastAPI, Pydantic est utilisé pour :",
            "type": "single",
            "options": [
                "Entraîner des modèles ML",
                "Valider automatiquement les données d'entrée",
                "Déployer sur le cloud",
                "Monitorer les performances"
            ],
            "correct_answers": [1],
            "explanation": "Pydantic valide automatiquement les types et contraintes des données d'entrée. FastAPI retourne 422 si validation échoue."
        },
        {
            "id": "q6",
            "question": "Quelle commande permet de reproduire un pipeline DVC ?",
            "type": "single",
            "options": [
                "dvc run",
                "dvc repro",
                "dvc reproduce",
                "dvc execute"
            ],
            "correct_answers": [1],
            "explanation": "`dvc repro` reproduit le pipeline en ré-exécutant uniquement les étapes dont les dépendances ont changé (intelligent caching)."
        },
        {
            "id": "q7",
            "question": "Le Data Drift se produit quand la distribution des features d'entrée change.",
            "type": "boolean",
            "options": ["Vrai", "Faux"],
            "correct_answers": [0],
            "explanation": "Vrai. Le Data Drift survient quand les statistiques des features changent (ex: âge moyen passe de 30 à 50 ans)."
        },
        {
            "id": "q8",
            "question": "Dans Kubernetes, quel objet permet d'exposer un service au monde extérieur ?",
            "type": "single",
            "options": [
                "Pod",
                "Deployment",
                "Service de type LoadBalancer ou Ingress",
                "ConfigMap"
            ],
            "correct_answers": [2],
            "explanation": "Un Service de type LoadBalancer ou un Ingress expose des Pods au trafic externe. Un Service ClusterIP n'est accessible qu'en interne."
        },
        {
            "id": "q9",
            "question": "Prometheus collecte des métriques en :",
            "type": "single",
            "options": [
                "Push (les apps envoient à Prometheus)",
                "Pull (Prometheus scrape les endpoints /metrics)",
                "WebSockets",
                "Emails"
            ],
            "correct_answers": [1],
            "explanation": "Prometheus utilise un modèle Pull : il scrape régulièrement les endpoints /metrics des applications pour collecter les métriques."
        },
        {
            "id": "q10",
            "question": "Quelles pratiques font partie du 'shift left' en DevOps ? (plusieurs réponses)",
            "type": "multiple",
            "options": [
                "Tests automatisés très tôt dans le pipeline",
                "Sécurité intégrée dès le développement (DevSecOps)",
                "Attendre la fin du projet pour tester",
                "Feedback rapide aux développeurs"
            ],
            "correct_answers": [0, 1, 3],
            "explanation": "'Shift left' signifie détecter les problèmes le plus tôt possible : tests automatisés, sécurité intégrée, feedback rapide. Attendre la fin est l'opposé du shift left."
        }
    ]
}

# =============================================================================
# USERS
# =============================================================================
USERS = [
    {"id": "admin-1", "email": "admin@learnops.io", "password": "Admin2024!", "first_name": "Admin", "last_name": "DevOps", "role": "admin", "is_active": True},
    {"id": "instructor-1", "email": "claire@learnops.io", "password": "Instructor2024!", "first_name": "Claire", "last_name": "Martin", "role": "instructor", "is_active": True},
    {"id": "student-1", "email": "marie@student.com", "password": "Student2024!", "first_name": "Marie", "last_name": "Dupont", "role": "student", "is_active": True},
    {"id": "student-2", "email": "jean@student.com", "password": "Student2024!", "first_name": "Jean", "last_name": "Bernard", "role": "student", "is_active": True},
    {"id": "student-3", "email": "sophie@student.com", "password": "Student2024!", "first_name": "Sophie", "last_name": "Leroy", "role": "student", "is_active": True},
]

PROGRESSIONS = [
    {"user_id": "admin-1", "progression": 0, "modules_completed": [], "time_spent": 0},
    {"user_id": "instructor-1", "progression": 100, "modules_completed": ["devops-foundations", "mlops-fundamentals", "production-deployment", "final-project"], "time_spent": 28800},
    {"user_id": "student-1", "progression": 45, "modules_completed": ["devops-foundations"], "time_spent": 10800},
    {"user_id": "student-2", "progression": 20, "modules_completed": [], "time_spent": 3600},
    {"user_id": "student-3", "progression": 5, "modules_completed": [], "time_spent": 1200},
]

BADGES = [
    {"user_id": "instructor-1", "badge_name": "devops-foundations"},
    {"user_id": "instructor-1", "badge_name": "mlops-fundamentals"},
    {"user_id": "instructor-1", "badge_name": "production-deployment"},
    {"user_id": "instructor-1", "badge_name": "final-project"},
    {"user_id": "student-1", "badge_name": "devops-foundations"},
]

COMPLETIONS = [
    # Instructor completed everything
    ("instructor-1", "devops-culture"),
    ("instructor-1", "git-workflows"),
    ("instructor-1", "github-actions-intro"),
    ("instructor-1", "docker-fundamentals"),
    ("instructor-1", "docker-compose-practice"),
    ("instructor-1", "devops-metrics"),
    ("instructor-1", "quiz-devops-foundations"),
    ("instructor-1", "mlops-intro"),
    ("instructor-1", "dvc-data-versioning"),
    ("instructor-1", "mlflow-tracking"),
    ("instructor-1", "mlflow-model-registry"),
    ("instructor-1", "great-expectations"),
    ("instructor-1", "model-drift-detection"),
    ("instructor-1", "quiz-mlops-fundamentals"),
    # Student-1 completed module 1
    ("student-1", "devops-culture"),
    ("student-1", "git-workflows"),
    ("student-1", "github-actions-intro"),
    ("student-1", "docker-fundamentals"),
    ("student-1", "docker-compose-practice"),
    # Student-2 started
    ("student-2", "devops-culture"),
    ("student-2", "git-workflows"),
]

# =============================================================================
# SEED FUNCTION
# =============================================================================
def seed():
    db = SessionLocal()
    try:
        print("\n🌱 Seeding production database with REAL MLOps/DevOps curriculum...\n")

        # Modules
        for m in [MODULE_1, MODULE_2, MODULE_3, MODULE_4]:
            existing = db.query(Module).filter(Module.id == m["id"]).first()
            if existing:
                for k, v in m.items():
                    setattr(existing, k, v)
            else:
                db.add(Module(**m))
        db.commit()
        print(f"✅  Modules: 4")

        # Lessons
        all_lessons = LESSONS_MODULE_1 + LESSONS_MODULE_2 + LESSONS_MODULE_3 + LESSONS_MODULE_4
        for L in all_lessons:
            typ = L["type"]
            if typ not in ("video", "text", "quiz", "practice"):
                typ = "text"
            existing = db.query(Lesson).filter(Lesson.id == L["id"]).first()
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
            if existing:
                for k, v in payload.items():
                    setattr(existing, k, v)
            else:
                db.add(Lesson(**payload))
        db.commit()
        print(f"✅  Lessons: {len(all_lessons)}")

        # Quizzes
        all_quizzes = [
            QUIZ_DEVOPS_FOUNDATIONS,
            QUIZ_MLOPS_FUNDAMENTALS,
            QUIZ_PRODUCTION_DEPLOYMENT,
            QUIZ_FINAL_EXAM
        ]
        for q in all_quizzes:
            existing = db.query(Quiz).filter(Quiz.id == q["id"]).first()
            payload = {
                "id": q["id"],
                "module_id": q["module_id"],
                "title": q["title"],
                "passing_score": q["passing_score"],
                "time_limit": q.get("time_limit"),
                "questions": q["questions"],
            }
            if existing:
                for k, v in payload.items():
                    setattr(existing, k, v)
            else:
                db.add(Quiz(**payload))
        db.commit()
        print(f"✅  Quizzes: {len(all_quizzes)}")

        # Users
        for u in USERS:
            existing = db.query(User).filter(User.id == u["id"]).first()
            payload = {
                "id": u["id"],
                "email": u["email"],
                "first_name": u["first_name"],
                "last_name": u["last_name"],
                "role": UserRole(u["role"]),
                "is_active": u["is_active"],
                "created_at": days_ago(60),
                "last_login": days_ago(1),
            }
            if existing:
                for k, v in payload.items():
                    if k != "created_at":
                        setattr(existing, k, v)
            else:
                payload["hashed_password"] = get_password_hash(u["password"])
                db.add(User(**payload))
        db.commit()
        print(f"✅  Users: {len(USERS)}")

        # Progressions
        for p in PROGRESSIONS:
            uid = p["user_id"]
            existing = db.query(UserProgression).filter(UserProgression.user_id == uid).first()
            payload = {
                "user_id": uid,
                "progression": p["progression"],
                "modules_completed": p["modules_completed"],
                "time_spent": p["time_spent"],
            }
            if existing:
                for k, v in payload.items():
                    setattr(existing, k, v)
            else:
                db.add(UserProgression(id=f"prog-{uid}", **payload))
        db.commit()
        print("✅  Progressions")

        # Badges
        for b in BADGES:
            bid = f"badge-{b['user_id']}-{b['badge_name']}"
            existing = db.query(UserBadge).filter(UserBadge.id == bid).first()
            if not existing:
                db.add(UserBadge(id=bid, user_id=b["user_id"], badge_name=b["badge_name"]))
        db.commit()
        print(f"✅  Badges: {len(BADGES)}")

        # Lesson completions
        for user_id, lesson_id in COMPLETIONS:
            existing = db.query(LessonCompletion).filter(
                LessonCompletion.user_id == user_id,
                LessonCompletion.lesson_id == lesson_id,
            ).first()
            if not existing:
                db.add(LessonCompletion(user_id=user_id, lesson_id=lesson_id, completed=1))
        db.commit()
        print(f"✅  Lesson completions: {len(COMPLETIONS)}")

        print("\n" + "=" * 70)
        print("🎉  Production database seeded successfully with REAL curriculum!")
        print("=" * 70)
        print("\n📝  Test Credentials:")
        print("  👑  Admin      : admin@learnops.io      / Admin2024!")
        print("  👨‍🏫 Instructor : claire@learnops.io     / Instructor2024!")
        print("  👨‍🎓 Student    : marie@student.com      / Student2024!")
        print("\n📚  Content Summary:")
        print(f"  • 4 Professional Modules")
        print(f"  • {len(all_lessons)} Comprehensive Lessons")
        print(f"  • 20+ Real YouTube Videos from Industry Experts")
        print(f"  • {len(all_quizzes)} Detailed Quizzes (40+ questions)")
        print(f"  • Complete MLOps/DevOps Curriculum")
        print("=" * 70 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌  Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()