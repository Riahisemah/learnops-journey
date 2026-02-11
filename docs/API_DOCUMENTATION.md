# 📡 Documentation API Backend - DevOps & MLOps

URL de base: `http://localhost:8000`

Documentation interactive (Swagger): `http://localhost:8000/docs`

---

## 🔐 AUTHENTIFICATION

Toutes les requêtes (sauf register/login) nécessitent un token JWT dans le header:

```
Authorization: Bearer <access_token>
```

### POST /api/auth/register

**Inscription d'un nouvel utilisateur**

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid-1234",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "is_active": true,
  "created_at": "2025-02-10T10:00:00Z",
  "last_login": null
}
```

---

### POST /api/auth/login

**Connexion utilisateur**

**Request Body:** (form-data)
```
username: user@example.com
password: SecurePass123
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-1234",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "student",
    "is_active": true,
    "created_at": "2025-02-10T10:00:00Z",
    "last_login": "2025-02-10T14:30:00Z"
  }
}
```

---

### GET /api/auth/me

**Récupérer le profil utilisateur connecté**

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": "uuid-1234",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "is_active": true,
  "created_at": "2025-02-10T10:00:00Z",
  "last_login": "2025-02-10T14:30:00Z"
}
```

---

### POST /api/auth/forgot-password

**Demander une réinitialisation de mot de passe**

**Request Body:**
```json
{ "email": "user@example.com" }
```

**Response:** `200 OK`
```json
{ "message": "Password reset email sent" }
```

---

## 👥 UTILISATEURS

### GET /api/users

**Liste tous les utilisateurs** (Admin uniquement)

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `role` | string | Filter par rôle (student, instructor, admin) |
| `is_active` | boolean | Filter par statut |
| `search` | string | Recherche par nom ou email |

**Response:** `200 OK` — Array de `User`

---

### GET /api/users/{user_id}

**Récupérer un utilisateur spécifique**

**Response:** `200 OK` — Objet `User`

---

### PUT /api/users/{user_id}

**Mettre à jour un utilisateur**

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "avatar": "https://example.com/new-avatar.jpg"
}
```

**Response:** `200 OK` — Objet `User` mis à jour

---

### DELETE /api/users/{user_id}

**Supprimer un utilisateur** (Admin uniquement)

**Response:** `204 No Content`

---

### GET /api/users/{user_id}/progression

**Récupérer la progression d'un utilisateur**

**Response:** `200 OK`
```json
{
  "user_id": "uuid-1234",
  "progression": 65,
  "modules_completed": [1, 2],
  "badges": ["first-lesson", "quiz-master"],
  "time_spent": 7200
}
```

---

## 📚 MODULES

### GET /api/modules

**Liste tous les modules**

**Response:** `200 OK` — Array de `Module` avec leurs `lessons`

---

### GET /api/modules/{module_id}

**Récupérer un module spécifique**

**Response:** `200 OK` — Objet `Module`

---

### POST /api/modules

**Créer un module** (Admin uniquement)

**Request Body:**
```json
{
  "title": "Advanced MLOps",
  "description": "Deep dive into MLOps tools",
  "week": 3,
  "order": 3
}
```

**Response:** `201 Created`

---

### PUT /api/modules/{module_id}

**Mettre à jour un module** (Admin uniquement)

**Response:** `200 OK`

---

### DELETE /api/modules/{module_id}

**Supprimer un module** (Admin uniquement)

**Response:** `204 No Content`

---

### GET /api/modules/{module_id}/lessons

**Liste les leçons d'un module**

**Response:** `200 OK` — Array de `Lesson`

---

### POST /api/lessons/{lesson_id}/complete

**Marquer une leçon comme complétée**

**Response:** `200 OK`

---

## ❓ QUIZ

### GET /api/quizzes/{quiz_id}

**Récupérer un quiz**

**Response:** `200 OK`
```json
{
  "id": "quiz-1",
  "title": "DevOps Fundamentals Quiz",
  "module_id": "module-1",
  "questions": [
    {
      "id": "q1",
      "question": "What does CI/CD stand for?",
      "type": "single",
      "options": ["Continuous Integration / Continuous Deployment", "..."],
      "correct_answers": [0],
      "explanation": "CI/CD stands for Continuous Integration and Continuous Deployment"
    }
  ],
  "passing_score": 70,
  "time_limit": 1800
}
```

---

### POST /api/quizzes/{quiz_id}/submit

**Soumettre les réponses d'un quiz**

**Request Body:**
```json
{
  "answers": {
    "q1": [0],
    "q2": [1, 3]
  }
}
```

**Response:** `200 OK`
```json
{
  "attempt_id": "attempt-abc123",
  "score": 85,
  "passed": true,
  "correct_answers": 17,
  "total_questions": 20,
  "time_taken": 1245,
  "answers": { "q1": true, "q2": false }
}
```

---

## 📊 ADMIN

### GET /api/admin/stats

**Statistiques du dashboard admin**

**Response:** `200 OK`
```json
{
  "total_users": 1247,
  "total_modules": 4,
  "total_completions": 892,
  "average_rating": 4.8,
  "users_growth": 12,
  "completions_rate": 71.5
}
```

---

### GET /api/admin/analytics

**Données analytiques détaillées**

**Response:** `200 OK`
```json
{
  "registrations_per_day": [{ "date": "2025-02-03", "count": 45 }],
  "popular_modules": [{ "module_id": "1", "title": "DevOps Basics", "views": 1234 }],
  "user_roles": [{ "role": "student", "count": 1200 }],
  "recent_activity": [{ "user": "Marie D.", "action": "completed Module 2", "timestamp": "2025-02-10T14:25:00Z" }]
}
```

---

## 🤖 MACHINE LEARNING

### POST /api/ml/predict

**Faire une prédiction avec le modèle ML**

**Request Body:**
```json
{
  "features": {
    "feature1": 42,
    "feature2": "category_a",
    "feature3": 3.14
  }
}
```

**Response:** `200 OK`
```json
{
  "prediction": 0.87,
  "model_version": "v1.2.3",
  "confidence": 0.95,
  "timestamp": "2025-02-10T14:30:00Z"
}
```

---

## 🚨 CODES D'ERREUR

| Code | Description |
|------|-------------|
| `200` | Success |
| `201` | Created |
| `204` | No Content |
| `400` | Bad Request (validation error) |
| `401` | Unauthorized (no/invalid token) |
| `403` | Forbidden (insufficient permissions) |
| `404` | Not Found |
| `500` | Internal Server Error |

**Format d'erreur:**
```json
{ "detail": "Error message description" }
```
