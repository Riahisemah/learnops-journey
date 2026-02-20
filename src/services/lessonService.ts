import httpClient from './httpClient';

export interface Lesson {
  id: string;
  title: string;
  type: 'video' | 'text' | 'quiz' | 'practice';
  duration: number;
  description: string;
  completed?: boolean;
  url?: string;
  content?: string;
}

export interface LessonContent {
  moduleId: string;
  lessonId: string;
  theory: {
    title: string;
    content: string;
    codeBlocks?: { language: string; code: string }[];
  };
  practice: {
    title: string;
    content: string;
    codeBlocks?: { language: string; code: string }[];
  };
}

export const lessonService = {
  // Récupérer toutes les leçons d'un module
  getLessonsByModule: async (moduleId: string): Promise<Lesson[]> => {
    const response = await httpClient.get<Lesson[]>(`/api/modules/${moduleId}/lessons`);
    return response.data;
  },

  // Récupérer une leçon spécifique
  getLessonById: async (moduleId: string, lessonId: string): Promise<Lesson> => {
    const response = await httpClient.get<Lesson>(`/api/modules/${moduleId}/lessons/${lessonId}`);
    return response.data;
  },

  // Récupérer le contenu d'une leçon
  getLessonContent: async (moduleId: string, lessonId: string): Promise<LessonContent> => {
    const response = await httpClient.get<LessonContent>(`/api/modules/${moduleId}/lessons/${lessonId}/content`);
    return response.data;
  },

  // Marquer une leçon comme complétée
  completeLesson: async (lessonId: string): Promise<void> => {
    await httpClient.post(`/api/lessons/${lessonId}/complete`);
  },

  // Vérifier si une leçon est complétée
  isLessonCompleted: async (lessonId: string): Promise<boolean> => {
    const response = await httpClient.get<{ completed: boolean }>(`/api/lessons/${lessonId}/status`);
    return response.data.completed;
  }
};