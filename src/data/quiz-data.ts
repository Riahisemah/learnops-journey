export type QuestionType = 'single' | 'multiple' | 'boolean';

export interface QuizQuestion {
  id: string;
  question: string;
  type: QuestionType;
  options: string[];
  correctAnswers: number[]; // indices of correct options
  explanation: string;
}

export interface Quiz {
  moduleId: string;
  lessonId: string;
  title: string;
  questions: QuizQuestion[];
}

export const quizzes: Quiz[] = [
  {
    moduleId: 'devops-basics',
    lessonId: 'quiz-devops',
    title: 'Quiz DevOps Basics',
    questions: [
      {
        id: 'devops-q1',
        question: 'Qu\'est-ce que CI/CD ?',
        type: 'single',
        options: [
          'Un langage de programmation',
          'Continuous Integration / Continuous Deployment',
          'Container Integration / Container Deployment',
          'Code Inspection / Code Delivery'
        ],
        correctAnswers: [1],
        explanation: 'CI/CD signifie Continuous Integration / Continuous Deployment. C\'est une pratique qui automatise l\'intégration et le déploiement du code.'
      },
      {
        id: 'devops-q2',
        question: 'Quelle commande lance un container Docker ?',
        type: 'single',
        options: [
          'docker start mycontainer',
          'docker launch myimage',
          'docker run myimage',
          'docker execute myimage'
        ],
        correctAnswers: [2],
        explanation: '`docker run` est la commande qui crée et démarre un nouveau container à partir d\'une image Docker.'
      },
      {
        id: 'devops-q3',
        question: 'Quels sont les avantages de GitHub Actions ?',
        type: 'multiple',
        options: [
          'Intégration native avec GitHub',
          'Workflows définis en YAML',
          'Marketplace d\'actions réutilisables',
          'Nécessite un serveur dédié'
        ],
        correctAnswers: [0, 1, 2],
        explanation: 'GitHub Actions s\'intègre nativement avec GitHub, utilise des fichiers YAML pour les workflows, et dispose d\'un marketplace. Il ne nécessite PAS de serveur dédié.'
      },
      {
        id: 'devops-q4',
        question: 'Docker Compose permet d\'orchestrer plusieurs containers.',
        type: 'boolean',
        options: ['Vrai', 'Faux'],
        correctAnswers: [0],
        explanation: 'Docker Compose est un outil pour définir et exécuter des applications multi-containers avec un fichier docker-compose.yml.'
      },
      {
        id: 'devops-q5',
        question: 'Quel fichier définit les instructions pour construire une image Docker ?',
        type: 'single',
        options: [
          'docker-compose.yml',
          'Dockerfile',
          'package.json',
          '.dockerignore'
        ],
        correctAnswers: [1],
        explanation: 'Le Dockerfile contient toutes les instructions nécessaires pour construire une image Docker.'
      }
    ]
  },
  {
    moduleId: 'mlops-fundamentals',
    lessonId: 'quiz-mlops',
    title: 'Quiz MLOps Fundamentals',
    questions: [
      {
        id: 'mlops-q1',
        question: 'Qu\'est-ce que DVC ?',
        type: 'single',
        options: [
          'Data Version Control - un outil de versioning de données',
          'Docker Virtual Container',
          'Distributed Version Control',
          'Data Visualization Component'
        ],
        correctAnswers: [0],
        explanation: 'DVC (Data Version Control) est un outil open-source de versioning de données et de modèles ML, complémentaire à Git.'
      },
      {
        id: 'mlops-q2',
        question: 'Quelles fonctionnalités offre MLflow ?',
        type: 'multiple',
        options: [
          'Tracking d\'expériences',
          'Registry de modèles',
          'Déploiement de modèles',
          'Entraînement distribué GPU'
        ],
        correctAnswers: [0, 1, 2],
        explanation: 'MLflow offre le tracking d\'expériences, un registry de modèles et des outils de déploiement. L\'entraînement distribué GPU n\'est pas une fonctionnalité native de MLflow.'
      },
      {
        id: 'mlops-q3',
        question: 'MLOps est uniquement utile pour les grandes entreprises.',
        type: 'boolean',
        options: ['Vrai', 'Faux'],
        correctAnswers: [1],
        explanation: 'MLOps est utile pour toute équipe travaillant avec des modèles ML, quelle que soit la taille de l\'entreprise. Il améliore la reproductibilité et la fiabilité.'
      },
      {
        id: 'mlops-q4',
        question: 'Quel est le rôle principal d\'un Model Registry ?',
        type: 'single',
        options: [
          'Entraîner des modèles plus rapidement',
          'Stocker et versionner les modèles avec leurs métadonnées',
          'Visualiser les données d\'entraînement',
          'Générer automatiquement du code ML'
        ],
        correctAnswers: [1],
        explanation: 'Un Model Registry permet de stocker, versionner et gérer le cycle de vie des modèles ML avec leurs métadonnées associées.'
      },
      {
        id: 'mlops-q5',
        question: 'Quelle commande DVC permet de suivre un fichier de données ?',
        type: 'single',
        options: [
          'dvc track data.csv',
          'dvc add data.csv',
          'dvc push data.csv',
          'dvc init data.csv'
        ],
        correctAnswers: [1],
        explanation: '`dvc add` est la commande pour commencer à suivre un fichier avec DVC. Elle crée un fichier .dvc qui contient les métadonnées.'
      }
    ]
  },
  {
    moduleId: 'deployment-api',
    lessonId: 'quiz-deployment',
    title: 'Quiz Déploiement & API',
    questions: [
      {
        id: 'deploy-q1',
        question: 'Quel framework Python est recommandé pour créer des APIs ML performantes ?',
        type: 'single',
        options: [
          'Django',
          'Flask',
          'FastAPI',
          'Pyramid'
        ],
        correctAnswers: [2],
        explanation: 'FastAPI est recommandé pour les APIs ML grâce à sa performance (basé sur Starlette/Uvicorn), la validation automatique avec Pydantic, et la documentation OpenAPI intégrée.'
      },
      {
        id: 'deploy-q2',
        question: 'Quels services cloud permettent de déployer des modèles ML ?',
        type: 'multiple',
        options: [
          'AWS SageMaker',
          'Google Cloud AI Platform',
          'Azure ML',
          'Tous les précédents'
        ],
        correctAnswers: [0, 1, 2, 3],
        explanation: 'AWS SageMaker, Google Cloud AI Platform et Azure ML sont tous des services cloud majeurs pour le déploiement de modèles ML.'
      },
      {
        id: 'deploy-q3',
        question: 'Le monitoring de modèles en production est optionnel.',
        type: 'boolean',
        options: ['Vrai', 'Faux'],
        correctAnswers: [1],
        explanation: 'Le monitoring est essentiel en production pour détecter le model drift, les anomalies de performance et garantir la fiabilité des prédictions.'
      },
      {
        id: 'deploy-q4',
        question: 'Qu\'est-ce que le "model drift" ?',
        type: 'single',
        options: [
          'Un modèle qui devient plus précis avec le temps',
          'La dégradation des performances du modèle due aux changements de données',
          'Le transfert d\'un modèle vers un autre serveur',
          'L\'optimisation automatique des hyperparamètres'
        ],
        correctAnswers: [1],
        explanation: 'Le model drift désigne la dégradation progressive des performances d\'un modèle lorsque les données en production diffèrent des données d\'entraînement.'
      },
      {
        id: 'deploy-q5',
        question: 'Quel format est couramment utilisé pour sérialiser des modèles ML ?',
        type: 'single',
        options: [
          'JSON',
          'ONNX',
          'CSV',
          'HTML'
        ],
        correctAnswers: [1],
        explanation: 'ONNX (Open Neural Network Exchange) est un format standard ouvert pour la sérialisation et l\'interopérabilité des modèles ML entre différents frameworks.'
      }
    ]
  },
  {
    moduleId: 'final-evaluation',
    lessonId: 'final-quiz',
    title: 'Quiz Final',
    questions: [
      {
        id: 'final-q1',
        question: 'Quel outil est utilisé pour le versioning de données dans un pipeline MLOps ?',
        type: 'single',
        options: [
          'Git LFS',
          'DVC',
          'Docker',
          'Kubernetes'
        ],
        correctAnswers: [1],
        explanation: 'DVC (Data Version Control) est spécifiquement conçu pour le versioning de données et de modèles dans les pipelines MLOps.'
      },
      {
        id: 'final-q2',
        question: 'Quels éléments font partie d\'un pipeline CI/CD complet ?',
        type: 'multiple',
        options: [
          'Tests automatisés',
          'Build et packaging',
          'Déploiement automatique',
          'Design de l\'interface utilisateur'
        ],
        correctAnswers: [0, 1, 2],
        explanation: 'Un pipeline CI/CD comprend les tests automatisés, le build/packaging et le déploiement automatique. Le design UI n\'est pas une étape du pipeline CI/CD.'
      },
      {
        id: 'final-q3',
        question: 'Docker et les machines virtuelles sont la même chose.',
        type: 'boolean',
        options: ['Vrai', 'Faux'],
        correctAnswers: [1],
        explanation: 'Docker utilise la containerisation (partage du kernel hôte), tandis que les VMs virtualisent tout le système d\'exploitation. Les containers sont plus légers et démarrent plus vite.'
      },
      {
        id: 'final-q4',
        question: 'Quelle est la meilleure pratique pour gérer les secrets (API keys, mots de passe) dans un pipeline CI/CD ?',
        type: 'single',
        options: [
          'Les stocker dans le code source',
          'Utiliser des variables d\'environnement ou un gestionnaire de secrets',
          'Les écrire dans un fichier README',
          'Les partager par email'
        ],
        correctAnswers: [1],
        explanation: 'Les secrets doivent être gérés via des variables d\'environnement ou un gestionnaire de secrets dédié (comme HashiCorp Vault), jamais dans le code source.'
      },
      {
        id: 'final-q5',
        question: 'Quel est l\'avantage principal de la containerisation pour le déploiement ML ?',
        type: 'single',
        options: [
          'Réduire le coût des serveurs',
          'Garantir la reproductibilité de l\'environnement',
          'Accélérer l\'entraînement des modèles',
          'Améliorer la précision des modèles'
        ],
        correctAnswers: [1],
        explanation: 'La containerisation garantit que l\'environnement de production est identique à celui de développement, assurant la reproductibilité et éliminant les problèmes "ça marche sur ma machine".'
      }
    ]
  }
];

export const getQuizByLesson = (moduleId: string, lessonId: string): Quiz | undefined => {
  return quizzes.find(q => q.moduleId === moduleId && q.lessonId === lessonId);
};
