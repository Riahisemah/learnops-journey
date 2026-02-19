# 📡 API Backend Mise à Jour - Compatibilité Frontend Lovable

**URL de base:** `http://localhost:8000`
**Documentation Swagger:** `http://localhost:8000/docs`

---

## ✅ NOUVEAUX ENDPOINTS AJOUTÉS

### 🔔 Notifications (Priorité HAUTE)

#### POST /api/notifications
Créer une notification

**Request:**
```json
{
  "title": "Nouveau module disponible",
  "message": "Le module Advanced MLOps est maintenant disponible",
  "type": "info",
  "user_id": "uuid-1234"  // optionnel, par défaut = utilisateur courant
}
```

**Response:** `200 OK`
```json
{
  "id": "notif-1234",
  "user_id": "uuid-1234",
  "title": "Nouveau module disponible",
  "message": "Le module Advanced MLOps est maintenant disponible",
  "type": "info",
  "read": false,
  "created_at": "2025-02-12T10:00:00Z"
}
```

---

#### GET /api/notifications/me
Récupérer mes notifications

**Response:** `200 OK`
```json
[
  {
    "id": "notif-1234",
    "title": "Nouveau module",
    "message": "...",
    "type": "info",
    "read": false,
    "created_at": "2025-02-12T10:00:00Z"
  }
]
```

---

#### PUT /api/notifications/{id}/read
Marquer comme lue

**Response:** `200 OK`
```json
{ "message": "Notification marked as read" }
```

---

#### DELETE /api/notifications/{id}
Supprimer une notification

**Response:** `200 OK`

---

#### GET /api/notifications/unread/count
Compter les notifications non lues

**Response:** `200 OK`
```json
{ "count": 5 }
```

---

### 🏆 Certificats (Priorité HAUTE)

#### POST /api/certificates/generate
Générer un certificat (si progression = 100%)

**Response:** `200 OK`
```json
{
  "certificate_id": "cert-1234",
  "message": "Certificat généré avec succès",
  "download_url": "/api/certificates/cert-1234"
}
```

**Error si progression < 100%:** `400 Bad Request`
```json
{
  "detail": "Progression insuffisante. Vous êtes à 75%"
}
```

---

#### GET /api/certificates/me
Lister mes certificats

**Response:** `200 OK`
```json
[
  {
    "id": "cert-1234",
    "user_id": "uuid-1234",
    "user_name": "John Doe",
    "generated_at": "2025-02-12T10:00:00Z",
    "modules_completed": [1, 2, 3, 4],
    "badges": ["first-lesson", "quiz-master", "completion-master"]
  }
]
```

---

#### GET /api/certificates/{id}
Télécharger un certificat

