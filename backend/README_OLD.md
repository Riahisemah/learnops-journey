# 📡 Didacticiel DevOps & MLOps - Backend API

Backend FastAPI pour la plateforme d'apprentissage DevOps & MLOps, compatible avec le frontend Lovable.

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16 (ou utiliser Docker)

### Option 1 : Avec Docker (Recommandé) 🐳

1. **Cloner le repo et naviguer vers le backend**
```bash
cd backend
```

2. **Lancer les services avec Docker Compose**
```bash
docker-compose up -d
```

3. **Peupler la base de données avec des données de test**
```bash
docker-compose exec api python seed_db.py
```

4. **Accéder à l'API**
- API: http://localhost:8000
- Documentation Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Option 2 : Installation locale 💻

1. **Créer l'environnement virtuel**
```bash
python -m venv venv
```

2. **Activer l'environnement**
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

5. **Lancer PostgreSQL** (si pas déjà fait)
```bash
# Avec Docker
docker run -d \
  --name didacticiel_db \
  -e POSTGRES_USER=devops_user \
  -e POSTGRES_PASSWORD=devops_password \
  -e POSTGRES_DB=didacticiel_db \
  -p 5432:5432 \
  postgres:16-alpine
```

6. **Lancer l'application**
```bash
uvicorn app.main:app --reload
```

7. **Peupler la base de données**
```bash
python seed_db.py
```

## 📚 Documentation API

La documentation complète des endpoints est disponible sur :
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Voir aussi : `/docs/API_DOCUMENTATION.md`

## 🔐 Comptes de Test

Après avoir exécuté `seed_db.py`, vous pouvez utiliser :

### Admin
- **Email**: `admin@didacticiel.com`
- **Password**: `Admin123!`

### Instructor
- **Email**: `instructor@didacticiel.com`
- **Password**: `Instructor123!`

### Student
- **Email**: `jean.martin@student.com`
- **Password**: `Student123!`

## 🛠️ Endpoints Principaux

### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `GET /api/auth/me` - Profil utilisateur

### Utilisateurs
- `GET /api/users` - Liste (Admin)
- `GET /api/users/{id}` - Détails
- `PUT /api/users/{id}` - Mise à jour
- `GET /api/users/{id}/progression` - Progression

### Modules
- `GET /api/modules` - Liste
- `GET /api/modules/{id}` - Détails
- `POST /api/modules` - Créer (Admin)
- `GET /api/modules/{id}/lessons` - Leçons

### Quiz
- `GET /api/quizzes/{id}` - Récupérer quiz
- `POST /api/quizzes/{id}/submit` - Soumettre réponses

### Admin
- `GET /api/admin/stats` - Statistiques
- `GET /api/admin/analytics` - Analytiques

### ML
- `POST /api/ml/predict` - Prédiction

## 📁 Structure du Projet

```
backend/
├── app/
│   ├── api/              # Endpoints API
│   │   ├── auth.py       # Authentification
│   │   ├── users.py      # Gestion utilisateurs
│   │   ├── modules.py    # Modules & leçons
│   │   ├── quiz.py       # Quiz
│   │   ├── progress.py   # Progression
│   │   ├── admin.py      # Dashboard admin
│   │   └── ml_predict.py # ML predictions
│   ├── models/           # Models SQLAlchemy
│   ├── schemas/          # Schemas Pydantic
│   ├── core/             # Sécurité, config
│   ├── config.py         # Configuration
│   ├── database.py       # DB connection
│   └── main.py           # Application FastAPI
├── tests/                # Tests
├── seed_db.py            # Script de seed
├── requirements.txt      # Dépendances Python
├── Dockerfile            # Image Docker
├── docker-compose.yml    # Services Docker
└── README.md
```

## 🧪 Tests

```bash
pytest
```

## 🗄️ Base de Données

### Migrations avec Alembic

```bash
# Créer une migration
alembic revision --autogenerate -m "Description"

# Appliquer les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1
```

### Réinitialiser la DB

```bash
# Avec Docker
docker-compose down -v
docker-compose up -d
docker-compose exec api python seed_db.py
```

## 🔧 Variables d'Environnement

Créer un fichier `.env` :

```env
DATABASE_URL=postgresql://devops_user:devops_password@localhost:5432/didacticiel_db
SECRET_KEY=votre-clé-secrète-très-longue
FRONTEND_URL=http://localhost:5173
DEBUG=True
```

## 📦 Technologies

- **FastAPI** - Framework web moderne
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de données
- **Pydantic** - Validation
- **JWT** - Authentification
- **Docker** - Conteneurisation
- **Alembic** - Migrations DB

## 🔒 Sécurité

- Mots de passe hashés avec bcrypt
- Tokens JWT pour l'authentification
- CORS configuré
- Validation des inputs avec Pydantic
- RBAC (Role-Based Access Control)

## 🌐 CORS

Le backend accepte les requêtes depuis :
- `http://localhost:5173` (Vite)
- `http://localhost:3000` (Create React App)

Modifiable dans `app/main.py`

## 📝 Logs

Les logs sont affichés dans la console. Pour les sauvegarder :

```bash
uvicorn app.main:app --log-level info > app.log 2>&1
```

## 🚨 Troubleshooting

### Erreur de connexion à la DB
```bash
# Vérifier que PostgreSQL est lancé
docker ps | grep didacticiel_db

# Vérifier les logs
docker logs didacticiel_db
```

### Port 8000 déjà utilisé
```bash
# Changer le port dans docker-compose.yml
ports:
  - "8001:8000"
```

### ImportError
```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

## 📄 License

MIT

## 👥 Contributeurs

- Backend API développé pour le projet Didacticiel DevOps & MLOps

## 🔗 Liens Utiles

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)

---

**Note**: Ce backend est conçu pour être 100% compatible avec le frontend Lovable. Toutes les routes et formats de données correspondent exactement à la documentation API attendue par le frontend.
