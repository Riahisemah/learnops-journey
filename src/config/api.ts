// Configuration de l'API Backend
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  ENDPOINTS: {
    AUTH: {
      REGISTER: '/api/auth/register',
      LOGIN: '/api/auth/login',
      LOGOUT: '/api/auth/logout',
      ME: '/api/auth/me',
      FORGOT_PASSWORD: '/api/auth/forgot-password',
    },
    USERS: {
      LIST: '/api/users',
      GET: (id: string) => `/api/users/${id}`,
      UPDATE: (id: string) => `/api/users/${id}`,
      DELETE: (id: string) => `/api/users/${id}`,
      PROGRESSION: (id: string) => `/api/users/${id}/progression`,
    },
    MODULES: {
      LIST: '/api/modules',
      GET: (id: string) => `/api/modules/${id}`,
      CREATE: '/api/modules',
      UPDATE: (id: string) => `/api/modules/${id}`,
      DELETE: (id: string) => `/api/modules/${id}`,
    },
    LESSONS: {
      LIST: (moduleId: string) => `/api/modules/${moduleId}/lessons`,
      GET: (moduleId: string, lessonId: string) => `/api/modules/${moduleId}/lessons/${lessonId}`,
      CONTENT: (moduleId: string, lessonId: string) => `/api/modules/${moduleId}/lessons/${lessonId}/content`,
      COMPLETE: (lessonId: string) => `/api/lessons/${lessonId}/complete`,
      PROGRESS: (lessonId: string) => `/api/lessons/${lessonId}/progress`,
    },
    QUIZ: {
      GET: (id: string) => `/api/quizzes/${id}`,
      SUBMIT: (id: string) => `/api/quizzes/${id}/submit`,
      RESULTS: (quizId: string, attemptId: string) => `/api/quizzes/${quizId}/results/${attemptId}`,
    },
    PROGRESS: {
      ME: '/api/progress/me',
      UPDATE: '/api/progress/update',
    },
    ADMIN: {
      STATS: '/api/admin/stats',
      USERS: '/api/admin/users',
      ANALYTICS: '/api/admin/analytics',
    },
    ML: {
      PREDICT: '/api/ml/predict',
    },
  },
  TIMEOUT: 30000,
};
