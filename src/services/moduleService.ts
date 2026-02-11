import httpClient from './httpClient';
import { API_CONFIG } from '@/config/api';

export interface Lesson {
  id: string;
  title: string;
  type: 'video' | 'text' | 'quiz' | 'practice';
  duration: string;
  completed: boolean;
  url?: string;
  content?: string;
}

export interface Module {
  id: string;
  title: string;
  description: string;
  week: number;
  order: number;
  lessons: Lesson[];
  completion_rate: number;
  total_duration: number;
}

export interface CreateModuleData {
  title: string;
  description: string;
  week: number;
  order: number;
}

export const moduleService = {
  getAll: async (): Promise<Module[]> => {
    const response = await httpClient.get<Module[]>(API_CONFIG.ENDPOINTS.MODULES.LIST);
    return response.data;
  },

  getById: async (id: string): Promise<Module> => {
    const response = await httpClient.get<Module>(API_CONFIG.ENDPOINTS.MODULES.GET(id));
    return response.data;
  },

  create: async (data: CreateModuleData): Promise<Module> => {
    const response = await httpClient.post<Module>(API_CONFIG.ENDPOINTS.MODULES.CREATE, data);
    return response.data;
  },

  update: async (id: string, data: Partial<CreateModuleData>): Promise<Module> => {
    const response = await httpClient.put<Module>(API_CONFIG.ENDPOINTS.MODULES.UPDATE(id), data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await httpClient.delete(API_CONFIG.ENDPOINTS.MODULES.DELETE(id));
  },

  getLessons: async (moduleId: string): Promise<Lesson[]> => {
    const response = await httpClient.get<Lesson[]>(API_CONFIG.ENDPOINTS.LESSONS.LIST(moduleId));
    return response.data;
  },

  completeLesson: async (lessonId: string): Promise<void> => {
    await httpClient.post(API_CONFIG.ENDPOINTS.LESSONS.COMPLETE(lessonId));
  },
};
