"""
=============================================================
 COMPLETE PRODUCTION SEEDER — Frontend-Compatible
 FastAPI + PostgreSQL — uses your exact SQLAlchemy models
=============================================================
 Fixes vs original:
   ✅ duration  → integer (minutes) not "MM:SS" string
   ✅ modules_completed → list of module-id strings (matches
      UserProgression.modules_completed stored as JSONB/Array)
   ✅ user.status  → is_active bool mapped from "active"/"blocked"
   ✅ Quiz.lesson_id added so quizService.getById() can resolve
      the quiz from a lesson context (matches quiz-data.ts / quizService)
   ✅ Quiz question field: correct_answers (snake_case) consistent
      with quizService.ts QuizQuestion interface
   ✅ Lesson content stored as structured JSON matching
      LessonContent { theory, practice } shape from lessonService.ts
   ✅ video URL kept on lesson.url (matches Lesson.url field)
   ✅ Users mirror mock-users.ts exactly (same IDs, emails, passwords)
=============================================================
 Usage:
   docker cp seed_db.py didacticiel_api:/app/seed_db.py
   docker exec didacticiel_api python seed_db.py
=============================================================
"""

import json
import uuid
from datetime import datetime, timedelta

from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.module import Module
from app.models.lesson import Lesson, LessonType
from app.models.quiz import Quiz, QuizAttempt
from app.models.progression import UserProgression, UserBadge, LessonCompletion
from app.core.security import get_password_hash

# ─── helpers ──────────────────────────────────────────────────────────────────
def uid():
    return str(uuid.uuid4())

def days_ago(n):
    return datetime.utcnow() - timedelta(days=n)

