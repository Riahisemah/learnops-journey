import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { mockUsers, type User } from "@/data/mock-users";

interface AuthContextType {
  user: User | null;
  users: User[];
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  register: (data: RegisterData) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  updateUser: (data: Partial<User>) => void;
  updateUserById: (id: string, data: Partial<User>) => void;
  deleteUser: (id: string) => void;
  addUser: (data: Omit<User, "id" | "createdAt" | "lastLogin">) => void;
  getAllUsers: () => User[];
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

function getStoredUsers(): User[] {
  const stored = localStorage.getItem(USERS_KEY);
  if (stored) {
    try { return JSON.parse(stored); } catch { /* fallthrough */ }
  }
  localStorage.setItem(USERS_KEY, JSON.stringify(mockUsers));
  return [...mockUsers];
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
    await new Promise(r => setTimeout(r, 600));
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
  }, [users]);

  const register = useCallback(async (data: RegisterData) => {
    setIsLoading(true);
    await new Promise(r => setTimeout(r, 600));
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
  }, [users]);

  const logout = useCallback(() => {
    setUser(null);
  }, []);

  const updateUser = useCallback((data: Partial<User>) => {
    setUser(prev => {
      if (!prev) return null;
      const updated = { ...prev, ...data };
      setUsers(us => us.map(u => u.id === prev.id ? updated : u));
      return updated;
    });
  }, []);

  const updateUserById = useCallback((id: string, data: Partial<User>) => {
    setUsers(prev => prev.map(u => u.id === id ? { ...u, ...data } : u));
  }, []);

  const deleteUser = useCallback((id: string) => {
    setUsers(prev => prev.filter(u => u.id !== id));
    if (user?.id === id) setUser(null);
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

  return (
    <AuthContext.Provider value={{
      user,
      users,
      isAuthenticated: !!user,
      isLoading,
      login,
      register,
      logout,
      updateUser,
      updateUserById,
      deleteUser,
      addUser,
      getAllUsers,
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
