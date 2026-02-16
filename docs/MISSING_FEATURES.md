# Fonctionnalités Manquantes — Analyse Complète

> Dernière mise à jour : 2026-02-16

---

## 1. Backend Disponible mais Frontend Non Connecté

### Quiz Interactif Complet
**Backend :**
- ✅ GET /api/quizzes/{id}
- ✅ POST /api/quizzes/{id}/submit
- ✅ GET /api/quizzes/{id}/results/{attempt_id}

**Frontend existant :**
- ⚠️ `QuizSystem.tsx` existe mais utilise `quiz-data.ts` en local
- ⚠️ `useQuiz()` et `useSubmitQuiz()` hooks prêts dans `use-api.ts`

**Frontend manquant :**
- ❌ Connexion du composant `QuizSystem` aux hooks API
- ❌ Timer pour quiz chronométrés (`time_limit` du backend)
- ❌ Historique des tentatives (`quizService.getResults()`)
- ❌ Affichage résultats avec feedback animé

**Action requise :**
```
1. Modifier QuizSystem.tsx → utiliser useQuiz(id) au lieu de quiz-data.ts
2. Ajouter timer avec useEffect basé sur quiz.time_limit
3. Créer QuizResults.tsx pour afficher les résultats détaillés
4. Créer QuizHistory.tsx pour l'historique des tentatives
```

---

### Dashboard Admin — Données API
**Backend :**
- ✅ GET /api/admin/stats
- ✅ GET /api/admin/analytics
- ✅ GET /api/admin/users

**Frontend existant :**
- ⚠️ `AdminOverview.tsx` — utilise `AuthContext.users` + données random
- ⚠️ `AdminAnalytics.tsx` — données générées localement
- ⚠️ `AdminUsers.tsx` — utilise `AuthContext.users` (localStorage)
- ⚠️ `useAdminStats()` et `useAdminAnalytics()` hooks prêts

**Frontend manquant :**
- ❌ Connexion `AdminOverview` → `useAdminStats()`
- ❌ Connexion `AdminAnalytics` → `useAdminAnalytics()`
- ❌ Connexion `AdminUsers` → `adminService.getUsers()`

**Action requise :**
```
1. AdminOverview.tsx → remplacer calculs locaux par useAdminStats()
2. AdminAnalytics.tsx → utiliser useAdminAnalytics()
3. AdminUsers.tsx → utiliser adminService.getUsers() avec filtres query params
```

---

### Progression Utilisateur Détaillée
**Backend :**
- ✅ GET /api/users/{id}/progression
- ✅ GET /api/progress/me
- ✅ POST /api/progress/update

**Frontend existant :**
- ⚠️ `ProgressDashboard.tsx` — utilise `use-progress.ts` (localStorage)
- ⚠️ `DashboardPage.tsx` — affiche ProgressDashboard

**Frontend manquant :**
- ❌ Service `progressService.ts` non créé
- ❌ Hook `useMyProgress()` non créé
- ❌ Synchronisation progression locale ↔ API

**Action requise :**
```
1. Créer src/services/progressService.ts
2. Ajouter useMyProgress() dans use-api.ts
3. Modifier use-progress.ts pour tenter l'API en premier
```

---

### Gestion Modules (Admin CRUD)
**Backend :**
- ✅ POST /api/modules
- ✅ PUT /api/modules/{id}
- ✅ DELETE /api/modules/{id}

**Frontend existant :**
- ⚠️ `AdminModules.tsx` — CRUD local (état React, pas persisté)
- ⚠️ `moduleService.create/update/delete()` services prêts

**Frontend manquant :**
- ❌ Mutations React Query pour create/update/delete
- ❌ Invalidation du cache après mutation
- ❌ Gestion erreurs API dans les formulaires

**Action requise :**
```
1. Créer useCreateModule(), useUpdateModule(), useDeleteModule() mutations
2. Connecter AdminModules.tsx aux mutations
3. Ajouter invalidateQueries(["modules"]) après chaque mutation
```

---

### Forgot Password
**Backend :**
- ✅ POST /api/auth/forgot-password

**Frontend existant :**
- ⚠️ `ForgotPasswordPage.tsx` — affiche un toast de confirmation sans appel API

**Action requise :**
```
1. Importer authService dans ForgotPasswordPage
2. Appeler authService.forgotPassword(email) dans le handleSubmit
3. Gérer les erreurs réseau
```

---

## 2. Frontend Existe mais Partiellement Fonctionnel

| Fonctionnalité | Page/Composant | Problème | Priorité |
|---------------|----------------|----------|----------|
| Upload avatar | AdminUsers / Profile | Bouton existe, pas d'upload réel | 🟡 Moyenne |
| Filtres admin users | AdminUsers | Filtres locaux, pas query params API | 🟢 Basse |
| Export CSV admin | AdminUsers | Exporte données locales, pas API | 🟢 Basse |
| Drag & drop modules | AdminModules | `GripVertical` affiché, pas de DnD réel | 🟢 Basse |
| Paramètres plateforme | AdminSettings | Sauvegarde locale (toast), pas d'API | 🟡 Moyenne |
| Vidéos admin | AdminVideos | CRUD local, pas d'API vidéo | 🟡 Moyenne |

