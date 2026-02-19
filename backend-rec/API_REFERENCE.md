# 📡 API Reference - Backend Compatible Lovable

**Base URL:** `http://localhost:8000`

---

## 🔐 AUTHENTIFICATION

### POST /api/auth/register
Créer un nouveau compte utilisateur.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student"  // "student" | "instructor" | "admin"
}
```

**Response: 201 Created**
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
Connexion utilisateur.

**Request (form-data):**
```
username: user@example.com
password: SecurePass123
```

**Response: 200 OK**
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

**Usage dans le frontend:**
```typescript
const formData = new FormData();
formData.append('username', email);
formData.append('password', password);

const response = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  body: formData
});
```

---

### GET /api/auth/me
Récupérer le profil de l'utilisateur connecté.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response: 200 OK**
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
Demander une réinitialisation de mot de passe.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response: 200 OK**
```json
{
  "message": "Password reset email sent"
}
```

---

## 👥 USERS

### GET /api/users
Liste tous les utilisateurs (Admin only).

**Query Parameters:**
- `role` (optional): "student" | "instructor" | "admin"
- `is_active` (optional): true | false
- `search` (optional): recherche par nom/email

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Response: 200 OK**
```json
[
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
]
```

---

### GET /api/users/{user_id}
Récupérer un utilisateur spécifique.

**Response: 200 OK**
```json
{
  "id": "uuid-1234",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "is_active": true,
  "avatar": "https://example.com/avatar.jpg",
  "created_at": "2025-02-10T10:00:00Z",
  "last_login": "2025-02-10T14:30:00Z"
}
```

---

### PUT /api/users/{user_id}
Mettre à jour un utilisateur.

**Request:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "avatar": "https://example.com/new-avatar.jpg"
}
```

**Response: 200 OK** (User object)

---

### DELETE /api/users/{user_id}
Supprimer un utilisateur (Admin only).

**Response: 204 No Content**

---

### GET /api/users/{user_id}/progression
Récupérer la progression d'un utilisateur.

**Response: 200 OK**
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
Liste tous les modules.

**Response: 200 OK**
```json
[
  {
    "id": "module-1",
    "title": "DevOps Basics",
    "description": "Introduction to DevOps principles",
    "week": 1,
    "order": 1,
    "lessons": [
      {
        "id": "lesson-1",
        "title": "Introduction to Docker",
        "type": "video",
        "duration": "3:24",
        "completed": false,
        "url": "https://loom.com/share/abc123",
        "content": null
      }
    ],
    "completion_rate": 0,
    "total_duration": 180
  }
]
```

---

### GET /api/modules/{module_id}
Récupérer un module spécifique.

**Response: 200 OK** (Module object)

---

### POST /api/modules
Créer un module (Admin only).

**Request:**
```json
{
  "title": "Advanced MLOps",
  "description": "Deep dive into MLOps tools",
  "week": 3,
  "order": 3
}
```

**Response: 201 Created**

---

### PUT /api/modules/{module_id}
Mettre à jour un module (Admin only).

**Response: 200 OK**

---

### DELETE /api/modules/{module_id}
Supprimer un module (Admin only).

**Response: 204 No Content**

---

### GET /api/modules/{module_id}/lessons
Liste les leçons d'un module.

**Response: 200 OK**
```json
[
  {
    "id": "lesson-1",
    "title": "Introduction to Docker",
    "type": "video",
    "duration": "3:24",
    "completed": false,
    "url": "https://loom.com/share/abc123",
    "content": null
  }
]
```

---

### POST /api/lessons/{lesson_id}/complete
Marquer une leçon comme complétée.

**Response: 200 OK**

---

## ❓ QUIZ

### GET /api/quizzes/{quiz_id}
Récupérer un quiz.

**Response: 200 OK**
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
      "options": [
        "Continuous Integration / Continuous Deployment",
        "Code Integration / Code Deployment",
        "Constant Integration / Constant Delivery",
        "None of the above"
      ],
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
Soumettre les réponses d'un quiz.

**Request:**
```json
{
  "answers": {
    "q1": [0],
    "q2": [1, 3],
    "q3": [2]
  }
}
```

**Response: 200 OK**
```json
{
  "attempt_id": "attempt-abc123",
  "score": 85,
  "passed": true,
  "correct_answers": 17,
  "total_questions": 20,
  "time_taken": 1245,
  "answers": {
    "q1": true,
    "q2": false,
    "q3": true
  }
}
```

---

### GET /api/quizzes/{quiz_id}/results/{attempt_id}
Récupérer les résultats d'un quiz.

**Response: 200 OK** (QuizResult object)

---

## 📊 ADMIN

### GET /api/admin/stats
Statistiques du dashboard.

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Response: 200 OK**
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
Données analytiques détaillées.

**Response: 200 OK**
```json
{
  "registrations_per_day": [
    { "date": "2025-02-03", "count": 45 },
    { "date": "2025-02-04", "count": 52 }
  ],
  "popular_modules": [
    { "module_id": "1", "title": "DevOps Basics", "views": 1234 }
  ],
  "user_roles": [
    { "role": "student", "count": 1200 },
    { "role": "instructor", "count": 45 },
    { "role": "admin", "count": 2 }
  ],
  "recent_activity": [
    {
      "user": "Marie D.",
      "action": "completed Module 2",
      "timestamp": "2025-02-10T14:25:00Z"
    }
  ]
}
```

---

## 🤖 MACHINE LEARNING

### POST /api/ml/predict
Faire une prédiction.

**Request:**
```json
{
  "features": {
    "feature1": 42,
    "feature2": "category_a",
    "feature3": 3.14
  }
}
```

**Response: 200 OK**
```json
{
  "prediction": 0.87,
  "model_version": "v1.2.3",
  "confidence": 0.95,
  "timestamp": "2025-02-10T14:30:00Z"
}
```

---

## 🚨 GESTION DES ERREURS

Toutes les erreurs suivent le même format:

**400 Bad Request**
```json
{
  "detail": "Validation error: password must be at least 8 characters"
}
```

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

**403 Forbidden**
```json
{
  "detail": "Insufficient permissions"
}
```

**404 Not Found**
```json
{
  "detail": "User not found"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error"
}
```

---

## 💡 EXEMPLES D'UTILISATION FRONTEND

### Exemple avec fetch (TypeScript)

```typescript
// Service d'authentification
const login = async (email: string, password: string) => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);

  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('user', JSON.stringify(data.user));
  
  return data;
};

// Récupérer les modules avec authentification
const getModules = async () => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/api/modules', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  return response.json();
};
```

---

## 📦 COMPTES DE TEST

Utilisez ces comptes après avoir exécuté `seed_db.py`:

**Admin:**
- Email: `admin@didacticiel.com`
- Password: `Admin123!`

**Formateur:**
- Email: `instructor@didacticiel.com`
- Password: `Instructor123!`

**Étudiant:**
- Email: `jean.martin@student.com`
- Password: `Student123!`
