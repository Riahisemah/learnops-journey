# ✅ Checklist d'Intégration Backend ↔ Frontend

> Dernière mise à jour : 2026-02-16
> Mode : **Hybride** (API first, fallback localStorage)

---

## 🏗️ Infrastructure

- [x] Configuration API (`src/config/api.ts`)
- [x] Client HTTP Axios avec intercepteurs (`src/services/httpClient.ts`)
- [x] Variable d'environnement `VITE_API_URL` (`.env.example`)
- [x] Détection automatique backend disponible (`checkBackend()`)
- [x] Fallback localStorage si backend indisponible
- [ ] Gestion CORS (à configurer côté backend)
- [ ] Rate limiting côté client
- [ ] Retry automatique sur erreurs réseau

---

## 🔐 Authentification

- [x] Service `authService.ts`
- [x] `authService.login()` — form-data pour OAuth2
- [x] `authService.register()` — JSON body
- [x] `authService.getCurrentUser()` — GET /api/auth/me
- [x] `authService.logout()` — clear tokens
- [x] `authService.forgotPassword()` — service prêt
- [x] `AuthContext.tsx` — mode hybride (API → fallback localStorage)
- [x] Stockage JWT dans localStorage (`access_token`)
- [x] Intercepteur auto-injection Bearer token
- [x] Redirection 401 → /login
- [ ] Refresh token (non implémenté côté backend)
- [ ] Remember me (prolonger durée token)
- [ ] Connexion `ForgotPasswordPage` → `authService.forgotPassword()`

---

## 👥 Utilisateurs

- [x] Service `userService.ts`
- [x] `userService.getAll()` — prêt
- [x] `userService.getById()` — prêt
- [x] `userService.update()` — appelé en background depuis AuthContext
- [x] `userService.delete()` — appelé en background depuis AuthContext
- [x] `userService.getProgression()` — prêt
- [ ] Hook `useUsers()` avec React Query
- [ ] Connexion `AdminUsers` → API au lieu de AuthContext.users
- [ ] Upload avatar → endpoint dédié

---

## 📚 Modules

- [x] Service `moduleService.ts`
- [x] Hook `useModules()` — hybride (API → course-data.ts)
- [x] Hook `useModule(id)` — hybride
- [x] Hook `useCompleteLesson()` — mutation
- [ ] Connexion `Home.tsx` → `useModules()` (utilise encore course-data directement)
- [ ] Connexion `ModulePage.tsx` → `useModule(id)`
- [ ] Connexion `LessonPage.tsx` → `moduleService.getLessons()`
- [ ] Mutations admin : `useCreateModule()`, `useUpdateModule()`, `useDeleteModule()`
- [ ] Connexion `AdminModules.tsx` → mutations API

---

## ❓ Quiz

- [x] Service `quizService.ts`
- [x] Hook `useQuiz(id)` — hybride
- [x] Hook `useSubmitQuiz()` — mutation avec fallback
- [ ] Connexion `QuizSystem.tsx` → `useQuiz(id)` + `useSubmitQuiz()`
- [ ] Timer basé sur `quiz.time_limit`
- [ ] Composant `QuizResults.tsx` avec `quizService.getResults()`
- [ ] Historique des tentatives

---

## 📊 Progression

- [ ] Service `progressService.ts` (non créé)
- [ ] Hook `useMyProgress()` (non créé)
- [ ] Connexion `use-progress.ts` → API `/api/progress/me`
- [ ] Sync progression locale ↔ serveur
- [ ] Connexion `DashboardPage` → données API

---

## 🛡️ Admin

- [x] Service `adminService.ts`
- [x] Hook `useAdminStats()` — hybride
- [x] Hook `useAdminAnalytics()` — hybride
- [ ] Connexion `AdminOverview.tsx` → `useAdminStats()`
- [ ] Connexion `AdminAnalytics.tsx` → `useAdminAnalytics()`
- [ ] Connexion `AdminUsers.tsx` → `adminService.getUsers()` avec filtres
- [ ] Gestion modules admin via API mutations
- [ ] Gestion quiz admin via API (CRUD endpoints manquants côté backend)
- [ ] Gestion vidéos admin (aucun endpoint backend)

---

## 🤖 Machine Learning

- [x] Service `mlService.ts`
- [x] Hook `usePredict()` — mutation avec fallback
- [ ] Connexion `MLDashboard.tsx` → `usePredict()`
- [ ] Affichage version modèle et confidence
- [ ] Historique des prédictions

---

## 📄 Documentation

- [x] `docs/API_DOCUMENTATION.md` — Documentation complète des endpoints
- [x] `docs/BACKEND_ENDPOINTS.md` — État d'intégration par endpoint
- [x] `docs/FRONTEND_ANALYSIS.md` — Analyse des composants frontend
- [x] `docs/MISSING_FEATURES.md` — Fonctionnalités manquantes détaillées
- [x] `docs/INTEGRATION_STATUS.md` — Cette checklist

---

## 📈 Progression globale

```
Infrastructure    : ████████████████████ 100%
Services API      : ████████████████████ 100%
Hooks React Query : ████████████████░░░░  80%
Auth connecté     : ████████████████░░░░  80%
Pages connectées  : ███░░░░░░░░░░░░░░░░░  15%
Admin connecté    : ██░░░░░░░░░░░░░░░░░░  10%
Nouvelles features: ░░░░░░░░░░░░░░░░░░░░   0%
─────────────────────────────────────────────
TOTAL             : █████████░░░░░░░░░░░  45%
```
