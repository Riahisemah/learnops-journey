  interface ContentSection {
    title: string;
    content: string;
    codeBlocks?: { language: string; code: string }[];
  }

  export interface LessonContent {
    moduleId: string;
    lessonId: string;
    theory: ContentSection;
    practice: ContentSection;
  }

  export const lessonContents: LessonContent[] = [
    // DevOps Basics
    {
      moduleId: 'devops-basics',
      lessonId: 'intro-devops',
      theory: {
        title: 'Introduction au DevOps',
        content: `Le DevOps est une approche qui combine le développement logiciel (Dev) et les opérations informatiques (Ops). L'objectif est d'accélérer le cycle de vie du développement tout en maintenant la qualité.

  Principes clés du DevOps :
  • Collaboration entre équipes Dev et Ops
  • Automatisation des processus répétitifs
  • Intégration et déploiement continus (CI/CD)
  • Monitoring et feedback continus
  • Infrastructure as Code (IaC)

  Le DevOps n'est pas un outil, c'est une culture et un ensemble de pratiques qui transforment la façon dont les équipes travaillent ensemble.`,
        codeBlocks: [
          {
            language: 'yaml',
            code: `# Exemple de workflow GitHub Actions
  name: CI Pipeline
  on: [push, pull_request]
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Run tests
          run: npm test`
          }
        ]
      },
      practice: {
        title: 'Exercice : Premiers pas DevOps',
        content: `Exercice 1 : Créer votre premier workflow CI/CD

  1. Créez un repository GitHub
  2. Ajoutez un fichier .github/workflows/ci.yml
  3. Configurez un job de build et test
  4. Faites un push et observez le pipeline

  Objectif : Comprendre le cycle complet d'un pipeline CI/CD.`,
        codeBlocks: [
          {
            language: 'bash',
            code: `# Initialiser un projet
  mkdir my-devops-project
  cd my-devops-project
  git init
  mkdir -p .github/workflows
  touch .github/workflows/ci.yml`
          }
        ]
      }
    },
    {
      moduleId: 'devops-basics',
      lessonId: 'docker-fundamentals',
      theory: {
        title: 'Docker Fondamentaux',
        content: `Docker est une plateforme de containerisation qui permet de packager une application avec toutes ses dépendances dans un container isolé.

  Concepts clés :
  • Image : Un template read-only pour créer des containers
  • Container : Une instance en cours d'exécution d'une image
  • Dockerfile : Un fichier de configuration pour construire une image
  • Registry : Un dépôt pour stocker et distribuer des images (Docker Hub)

  Avantages de Docker :
  • Portabilité : "Ça marche sur ma machine" devient "Ça marche partout"
  • Isolation : Chaque container est indépendant
  • Légèreté : Plus léger que les machines virtuelles
  • Reproductibilité : Même environnement en dev, test et prod`,
        codeBlocks: [
          {
            language: 'dockerfile',
            code: `# Exemple de Dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  EXPOSE 8000
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]`
          }
        ]
      },
      practice: {
        title: 'Exercice : Containeriser une application',
        content: `Exercice : Créer et lancer votre premier container Docker

  1. Écrivez un Dockerfile pour une application Python simple
  2. Construisez l'image avec docker build
  3. Lancez le container avec docker run
  4. Vérifiez que l'application fonctionne`,
        codeBlocks: [
          {
            language: 'bash',
            code: `# Commandes Docker essentielles
  docker build -t my-app .
  docker run -d -p 8000:8000 my-app
  docker ps
  docker logs <container_id>
  docker stop <container_id>`
          }
        ]
      }
    },
    {
      moduleId: 'devops-basics',
      lessonId: 'docker-compose',
      theory: {
        title: 'Docker Compose',
        content: `Docker Compose est un outil pour définir et gérer des applications multi-containers. Il utilise un fichier YAML pour configurer les services de l'application.

  Cas d'utilisation :
  • Application web + base de données + cache
  • Microservices qui communiquent entre eux
  • Environnements de développement complexes

  Commandes principales :
  • docker-compose up : Démarrer tous les services
  • docker-compose down : Arrêter et supprimer les containers
  • docker-compose logs : Voir les logs de tous les services
  • docker-compose build : Rebuilder les images`,
        codeBlocks: [
          {
            language: 'yaml',
            code: `# docker-compose.yml
  version: '3.8'
  services:
    web:
      build: .
      ports:
        - "8000:8000"
      depends_on:
        - db
      environment:
        - DATABASE_URL=postgresql://user:pass@db/mydb
    db:
      image: postgres:15
      environment:
        - POSTGRES_PASSWORD=pass
        - POSTGRES_DB=mydb
      volumes:
        - pgdata:/var/lib/postgresql/data
  volumes:
    pgdata:`
          }
        ]
      },
      practice: {
        title: 'Exercice : Orchestrer avec Docker Compose',
        content: `Exercice : Créer un environnement multi-containers

  1. Créez un docker-compose.yml avec une app web et une base de données
  2. Configurez les volumes pour la persistance
  3. Utilisez des variables d'environnement
  4. Testez la communication entre les services`,
        codeBlocks: [
          {
            language: 'bash',
            code: `# Commandes Docker Compose
  docker-compose up -d
  docker-compose ps
  docker-compose logs -f web
  docker-compose exec web bash
  docker-compose down -v`
          }
        ]
      }
    },
    // MLOps
    {
      moduleId: 'mlops-fundamentals',
      lessonId: 'intro-mlops',
      theory: {
        title: 'Introduction au MLOps',
        content: `MLOps (Machine Learning Operations) est un ensemble de pratiques qui combine Machine Learning, DevOps et Data Engineering pour déployer et maintenir des systèmes ML en production de manière fiable.

  Pourquoi MLOps ?
  • Reproduire les résultats d'expériences
  • Automatiser le pipeline ML (données → entraînement → déploiement)
  • Monitorer les modèles en production
  • Gérer le versioning des données et des modèles

  Les 3 piliers du MLOps :
  1. Data Management : Versioning, qualité, pipelines de données
  2. Model Management : Entraînement, évaluation, registry
  3. Deployment : Serving, monitoring, feedback loop`,
      },
      practice: {
        title: 'Exercice : Planifier un pipeline MLOps',
        content: `Exercice : Concevoir l'architecture d'un pipeline MLOps

  1. Identifiez les étapes du pipeline (collecte, préparation, entraînement, évaluation, déploiement)
  2. Choisissez les outils pour chaque étape
  3. Définissez les métriques de monitoring
  4. Planifiez la stratégie de réentraînement`,
      }
    },
    {
      moduleId: 'mlops-fundamentals',
      lessonId: 'mlflow-tracking',
      theory: {
        title: 'MLflow pour le tracking',
        content: `MLflow est une plateforme open-source pour gérer le cycle de vie ML complet. Le composant Tracking permet de logger les expériences.

  Concepts MLflow Tracking :
  • Run : Une exécution d'un code ML
  • Experiment : Un groupe de runs
  • Parameters : Les hyperparamètres du modèle
  • Metrics : Les résultats de performance
  • Artifacts : Les fichiers générés (modèles, graphiques)`,
        codeBlocks: [
          {
            language: 'python',
            code: `import mlflow

  mlflow.set_experiment("iris-classification")

  with mlflow.start_run():
      mlflow.log_param("n_estimators", 100)
      mlflow.log_param("max_depth", 5)
      mlflow.log_metric("accuracy", 0.95)
      mlflow.log_metric("f1_score", 0.94)
      mlflow.sklearn.log_model(model, "model")`
          }
        ]
      },
      practice: {
        title: 'Exercice : Tracker des expériences',
        content: `Exercice : Utiliser MLflow pour tracker un modèle

  1. Installez MLflow : pip install mlflow
  2. Créez un script d'entraînement avec tracking
  3. Lancez l'UI MLflow : mlflow ui
  4. Comparez les résultats de plusieurs runs`,
        codeBlocks: [
          {
            language: 'bash',
            code: `pip install mlflow
  mlflow ui --port 5000
  # Ouvrez http://localhost:5000`
          }
        ]
      }
    },
    {
      moduleId: 'mlops-fundamentals',
      lessonId: 'experiment-management',
      theory: {
        title: 'Gestion des expériences',
        content: `La gestion des expériences est cruciale pour maintenir la traçabilité et la reproductibilité des projets ML.

  Bonnes pratiques :
  • Versionner le code ET les données
  • Logger systématiquement les hyperparamètres
  • Comparer les métriques entre runs
  • Documenter les décisions et observations
  • Utiliser des tags pour organiser les expériences`,
      },
      practice: {
        title: 'Exercice : Organiser vos expériences',
        content: `Exercice : Mettre en place un workflow d'expérimentation

  1. Créez une structure de projet standardisée
  2. Définissez un fichier de configuration pour les hyperparamètres
  3. Implémentez un script de comparaison des résultats
  4. Documentez vos découvertes dans un journal d'expériences`,
      }
    },
    // Deployment
    {
      moduleId: 'deployment-api',
      lessonId: 'model-containerization',
      theory: {
        title: 'Containerisation de modèles',
        content: `La containerisation est essentielle pour déployer des modèles ML de manière reproductible et scalable.

  Étapes clés :
  1. Sérialiser le modèle (pickle, joblib, ONNX)
  2. Créer une API autour du modèle (FastAPI, Flask)
  3. Écrire un Dockerfile optimisé
  4. Builder et tester l'image
  5. Pousser vers un registry (Docker Hub, ECR, GCR)`,
        codeBlocks: [
          {
            language: 'dockerfile',
            code: `FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY model/ ./model/
  COPY app.py .
  EXPOSE 8000
  CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]`
          }
        ]
      },
      practice: {
        title: 'Exercice : Containeriser un modèle ML',
        content: `Exercice : Packager un modèle de classification dans un container

  1. Entraînez un modèle simple et sauvegardez-le
  2. Créez une API FastAPI pour servir les prédictions
  3. Écrivez un Dockerfile multi-stage optimisé
  4. Testez l'API containerisée localement`,
        codeBlocks: [
          {
            language: 'python',
            code: `# app.py
  from fastapi import FastAPI
  import joblib
  import numpy as np

  app = FastAPI()
  model = joblib.load("model/classifier.pkl")

  @app.post("/predict")
  async def predict(features: list[float]):
      prediction = model.predict([features])
      return {"prediction": prediction[0].tolist()}`
          }
        ]
      }
    },
    {
      moduleId: 'deployment-api',
      lessonId: 'monitoring',
      theory: {
        title: 'Monitoring en production',
        content: `Le monitoring des modèles ML en production est essentiel pour détecter les dégradations de performance.

  Types de monitoring :
  • Performance du modèle : accuracy, latence, throughput
  • Data drift : changement dans la distribution des données
  • Concept drift : changement dans la relation input/output
  • Infrastructure : CPU, mémoire, erreurs

  Outils recommandés :
  • Prometheus + Grafana pour les métriques système
  • Evidently AI pour le data drift
  • WhyLabs pour le monitoring ML complet`,
        codeBlocks: [
          {
            language: 'python',
            code: `# Exemple de monitoring avec Prometheus
  from prometheus_client import Counter, Histogram

  prediction_counter = Counter(
      'predictions_total', 
      'Total predictions', 
      ['model_version', 'result']
  )

  prediction_latency = Histogram(
      'prediction_latency_seconds',
      'Prediction latency'
  )`
          }
        ]
      },
      practice: {
        title: 'Exercice : Mettre en place le monitoring',
        content: `Exercice : Configurer le monitoring d'un modèle

  1. Ajoutez des métriques Prometheus à votre API
  2. Configurez Grafana pour visualiser les métriques
  3. Créez des alertes pour la latence et les erreurs
  4. Simulez un data drift et observez les métriques`,
      }
    },
    // Final
    {
      moduleId: 'final-evaluation',
      lessonId: 'project-recap',
      theory: {
        title: 'Projet récapitulatif',
        content: `Ce projet final vous demande de mettre en pratique l'ensemble des compétences acquises pendant les 4 semaines.

  Objectif : Créer un pipeline MLOps complet qui inclut :
  1. Un modèle de classification entraîné et versionné
  2. Une API de prédiction containerisée
  3. Un pipeline CI/CD pour le déploiement automatique
  4. Un système de monitoring des performances

  Critères d'évaluation :
  • Qualité du code et documentation
  • Reproductibilité de l'environnement
  • Automatisation du pipeline
  • Monitoring et observabilité`,
      },
      practice: {
        title: 'Instructions du projet',
        content: `Étapes du projet :

  1. Cloner le template du projet
  2. Implémenter le modèle ML avec tracking MLflow
  3. Créer l'API FastAPI + Dockerfile
  4. Configurer GitHub Actions pour CI/CD
  5. Ajouter le monitoring
  6. Documenter le projet`,
        codeBlocks: [
          {
            language: 'bash',
            code: `# Structure du projet
  mlops-project/
  ├── data/
  ├── model/
  ├── api/
  │   ├── app.py
  │   └── Dockerfile
  ├── .github/workflows/
  │   └── ci-cd.yml
  ├── docker-compose.yml
  ├── requirements.txt
  └── README.md`
          }
        ]
      }
    },
    {
      moduleId: 'final-evaluation',
      lessonId: 'additional-resources',
      theory: {
        title: 'Ressources complémentaires',
        content: `Voici une sélection de ressources pour approfondir vos connaissances en DevOps et MLOps :

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
  • Azure DevOps Solutions Expert`,
      },
      practice: {
        title: 'Prochaines étapes',
        content: `Pour continuer votre apprentissage :

  1. Rejoignez la communauté MLOps sur Slack/Discord
  2. Contribuez à des projets open-source
  3. Participez à des hackathons ML
  4. Créez votre propre projet de portfolio
  5. Préparez une certification cloud`,
      }
    },
  ];

  export const getLessonContent = (moduleId: string, lessonId: string): LessonContent | undefined => {
    return lessonContents.find(c => c.moduleId === moduleId && c.lessonId === lessonId);
  };
