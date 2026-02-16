# 🔍 Analyse Frontend — Composants & Connexions

> Dernière mise à jour : 2026-02-16

---

## 📁 Architecture des fichiers

```
src/
├── components/
│   ├── AdminLayout.tsx        # Layout admin avec sidebar
│   ├── AppSidebar.tsx         # Sidebar principale (étudiant/formateur)
│   ├── MainLayout.tsx         # Layout principal avec Outlet
│   ├── NavLink.tsx            # Lien de navigation actif
│   ├── ProtectedRoute.tsx     # Guard de route avec rôles
│   ├── ThemeProvider.tsx      # Thème clair/sombre
│   ├── ThemeToggle.tsx        # Toggle thème
│   └── lesson/
│       ├── MLDashboard.tsx    # Dashboard ML (prédictions)
│       ├── MarkdownViewer.tsx # Rendu Markdown
│       ├── ProgressDashboard.tsx # Dashboard progression
│       ├── QuizSystem.tsx     # Système de quiz
│       └── VideoPlayer.tsx    # Lecteur vidéo
├── contexts/
│   └── AuthContext.tsx        # État auth global (hybride API/localStorage)
├── config/
│   └── api.ts                 # Configuration endpoints API
├── data/
│   ├── course-data.ts         # Données modules/leçons locales
│   ├── lesson-content.ts      # Contenu des leçons (Markdown)
│   ├── mock-users.ts          # 20 utilisateurs fictifs
│   ├── quiz-data.ts           # Questions de quiz locales
│   └── video-data.ts          # URLs vidéos
├── hooks/
│   ├── use-api.ts             # Hooks React Query (hybride)
│   ├── use-mobile.tsx         # Détection mobile
│   ├── use-progress.ts        # Progression locale
│   └── use-toast.ts           # Notifications toast
├── pages/
│   ├── DashboardPage.tsx      # Tableau de bord étudiant
│   ├── ForgotPasswordPage.tsx # Mot de passe oublié
│   ├── Home.tsx               # Page d'accueil (modules)
│   ├── LessonPage.tsx         # Page d'une leçon
│   ├── LoginPage.tsx          # Connexion
│   ├── ModulePage.tsx         # Détail d'un module
│   ├── RegisterPage.tsx       # Inscription
│   └── admin/
│       ├── AdminAnalytics.tsx # Statistiques détaillées
│       ├── AdminModules.tsx   # CRUD modules
│       ├── AdminOverview.tsx  # Vue d'ensemble KPIs
│       ├── AdminQuizzes.tsx   # CRUD quiz
│       ├── AdminSettings.tsx  # Paramètres plateforme
│       ├── AdminUsers.tsx     # Gestion utilisateurs
│       └── AdminVideos.tsx    # Gestion vidéos
└── services/
    ├── adminService.ts        # API admin (stats, analytics, users)
    ├── authService.ts         # API auth (login, register, me)
    ├── httpClient.ts          # Client Axios avec intercepteurs
    ├── mlService.ts           # API ML (predict)
    ├── moduleService.ts       # API modules (CRUD, lessons)
    ├── quizService.ts         # API quiz (get, submit, results)
    └── userService.ts         # API users (CRUD, progression)
```

---

## 🔗 Matrice de connexion Composant → Source de données

| Composant | Source actuelle | Service API disponible | Connecté ? |
|-----------|----------------|----------------------|------------|
| `LoginPage` | `AuthContext.login()` | `authService.login()` | ✅ Hybride |
| `RegisterPage` | `AuthContext.register()` | `authService.register()` | ✅ Hybride |
| `ForgotPasswordPage` | Toast local | `authService.forgotPassword()` | ⚠️ Non connecté |
| `Home` | `course-data.ts` + `use-progress.ts` | `moduleService.getAll()` | ⚠️ Hook prêt, non utilisé |
| `ModulePage` | `course-data.ts` | `moduleService.getById()` | ⚠️ Hook prêt, non utilisé |
| `LessonPage` | `lesson-content.ts` | `moduleService.getLessons()` | ⚠️ Hook prêt, non utilisé |
| `DashboardPage` | `use-progress.ts` (localStorage) | Aucun endpoint `/progress/me` | ❌ |
| `QuizSystem` | `quiz-data.ts` | `quizService` | ⚠️ Hook prêt, non utilisé |
| `MLDashboard` | Données locales | `mlService.predict()` | ⚠️ Hook prêt, non utilisé |
| `AdminOverview` | `AuthContext.users` + `course-data` | `adminService.getStats()` | ⚠️ Hook prêt, non utilisé |
| `AdminUsers` | `AuthContext.users` | `adminService.getUsers()` | ⚠️ Non connecté |
| `AdminModules` | `course-data.ts` (état local) | `moduleService.create/update/delete()` | ❌ |
| `AdminVideos` | État local | Aucun endpoint dédié | ❌ |
| `AdminQuizzes` | État local | `quizService` (lecture seule) | ❌ |
| `AdminAnalytics` | Données calculées localement | `adminService.getAnalytics()` | ⚠️ Hook prêt, non utilisé |
| `AdminSettings` | État local (toast) | Aucun endpoint | ❌ |

---

## 🧩 Composants UI réutilisables (shadcn/ui)

Tous les composants shadcn sont installés et fonctionnels :
`accordion`, `alert-dialog`, `avatar`, `badge`, `breadcrumb`, `button`, `calendar`, `card`, `carousel`, `chart`, `checkbox`, `collapsible`, `command`, `context-menu`, `dialog`, `drawer`, `dropdown-menu`, `form`, `hover-card`, `input`, `label`, `menubar`, `navigation-menu`, `pagination`, `popover`, `progress`, `radio-group`, `resizable`, `scroll-area`, `select`, `separator`, `sheet`, `sidebar`, `skeleton`, `slider`, `sonner`, `switch`, `table`, `tabs`, `textarea`, `toast`, `toggle`, `tooltip`

---

## 📊 Dépendances principales

| Package | Version | Usage |
|---------|---------|-------|
| `react` | ^18.3.1 | Framework UI |
| `react-router-dom` | ^6.30.1 | Routing SPA |
| `@tanstack/react-query` | ^5.83.0 | Gestion cache/état serveur |
| `axios` | ^1.13.5 | Client HTTP |
| `recharts` | ^2.15.4 | Graphiques |
| `react-hook-form` | ^7.61.1 | Formulaires |
| `zod` | ^3.25.76 | Validation |
| `lucide-react` | ^0.462.0 | Icônes |
| `date-fns` | ^3.6.0 | Formatage dates |
| `sonner` | ^1.7.4 | Notifications toast |