---

## 3. Nouvelles Fonctionnalités à Développer

### 🔴 PRIORITÉ HAUTE

#### Notifications en Temps Réel
**Backend nécessaire :**
```
POST   /api/notifications           → Créer une notification
GET    /api/notifications/me        → Mes notifications
PUT    /api/notifications/{id}/read → Marquer comme lue
DELETE /api/notifications/{id}      → Supprimer
```

**Frontend nécessaire :**
- Composant `NotificationBell` avec badge compteur dans le header
- Dropdown liste des notifications
- Marquage lu/non-lu avec animation
- WebSocket ou polling pour temps réel

---

#### Certificats PDF
**Backend nécessaire :**
```
POST /api/certificates/generate     → Générer un certificat (si progression = 100%)
GET  /api/certificates/{id}         → Télécharger le PDF
GET  /api/certificates/me           → Lister mes certificats
```

**Frontend nécessaire :**
- Bouton « Télécharger certificat » visible si module complété à 100%
- Modal de prévisualisation du certificat
- Download automatique du PDF

---

#### Page Profil Utilisateur
**Backend existant :**
```
GET /api/auth/me                    → Profil courant
PUT /api/users/{id}                 → Mettre à jour
GET /api/users/{id}/progression     → Progression détaillée
```

**Frontend nécessaire :**
- Page `/profile` avec formulaire éditable (nom, email, avatar)
- Changement de mot de passe
- Affichage progression et badges
- Upload d'avatar

---

### 🟡 PRIORITÉ MOYENNE

#### Commentaires sur Leçons
**Backend nécessaire :**
```
POST   /api/lessons/{id}/comments   → Ajouter un commentaire
GET    /api/lessons/{id}/comments   → Lister les commentaires
DELETE /api/comments/{id}           → Supprimer (admin)
```

**Frontend nécessaire :**
- `CommentSection` sous chaque leçon
- Formulaire avec textarea
- Liste paginée avec avatar et date

---

#### Recherche Globale
**Backend nécessaire :**
```
GET /api/search?q=docker            → Recherche modules, leçons, quiz
```

**Frontend nécessaire :**
- Barre de recherche dans le header (`Cmd+K`)
- Dialog type `cmdk` (déjà installé) avec résultats groupés
- Navigation vers le résultat sélectionné

---

#### Favoris / Bookmarks
**Backend nécessaire :**
```
POST   /api/bookmarks               → Ajouter un favori
GET    /api/bookmarks/me            → Mes favoris
DELETE /api/bookmarks/{id}          → Retirer
```

**Frontend nécessaire :**
- Icône étoile sur chaque leçon/module
- Page « Mes favoris » dans la sidebar

---

#### Export Données (Admin)
**Backend nécessaire :**
```
GET /api/admin/export/users?format=csv    → Export utilisateurs
GET /api/admin/export/stats?format=xlsx   → Export statistiques
```

**Frontend existant :** Export CSV local dans `AdminUsers`
**Amélioration :** Connecter à l'API pour export côté serveur

---

### 🟢 PRIORITÉ BASSE

| Fonctionnalité | Description | Complexité |
|---------------|-------------|------------|
| Spaced Repetition | Système de révision espacée pour quiz | Élevée |
| Forum de discussion | Threads par module/leçon | Élevée |
| Leaderboard | Classement par progression et badges | Moyenne |
| Intégration calendrier | Sync Google Calendar pour deadlines | Élevée |
| Mode hors-ligne (PWA) | Service Worker + cache leçons | Élevée |
| Multi-langue (i18n) | Support FR/EN/AR | Moyenne |
| Dark mode avancé | Thèmes personnalisables | Basse |

---

## 4. Résumé Exécutif

### Statistiques actuelles

| Métrique | Valeur |
|----------|--------|
| Endpoints backend documentés | 25 |
| Services frontend créés | 6/6 (100%) |
| Hooks React Query créés | 8 |
| Composants connectés à l'API (hybride) | 2/15 (13%) — Auth uniquement |
| Composants avec hook prêt non utilisé | 8/15 (53%) |
| Fonctionnalités backend sans frontend | 3 (progression, certificats, notifications) |
| Nouvelles fonctionnalités proposées | 10 |

### Plan de développement

| Semaine | Objectif | Tâches clés |
|---------|----------|-------------|
| **S1** ✅ | Connexion basique | Services API, AuthContext hybride, hooks React Query |
| **S2** | Connexion complète | Connecter AdminOverview, AdminAnalytics, QuizSystem, Home aux hooks |
| **S3** | Fonctionnalités manquantes | Page profil, progressService, timer quiz, certificats |
| **S4** | Améliorations | Notifications, recherche globale, favoris, commentaires |
| **S5** | Polish | Export serveur, DnD modules, upload avatar, PWA |
