# Didacticiel DevOps & MLOps - Backend API

Backend FastAPI pour la plateforme d'apprentissage DevOps & MLOps.

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16

### Installation

1. **Cloner le repo et naviguer vers le backend**
```bash
cd backend
```

2. **Créer l'environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement**
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

### Lancement avec Docker (Recommandé)
```bash
docker-compose up -d
```

L'API sera disponible sur: http://localhost:8000

Documentation interactive: http://localhost:8000/docs

### Lancement en développement local
```bash
uvicorn app.main:app --reload
```

## 📚 Documentation API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

### Endpoints d'authentification

- POST /api/auth/register - Inscription
- POST /api/auth/login - Connexion
- POST /api/auth/forgot-password - Mot de passe oublié
- GET /api/auth/me - Profil utilisateur

## 🗄️ Base de données

PostgreSQL avec SQLAlchemy ORM.

### Migrations avec Alembic
```bash
# Créer une migration
alembic revision --autogenerate -m "Description"

# Appliquer les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1
```

## 📁 Structure du Projet
```
backend/
├── app/
│   ├── api/          # Endpoints API
│   ├── core/         # Sécurité, config
│   ├── models/       # Models SQLAlchemy
│   ├── schemas/      # Schemas Pydantic
│   ├── services/     # Logique métier
│   └── ml/           # ML Pipeline
├── tests/            # Tests unitaires
├── alembic/          # Migrations DB
└── docker-compose.yml
```

## 🧪 Tests
```bash
pytest
```

## 📦 Technologies

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de données
- **Pydantic** - Validation
- **JWT** - Authentification
- **Docker** - Conteneurisation

## 👥 Rôles Utilisateurs

- student - Étudiant
- instructor - Formateur
- dmin - Administrateur

## 📝 License

MIT
