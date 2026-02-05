export type LessonType = 'video' | 'text' | 'quiz' | 'practice';

export interface Lesson {
  id: string;
  title: string;
  type: LessonType;
  duration: number; // in minutes
  description: string;
}

export interface Module {
  id: string;
  week: number;
  title: string;
  description: string;
  icon: string;
  lessons: Lesson[];
}

export const modules: Module[] = [
  {
    id: 'devops-basics',
    week: 1,
    title: 'DevOps Basics',
    description: 'Découvrez les fondamentaux du DevOps, CI/CD et Docker',
    icon: 'GitBranch',
    lessons: [
      {
        id: 'intro-devops',
        title: 'Introduction au DevOps',
        type: 'text',
        duration: 15,
        description: 'Comprendre la philosophie et les principes du DevOps',
      },
      {
        id: 'cicd-github-actions',
        title: 'CI/CD avec GitHub Actions',
        type: 'video',
        duration: 25,
        description: 'Mettre en place un pipeline CI/CD avec GitHub Actions',
      },
      {
        id: 'docker-fundamentals',
        title: 'Docker Fondamentaux',
        type: 'practice',
        duration: 30,
        description: 'Apprendre à containeriser vos applications',
      },
      {
        id: 'docker-compose',
        title: 'Docker Compose',
        type: 'practice',
        duration: 25,
        description: 'Orchestrer plusieurs containers avec Docker Compose',
      },
      {
        id: 'quiz-devops',
        title: 'Quiz DevOps Basics',
        type: 'quiz',
        duration: 10,
        description: 'Testez vos connaissances sur le DevOps',
      },
    ],
  },
  {
    id: 'mlops-fundamentals',
    week: 2,
    title: 'MLOps Fundamentals',
    description: 'Maîtrisez le versioning de données et le tracking d\'expériences',
    icon: 'Brain',
    lessons: [
      {
        id: 'intro-mlops',
        title: 'Introduction au MLOps',
        type: 'text',
        duration: 20,
        description: 'Comprendre les enjeux du MLOps et son importance',
      },
      {
        id: 'dvc-versioning',
        title: 'Versioning avec DVC',
        type: 'video',
        duration: 30,
        description: 'Gérer le versioning de vos données et modèles',
      },
      {
        id: 'mlflow-tracking',
        title: 'MLflow pour le tracking',
        type: 'practice',
        duration: 35,
        description: 'Tracker vos expériences ML avec MLflow',
      },
      {
        id: 'experiment-management',
        title: 'Gestion des expériences',
        type: 'practice',
        duration: 25,
        description: 'Organiser et comparer vos expériences',
      },
      {
        id: 'quiz-mlops',
        title: 'Quiz MLOps Fundamentals',
        type: 'quiz',
        duration: 10,
        description: 'Testez vos connaissances sur le MLOps',
      },
    ],
  },
  {
    id: 'deployment-api',
    week: 3,
    title: 'Déploiement & API',
    description: 'Déployez vos modèles ML via des APIs robustes',
    icon: 'Rocket',
    lessons: [
      {
        id: 'fastapi-ml',
        title: 'FastAPI pour ML',
        type: 'video',
        duration: 25,
        description: 'Créer des APIs performantes pour vos modèles',
      },
      {
        id: 'model-containerization',
        title: 'Containerisation de modèles',
        type: 'practice',
        duration: 30,
        description: 'Packager vos modèles dans des containers Docker',
      },
      {
        id: 'cloud-deployment',
        title: 'Déploiement cloud',
        type: 'video',
        duration: 35,
        description: 'Déployer sur AWS, GCP ou Azure',
      },
      {
        id: 'monitoring',
        title: 'Monitoring',
        type: 'practice',
        duration: 30,
        description: 'Surveiller vos modèles en production',
      },
      {
        id: 'quiz-deployment',
        title: 'Quiz Déploiement',
        type: 'quiz',
        duration: 10,
        description: 'Testez vos connaissances sur le déploiement',
      },
    ],
  },
  {
    id: 'final-evaluation',
    week: 4,
    title: 'Évaluation finale',
    description: 'Mettez en pratique tout ce que vous avez appris',
    icon: 'Award',
    lessons: [
      {
        id: 'project-recap',
        title: 'Projet récapitulatif',
        type: 'practice',
        duration: 120,
        description: 'Réalisez un projet complet de bout en bout',
      },
      {
        id: 'final-quiz',
        title: 'Quiz final',
        type: 'quiz',
        duration: 30,
        description: 'Évaluation finale de vos compétences',
      },
      {
        id: 'additional-resources',
        title: 'Ressources complémentaires',
        type: 'text',
        duration: 15,
        description: 'Liens et ressources pour aller plus loin',
      },
    ],
  },
];

export const getTotalLessons = (): number => {
  return modules.reduce((acc, module) => acc + module.lessons.length, 0);
};

export const getTotalDuration = (): number => {
  return modules.reduce((acc, module) => 
    acc + module.lessons.reduce((lessonAcc, lesson) => lessonAcc + lesson.duration, 0), 0
  );
};

export const getModuleById = (moduleId: string): Module | undefined => {
  return modules.find(m => m.id === moduleId);
};

export const getLessonById = (moduleId: string, lessonId: string): Lesson | undefined => {
  const module = getModuleById(moduleId);
  return module?.lessons.find(l => l.id === lessonId);
};
