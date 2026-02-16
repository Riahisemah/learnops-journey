import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import type { User } from "@/data/mock-users";
import { API_CONFIG } from "@/config/api";

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  register: (data: RegisterData) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
}

export interface RegisterData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  role: "student" | "instructor" | "admin";
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_KEY = "auth-token";

/* ---------------------------------------------------- */
/* Helper: Fetch with Auth Header */
/* ---------------------------------------------------- */
async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem(TOKEN_KEY);

  const res = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  // Handle empty responses
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    throw new Error(data?.detail || "API Error");
  }

  return data;
}

/* ---------------------------------------------------- */
/* Provider */
/* ---------------------------------------------------- */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /* ---------------------------------------------------- */
  /* Load user on app start */
  /* ---------------------------------------------------- */
  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem(TOKEN_KEY);
      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        const data = await apiFetch(API_CONFIG.ENDPOINTS.AUTH.ME);
        setUser(data);
      } catch {
        localStorage.removeItem(TOKEN_KEY);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    loadUser();
  }, []);

  /* ---------------------------------------------------- */
  /* Login - FIXED for OAuth2PasswordRequestForm */
  /* ---------------------------------------------------- */
  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    try {
      // OAuth2PasswordRequestForm expects form-urlencoded with 'username' field
      const formData = new URLSearchParams();
      formData.append('username', email);  // Must be 'username', not 'email'
      formData.append('password', password);

      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.AUTH.LOGIN}`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      // The response includes access_token, token_type, and user
      localStorage.setItem(TOKEN_KEY, data.access_token);
      setUser(data.user);

      return { success: true };
    } catch (error: any) {
      console.error('Login error:', error);
      return { success: false, error: error.message };
    } finally {
      setIsLoading(false);
    }
  }, []);

  /* ---------------------------------------------------- */
  /* Register - FIXED with proper data transformation */
  /* ---------------------------------------------------- */
  const register = useCallback(async (data: RegisterData) => {
    setIsLoading(true);
    try {
      // Transform camelCase to snake_case as expected by backend
      const backendData = {
        email: data.email,
        password: data.password,
        first_name: data.first_name,  // Transform
        last_name: data.last_name,     // Transform
        role: data.role               // Already correct format
      };

      console.log('Sending registration data:', backendData);

      // Register the user - endpoint returns UserResponse, not Token
      const userData = await apiFetch(API_CONFIG.ENDPOINTS.AUTH.REGISTER, {
        method: "POST",
        body: JSON.stringify(backendData),
      });

      console.log('Registration successful:', userData);

      // Automatically log in after successful registration
      const loginResult = await login(data.email, data.password);
      
      if (!loginResult.success) {
        return { success: false, error: "Registration succeeded but auto-login failed. Please try logging in manually." };
      }

      return { success: true };
    } catch (error: any) {
      console.error('Registration error:', error);
      return { success: false, error: error.message };
    } finally {
      setIsLoading(false);
    }
  }, [login]);

  /* ---------------------------------------------------- */
  /* Logout */
  /* ---------------------------------------------------- */
  const logout = useCallback(async () => {
    try {
      // Your backend might not have a logout endpoint
      await apiFetch(API_CONFIG.ENDPOINTS.AUTH.LOGOUT, {
        method: "POST",
      }).catch(() => {
        // Ignore errors if endpoint doesn't exist
      });
    } finally {
      localStorage.removeItem(TOKEN_KEY);
      setUser(null);
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

/* ---------------------------------------------------- */
/* Hook */
/* ---------------------------------------------------- */
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}