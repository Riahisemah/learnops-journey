# 🎓 Didacticiel DevOps & MLOps - Backend API

Backend FastAPI pour la plateforme d'apprentissage interactive DevOps & MLOps. **100% Compatible avec le frontend Lovable.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)](https://www.sqlalchemy.org/)

---

## 🚀 Démarrage Ultra-Rapide (2 minutes)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Créer les données de test
python seed_db.py

# 3. Lancer l'API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ✅ API disponible sur http://localhost:8000
# 📚 Documentation sur http://localhost:8000/docs
```

---

## ✨ Fonctionnalités

### 🔐 Authentification
- ✅ JWT avec refresh tokens
- ✅ Rôles (Student, Instructor, Admin)
- ✅ Réinitialisation de mot de passe

### 📚 Modules d'Apprentissage
- ✅ CRUD complet
- ✅ Leçons (vidéo, texte, quiz, pratique)
- ✅ Progression par utilisateur
- ✅ Badges automatiques

### ❓ Système de Quiz
- ✅ Questions multiples/uniques
- ✅ Correction automatique
- ✅ Historique des tentatives

### 👥 Dashboard Admin
- ✅ Statistiques en temps réel
- ✅ Gestion utilisateurs
- ✅ Analytics détaillés

---

## 📚 Documentation Complète

| 📄 Document | 🎯 Utilité |
|------------|-----------|
| [**QUICKSTART.md**](QUICKSTART.md) | Démarrage en 5 min |
| [**API_REFERENCE.md**](API_REFERENCE.md) | Tous les endpoints |
| [**INTEGRATION_GUIDE.md**](INTEGRATION_GUIDE.md) | Connecter Lovable |
| [**Swagger UI**](http://localhost:8000/docs) | Doc interactive |

---

## 🔌 Endpoints Principaux

```
🔐 AUTH
POST   /api/auth/register       # Inscription
POST   /api/auth/login          # Connexion (retourne JWT)
GET    /api/auth/me             # Profil utilisateur

👥 USERS
GET    /api/users               # Liste (admin)
GET    /api/users/{id}/progression # Progression

📚 MODULES
GET    /api/modules             # Liste modules
POST   /api/lessons/{id}/complete # Marquer complété

❓ QUIZ
POST   /api/quizzes/{id}/submit # Soumettre réponses

📊 ADMIN
GET    /api/admin/stats         # Dashboard stats
GET    /api/admin/analytics     # Analytics
```

**→ Voir [API_REFERENCE.md](API_REFERENCE.md) pour les formats JSON**

---

## 🧪 Tester l'API

### 1. Vérifier que ça fonctionne

```bash
python test_api.py
```

### 2. Comptes de test (après seed_db.py)

| Rôle | Email | Password |
|------|-------|----------|
| 👑 **Admin** | admin@didacticiel.com | Admin123! |
| 👨‍🏫 Formateur | instructor@didacticiel.com | Instructor123! |
| 👨‍🎓 Étudiant | jean.martin@student.com | Student123! |

### 3. Tester avec Swagger

Ouvre http://localhost:8000/docs et teste les endpoints interactivement.

---

## 🔗 Connecter le Frontend Lovable

### Étape 1 : Créer le service API dans Lovable

```typescript
// src/services/authService.ts
export const authService = {
  async login(email: string, password: string) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data;
  }
};
```

### Étape 2 : Utiliser dans un composant

```typescript
const handleLogin = async () => {
  try {
    const result = await authService.login(email, password);
    // Rediriger vers dashboard
  } catch (error) {
    // Afficher erreur
  }
};
```

**→ Guide complet dans [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)**

---

## 📁 Structure du Projet

```
backend/
├── app/
│   ├── api/          # 🔌 Routes API
│   ├── models/       # 🗄️ SQLAlchemy models
│   ├── schemas/      # 📋 Pydantic schemas
│   ├── core/         # 🔒 Sécurité & config
│   └── main.py       # 🚀 App FastAPI
├── seed_db.py        # 🌱 Données de test
├── test_api.py       # 🧪 Tests
└── requirements.txt  # 📦 Dépendances
```

---

## 🛠 Stack Technique

- **FastAPI** 0.109.0 - Framework web
- **SQLAlchemy** 2.0 - ORM
- **SQLite** - Base de données (dev)
- **Pydantic** 2.5 - Validation
- **JWT** - Authentification
- **bcrypt** - Hashing mots de passe

---

## 🐳 Avec Docker

```bash
# Lancer backend + DB
docker-compose up -d

# Seed la base
docker-compose exec api python seed_db.py

# Voir les logs
docker-compose logs -f api
```

---

## 📊 Données de Démonstration

Après `seed_db.py`, vous aurez :

- 📦 **15 utilisateurs** (admins, formateurs, étudiants)
- 📚 **4 modules** (DevOps, MLOps, Deployment, Advanced)
- 📖 **15+ leçons** avec contenu
- ❓ **Quiz** avec corrections
- 🏆 **Badges** pré-configurés

---

## 🔒 Sécurité

- ✅ JWT avec expiration
- ✅ Mots de passe hashés (bcrypt)
- ✅ CORS configuré pour Lovable
- ✅ Validation stricte (Pydantic)
- ✅ Protection par rôles

---

## 🐛 Troubleshooting

### Erreur CORS

```
Access blocked by CORS policy
```

**Solution :** Vérifie que le backend tourne sur `localhost:8000` et redémarre-le.

### Base de données vide

```bash
rm didacticiel.db  # Supprimer l'ancienne
python seed_db.py  # Recréer
```

### Port déjà utilisé

```bash
uvicorn app.main:app --port 8001  # Changer le port
```

---

## 📞 Support

- 📖 [Documentation API](http://localhost:8000/docs)
- 📚 [Guide d'intégration](INTEGRATION_GUIDE.md)
- 🔍 [API Reference](API_REFERENCE.md)

---

## 🎯 Prochaines Étapes

1. ✅ Lancer le backend (`python seed_db.py` puis `uvicorn app.main:app --reload`)
2. ✅ Tester avec `python test_api.py`
3. ✅ Ouvrir http://localhost:8000/docs
4. 🔄 Connecter le frontend Lovable (voir INTEGRATION_GUIDE.md)
5. 🚀 Développer !

---

<div align="center">

**Fait avec ❤️ pour l'apprentissage DevOps & MLOps**

⭐ **100% Compatible Lovable** ⭐

</div>
