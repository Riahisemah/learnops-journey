# 📡 Backend Endpoints — État de l'intégration Frontend

> URL de base : `http://localhost:8000` (configurable via `VITE_API_URL`)
> Mode : **Hybride** — API d'abord, fallback localStorage si backend indisponible.

---

## 🔌 Statut de connexion

| Composant | Source de données | Fallback |
|-----------|-------------------|----------|
| `AuthContext` | `authService` → API | localStorage + mock-users |
| `Home` / Modules | `moduleService.getAll()` direct | Erreur console |
| `ModulePage` | `course-data.ts` local | ❌ Pas d'API |
| `AdminOverview` | `useAuth().users` + mock | ❌ Pas d'API |
| `AdminAnalytics` | Données hardcodées | ❌ Pas d'API |
| `AdminUsers` | `AuthContext.users` | localStorage |
| `QuizSystem` | `quiz-data.ts` local | ❌ Pas d'API |
| `ML Predict` | Non connecté | ❌ Pas d'API |

---

## 🔐 Authentification (4 endpoints)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| POST | `/api/auth/register` | RegisterPage | `authService.register()` | ✅ Connecté (hybride) |
| POST | `/api/auth/login` | LoginPage | `authService.login()` | ✅ Connecté (hybride) |
| GET | `/api/auth/me` | AuthContext | `authService.getCurrentUser()` | ✅ Connecté |
| POST | `/api/auth/forgot-password` | ForgotPasswordPage | `authService.forgotPassword()` | ✅ Connecté |

---

## 👥 Utilisateurs (5 endpoints)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| GET | `/api/users` | AdminUsers | `userService.getAll()` | ⚠️ Service prêt, UI utilise localStorage |
| GET | `/api/users/{id}` | — | `userService.getById()` | 🔧 Service prêt |
| PUT | `/api/users/{id}` | AuthContext | `userService.update()` | ✅ Connecté (background) |
| DELETE | `/api/users/{id}` | AdminUsers | `userService.delete()` | 🔧 Service prêt |
| GET | `/api/users/{id}/progression` | — | `userService.getProgression()` | 🔧 Service prêt |

---

## 📚 Modules (6 endpoints)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| GET | `/api/modules` | Home | `moduleService.getAll()` | ⚠️ Appelé directement (pas via hook RQ) |
| GET | `/api/modules/{id}` | ModulePage | `useModule(id)` hook prêt | ❌ Page utilise `course-data.ts` local |
| POST | `/api/modules` | AdminModules | `moduleService.create()` | 🔧 Service prêt |
| PUT | `/api/modules/{id}` | AdminModules | `moduleService.update()` | 🔧 Service prêt |
| DELETE | `/api/modules/{id}` | AdminModules | `moduleService.delete()` | 🔧 Service prêt |
| GET | `/api/modules/{id}/lessons` | LessonPage | `moduleService.getLessons()` | 🔧 Service prêt |

---

## 📖 Leçons (1 endpoint)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| POST | `/api/lessons/{id}/complete` | LessonPage | `useCompleteLesson()` | 🔧 Hook prêt, non appelé dans UI |

---

## ❓ Quiz (3 endpoints)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| GET | `/api/quizzes/{id}` | QuizSystem | `useQuiz(id)` | 🔧 Hook prêt, composant utilise props locales |
| POST | `/api/quizzes/{id}/submit` | QuizSystem | `useSubmitQuiz()` | 🔧 Hook prêt, composant gère en local |
| GET | `/api/quizzes/{id}/results/{attemptId}` | — | `quizService.getResults()` | 🔧 Service prêt |

---

## 📊 Progression (2 endpoints)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| GET | `/api/progress/me` | DashboardPage | — | ❌ Non implémenté |
| POST | `/api/progress/update` | — | — | ❌ Non implémenté |

---

## 🛡️ Admin (3 endpoints)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| GET | `/api/admin/stats` | AdminOverview | `useAdminStats()` hook prêt | ❌ Page utilise mock local |
| GET | `/api/admin/users` | AdminUsers | `adminService.getUsers()` | ❌ Page utilise AuthContext.users |
| GET | `/api/admin/analytics` | AdminAnalytics | `useAdminAnalytics()` hook prêt | ❌ Page utilise données hardcodées |

---

## 🤖 Machine Learning (1 endpoint)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| POST | `/api/ml/predict` | MLDashboard | `usePredict()` | 🔧 Hook prêt, non vérifié dans UI |

---

## 📋 Légende

| Icône | Signification |
|-------|---------------|
| ✅ | Connecté — appel API avec fallback automatique |
| ⚠️ | Partiellement connecté — service appelé mais pas via hook React Query |
| 🔧 | Service/Hook prêt — code écrit mais pas encore utilisé dans l'UI |
| ❌ | Non connecté — page utilise données locales/mock |

---

## 🚀 Travail restant

1. **ModulePage** : Remplacer `getModuleById()` local par le hook `useModule(id)`
2. **AdminOverview** : Remplacer mock par `useAdminStats()` + `useAdminAnalytics()`
3. **AdminUsers** : Remplacer `AuthContext.users` par `adminService.getUsers()`
4. **QuizSystem** : Intégrer `useQuiz()` et `useSubmitQuiz()` dans le composant
5. **Progression** : Créer `progressService.ts` + hook + connecter DashboardPage
6. **Home.tsx** : Migrer `moduleService.getAll()` direct vers hook `useModules()`

---

## ⚙️ Configuration

```bash
# .env (racine du projet frontend)
VITE_API_URL=http://localhost:8000
```

Le mode hybride vérifie la disponibilité du backend au démarrage via `HEAD /docs`. Si le backend ne répond pas sous 3 secondes, toutes les fonctionnalités passent en mode localStorage.