**Response:** `200 OK` (JSON pour l'instant, PDF à venir)

---

#### DELETE /api/certificates/{id}
Supprimer un certificat

**Response:** `200 OK`

---

### 💬 Commentaires sur Leçons (Priorité MOYENNE)

#### POST /api/lessons/{lesson_id}/comments
Ajouter un commentaire

**Request:**
```json
{
  "content": "Excellente explication du CI/CD !"
}
```

**Response:** `201 Created`
```json
{
  "id": "comment-1234",
  "lesson_id": "lesson-1-1",
  "user_id": "uuid-1234",
  "user_name": "John Doe",
  "content": "Excellente explication du CI/CD !",
  "created_at": "2025-02-12T10:00:00Z"
}
```

---

#### GET /api/lessons/{lesson_id}/comments
Lister les commentaires (avec pagination)

**Query params:**
- `skip`: int (default: 0)
- `limit`: int (default: 50)

**Response:** `200 OK`
```json
{
  "total": 15,
  "comments": [
    {
      "id": "comment-1234",
      "lesson_id": "lesson-1-1",
      "user_id": "uuid-1234",
      "user_name": "John Doe",
      "content": "Excellente explication !",
      "created_at": "2025-02-12T10:00:00Z"
    }
  ]
}
```

---

#### DELETE /api/comments/{comment_id}
Supprimer un commentaire (auteur ou admin)

**Response:** `200 OK`

---

### 🔍 Recherche Globale (Priorité MOYENNE)

#### GET /api/search?q=docker
Recherche dans modules, leçons et quiz

**Query params:**
- `q`: string (min 2 caractères) - Terme de recherche
- `limit`: int (default: 20)

**Response:** `200 OK`
```json
{
  "query": "docker",
  "total": 8,
  "results": {
    "modules": [
      {
        "id": "module-1",
        "title": "DevOps Basics",
        "description": "Introduction to Docker and CI/CD",
        "week": 1,
        "type": "module"
      }
    ],
    "lessons": [
      {
        "id": "lesson-1-3",
        "title": "Docker Fundamentals",
        "type": "video",
        "module_id": "module-1",
        "duration": "10:45",
        "result_type": "lesson"
      }
    ],
    "quizzes": [
      {
        "id": "quiz-1",
        "title": "DevOps Fundamentals Quiz",
        "module_id": "module-1",
        "type": "quiz"
      }
    ]
  }
}
```

---

### ⭐ Favoris/Bookmarks (Priorité MOYENNE)

#### POST /api/bookmarks
Ajouter un favori

**Request:**
```json
{
  "resource_type": "lesson",  // "module" | "lesson" | "quiz"
  "resource_id": "lesson-1-3",
  "title": "Docker Fundamentals"
}
```

**Response:** `200 OK`
```json
{
  "id": "bookmark-1234",
  "resource_type": "lesson",
  "resource_id": "lesson-1-3",
  "title": "Docker Fundamentals",
  "created_at": "2025-02-12T10:00:00Z"
}
```

---

#### GET /api/bookmarks/me
Mes favoris (avec filtre optionnel)

**Query params:**
- `resource_type`: string (optionnel) - Filtrer par type

**Response:** `200 OK`
```json
[
  {
    "id": "bookmark-1234",
    "resource_type": "lesson",
    "resource_id": "lesson-1-3",
    "title": "Docker Fundamentals",
    "created_at": "2025-02-12T10:00:00Z"
  }
]
```

---

#### DELETE /api/bookmarks/{id}
Retirer des favoris

**Response:** `200 OK`

---

#### GET /api/bookmarks/check
Vérifier si une ressource est en favoris

**Query params:**
- `resource_type`: string
- `resource_id`: string

**Response:** `200 OK`
```json
{ "is_bookmarked": true }
```

---

## ✨ ENDPOINTS AMÉLIORÉS

### GET /api/progress/me
**Améliorations:**
- Calcul automatique de la progression en temps réel
- Attribution automatique des badges
- Champs supplémentaires : `lessons_completed`, `total_lessons`

**Response:** `200 OK`
```json
{
  "user_id": "uuid-1234",
  "progression": 65,
  "modules_completed": [1, 2],
  "badges": ["first-lesson", "5-lessons", "quiz-master"],
  "time_spent": 7200,
  "lessons_completed": 13,
  "total_lessons": 20
}
```

---

### POST /api/progress/update
**Améliorations:**
- Champs optionnels (peut mettre à jour un seul champ)
- Vérification automatique des badges après mise à jour
- Retourne la progression complète mise à jour

**Request:**
```json
{
  "progression": 70,  // optionnel
  "modules_completed": [1, 2, 3],  // optionnel
  "time_spent": 8000  // optionnel
}
```

**Response:** `200 OK` (progression complète)

---

## 📋 BADGES AUTOMATIQUES

Les badges suivants sont attribués automatiquement :

| Badge | Condition |
|-------|-----------|
| `first-lesson` | 1 leçon complétée |
| `5-lessons` | 5 leçons complétées |
| `10-lessons` | 10 leçons complétées |
| `module-complete` | 25% progression |
| `half-way` | 50% progression |
| `completion-master` | 100% progression |

---

## 📊 RÉSUMÉ DES ENDPOINTS

| Catégorie | Endpoints Totaux |
|-----------|------------------|
| Auth | 4 |
| Users | 5 |
| Modules | 6 |
| Lessons | 2 (+commentaires) |
| Quiz | 3 |
| Progress | 2 (améliorés) |
| Admin | 3 |
| ML | 1 |
| **🆕 Notifications** | **5** |
| **🆕 Certificats** | **4** |
| **🆕 Commentaires** | **3** |
| **🆕 Recherche** | **1** |
| **🆕 Bookmarks** | **4** |
| **TOTAL** | **43** |

---

## 🔄 COMPATIBILITÉ FRONTEND LOVABLE

### Endpoints Frontend Attendus vs Backend Disponible

| Frontend (Lovable) | Backend | Statut |
|-------------------|---------|--------|
| `progressService.getMe()` | GET /api/progress/me | ✅ Amélioré |
| `progressService.update()` | POST /api/progress/update | ✅ Amélioré |
| `notificationService.*` | /api/notifications/* | ✅ Nouveau |
| `certificateService.*` | /api/certificates/* | ✅ Nouveau |
| `commentService.*` | /api/lessons/*/comments | ✅ Nouveau |
| `searchService.search()` | GET /api/search | ✅ Nouveau |
| `bookmarkService.*` | /api/bookmarks/* | ✅ Nouveau |

---

## 🚀 PROCHAINES ÉTAPES

1. ✅ Endpoints créés et testables dans Swagger
2. ⏳ Frontend Lovable doit créer les services correspondants
3. ⏳ Migrations DB pour stocker notifications/commentaires (actuellement en mémoire)
4. ⏳ Génération PDF pour certificats (ReportLab)
5. ⏳ WebSocket pour notifications temps réel

---

## 💡 NOTES D'IMPLÉMENTATION

**Stockage temporaire:**
- Notifications, certificats, commentaires et bookmarks utilisent un stockage en mémoire
- À migrer vers la base de données pour la production
- Les données sont perdues au redémarrage du serveur

**Pour passer en production:**
```python
# Créer les models SQLAlchemy correspondants
# Créer les migrations Alembic
# Remplacer les listes en mémoire par des requêtes DB
```
