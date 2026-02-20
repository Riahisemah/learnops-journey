import httpClient from './httpClient';
import { API_CONFIG } from '@/config/api';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role?: 'student' | 'instructor' | 'admin';
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'student' | 'instructor' | 'admin';
  is_active: boolean;
  created_at: string;
  last_login: string | null;
  avatar?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const authService = {
  register: async (data: RegisterData): Promise<User> => {
    const response = await httpClient.post<User>(API_CONFIG.ENDPOINTS.AUTH.REGISTER, data);
    return response.data;
  },

  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await httpClient.post<AuthResponse>(
      API_CONFIG.ENDPOINTS.AUTH.LOGIN,  
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );

    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await httpClient.get<User>(API_CONFIG.ENDPOINTS.AUTH.ME);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  },

  forgotPassword: async (email: string): Promise<{ message: string }> => {
    const response = await httpClient.post(API_CONFIG.ENDPOINTS.AUTH.FORGOT_PASSWORD, { email });
    return response.data;
  },
};
