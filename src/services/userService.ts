import httpClient from './httpClient';
import { API_CONFIG } from '@/config/api';
import { User } from './authService';

export interface UpdateUserData {
  first_name?: string;
  last_name?: string;
  avatar?: string;
}

export interface UserProgression {
  user_id: string;
  progression: number;
  modules_completed: number[];
  badges: string[];
  time_spent: number;
}

export const userService = {
  getAll: async (): Promise<User[]> => {
    const response = await httpClient.get<User[]>(API_CONFIG.ENDPOINTS.USERS.LIST);
    return response.data;
  },

  getById: async (id: string): Promise<User> => {
    const response = await httpClient.get<User>(API_CONFIG.ENDPOINTS.USERS.GET(id));
    return response.data;
  },

  update: async (id: string, data: UpdateUserData): Promise<User> => {
    const response = await httpClient.put<User>(API_CONFIG.ENDPOINTS.USERS.UPDATE(id), data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await httpClient.delete(API_CONFIG.ENDPOINTS.USERS.DELETE(id));
  },

  getProgression: async (id: string): Promise<UserProgression> => {
    const response = await httpClient.get<UserProgression>(API_CONFIG.ENDPOINTS.USERS.PROGRESSION(id));
    return response.data;
  },
};
