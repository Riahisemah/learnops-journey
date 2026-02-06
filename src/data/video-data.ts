export interface VideoChapter {
  time: number; // seconds
  title: string;
}

export interface VideoData {
  moduleId: string;
  lessonId: string;
  title: string;
  embedUrl?: string; // Loom or YouTube embed URL
  chapters: VideoChapter[];
}

export const videoData: VideoData[] = [
  {
    moduleId: 'devops-basics',
    lessonId: 'cicd-github-actions',
    title: 'CI/CD avec GitHub Actions',
    embedUrl: 'https://www.youtube.com/embed/R8_veQiYBjI',
    chapters: [
      { time: 0, title: 'Introduction' },
      { time: 60, title: 'Créer un workflow' },
      { time: 180, title: 'Jobs et steps' },
      { time: 300, title: 'Variables et secrets' },
      { time: 420, title: 'Déploiement automatique' },
    ],
  },
  {
    moduleId: 'mlops-fundamentals',
    lessonId: 'dvc-versioning',
    title: 'Versioning avec DVC',
    embedUrl: 'https://www.youtube.com/embed/kLKBcPonMYw',
    chapters: [
      { time: 0, title: 'Pourquoi versionner les données ?' },
      { time: 90, title: 'Installation de DVC' },
      { time: 200, title: 'dvc init & dvc add' },
      { time: 350, title: 'Remote storage' },
      { time: 480, title: 'Pipelines DVC' },
    ],
  },
  {
    moduleId: 'deployment-api',
    lessonId: 'fastapi-ml',
    title: 'FastAPI pour ML',
    embedUrl: 'https://www.youtube.com/embed/7t2alSnE2-I',
    chapters: [
      { time: 0, title: 'Introduction à FastAPI' },
      { time: 75, title: 'Premier endpoint' },
      { time: 180, title: 'Schémas Pydantic' },
      { time: 300, title: 'Charger un modèle ML' },
      { time: 420, title: 'Endpoint de prédiction' },
    ],
  },
  {
    moduleId: 'deployment-api',
    lessonId: 'cloud-deployment',
    title: 'Déploiement cloud',
    embedUrl: 'https://www.youtube.com/embed/NTkn6_mEdFM',
    chapters: [
      { time: 0, title: 'Aperçu des options cloud' },
      { time: 120, title: 'AWS Deployment' },
      { time: 280, title: 'Google Cloud Run' },
      { time: 400, title: 'Azure Container Instances' },
      { time: 520, title: 'Comparaison et choix' },
    ],
  },
];

export const getVideoByLesson = (moduleId: string, lessonId: string): VideoData | undefined => {
  return videoData.find(v => v.moduleId === moduleId && v.lessonId === lessonId);
};
