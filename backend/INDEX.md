# 📁 Backend FastAPI - Index des Fichiers

## 🚀 DÉMARRAGE RAPIDE

**Commandes essentielles :**
```bash
pip install -r requirements.txt
python seed_db.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**URLs :**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## 📚 DOCUMENTATION À LIRE EN PREMIER

1. **README.md** ⭐ START HERE
   - Vue d'ensemble du projet
   - Installation rapide
   - Fonctionnalités principales

2. **QUICKSTART.md**
   - Guide de démarrage en 5 minutes
   - Étapes détaillées
   - Troubleshooting

3. **API_REFERENCE.md**
   - Tous les endpoints
   - Formats de requête/réponse
   - Codes d'erreur

4. **INTEGRATION_GUIDE.md**
   - Comment connecter Lovable
   - Exemples de code TypeScript
   - Services React

5. **SUMMARY.md**
   - Récapitulatif de tout ce qui a été créé
   - Statistiques du projet
   - Checklist

---

## 🔑 FICHIERS IMPORTANTS

### Configuration
- **.env** - Variables d'environnement (MODIFIER AVANT UTILISATION)
- **requirements.txt** - Dépendances Python
- **docker-compose.yml** - Configuration Docker

### Scripts Utiles
- **seed_db.py** - Créer les données de test (À EXÉCUTER EN PREMIER)
- **test_api.py** - Tester que l'API fonctionne

### Code Principal
- **app/main.py** - Point d'entrée FastAPI
- **app/config.py** - Configuration de l'app
- **app/database.py** - Connexion base de données

---

## 🗂️ STRUCTURE COMPLÈTE

```
backend/
│
├── 📚 DOCUMENTATION
│   ├── README.md              ⭐ Commencer ici
│   ├── QUICKSTART.md          Guide de démarrage
│   ├── API_REFERENCE.md       Référence API
│   ├── INTEGRATION_GUIDE.md   Intégration Lovable
│   ├── SUMMARY.md             Récapitulatif
│   └── INDEX.md               Ce fichier
│
├── ⚙️ CONFIGURATION
│   ├── .env                   Variables d'environnement
│   ├── requirements.txt       Dépendances Python
│   ├── Dockerfile             Image Docker
│   └── docker-compose.yml     Orchestration
│
├── 🔧 SCRIPTS
│   ├── seed_db.py             Peupler la DB
│   └── test_api.py            Tester l'API
│
├── 📁 app/
│   ├── main.py                Point d'entrée
│   ├── config.py              Configuration
│   ├── database.py            Connexion DB
│   │
│   ├── 🔌 api/                Endpoints
│   │   ├── auth.py            Authentification
│   │   ├── users.py           Utilisateurs
│   │   ├── modules.py         Modules
│   │   ├── lessons.py         Leçons
│   │   ├── quiz.py            Quiz
│   │   ├── progress.py        Progression
│   │   ├── admin.py           Dashboard admin
│   │   ├── ml_predict.py      ML
│   │   └── deps.py            Dépendances
│   │
│   ├── 🗄️ models/             Models SQLAlchemy
│   │   ├── user.py
│   │   ├── module.py
│   │   ├── lesson.py
│   │   ├── quiz.py
│   │   └── progression.py
│   │
│   ├── 📋 schemas/            Schemas Pydantic
│   │   ├── user.py
│   │   ├── module.py
│   │   ├── quiz.py
│   │   ├── admin.py
│   │   ├── progression.py
│   │   └── ml.py
│   │
│   └── 🔒 core/               Sécurité
│       ├── security.py        JWT, hashing
│       └── permissions.py     Rôles
│
├── 🧪 tests/                  Tests
└── 🗄️ alembic/               Migrations DB
```

---

## 🎯 WORKFLOW RECOMMANDÉ

### Première fois
1. ✅ Lire **README.md**
2. ✅ Lire **QUICKSTART.md**
3. ✅ Exécuter `pip install -r requirements.txt`
4. ✅ Exécuter `python seed_db.py`
5. ✅ Lancer `uvicorn app.main:app --reload`
6. ✅ Ouvrir http://localhost:8000/docs
7. ✅ Tester avec `python test_api.py`

### Développement
1. 📖 Consulter **API_REFERENCE.md** pour les endpoints
2. 🔗 Suivre **INTEGRATION_GUIDE.md** pour connecter Lovable
3. 🧪 Utiliser Swagger UI pour tester
4. 📝 Modifier le code selon tes besoins

---

## 👤 COMPTES DE TEST

| Rôle | Email | Password |
|------|-------|----------|
| Admin | admin@didacticiel.com | Admin123! |
| Formateur | instructor@didacticiel.com | Instructor123! |
| Étudiant | jean.martin@student.com | Student123! |

---

## 🔍 RECHERCHE RAPIDE

**Je veux...**

- Démarrer rapidement → **QUICKSTART.md**
- Voir tous les endpoints → **API_REFERENCE.md**
- Connecter Lovable → **INTEGRATION_GUIDE.md**
- Comprendre le projet → **README.md**
- Voir ce qui a été fait → **SUMMARY.md**
- Tester l'API → **test_api.py**
- Créer des données → **seed_db.py**

---

## 📞 RESSOURCES

- 🌐 API en cours d'exécution : http://localhost:8000
- 📚 Documentation Swagger : http://localhost:8000/docs
- 📖 Documentation ReDoc : http://localhost:8000/redoc
- ❤️ Health Check : http://localhost:8000/health

---

## ⚡ COMMANDES RAPIDES

```bash
# Installer
pip install -r requirements.txt

# Créer la DB
python seed_db.py

# Lancer
uvicorn app.main:app --reload

# Tester
python test_api.py

# Docker
docker-compose up -d
docker-compose exec api python seed_db.py

# Réinitialiser DB
rm didacticiel.db
python seed_db.py
```

---

<div align="center">

## 🎉 Tout est prêt !

**Commence par lire README.md**

Ensuite suis QUICKSTART.md pour lancer l'API

</div>
