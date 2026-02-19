import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { authService, type RegisterData as ApiRegisterData, type User as ApiUser } from "@/services/authService";
import { userService } from "@/services/userService";

export interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  role: "student" | "instructor" | "admin";
  status: "active" | "blocked";
  createdAt: string;
  lastLogin: string;
  progression: number;
  modulesCompleted: (string | number)[];
  badges: string[];
  avatar: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  register: (data: RegisterData) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  updateUser: (data: Partial<User>) => void;
  refreshUser: () => Promise<void>;
}

export interface RegisterData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  role: "student" | "instructor" | "admin";
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const CURRENT_USER_KEY = "devops-mlops-current-user";

function mapApiUserToLocal(apiUser: any): User {
  return {
    id: apiUser.id,
    first_name: apiUser.first_name || "",
    last_name: apiUser.last_name || "",
    email: apiUser.email,
    role: apiUser.role || "student",
    status: apiUser.is_active === false ? "blocked" : "active",
    createdAt: apiUser.created_at || apiUser.createdAt || new Date().toISOString(),
    lastLogin: apiUser.last_login || apiUser.lastLogin || new Date().toISOString(),
    progression: apiUser.progression || 0,
    modulesCompleted: apiUser.modules_completed || apiUser.modulesCompleted || [],
    badges: apiUser.badges || [],
    avatar: apiUser.avatar || "",
  };
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    const stored = localStorage.getItem(CURRENT_USER_KEY);
    if (stored) {
      try { return JSON.parse(stored); } catch { /* fallthrough */ }
    }
    return null;
  });
  const [isLoading, setIsLoading] = useState(false);

  // Try to restore session from API on mount
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    authService.getCurrentUser()
      .then(apiUser => {
        const mapped = mapApiUserToLocal(apiUser);
        setUser(mapped);
        localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(mapped));
      })
      .catch(() => {
        localStorage.removeItem("access_token");
        localStorage.removeItem(CURRENT_USER_KEY);
        setUser(null);
      });
  }, []);

  // Persist current user to localStorage
  useEffect(() => {
    if (user) {
      localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(user));
    } else {
      localStorage.removeItem(CURRENT_USER_KEY);
    }
  }, [user]);

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await authService.login({ email, password });
      const mapped = mapApiUserToLocal(response.user);
      setUser(mapped);
      return { success: true };
    } catch (error: any) {
      const detail = error?.response?.data?.detail;
      return { success: false, error: detail || "Identifiants incorrects" };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = useCallback(async (data: RegisterData) => {
    setIsLoading(true);
    try {
      const apiData: ApiRegisterData = {
        email: data.email,
        password: data.password,
        first_name: data.first_name,
        last_name: data.last_name,
        role: data.role,
      };
      await authService.register(apiData);
      const loginResponse = await authService.login({ email: data.email, password: data.password });
      const mapped = mapApiUserToLocal(loginResponse.user);
      setUser(mapped);
      return { success: true };
    } catch (error: any) {
      const detail = error?.response?.data?.detail;
      return { success: false, error: detail || "Erreur lors de l'inscription" };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    localStorage.removeItem(CURRENT_USER_KEY);
  }, []);

  const updateUser = useCallback((data: Partial<User>) => {
    setUser(prev => {
      if (!prev) return null;
      const updated = { ...prev, ...data };
      userService.update(prev.id, {
        first_name: updated.first_name,
        last_name: updated.last_name,
        avatar: updated.avatar,
      }).catch(console.error);
      return updated;
    });
  }, []);

  const refreshUser = useCallback(async () => {
    try {
      const apiUser = await authService.getCurrentUser();
      const mapped = mapApiUserToLocal(apiUser);
      setUser(mapped);
    } catch {
      // Silently fail
    }
  }, []);

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      register,
      logout,
      updateUser,
      refreshUser,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
