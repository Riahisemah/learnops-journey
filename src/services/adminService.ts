import httpClient from './httpClient';
import { API_CONFIG } from '@/config/api';

export interface AdminStats {
  total_users: number;
  total_modules: number;
  total_completions: number;
  average_rating: number;
  users_growth: number;
  completions_rate: number;
}

export interface UserFilters {
  role?: 'student' | 'instructor' | 'admin';
  is_active?: boolean;
  search?: string;
}

export interface Analytics {
  registrations_per_day: { date: string; count: number }[];
  popular_modules: { module_id: string; title: string; views: number }[];
  user_roles: { role: string; count: number }[];
  recent_activity: { user: string; action: string; timestamp: string }[];
}

export const adminService = {
  getStats: async (): Promise<AdminStats> => {
    const response = await httpClient.get<AdminStats>(API_CONFIG.ENDPOINTS.ADMIN.STATS);
    return response.data;
  },

  getUsers: async (filters?: UserFilters): Promise<any[]> => {
    const response = await httpClient.get(API_CONFIG.ENDPOINTS.ADMIN.USERS, { params: filters });
    return response.data;
  },

  getAnalytics: async (): Promise<Analytics> => {
    const response = await httpClient.get<Analytics>(API_CONFIG.ENDPOINTS.ADMIN.ANALYTICS);
    return response.data;
  },
};
