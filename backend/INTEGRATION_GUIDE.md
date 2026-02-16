# 🔗 Guide d'Intégration Frontend Lovable ↔️ Backend FastAPI

Ce document explique comment connecter le frontend Lovable au backend FastAPI.

---

## 📋 Étape 1 : Vérifier que le Backend Fonctionne

```bash
# Dans le dossier backend/
python seed_db.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Ou avec Docker
docker-compose up -d

# Tester l'API
python test_api.py
```

✅ Le backend devrait être accessible sur **http://localhost:8000**
✅ La documentation Swagger sur **http://localhost:8000/docs**

---

## 📋 Étape 2 : Configurer le Frontend Lovable

### 2.1 Créer le fichier de configuration API

Dans ton projet Lovable, crée `/src/config/api.ts` :

```typescript
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',
  ENDPOINTS: {
    AUTH: {
      REGISTER: '/api/auth/register',
      LOGIN: '/api/auth/login',
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
      COMPLETE: (id: string) => `/api/lessons/${id}/complete`,
    },
    QUIZ: {
      GET: (id: string) => `/api/quizzes/${id}`,
      SUBMIT: (id: string) => `/api/quizzes/${id}/submit`,
    },
    ADMIN: {
      STATS: '/api/admin/stats',
      USERS: '/api/admin/users',
      ANALYTICS: '/api/admin/analytics',
    },
  },
};
```

### 2.2 Créer le Service d'Authentification

Crée `/src/services/authService.ts` :

```typescript
import { API_CONFIG } from '@/config/api';

export interface LoginCredentials {
  email: string;
  password: string;
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
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await fetch(
      `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.AUTH.LOGIN}`,
      {
        method: 'POST',
        body: formData,
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    const data = await response.json();
    
    // Sauvegarder le token
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  },

  async register(userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
    role?: string;
  }): Promise<User> {
    const response = await fetch(
      `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.AUTH.REGISTER}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }

    return response.json();
  },

  async getCurrentUser(): Promise<User> {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch(
      `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.AUTH.ME}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error('Failed to get current user');
    }

    return response.json();
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
};
```

### 2.3 Créer un Hook Custom pour l'Authentification

Crée `/src/hooks/useAuth.ts` :

```typescript
import { useState, useEffect } from 'react';
import { authService, User, LoginCredentials } from '@/services/authService';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
        } catch (error) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
        }
      }
      setIsLoading(false);
    };

    loadUser();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    const response = await authService.login(credentials);
    setUser(response.user);
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    logout,
  };
}
```

### 2.4 Créer le Service pour les Modules

Crée `/src/services/moduleService.ts` :

```typescript
import { API_CONFIG } from '@/config/api';

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

export interface Lesson {
  id: string;
  title: string;
  type: 'video' | 'text' | 'quiz' | 'practice';
  duration: string;
  completed: boolean;
  url?: string;
  content?: string;
}

const getAuthHeader = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
};

export const moduleService = {
  async getAll(): Promise<Module[]> {
    const response = await fetch(
      `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.MODULES.LIST}`,
      { headers: getAuthHeader() }
    );

    if (!response.ok) {
      throw new Error('Failed to fetch modules');
    }

    return response.json();
  },

  async getById(id: string): Promise<Module> {
    const response = await fetch(
      `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.MODULES.GET(id)}`,
      { headers: getAuthHeader() }
    );

    if (!response.ok) {
      throw new Error('Failed to fetch module');
    }

    return response.json();
  },

  async completeLesson(lessonId: string): Promise<void> {
    const response = await fetch(
      `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.LESSONS.COMPLETE(lessonId)}`,
      {
        method: 'POST',
        headers: getAuthHeader(),
      }
    );

    if (!response.ok) {
      throw new Error('Failed to complete lesson');
    }
  },
};
```

---

## 📋 Étape 3 : Modifier les Composants Existants

### 3.1 Page de Login

```tsx
import { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate } from 'react-router-dom';

export function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await login({ email, password });
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}
      
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      
      <button type="submit">Se connecter</button>
    </form>
  );
}
```

### 3.2 Liste des Modules

```tsx
import { useEffect, useState } from 'react';
import { moduleService, Module } from '@/services/moduleService';

export function ModulesList() {
  const [modules, setModules] = useState<Module[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadModules = async () => {
      try {
        const data = await moduleService.getAll();
        setModules(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    loadModules();
  }, []);

  if (isLoading) return <div>Chargement...</div>;
  if (error) return <div>Erreur: {error}</div>;

  return (
    <div className="modules-list">
      {modules.map((module) => (
        <div key={module.id} className="module-card">
          <h3>{module.title}</h3>
          <p>{module.description}</p>
          <div>Semaine {module.week}</div>
          <div>{module.lessons.length} leçons</div>
          <div>Progression: {module.completion_rate}%</div>
        </div>
      ))}
    </div>
  );
}
```

---

## 📋 Étape 4 : Tester l'Intégration

### 4.1 Comptes de Test

Utilise ces credentials pour tester :

**Admin:**
- Email: `admin@didacticiel.com`
- Password: `Admin123!`

**Étudiant:**
- Email: `jean.martin@student.com`
- Password: `Student123!`

### 4.2 Checklist de Test

- [ ] La page de login affiche le formulaire
- [ ] La connexion avec les credentials admin fonctionne
- [ ] Le token est sauvegardé dans localStorage
- [ ] La redirection vers le dashboard fonctionne
- [ ] Les modules s'affichent correctement
- [ ] Les leçons peuvent être complétées
- [ ] La déconnexion nettoie le localStorage

---

## 🐛 Troubleshooting

### Erreur CORS

Si tu vois une erreur CORS dans la console :

```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Solution:** Le backend est déjà configuré pour accepter CORS depuis `http://localhost:5173`. Redémarre le backend.

### Token expiré

Si tu vois "Unauthorized" après quelques jours :

**Solution:** Le token JWT expire après 7 jours. Reconnecte-toi.

### Cannot connect to backend

```
TypeError: Failed to fetch
```

**Solution:** Vérifie que le backend tourne sur `http://localhost:8000`

```bash
# Vérifier que le backend est démarré
curl http://localhost:8000/health
```

---

## 📊 Données Disponibles

Après `seed_db.py`, tu as :

- **4 modules** (DevOps Basics, MLOps Fundamentals, Deployment & API, Advanced MLOps)
- **12+ leçons** (vidéos et textes)
- **1 quiz** complet avec questions
- **15 utilisateurs** (2 admins, 3 formateurs, 10+ étudiants)

---

## 🚀 Prochaines Étapes

1. ✅ Créer les services pour tous les endpoints (quiz, admin, etc.)
2. ✅ Ajouter la gestion d'erreurs globale
3. ✅ Implémenter le refresh automatique du token
4. ✅ Ajouter des loading states partout
5. ✅ Créer un interceptor pour gérer les erreurs 401
6. ✅ Implémenter le dashboard admin avec stats réelles

---

## 📚 Ressources

- **API Documentation:** http://localhost:8000/docs
- **API Reference:** Voir `API_REFERENCE.md`
- **Quick Start:** Voir `QUICKSTART.md`

Bon développement ! 🎉
