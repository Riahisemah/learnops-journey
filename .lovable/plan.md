

# Didacticiel DevOps & MLOps - Plan d'implémentation

## Vue d'ensemble
Application web éducative moderne avec 4 modules répartis sur 4 semaines, style "learning platform" comme Udemy/Coursera.

---

## 🎨 Design & Thème

**Palette de couleurs tech :**
- Bleu marine principal (#1e3a5f)
- Vert tech pour les accents/succès (#10b981)
- Gris modernes pour le fond et texte
- Mode clair/sombre avec toggle dans le header

**Style visuel :**
- Cards avec ombres douces et coins arrondis
- Icônes Lucide pour clarté visuelle
- Animations subtiles sur les interactions
- Design responsive (mobile-first)

---

## 📄 Pages & Structure

### 1. Page d'accueil
- **Hero section** avec titre accrocheur et illustration tech
- **Timeline visuelle** des 4 semaines avec preview des modules
- **Carte statistiques** : progression globale, temps estimé, badges gagnés
- **Bouton CTA** "Commencer le parcours" bien visible

### 2. Page Module (x4)
- En-tête avec titre, description et barre de progression
- Liste des leçons avec :
  - Icônes par type (📹 vidéo, 📖 texte, ❓ quiz, 💻 pratique)
  - Durée estimée
  - Statut (✅ Complété, 🔄 En cours, 🔒 Verrouillé)
- Bouton "Leçon suivante" contextuel

### 3. Page Leçon
- Contenu de la leçon (placeholder pour l'instant)
- Boutons navigation précédent/suivant
- Bouton "Marquer comme terminé"

---

## 🧭 Navigation

**Sidebar latérale persistante :**
- Logo/titre de l'application
- 4 modules avec indicateur de progression
- Section profil/statistiques en bas
- Collapsible sur mobile

**Header :**
- Toggle mode sombre
- Indicateur de progression global

---

## 🎮 Gamification (Simple)

- **Barre de progression** par module (% de leçons complétées)
- **Badges de module** : badge débloqué à la complétion de chaque module
- **Statistiques** : nombre de leçons terminées, temps passé
- Tout sauvegardé en **LocalStorage**

---

## 📚 Contenu des modules (Placeholder)

**Module 1 : DevOps Basics**
- Introduction au DevOps
- CI/CD avec GitHub Actions
- Docker fondamentaux
- Docker Compose

**Module 2 : MLOps Fundamentals**
- Introduction au MLOps
- Versioning avec DVC
- MLflow pour le tracking
- Gestion des expériences

**Module 3 : Déploiement & API**
- FastAPI pour ML
- Containerisation de modèles
- Déploiement cloud
- Monitoring

**Module 4 : Évaluation finale**
- Projet récapitulatif
- Quiz final
- Ressources complémentaires

---

## ⚙️ Fonctionnalités techniques

- **React Router** pour la navigation entre pages
- **LocalStorage** pour sauvegarder la progression utilisateur
- **next-themes** pour le mode clair/sombre
- **Recharts** pour les visualisations de progression (optionnel)
- Structure de données modulaire pour faciliter l'ajout de contenu

