# 📡 Backend Endpoints — État de l'intégration Frontend

> URL de base : `http://localhost:8000` (configurable via `VITE_API_URL`)
> Mode : **Hybride** — API d'abord, fallback localStorage si backend indisponible.

---

## 🔌 Statut de connexion

| Composant | Source de données | Fallback |
|-----------|-------------------|----------|
| `AuthContext` | `authService` → API | localStorage + mock-users |
| `Home` / Modules | `useModules()` hook | `course-data.ts` local |
| `AdminOverview` | `useAdminStats()` | Calcul depuis mock-users |
| `AdminAnalytics` | `useAdminAnalytics()` | Données générées localement |
| `AdminUsers` | `AuthContext.users` | localStorage |
| `Quiz` | `useQuiz()` / `useSubmitQuiz()` | `quiz-data.ts` local |
| `ML Predict` | `usePredict()` | Résultat simulé |

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
| GET | `/api/users` | AdminUsers | `userService.getAll()` | ⚠️ Fallback localStorage |
| GET | `/api/users/{id}` | — | `userService.getById()` | 🔧 Service prêt |
| PUT | `/api/users/{id}` | AuthContext | `userService.update()` | ✅ Connecté (background) |
| DELETE | `/api/users/{id}` | AdminUsers | `userService.delete()` | ✅ Connecté (background) |
| GET | `/api/users/{id}/progression` | — | `userService.getProgression()` | 🔧 Service prêt |

---

## 📚 Modules (6 endpoints)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| GET | `/api/modules` | Home | `useModules()` | ✅ Connecté (hybride) |
| GET | `/api/modules/{id}` | ModulePage | `useModule(id)` | ✅ Connecté (hybride) |
| POST | `/api/modules` | AdminModules | `moduleService.create()` | 🔧 Service prêt |
| PUT | `/api/modules/{id}` | AdminModules | `moduleService.update()` | 🔧 Service prêt |
| DELETE | `/api/modules/{id}` | AdminModules | `moduleService.delete()` | 🔧 Service prêt |
| GET | `/api/modules/{id}/lessons` | LessonPage | `moduleService.getLessons()` | 🔧 Service prêt |

---

## 📖 Leçons (1 endpoint)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| POST | `/api/lessons/{id}/complete` | LessonPage | `useCompleteLesson()` | ✅ Connecté (hybride) |

---

## ❓ Quiz (3 endpoints)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| GET | `/api/quizzes/{id}` | QuizSystem | `useQuiz(id)` | ✅ Connecté (hybride) |
| POST | `/api/quizzes/{id}/submit` | QuizSystem | `useSubmitQuiz()` | ✅ Connecté (hybride) |
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
| GET | `/api/admin/stats` | AdminOverview | `useAdminStats()` | ✅ Connecté (hybride) |
| GET | `/api/admin/users` | AdminUsers | `adminService.getUsers()` | ⚠️ Fallback localStorage |
| GET | `/api/admin/analytics` | AdminAnalytics | `useAdminAnalytics()` | ✅ Connecté (hybride) |

---

## 🤖 Machine Learning (1 endpoint)

| Méthode | Endpoint | Frontend | Hook/Service | Statut |
|---------|----------|----------|--------------|--------|
| POST | `/api/ml/predict` | MLDashboard | `usePredict()` | ✅ Connecté (hybride) |

---

## 📋 Légende

| Icône | Signification |
|-------|---------------|
| ✅ | Connecté — appel API avec fallback automatique |
| ⚠️ | Partiellement connecté — service prêt, données locales par défaut |
| 🔧 | Service prêt — code écrit mais pas encore appelé dans l'UI |
| ❌ | Non implémenté — endpoint backend existe mais aucun code frontend |

---

## 🚀 Fonctionnalités manquantes à implémenter

1. **`/api/progress/me`** et **`/api/progress/update`** : Créer un `progressService.ts` et un hook `useProgress` connecté à l'API.
2. **CRUD Modules Admin** : Connecter `AdminModules` aux mutations `moduleService.create/update/delete`.
3. **Page profil utilisateur** : Appeler `userService.update()` et `userService.getProgression()`.
4. **Admin Users via API** : Remplacer `AuthContext.users` par `adminService.getUsers()` dans `AdminUsers`.
5. **Résultats Quiz détaillés** : Utiliser `quizService.getResults()` pour afficher l'historique.

---

## ⚙️ Configuration

```bash
# .env (racine du projet frontend)
VITE_API_URL=http://localhost:8000
```

Le mode hybride vérifie la disponibilité du backend au démarrage via `HEAD /docs`. Si le backend ne répond pas sous 3 secondes, toutes les fonctionnalités passent en mode localStorage.
