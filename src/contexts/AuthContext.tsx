import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { mockUsers, type User } from "@/data/mock-users";
import { authService, type LoginCredentials, type RegisterData as ApiRegisterData } from "@/services/authService";
import { userService } from "@/services/userService";
import { adminService } from "@/services/adminService";

interface AuthContextType {
  user: User | null;
  users: User[];
  isAuthenticated: boolean;
  isLoading: boolean;
  isBackendAvailable: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  register: (data: RegisterData) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  updateUser: (data: Partial<User>) => void;
  updateUserById: (id: string, data: Partial<User>) => void;
  deleteUser: (id: string) => void;
  addUser: (data: Omit<User, "id" | "createdAt" | "lastLogin">) => void;
  getAllUsers: () => User[];
  refreshUser: () => Promise<void>;
}

export interface RegisterData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  role: "student" | "instructor" | "admin";
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const USERS_KEY = "devops-mlops-users";
const CURRENT_USER_KEY = "devops-mlops-current-user";
const BACKEND_STATUS_KEY = "devops-mlops-backend-status";

function getStoredUsers(): User[] {
  const stored = localStorage.getItem(USERS_KEY);
  if (stored) {
    try { return JSON.parse(stored); } catch { /* fallthrough */ }
  }
  localStorage.setItem(USERS_KEY, JSON.stringify(mockUsers));
  return [...mockUsers];
}