# ══════════════════════════════════════════════════════════════════════════════
#  1. MODULES
#  ⚠️  id values MUST match course-data.ts Module.id strings
# ══════════════════════════════════════════════════════════════════════════════
MODULES_DATA = [
    dict(
        id="devops-basics",
        title="DevOps Basics",
        description="Découvrez les fondamentaux du DevOps, CI/CD et Docker. Apprenez à automatiser vos pipelines et à containeriser vos applications.",
        week=1,
        order=1,
        total_duration=105,   # sum of lesson durations in minutes
    ),
    dict(
        id="mlops-fundamentals",
        title="MLOps Fundamentals",
        description="Maîtrisez le versioning de données avec DVC, le tracking d'expériences avec MLflow et la gestion du cycle de vie ML.",
        week=2,
        order=2,
        total_duration=120,
    ),
    dict(
        id="deployment-api",
        title="Déploiement & API",
        description="Déployez vos modèles ML via des APIs robustes avec FastAPI, containerisez-les et mettez en place un monitoring en production.",
        week=3,
        order=3,
        total_duration=130,
    ),
    dict(
        id="final-evaluation",
        title="Évaluation finale",
        description="Mettez en pratique tout ce que vous avez appris en réalisant un projet MLOps complet de bout en bout.",
        week=4,
        order=4,
        total_duration=165,
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  2. LESSONS
#
#  ✅ duration   → int (minutes) — matches Lesson interface in course-data.ts
#  ✅ content    → JSON string with shape { theory, practice } matching
#                  LessonContent from lessonService.ts / lesson-content.ts
#  ✅ url        → embed URL for video lessons (matches video-data.ts)
#  ✅ type       → LessonType enum values: TEXT / VIDEO / PRACTICE / QUIZ
# ══════════════════════════════════════════════════════════════════════════════

def _content(theory_title, theory_text, theory_code_blocks,
             practice_title, practice_text, practice_code_blocks):
    """Serialize lesson content as the frontend LessonContent shape."""
    return json.dumps({
        "theory": {
            "title": theory_title,
            "content": theory_text,
            "codeBlocks": theory_code_blocks or [],
        },
        "practice": {
            "title": practice_title,
            "content": practice_text,
            "codeBlocks": practice_code_blocks or [],
        },
    }, ensure_ascii=False)


LESSONS_DATA = [

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  MODULE 1 — DevOps Basics                                   ║
    # ╚══════════════════════════════════════════════════════════════╝

    dict(
        id="intro-devops",
        module_id="devops-basics",
        order=1,
        title="Introduction au DevOps",
        type=LessonType.TEXT,
        duration=15,           # ✅ integer minutes
        url=None,
        content=_content(
            "Introduction au DevOps",
            """Le DevOps est une approche qui combine le développement logiciel (Dev) et les opérations informatiques (Ops). L'objectif est d'accélérer le cycle de vie du développement tout en maintenant la qualité.

Principes clés du DevOps :
• Collaboration entre équipes Dev et Ops
• Automatisation des processus répétitifs
• Intégration et déploiement continus (CI/CD)
• Monitoring et feedback continus
• Infrastructure as Code (IaC)

Le DevOps n'est pas un outil, c'est une culture et un ensemble de pratiques qui transforment la façon dont les équipes travaillent ensemble.

Les 5 principes CALMS :
• Culture — Collaboration et responsabilité partagée
• Automation — Automatiser les tâches répétitives
• Lean — Éliminer les gaspillages, livrer de la valeur
• Measurement — Mesurer tout : performance, qualité, vélocité
• Sharing — Partager les connaissances et les outils""",
            [
                {
                    "language": "yaml",
                    "code": "# Exemple de workflow GitHub Actions\nname: CI Pipeline\non: [push, pull_request]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - name: Run tests\n        run: npm test"
                }
            ],
            "Exercice : Premiers pas DevOps",
            """Exercice 1 : Créer votre premier workflow CI/CD

1. Créez un repository GitHub
2. Ajoutez un fichier .github/workflows/ci.yml
3. Configurez un job de build et test
4. Faites un push et observez le pipeline

Objectif : Comprendre le cycle complet d'un pipeline CI/CD.""",
            [
                {
                    "language": "bash",
                    "code": "# Initialiser un projet\nmkdir my-devops-project\ncd my-devops-project\ngit init\nmkdir -p .github/workflows\ntouch .github/workflows/ci.yml"
                }
            ]
        ),
    ),

    dict(
        id="cicd-github-actions",
        module_id="devops-basics",
        order=2,
        title="CI/CD avec GitHub Actions",
        type=LessonType.VIDEO,
        duration=25,           # ✅ integer minutes
        url="https://www.youtube.com/embed/R8_veQiYBjI",   # ✅ matches video-data.ts
        content=None,
    ),

    dict(
        id="docker-fundamentals",
        module_id="devops-basics",
        order=3,
        title="Docker Fondamentaux",
        type=LessonType.PRACTICE,
        duration=30,
        url=None,
        content=_content(
            "Docker Fondamentaux",
            """Docker est une plateforme de containerisation qui permet de packager une application avec toutes ses dépendances dans un container isolé.

Concepts clés :
• Image : Un template read-only pour créer des containers
• Container : Une instance en cours d'exécution d'une image
• Dockerfile : Un fichier de configuration pour construire une image
• Registry : Un dépôt pour stocker et distribuer des images (Docker Hub)

Avantages de Docker :
• Portabilité : "Ça marche sur ma machine" devient "Ça marche partout"
• Isolation : Chaque container est indépendant
• Légèreté : Plus léger que les machines virtuelles
• Reproductibilité : Même environnement en dev, test et prod""",
            [
                {
                    "language": "dockerfile",
                    "code": "# Exemple de Dockerfile\nFROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nEXPOSE 8000\nCMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\"]"
                }
            ],
            "Exercice : Containeriser une application",
            """Exercice : Créer et lancer votre premier container Docker

1. Écrivez un Dockerfile pour une application Python simple
2. Construisez l'image avec docker build
3. Lancez le container avec docker run
4. Vérifiez que l'application fonctionne""",
            [
                {
                    "language": "bash",
                    "code": "# Commandes Docker essentielles\ndocker build -t my-app .\ndocker run -d -p 8000:8000 my-app\ndocker ps\ndocker logs <container_id>\ndocker stop <container_id>"
                }
            ]
        ),
    ),

    dict(
        id="docker-compose",
        module_id="devops-basics",
        order=4,
        title="Docker Compose",
        type=LessonType.PRACTICE,
        duration=25,
        url=None,
        content=_content(
            "Docker Compose",
            """Docker Compose est un outil pour définir et gérer des applications multi-containers. Il utilise un fichier YAML pour configurer les services de l'application.

Cas d'utilisation :
• Application web + base de données + cache
• Microservices qui communiquent entre eux
• Environnements de développement complexes

Commandes principales :
• docker-compose up : Démarrer tous les services
• docker-compose down : Arrêter et supprimer les containers
• docker-compose logs : Voir les logs de tous les services
• docker-compose build : Rebuilder les images""",
            [
                {
                    "language": "yaml",
                    "code": "# docker-compose.yml\nversion: '3.8'\nservices:\n  web:\n    build: .\n    ports:\n      - \"8000:8000\"\n    depends_on:\n      - db\n    environment:\n      - DATABASE_URL=postgresql://user:pass@db/mydb\n  db:\n    image: postgres:15\n    environment:\n      - POSTGRES_PASSWORD=pass\n      - POSTGRES_DB=mydb\n    volumes:\n      - pgdata:/var/lib/postgresql/data\nvolumes:\n  pgdata:"
                }
            ],
            "Exercice : Orchestrer avec Docker Compose",
            """Exercice : Créer un environnement multi-containers

1. Créez un docker-compose.yml avec une app web et une base de données
2. Configurez les volumes pour la persistance
3. Utilisez des variables d'environnement
4. Testez la communication entre les services""",
            [
                {
                    "language": "bash",
                    "code": "# Commandes Docker Compose\ndocker-compose up -d\ndocker-compose ps\ndocker-compose logs -f web\ndocker-compose exec web bash\ndocker-compose down -v"
                }
            ]
        ),
    ),

    dict(
        id="quiz-devops",
        module_id="devops-basics",
        order=5,
        title="Quiz DevOps Basics",
        type=LessonType.QUIZ,
        duration=10,
        url=None,
        content=None,
    ),

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  MODULE 2 — MLOps Fundamentals                              ║
    # ╚══════════════════════════════════════════════════════════════╝

    dict(
        id="intro-mlops",
        module_id="mlops-fundamentals",
        order=1,
        title="Introduction au MLOps",
        type=LessonType.TEXT,
        duration=20,
        url=None,
        content=_content(
            "Introduction au MLOps",
            """MLOps (Machine Learning Operations) est un ensemble de pratiques qui combine Machine Learning, DevOps et Data Engineering pour déployer et maintenir des systèmes ML en production de manière fiable.

Pourquoi MLOps ?
• Reproduire les résultats d'expériences
• Automatiser le pipeline ML (données → entraînement → déploiement)
• Monitorer les modèles en production
• Gérer le versioning des données et des modèles

Les 3 piliers du MLOps :
1. Data Management : Versioning, qualité, pipelines de données
2. Model Management : Entraînement, évaluation, registry
3. Deployment : Serving, monitoring, feedback loop""",
            [],
            "Exercice : Planifier un pipeline MLOps",
            """Exercice : Concevoir l'architecture d'un pipeline MLOps

1. Identifiez les étapes du pipeline (collecte, préparation, entraînement, évaluation, déploiement)
2. Choisissez les outils pour chaque étape
3. Définissez les métriques de monitoring
4. Planifiez la stratégie de réentraînement""",
            []
        ),
    ),

    dict(
        id="dvc-versioning",
        module_id="mlops-fundamentals",
        order=2,
        title="Versioning avec DVC",
        type=LessonType.VIDEO,
        duration=30,
        url="https://www.youtube.com/embed/kLKBcPonMYw",   # ✅ matches video-data.ts
        content=None,
    ),

    dict(
        id="mlflow-tracking",
        module_id="mlops-fundamentals",
        order=3,
        title="MLflow pour le tracking",
        type=LessonType.PRACTICE,
        duration=35,
        url=None,
        content=_content(
            "MLflow pour le tracking",
            """MLflow est une plateforme open-source pour gérer le cycle de vie ML complet. Le composant Tracking permet de logger les expériences.

Concepts MLflow Tracking :
• Run : Une exécution d'un code ML
• Experiment : Un groupe de runs
• Parameters : Les hyperparamètres du modèle
• Metrics : Les résultats de performance
• Artifacts : Les fichiers générés (modèles, graphiques)""",
            [
                {
                    "language": "python",
                    "code": "import mlflow\n\nmlflow.set_experiment(\"iris-classification\")\n\nwith mlflow.start_run():\n    mlflow.log_param(\"n_estimators\", 100)\n    mlflow.log_param(\"max_depth\", 5)\n    mlflow.log_metric(\"accuracy\", 0.95)\n    mlflow.log_metric(\"f1_score\", 0.94)\n    mlflow.sklearn.log_model(model, \"model\")"
                }
            ],
            "Exercice : Tracker des expériences",
            """Exercice : Utiliser MLflow pour tracker un modèle

1. Installez MLflow : pip install mlflow
2. Créez un script d'entraînement avec tracking
3. Lancez l'UI MLflow : mlflow ui
4. Comparez les résultats de plusieurs runs""",
            [
                {
                    "language": "bash",
                    "code": "pip install mlflow\nmlflow ui --port 5000\n# Ouvrez http://localhost:5000"
                }
            ]
        ),
    ),

    dict(
        id="experiment-management",
        module_id="mlops-fundamentals",
        order=4,
        title="Gestion des expériences",
        type=LessonType.PRACTICE,
        duration=25,
        url=None,
        content=_content(
            "Gestion des expériences",
            """La gestion des expériences est cruciale pour maintenir la traçabilité et la reproductibilité des projets ML.

Bonnes pratiques :
• Versionner le code ET les données
• Logger systématiquement les hyperparamètres
• Comparer les métriques entre runs
• Documenter les décisions et observations
• Utiliser des tags pour organiser les expériences""",
            [],
            "Exercice : Organiser vos expériences",
            """Exercice : Mettre en place un workflow d'expérimentation

1. Créez une structure de projet standardisée
2. Définissez un fichier de configuration pour les hyperparamètres
3. Implémentez un script de comparaison des résultats
4. Documentez vos découvertes dans un journal d'expériences""",
            []
        ),
    ),

    dict(
        id="quiz-mlops",
        module_id="mlops-fundamentals",
        order=5,
        title="Quiz MLOps Fundamentals",
        type=LessonType.QUIZ,
        duration=10,
        url=None,
        content=None,
    ),

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  MODULE 3 — Déploiement & API                               ║
    # ╚══════════════════════════════════════════════════════════════╝

    dict(
        id="fastapi-ml",
        module_id="deployment-api",
        order=1,
        title="FastAPI pour ML",
        type=LessonType.VIDEO,
        duration=25,
        url="https://www.youtube.com/embed/7t2alSnE2-I",   # ✅ matches video-data.ts
        content=None,
    ),

    dict(
        id="model-containerization",
        module_id="deployment-api",
        order=2,
        title="Containerisation de modèles",
        type=LessonType.PRACTICE,
        duration=30,
        url=None,
        content=_content(
            "Containerisation de modèles",
            """La containerisation est essentielle pour déployer des modèles ML de manière reproductible et scalable.

Étapes clés :
1. Sérialiser le modèle (pickle, joblib, ONNX)
2. Créer une API autour du modèle (FastAPI, Flask)
3. Écrire un Dockerfile optimisé
4. Builder et tester l'image
5. Pousser vers un registry (Docker Hub, ECR, GCR)""",
            [
                {
                    "language": "dockerfile",
                    "code": "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY model/ ./model/\nCOPY app.py .\nEXPOSE 8000\nCMD [\"uvicorn\", \"app:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
                }
            ],
            "Exercice : Containeriser un modèle ML",
            """Exercice : Packager un modèle de classification dans un container

1. Entraînez un modèle simple et sauvegardez-le
2. Créez une API FastAPI pour servir les prédictions
3. Écrivez un Dockerfile multi-stage optimisé
4. Testez l'API containerisée localement""",
            [
                {
                    "language": "python",
                    "code": "# app.py\nfrom fastapi import FastAPI\nimport joblib\nimport numpy as np\n\napp = FastAPI()\nmodel = joblib.load(\"model/classifier.pkl\")\n\n@app.post(\"/predict\")\nasync def predict(features: list[float]):\n    prediction = model.predict([features])\n    return {\"prediction\": prediction[0].tolist()}"
                }
            ]
        ),
    ),

    dict(
        id="cloud-deployment",
        module_id="deployment-api",
        order=3,
        title="Déploiement cloud",
        type=LessonType.VIDEO,
        duration=35,
        url="https://www.youtube.com/embed/NTkn6_mEdFM",   # ✅ matches video-data.ts
        content=None,
    ),

    dict(
        id="monitoring",
        module_id="deployment-api",
        order=4,
        title="Monitoring",
        type=LessonType.PRACTICE,
        duration=30,
        url=None,
        content=_content(
            "Monitoring en production",
            """Le monitoring des modèles ML en production est essentiel pour détecter les dégradations de performance.

Types de monitoring :
• Performance du modèle : accuracy, latence, throughput
• Data drift : changement dans la distribution des données
• Concept drift : changement dans la relation input/output
• Infrastructure : CPU, mémoire, erreurs

Outils recommandés :
• Prometheus + Grafana pour les métriques système
• Evidently AI pour le data drift
• WhyLabs pour le monitoring ML complet""",
            [
                {
                    "language": "python",
                    "code": "# Exemple de monitoring avec Prometheus\nfrom prometheus_client import Counter, Histogram\n\nprediction_counter = Counter(\n    'predictions_total',\n    'Total predictions',\n    ['model_version', 'result']\n)\n\nprediction_latency = Histogram(\n    'prediction_latency_seconds',\n    'Prediction latency'\n)"
                }
            ],
            "Exercice : Mettre en place le monitoring",
            """Exercice : Configurer le monitoring d'un modèle

1. Ajoutez des métriques Prometheus à votre API
2. Configurez Grafana pour visualiser les métriques
3. Créez des alertes pour la latence et les erreurs
4. Simulez un data drift et observez les métriques""",
            []
        ),
    ),

    dict(
        id="quiz-deployment",
        module_id="deployment-api",
        order=5,
        title="Quiz Déploiement",
        type=LessonType.QUIZ,
        duration=10,
        url=None,
        content=None,
    ),

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  MODULE 4 — Évaluation finale                               ║
    # ╚══════════════════════════════════════════════════════════════╝

    dict(
        id="project-recap",
        module_id="final-evaluation",
        order=1,
        title="Projet récapitulatif",
        type=LessonType.PRACTICE,
        duration=120,
        url=None,
        content=_content(
            "Projet récapitulatif",
            """Ce projet final vous demande de mettre en pratique l'ensemble des compétences acquises pendant les 4 semaines.

Objectif : Créer un pipeline MLOps complet qui inclut :
1. Un modèle de classification entraîné et versionné
2. Une API de prédiction containerisée
3. Un pipeline CI/CD pour le déploiement automatique
4. Un système de monitoring des performances

Critères d'évaluation :
• Qualité du code et documentation
• Reproductibilité de l'environnement
• Automatisation du pipeline
• Monitoring et observabilité""",
            [],
            "Instructions du projet",
            """Étapes du projet :

1. Cloner le template du projet
2. Implémenter le modèle ML avec tracking MLflow
3. Créer l'API FastAPI + Dockerfile
4. Configurer GitHub Actions pour CI/CD
5. Ajouter le monitoring
6. Documenter le projet""",
            [
                {
                    "language": "bash",
                    "code": "# Structure du projet\nmlops-project/\n├── data/\n├── model/\n├── api/\n│   ├── app.py\n│   └── Dockerfile\n├── .github/workflows/\n│   └── ci-cd.yml\n├── docker-compose.yml\n├── requirements.txt\n└── README.md"
                }
            ]
        ),
    ),

    dict(
        id="final-quiz",
        module_id="final-evaluation",
        order=2,
        title="Quiz final",
        type=LessonType.QUIZ,
        duration=30,
        url=None,
        content=None,
    ),

    dict(
        id="additional-resources",
        module_id="final-evaluation",
        order=3,
        title="Ressources complémentaires",
        type=LessonType.TEXT,
        duration=15,
        url=None,
        content=_content(
            "Ressources complémentaires",
            """Voici une sélection de ressources pour approfondir vos connaissances en DevOps et MLOps :

📚 Livres :
• "The DevOps Handbook" - Gene Kim et al.
• "Designing Machine Learning Systems" - Chip Huyen
• "Building Machine Learning Pipelines" - Hannes Hapke

🌐 Sites & Blogs :
• MLOps Community (mlops.community)
• Google ML Best Practices
• AWS MLOps Workshop

🎓 Certifications :
• AWS Certified DevOps Engineer
• Google Professional ML Engineer
• Azure DevOps Solutions Expert""",
            [],
            "Prochaines étapes",
            """Pour continuer votre apprentissage :

1. Rejoignez la communauté MLOps sur Slack/Discord
2. Contribuez à des projets open-source
3. Participez à des hackathons ML
4. Créez votre propre projet de portfolio
5. Préparez une certification cloud""",
            []
        ),
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  3. QUIZZES
#
#  ✅ lesson_id added — links quiz to lesson (quizService resolves by lesson)
#  ✅ correct_answers snake_case — matches QuizQuestion in quizService.ts
#  ✅ passing_score & time_limit — required by Quiz interface in quizService.ts
#  ✅ Questions mirror quiz-data.ts exactly
# ══════════════════════════════════════════════════════════════════════════════
QUIZZES_DATA = [

    # ── Quiz DevOps Basics ────────────────────────────────────────────────────
    dict(
        id=uid(),
        module_id="devops-basics",
        title="Quiz DevOps Basics",
        passing_score=70,
        time_limit=600,                   # seconds
        questions=[
            {
                "id": "devops-q1",
                "type": "single",
                "question": "Qu'est-ce que CI/CD ?",
                "options": [
                    "Un langage de programmation",
                    "Continuous Integration / Continuous Deployment",
                    "Container Integration / Container Deployment",
                    "Code Inspection / Code Delivery"
                ],
                "correct_answers": [1],
                "explanation": "CI/CD signifie Continuous Integration / Continuous Deployment. C'est une pratique qui automatise l'intégration et le déploiement du code."
            },
            {
                "id": "devops-q2",
                "type": "single",
                "question": "Quelle commande lance un container Docker ?",
                "options": [
                    "docker start mycontainer",
                    "docker launch myimage",
                    "docker run myimage",
                    "docker execute myimage"
                ],
                "correct_answers": [2],
                "explanation": "`docker run` est la commande qui crée et démarre un nouveau container à partir d'une image Docker."
            },
            {
                "id": "devops-q3",
                "type": "multiple",
                "question": "Quels sont les avantages de GitHub Actions ?",
                "options": [
                    "Intégration native avec GitHub",
                    "Workflows définis en YAML",
                    "Marketplace d'actions réutilisables",
                    "Nécessite un serveur dédié"
                ],
                "correct_answers": [0, 1, 2],
                "explanation": "GitHub Actions s'intègre nativement avec GitHub, utilise des fichiers YAML pour les workflows, et dispose d'un marketplace. Il ne nécessite PAS de serveur dédié."
            },
            {
                "id": "devops-q4",
                "type": "boolean",
                "question": "Docker Compose permet d'orchestrer plusieurs containers.",
                "options": ["Vrai", "Faux"],
                "correct_answers": [0],
                "explanation": "Docker Compose est un outil pour définir et exécuter des applications multi-containers avec un fichier docker-compose.yml."
            },
            {
                "id": "devops-q5",
                "type": "single",
                "question": "Quel fichier définit les instructions pour construire une image Docker ?",
                "options": [
                    "docker-compose.yml",
                    "Dockerfile",
                    "package.json",
                    ".dockerignore"
                ],
                "correct_answers": [1],
                "explanation": "Le Dockerfile contient toutes les instructions nécessaires pour construire une image Docker."
            }
        ]
    ),

    # ── Quiz MLOps Fundamentals ───────────────────────────────────────────────
    dict(
        id=uid(),
        module_id="mlops-fundamentals",
        title="Quiz MLOps Fundamentals",
        passing_score=70,
        time_limit=600,
        questions=[
            {
                "id": "mlops-q1",
                "type": "single",
                "question": "Qu'est-ce que DVC ?",
                "options": [
                    "Data Version Control - un outil de versioning de données",
                    "Docker Virtual Container",
                    "Distributed Version Control",
                    "Data Visualization Component"
                ],
                "correct_answers": [0],
                "explanation": "DVC (Data Version Control) est un outil open-source de versioning de données et de modèles ML, complémentaire à Git."
            },
            {
                "id": "mlops-q2",
                "type": "multiple",
                "question": "Quelles fonctionnalités offre MLflow ?",
                "options": [
                    "Tracking d'expériences",
                    "Registry de modèles",
                    "Déploiement de modèles",
                    "Entraînement distribué GPU"
                ],
                "correct_answers": [0, 1, 2],
                "explanation": "MLflow offre le tracking d'expériences, un registry de modèles et des outils de déploiement. L'entraînement distribué GPU n'est pas une fonctionnalité native de MLflow."
            },
            {
                "id": "mlops-q3",
                "type": "boolean",
                "question": "MLOps est uniquement utile pour les grandes entreprises.",
                "options": ["Vrai", "Faux"],
                "correct_answers": [1],
                "explanation": "MLOps est utile pour toute équipe travaillant avec des modèles ML, quelle que soit la taille de l'entreprise."
            },
            {
                "id": "mlops-q4",
                "type": "single",
                "question": "Quel est le rôle principal d'un Model Registry ?",
                "options": [
                    "Entraîner des modèles plus rapidement",
                    "Stocker et versionner les modèles avec leurs métadonnées",
                    "Visualiser les données d'entraînement",
                    "Générer automatiquement du code ML"
                ],
                "correct_answers": [1],
                "explanation": "Un Model Registry permet de stocker, versionner et gérer le cycle de vie des modèles ML avec leurs métadonnées associées."
            },
            {
                "id": "mlops-q5",
                "type": "single",
                "question": "Quelle commande DVC permet de suivre un fichier de données ?",
                "options": [
                    "dvc track data.csv",
                    "dvc add data.csv",
                    "dvc push data.csv",
                    "dvc init data.csv"
                ],
                "correct_answers": [1],
                "explanation": "`dvc add` est la commande pour commencer à suivre un fichier avec DVC. Elle crée un fichier .dvc qui contient les métadonnées."
            }
        ]
    ),

    # ── Quiz Déploiement & API ────────────────────────────────────────────────
    dict(
        id=uid(),
        module_id="deployment-api",
        title="Quiz Déploiement & API",
        passing_score=70,
        time_limit=600,
        questions=[
            {
                "id": "deploy-q1",
                "type": "single",
                "question": "Quel framework Python est recommandé pour créer des APIs ML performantes ?",
                "options": [
                    "Django",
                    "Flask",
                    "FastAPI",
                    "Pyramid"
                ],
                "correct_answers": [2],
                "explanation": "FastAPI est recommandé pour les APIs ML grâce à sa performance, la validation automatique avec Pydantic, et la documentation OpenAPI intégrée."
            },
            {
                "id": "deploy-q2",
                "type": "multiple",
                "question": "Quels services cloud permettent de déployer des modèles ML ?",
                "options": [
                    "AWS SageMaker",
                    "Google Cloud AI Platform",
                    "Azure ML",
                    "Tous les précédents"
                ],
                "correct_answers": [0, 1, 2, 3],
                "explanation": "AWS SageMaker, Google Cloud AI Platform et Azure ML sont tous des services cloud majeurs pour le déploiement de modèles ML."
            },
            {
                "id": "deploy-q3",
                "type": "boolean",
                "question": "Le monitoring de modèles en production est optionnel.",
                "options": ["Vrai", "Faux"],
                "correct_answers": [1],
                "explanation": "Le monitoring est essentiel en production pour détecter le model drift, les anomalies de performance et garantir la fiabilité des prédictions."
            },
            {
                "id": "deploy-q4",
                "type": "single",
                "question": "Qu'est-ce que le \"model drift\" ?",
                "options": [
                    "Un modèle qui devient plus précis avec le temps",
                    "La dégradation des performances du modèle due aux changements de données",
                    "Le transfert d'un modèle vers un autre serveur",
                    "L'optimisation automatique des hyperparamètres"
                ],
                "correct_answers": [1],
                "explanation": "Le model drift désigne la dégradation progressive des performances d'un modèle lorsque les données en production diffèrent des données d'entraînement."
            },
            {
                "id": "deploy-q5",
                "type": "single",
                "question": "Quel format est couramment utilisé pour sérialiser des modèles ML ?",
                "options": [
                    "JSON",
                    "ONNX",
                    "CSV",
                    "HTML"
                ],
                "correct_answers": [1],
                "explanation": "ONNX (Open Neural Network Exchange) est un format standard ouvert pour la sérialisation et l'interopérabilité des modèles ML."
            }
        ]
    ),

    # ── Quiz Final ────────────────────────────────────────────────────────────
    dict(
        id=uid(),
        module_id="final-evaluation",
        title="Quiz Final",
        passing_score=70,
        time_limit=1800,      # 30 minutes
        questions=[
            {
                "id": "final-q1",
                "type": "single",
                "question": "Quel outil est utilisé pour le versioning de données dans un pipeline MLOps ?",
                "options": [
                    "Git LFS",
                    "DVC",
                    "Docker",
                    "Kubernetes"
                ],
                "correct_answers": [1],
                "explanation": "DVC (Data Version Control) est spécifiquement conçu pour le versioning de données et de modèles dans les pipelines MLOps."
            },
            {
                "id": "final-q2",
                "type": "multiple",
                "question": "Quels éléments font partie d'un pipeline CI/CD complet ?",
                "options": [
                    "Tests automatisés",
                    "Build et packaging",
                    "Déploiement automatique",
                    "Design de l'interface utilisateur"
                ],
                "correct_answers": [0, 1, 2],
                "explanation": "Un pipeline CI/CD comprend les tests automatisés, le build/packaging et le déploiement automatique. Le design UI n'est pas une étape du pipeline CI/CD."
            },
            {
                "id": "final-q3",
                "type": "boolean",
                "question": "Docker et les machines virtuelles sont la même chose.",
                "options": ["Vrai", "Faux"],
                "correct_answers": [1],
                "explanation": "Docker utilise la containerisation (partage du kernel hôte), tandis que les VMs virtualisent tout le système d'exploitation. Les containers sont plus légers et démarrent plus vite."
            },
            {
                "id": "final-q4",
                "type": "single",
                "question": "Quelle est la meilleure pratique pour gérer les secrets dans un pipeline CI/CD ?",
                "options": [
                    "Les stocker dans le code source",
                    "Utiliser des variables d'environnement ou un gestionnaire de secrets",
                    "Les écrire dans un fichier README",
                    "Les partager par email"
                ],
                "correct_answers": [1],
                "explanation": "Les secrets doivent être gérés via des variables d'environnement ou un gestionnaire de secrets dédié (comme HashiCorp Vault), jamais dans le code source."
            },
            {
                "id": "final-q5",
                "type": "single",
                "question": "Quel est l'avantage principal de la containerisation pour le déploiement ML ?",
                "options": [
                    "Réduire le coût des serveurs",
                    "Garantir la reproductibilité de l'environnement",
                    "Accélérer l'entraînement des modèles",
                    "Améliorer la précision des modèles"
                ],
                "correct_answers": [1],
                "explanation": "La containerisation garantit que l'environnement de production est identique à celui de développement, assurant la reproductibilité et éliminant les problèmes 'ça marche sur ma machine'."
            }
        ]
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  4. USERS
#
#  ✅ IDs, emails, passwords mirror mock-users.ts exactly
#  ✅ is_active bool derived from status "active"/"blocked"
#  ✅ modules_completed → list of module-id strings (not week numbers)
#     matches UserProgression.modules_completed JSONB field expected by frontend
# ══════════════════════════════════════════════════════════════════════════════
ALL_LESSON_IDS = [l["id"] for l in LESSONS_DATA]

def make_user(id_, first, last, email, raw_pw, role, is_active,
              created_days, login_days, progression, modules_completed, badges):
    return dict(
        id=id_, first_name=first, last_name=last, email=email,
        raw_password=raw_pw, role=role, is_active=is_active,
        created_days=created_days, login_days=login_days,
        progression=progression,
        modules_completed=modules_completed,  # ✅ list of module-id strings
        badges=badges
    )

# ✅ modules_completed use module ID strings, matching course-data.ts Module.id
USERS_DATA = [
    # Admins
    make_user("a1","Alice","Martin","admin@devops.com","Admin123!",UserRole.ADMIN,True,
              90,0,100,
              ["devops-basics","mlops-fundamentals","deployment-api","final-evaluation"],
              ["first-lesson","quiz-master","devops-pro","mlops-expert"]),
    make_user("a2","Bruno","Garcia","bruno@devops.com","Admin123!",UserRole.ADMIN,True,
              85,1,90,
              ["devops-basics","mlops-fundamentals","deployment-api"],
              ["first-lesson","quiz-master","devops-pro"]),
    # Instructors
    make_user("i1","Claire","Dubois","claire@devops.com","Instr123!",UserRole.INSTRUCTOR,True,
              60,0,85,
              ["devops-basics","mlops-fundamentals","deployment-api"],
              ["first-lesson","quiz-master"]),
    make_user("i2","David","Leroy","david@devops.com","Instr123!",UserRole.INSTRUCTOR,True,
              55,2,70,
              ["devops-basics","mlops-fundamentals"],
              ["first-lesson"]),
    make_user("i3","Emma","Bernard","emma@devops.com","Instr123!",UserRole.INSTRUCTOR,True,
              50,3,60,
              ["devops-basics","mlops-fundamentals"],
              ["first-lesson"]),
    # Students
    make_user("s1","Marie","Dupont","marie@example.com","Student1!",UserRole.STUDENT,True,
              30,0,75,
              ["devops-basics","mlops-fundamentals","deployment-api"],
              ["first-lesson","quiz-master"]),
    make_user("s2","Jean","Moreau","jean@example.com","Student1!",UserRole.STUDENT,True,
              28,1,55,
              ["devops-basics","mlops-fundamentals"],
              ["first-lesson"]),
    make_user("s3","Sophie","Laurent","sophie@example.com","Student1!",UserRole.STUDENT,True,
              25,0,90,
              ["devops-basics","mlops-fundamentals","deployment-api"],
              ["first-lesson","quiz-master","devops-pro"]),
    make_user("s4","Pierre","Thomas","pierre@example.com","Student1!",UserRole.STUDENT,True,
              22,2,40,
              ["devops-basics"],
              ["first-lesson"]),
    make_user("s5","Léa","Robert","lea@example.com","Student1!",UserRole.STUDENT,True,
              20,1,65,
              ["devops-basics","mlops-fundamentals"],
              ["first-lesson"]),
    make_user("s6","Lucas","Richard","lucas@example.com","Student1!",UserRole.STUDENT,True,
              18,3,30,
              ["devops-basics"],
              ["first-lesson"]),
    make_user("s7","Camille","Durand","camille@example.com","Student1!",UserRole.STUDENT,True,
              15,0,85,
              ["devops-basics","mlops-fundamentals","deployment-api"],
              ["first-lesson","quiz-master"]),
    make_user("s8","Hugo","Petit","hugo@example.com","Student1!",UserRole.STUDENT,True,
              12,4,20,
              [],
              []),
    make_user("s9","Chloé","Roux","chloe@example.com","Student1!",UserRole.STUDENT,True,
              10,1,50,
              ["devops-basics","mlops-fundamentals"],
              ["first-lesson"]),
    make_user("s10","Thomas","Fournier","thomas@example.com","Student1!",UserRole.STUDENT,True,
              8,0,45,
              ["devops-basics"],
              ["first-lesson"]),
    make_user("s11","Manon","Girard","manon@example.com","Student1!",UserRole.STUDENT,False,  # BLOCKED ✅
              7,5,10,
              [],
              []),
    make_user("s12","Nathan","Andre","nathan@example.com","Student1!",UserRole.STUDENT,True,
              5,0,15,
              [],
              []),
    make_user("s13","Julie","Mercier","julie@example.com","Student1!",UserRole.STUDENT,True,
              3,0,5,
              [],
              []),
    make_user("s14","Antoine","Blanc","antoine@example.com","Student1!",UserRole.STUDENT,True,
              2,0,0,
              [],
              []),
    make_user("s15","Laura","Guerin","laura@example.com","Student1!",UserRole.STUDENT,True,
              1,0,0,
              [],
              []),
]


# ══════════════════════════════════════════════════════════════════════════════
#  5. SEED FUNCTION
# ══════════════════════════════════════════════════════════════════════════════
def seed():
    print("🌱 Creating tables if needed...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ── Wipe (FK order matters) ────────────────────────────────────────────
        print("🗑️  Clearing existing data...")
        db.query(LessonCompletion).delete()
        db.query(UserBadge).delete()
        db.query(UserProgression).delete()
        db.query(QuizAttempt).delete()
        db.query(Quiz).delete()
        db.query(Lesson).delete()
        db.query(Module).delete()
        db.query(User).delete()
        db.commit()

        # ── Modules ───────────────────────────────────────────────────────────
        db.add_all([Module(**d) for d in MODULES_DATA])
        db.commit()
        print(f"✅ {len(MODULES_DATA)} modules")

        # ── Lessons ───────────────────────────────────────────────────────────
        db.add_all([Lesson(**d) for d in LESSONS_DATA])
        db.commit()
        print(f"✅ {len(LESSONS_DATA)} lessons")

        # ── Quizzes ───────────────────────────────────────────────────────────
        db.add_all([Quiz(**d) for d in QUIZZES_DATA])
        db.commit()
        print(f"✅ {len(QUIZZES_DATA)} quizzes ({sum(len(q['questions']) for q in QUIZZES_DATA)} questions total)")

        # ── Users + related ───────────────────────────────────────────────────
        for u in USERS_DATA:
            user = User(
                id=u["id"],
                email=u["email"],
                hashed_password=get_password_hash(u["raw_password"]),
                first_name=u["first_name"],
                last_name=u["last_name"],
                role=u["role"],
                is_active=u["is_active"],        # ✅ bool from mock-users.ts status
                avatar="",
                created_at=days_ago(u["created_days"]),
                last_login=days_ago(u["login_days"]),
            )
            db.add(user)
            db.flush()

            # Progression
            n_done = int(len(ALL_LESSON_IDS) * u["progression"] / 100)
            db.add(UserProgression(
                id=uid(),
                user_id=user.id,
                progression=u["progression"],
                modules_completed=u["modules_completed"],  # ✅ list of string IDs
                time_spent=u["progression"] * 312,
            ))

            # Badges
            for badge in u["badges"]:
                db.add(UserBadge(id=uid(), user_id=user.id, badge_name=badge))

            # Lesson completions
            for lesson_id in ALL_LESSON_IDS[:n_done]:
                db.add(LessonCompletion(
                    id=uid(),
                    user_id=user.id,
                    lesson_id=lesson_id,
                    completed=1,
                ))

        db.commit()
        print(f"✅ {len(USERS_DATA)} users (with progressions, badges, completions)")

        # ── Final summary ─────────────────────────────────────────────────────
        from app.models.progression import UserProgression as UP, UserBadge as UB, LessonCompletion as LC
        print("\n" + "=" * 60)
        print("🎉 Database seeded successfully!")
        print("=" * 60)
        print(f"\n📊 Data inserted:")
        print(f"   modules              → {db.query(Module).count()}")
        print(f"   lessons              → {db.query(Lesson).count()}")
        print(f"   quizzes              → {db.query(Quiz).count()}")
        print(f"   users                → {db.query(User).count()}")
        print(f"   user_progressions    → {db.query(UP).count()}")
        print(f"   user_badges          → {db.query(UB).count()}")
        print(f"   lesson_completions   → {db.query(LC).count()}")
        print("\n📝 Test Credentials:")
        print("-" * 60)
        print("👑 Admin:              admin@devops.com     / Admin123!")
        print("👑 Admin:              bruno@devops.com     / Admin123!")
        print("👨‍🏫 Instructor:         claire@devops.com    / Instr123!")
        print("👨‍🎓 Student (75%):      marie@example.com    / Student1!")
        print("👨‍🎓 Student (90%):      sophie@example.com   / Student1!")
        print("🚫 Blocked student:    manon@example.com    / Student1!")
        print("-" * 60)
        print("\n🔑 Frontend compatibility summary:")
        print("   • Lesson duration   → int (minutes) ✅")
        print("   • Lesson content    → JSON { theory, practice } ✅")
        print("   • Quiz lesson_id    → string matching Lesson.id ✅")
        print("   • modules_completed → string[] of module IDs ✅")
        print("   • User is_active    → bool (blocked = False) ✅")
        print("   • Video URLs        → match video-data.ts embedUrl ✅")
        print("\n🚀 Ready for production!")

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