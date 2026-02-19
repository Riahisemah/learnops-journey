# 🚀 Guide de Démarrage Rapide - Backend API

## Installation et Lancement

### Option 1 : Avec Docker (Recommandé)

```bash
# Lancer la base de données et l'API
docker-compose up -d

# Vérifier que tout fonctionne
curl http://localhost:8000/health

# Accéder à la documentation
# http://localhost:8000/docs
```

### Option 2 : Installation locale

```bash
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer .env (déjà créé)
# Vérifier que DATABASE_URL pointe vers SQLite

# 5. Peupler la base de données
python seed_db.py

# 6. Lancer l'API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Données de Test

Après avoir exécuté `seed_db.py`, vous aurez :

**👑 Compte Admin:**
- Email: `admin@didacticiel.com`
- Password: `Admin123!`

**👨‍🏫 Compte Formateur:**
- Email: `instructor@didacticiel.com`
- Password: `Instructor123!`

**👨‍🎓 Compte Étudiant:**
- Email: `jean.martin@student.com`
- Password: `Student123!`

## 🔗 Endpoints Principaux

- **API Documentation:** http://localhost:8000/docs
- **API ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **Root:** http://localhost:8000/

## 🧪 Tester l'API

### 1. Inscription
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "first_name": "Test",
    "last_name": "User",
    "role": "student"
  }'
```

### 2. Connexion
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@didacticiel.com&password=Admin123!"
```

### 3. Récupérer les modules
```bash
curl -X GET "http://localhost:8000/api/modules" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 Structure du Projet

```
backend/
├── app/
│   ├── api/           # Endpoints API
│   │   ├── auth.py    # Authentification
│   │   ├── users.py   # Gestion utilisateurs
│   │   ├── modules.py # Modules & leçons
│   │   ├── quiz.py    # Quiz & évaluations
│   │   ├── admin.py   # Dashboard admin
│   │   └── ...
│   ├── models/        # Models SQLAlchemy
│   ├── schemas/       # Schemas Pydantic
│   ├── core/          # Sécurité & config
│   └── ml/            # Pipeline ML
├── seed_db.py         # Script de seed
├── docker-compose.yml # Configuration Docker
└── requirements.txt   # Dépendances Python
```

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens).

**Pour accéder aux endpoints protégés:**
1. Se connecter via `/api/auth/login`
2. Récupérer le `access_token`
3. Ajouter le header: `Authorization: Bearer <token>`

## 🛠️ Commandes Utiles

```bash
# Réinitialiser la base de données
rm didacticiel.db
python seed_db.py

# Lancer les tests
pytest

# Voir les logs Docker
docker-compose logs -f api

# Arrêter Docker
docker-compose down
```

## 📝 Notes Importantes

- Le backend est configuré pour accepter CORS depuis `http://localhost:5173` (frontend Lovable)
- La base de données SQLite est utilisée par défaut (`didacticiel.db`)
- Pour passer à PostgreSQL, modifier `DATABASE_URL` dans `.env`

## 🐛 Troubleshooting

**Erreur de connexion à la DB:**
```bash
# Supprimer l'ancienne DB et recréer
rm didacticiel.db
python seed_db.py
```

**Port 8000 déjà utilisé:**
```bash
# Changer le port dans docker-compose.yml ou uvicorn
uvicorn app.main:app --port 8001
```

**CORS Error:**
- Vérifier que `FRONTEND_URL` dans `.env` correspond à l'URL du frontend

## 🎯 Prochaines Étapes

1. ✅ Lancer le backend
2. ✅ Tester avec Swagger UI
3. 🔄 Connecter le frontend Lovable
4. 🚀 Développer les fonctionnalités manquantes