// Helper to check if backend is reachable
async function checkBackend(): Promise<boolean> {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/docs`,
      { method: 'HEAD', signal: AbortSignal.timeout(3000) }
    );
    return response.ok;
  } catch {
    return false;
  }
}

// Map API user to local User type
function mapApiUserToLocal(apiUser: any): User {
  return {
    id: apiUser.id,
    firstName: apiUser.first_name || apiUser.firstName || "",
    lastName: apiUser.last_name || apiUser.lastName || "",
    email: apiUser.email,
    password: "",
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
  const [users, setUsers] = useState<User[]>(getStoredUsers);
  const [user, setUser] = useState<User | null>(() => {
    const stored = localStorage.getItem(CURRENT_USER_KEY);
    if (stored) {
      try { return JSON.parse(stored); } catch { /* fallthrough */ }
    }
    return null;
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isBackendAvailable, setIsBackendAvailable] = useState(false);

  // Check backend availability on mount
  useEffect(() => {
    checkBackend().then(available => {
      setIsBackendAvailable(available);
      localStorage.setItem(BACKEND_STATUS_KEY, String(available));
      if (available) {
        console.log("✅ Backend API connecté");
      } else {
        console.log("⚠️ Backend non disponible — mode localStorage activé");
      }
    });
  }, []);

  // Try to restore session from API if backend is available
  useEffect(() => {
    if (!isBackendAvailable) return;
    const token = localStorage.getItem("access_token");
    if (!token) return;

    authService.getCurrentUser()
      .then(apiUser => {
        const mapped = mapApiUserToLocal(apiUser);
        setUser(mapped);
      })
      .catch(() => {
        // Token expired or invalid — keep localStorage user
        localStorage.removeItem("access_token");
      });
  }, [isBackendAvailable]);

  useEffect(() => {
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
  }, [users]);

  useEffect(() => {
    if (user) {
      localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(user));
    } else {
      localStorage.removeItem(CURRENT_USER_KEY);
    }
  }, [user]);

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);

    // Try API first if backend is available
    if (isBackendAvailable) {
      try {
        const response = await authService.login({ email, password });
        const mapped = mapApiUserToLocal(response.user);
        setUser(mapped);
        setIsLoading(false);
        return { success: true };
      } catch (error: any) {
        const detail = error?.response?.data?.detail;
        // If it's a real auth error from the backend, don't fallback
        if (error?.response?.status === 401 || error?.response?.status === 400) {
          setIsLoading(false);
          return { success: false, error: detail || "Identifiants incorrects" };
        }
        // Network error — fall through to localStorage
        console.warn("Backend login failed, falling back to localStorage");
      }
    }

    // Fallback: localStorage
    await new Promise(r => setTimeout(r, 400));
    const found = users.find(u => u.email === email.toLowerCase());
    if (!found) {
      setIsLoading(false);
      return { success: false, error: "Aucun compte trouvé avec cet email" };
    }
    if (found.password !== password) {
      setIsLoading(false);
      return { success: false, error: "Mot de passe incorrect" };
    }
    if (found.status === "blocked") {
      setIsLoading(false);
      return { success: false, error: "Ce compte a été bloqué" };
    }
    const updated = { ...found, lastLogin: new Date().toISOString() };
    setUsers(prev => prev.map(u => u.id === found.id ? updated : u));
    setUser(updated);
    setIsLoading(false);
    return { success: true };
  }, [users, isBackendAvailable]);

  const register = useCallback(async (data: RegisterData) => {
    setIsLoading(true);

    // Try API first
    if (isBackendAvailable) {
      try {
        const apiData: ApiRegisterData = {
          email: data.email,
          password: data.password,
          first_name: data.firstName,
          last_name: data.lastName,
          role: data.role,
        };
        await authService.register(apiData);
        // Auto-login after registration
        const loginResponse = await authService.login({ email: data.email, password: data.password });
        const mapped = mapApiUserToLocal(loginResponse.user);
        setUser(mapped);
        setIsLoading(false);
        return { success: true };
      } catch (error: any) {
        const detail = error?.response?.data?.detail;
        if (error?.response?.status === 400 || error?.response?.status === 409) {
          setIsLoading(false);
          return { success: false, error: detail || "Erreur lors de l'inscription" };
        }
        console.warn("Backend register failed, falling back to localStorage");
      }
    }

    // Fallback: localStorage
    await new Promise(r => setTimeout(r, 400));
    const exists = users.find(u => u.email === data.email.toLowerCase());
    if (exists) {
      setIsLoading(false);
      return { success: false, error: "Un compte existe déjà avec cet email" };
    }
    const newUser: User = {
      id: crypto.randomUUID(),
      firstName: data.firstName,
      lastName: data.lastName,
      email: data.email.toLowerCase(),
      password: data.password,
      role: data.role,
      status: "active",
      createdAt: new Date().toISOString(),
      lastLogin: new Date().toISOString(),
      progression: 0,
      modulesCompleted: [],
      badges: [],
      avatar: "",
    };
    setUsers(prev => [...prev, newUser]);
    setUser(newUser);
    setIsLoading(false);
    return { success: true };
  }, [users, isBackendAvailable]);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
  }, []);

  const updateUser = useCallback((data: Partial<User>) => {
    setUser(prev => {
      if (!prev) return null;
      const updated = { ...prev, ...data };
      setUsers(us => us.map(u => u.id === prev.id ? updated : u));

      // Try API update in background
      if (localStorage.getItem(BACKEND_STATUS_KEY) === "true") {
        userService.update(prev.id, {
          first_name: updated.firstName,
          last_name: updated.lastName,
          avatar: updated.avatar,
        }).catch(() => {});
      }

      return updated;
    });
  }, []);

  const updateUserById = useCallback((id: string, data: Partial<User>) => {
    setUsers(prev => prev.map(u => u.id === id ? { ...u, ...data } : u));

    if (localStorage.getItem(BACKEND_STATUS_KEY) === "true") {
      userService.update(id, {
        first_name: data.firstName,
        last_name: data.lastName,
        avatar: data.avatar,
      }).catch(() => {});
    }
  }, []);

  const deleteUser = useCallback((id: string) => {
    setUsers(prev => prev.filter(u => u.id !== id));
    if (user?.id === id) setUser(null);

    if (localStorage.getItem(BACKEND_STATUS_KEY) === "true") {
      userService.delete(id).catch(() => {});
    }
  }, [user]);

  const addUser = useCallback((data: Omit<User, "id" | "createdAt" | "lastLogin">) => {
    const newUser: User = {
      ...data,
      id: crypto.randomUUID(),
      createdAt: new Date().toISOString(),
      lastLogin: new Date().toISOString(),
    };
    setUsers(prev => [...prev, newUser]);
  }, []);

  const getAllUsers = useCallback(() => users, [users]);

  const refreshUser = useCallback(async () => {
    if (!isBackendAvailable) return;
    try {
      const apiUser = await authService.getCurrentUser();
      const mapped = mapApiUserToLocal(apiUser);
      setUser(mapped);
    } catch {
      // Silently fail
    }
  }, [isBackendAvailable]);

  return (
    <AuthContext.Provider value={{
      user,
      users,
      isAuthenticated: !!user,
      isLoading,
      isBackendAvailable,
      login,
      register,
      logout,
      updateUser,
      updateUserById,
      deleteUser,
      addUser,
      getAllUsers,
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
