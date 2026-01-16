# Help-Desk - Compagnon du quotidien

> Un compagnon de soutien personnel TDAH-friendly pour faciliter le quotidien des personnes ayant un TDAH, de l'anxiété ou des difficultés émotionnelles.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/IjustStartPython/Help-Desk)
[![Python](https://img.shields.io/badge/python-3.13+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPL--3.0-orange.svg)](LICENSE)

---

## 📖 À propos de ce projet

Help-Desk est un projet personnel que j'ai développé pour **apprendre à créer une application complète en Python** tout en répondant à un vrai besoin : offrir un espace sécurisé et privé pour suivre son humeur, ses habitudes et dialoguer avec un assistant IA bienveillant.

###  Pourquoi ce projet ?

J'ai voulu créer une application qui :
-  **Respecte la vie privée** (données 100% locales)
-  **Soit simple et accessible** à utiliser (design TDAH-friendly)
-  **Intègre une IA locale** qui fonctionne sans envoyer de données dans le cloud
-  **Aide à mieux comprendre** ses émotions et habitudes
-  **Motive par la gamification** (points, badges, séries)

---

##  Fonctionnalités

###  Spécial TDAH

- ** Mode Focus** : Timer Pomodoro 25 min avec interface immersive et messages d'encouragement
- ** Système de gamification** :
  - Points automatiques (humeur, tâches, séries)
  - 7 badges à débloquer
  - Suivi des séries de jours consécutifs
  - Confettis et célébrations 🎉
- ** Dashboard TDAH** : Couleurs apaisantes (pas de rouge/noir)
- ** Thème optimisé** : Palette de couleurs douces (bleus, verts, lavande)
- ** Interface claire** : Espacements généreux, boutons larges (48px min)

### 💙 Fonctionnalités principales

- ** Profil personnalisé** : Création avec tags personnalisables
- ** Journal d'humeur** : Suivi quotidien avec émojis et notes
- ** Suivi d'habitudes** : Définir et suivre des tâches avec temps passé
- ** Chat IA local** : Discussion avec Mathi (assistant bienveillant via Ollama)
- ** Exports** : Génération de rapports PDF et Excel
- ** Sauvegardes** : Backup automatique au démarrage + backups manuels
- ** Sécurité** : Chiffrement optionnel (Fernet AES 128-bit)
- ** Visualisations** : Graphiques d'évolution de l'humeur

---

## 🛠️ Technologies utilisées

### Core
- **Python 3.13** - Langage de programmation
- **Streamlit** - Framework pour l'interface utilisateur
- **SQLite** - Base de données locale

### IA & Données
- **Ollama** - Modèle IA local (llama3.1:8b)
- **Pandas** - Analyse de données
- **Plotly** - Graphiques interactifs

### Sécurité & Export
- **Cryptography** - Chiffrement Fernet (AES 128-bit)
- **FPDF2** - Génération de PDF
- **openpyxl** - Export Excel

---

## 📁 Architecture du projet

J'ai organisé le code de manière **modulaire** pour faciliter la maintenance et l'évolution :

```
help-desk/
│
├── main.py                    # Point d'entrée de l'application
├── requirements.txt           # Dépendances Python
├── requirements-dev.txt       # Dépendances de développement
├── pytest.ini                 # Configuration des tests
│
├──Documentation/
│   ├── README.md              # Ce fichier
│   ├── CHANGELOG.md           # Historique des versions
│   ├── ROADMAP.md             # Fonctionnalités futures
│   ├── KNOWN_ISSUES.md        # Problèmes connus et limitations
│   ├── CONTRIBUTING.md        # Guide de contribution
│   ├── SECURITE.md            # Politique de sécurité
│   ├── GUIDE_UTILISATEUR.md   # Guide d'utilisation
│   ├── GUIDE_OLLAMA.md        # Installation Ollama
│   ├── GUIDE_SECURITE.md      # Guide chiffrement
│   └── REMERCIEMENTS.md       # Crédits et ressources
│
├──assets/                 # Ressources visuelles
│   ├── icon.ico               # Icône de l'application
│   └── theme.css              # Thème TDAH-friendly
│
├──db/                     # Couche base de données
│   ├── __init__.py
│   ├── database.py            # Connexion et configuration
│   └── models.py              # Schéma et requêtes SQL
│
├──services/               # Logique métier
│   ├── __init__.py
│   ├── backup_service.py      # Interface de gestion des backups
│   ├── chat_ai.py             # Interaction avec Ollama
│   ├── chat_service.py        # Gestion des conversations
│   ├── export_service.py      # Génération PDF/Excel
│   ├── habit_service.py       # Gestion des tâches
│   ├── mood_service.py        # Suivi de l'humeur
│   ├── profile_service.py     # Gestion du profil
│   ├── security_service.py    # Interface de chiffrement
│   └── tdah_features.py       # Gamification, Focus Mode, Points
│
├──ui/                      # Interface utilisateur
│   ├── __init__.py
│   ├── components.py          # Composants réutilisables
│   ├── layout.py              # Pages principales (Accueil, Plus, etc.)
│   └── tdah_dashboard.py      # Dashboard TDAH (Progrès)
│
├──utils/                  # Utilitaires
│   ├── __init__.py
│   ├── backup.py              # Système de backup automatique
│   ├── dates.py               # Gestion des dates
│   ├── encryption_config.py   # Configuration du chiffrement
│   ├── logger.py              # Logging centralisé
│   ├── safety.py              # Détection de détresse
│   ├── security.py            # Chiffrement Fernet
│   └── validation.py          # Validation des entrées
│
└──tests/                  # Tests unitaires
    ├── __init__.py
    ├── test_backup.py         # Tests du système de backup
    └── test_validation.py     # Tests de validation
```

---

## 🎯 Points techniques intéressants

###  Séparation des responsabilités (MVC)
- **Services** : Gèrent la logique métier (calcul de points, backup, export)
- **Models** : Gèrent l'accès aux données (SQLite)
- **UI** : Se concentre sur l'affichage (Streamlit)

###  Sécurité et confidentialité
- **Base de données SQLite** avec permissions restrictives (600)
- **Dossier `data/`** protégé (permissions 700)
- **Aucune connexion externe** pour les données personnelles
- **IA locale** via Ollama (pas de cloud)
- **Chiffrement optionnel** (Fernet AES 128-bit)
- **Backups automatiques** au démarrage
- **Validation** de toutes les entrées utilisateur

###  IA locale avec Ollama
- Utilisation du modèle **llama3.1:8b**
- Prompt système personnalisé pour un **ton bienveillant**
- **Détection de détresse** avec réponses appropriées
- **Pas de dépendance** à une API cloud

###  Système de gamification
- **Points automatiques** :
  - 10 pts : Humeur enregistrée
  - 20 pts : Tâche complétée
  - 30 pts : Tâche avec temps défini
  - 50-500 pts : Séries (3, 7, 14, 30 jours)
- **7 badges** : Premier Jour, Première Semaine, Maître des Émotions, etc.
- **Streaks** : Calcul automatique des jours consécutifs
- **Confettis** : À 30 jours de suite ! 🎉

###  Visualisations TDAH-friendly
- Couleurs apaisantes : **Ocean Blue** (#3B82F6), **Mint Green** (#10B981), **Lavender** (#A78BFA)
- Pas de **noir pur** ni de **rouge agressif**
- **Espacements généreux** (24px padding)

---

##  Installation

### Prérequis

- **Python 3.13+**
- **[Ollama](https://ollama.ai/)** (optionnel, pour le chat IA)

### Étapes

#### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/IjustStartPython/Help-Desk.git
cd Help-Desk
```

#### 2️⃣ Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

#### 4️⃣ (Optionnel) Installer Ollama

Voir le guide complet : [GUIDE_OLLAMA.md](Documentations/GUIDE_OLLAMA.md)

```bash
# Télécharger le modèle
ollama pull llama3.1:8b

# Démarrer Ollama
ollama serve
```

#### 5️⃣ Lancer l'application

```bash
streamlit run main.py
```

L'application s'ouvrira dans votre navigateur à l'adresse **`http://localhost:8501`**

---

## 📚 Utilisation

###  Première utilisation

1. **Créer ton profil** : Prénom, date de naissance, tags personnalisés (TDAH, anxiété, etc.)
2. **Découvrir l'interface** : Introduction interactive

###  Utilisation quotidienne

1. ** Enregistre ton humeur** : Slider 1-10, émotions, motivation, notes
2. ** Gère tes tâches** : Ajoute, complète, définis le temps passé
3. ** Discute avec Mathi** : Assistant IA bienveillant
4. ** Consulte tes stats** : Dashboard TDAH avec points, badges, séries
5. ** Utilise le Focus Mode** : Timer 25 min pour rester concentré

### ⚙️ Fonctionnalités avancées

- ** Export PDF/Excel** : Partage avec un professionnel
- ** Backups** : Automatiques au démarrage + manuels
- ** Chiffrement** : Active pour protéger tes notes (optionnel)
- ** Préférences** : Taille du texte, notifications, animations

---

## 🎓 Ce que j'apprends

En développant Help-Desk, j'ai approfondi mes connaissances en :

- **Architecture** : Pattern MVC, séparation des responsabilités
- **Python** : Streamlit, SQLite, Pandas, Cryptography
- **Base de données** : Schéma, migrations, requêtes SQL
- **IA locale** : Intégration Ollama, prompt engineering
- **Sécurité** : Chiffrement, permissions fichiers, validation
- **UX** : Design TDAH-friendly, gamification, accessibilité
- **Export** : Génération PDF (FPDF2), Excel (openpyxl)
- **Tests** : pytest, couverture de code
- **Documentation** : Guides utilisateur, contribution, sécurité

---

##  Limitations et améliorations futures

### Actuellement

- ⚠️ Mono-utilisateur (une seule personne par installation)
- ⚠️ IA nécessite Ollama installé localement
- ⚠️ Interface desktop uniquement

### Roadmap (voir [ROADMAP.md](ROADMAP.md))

#### v0.9.0 - Sécurité et Stabilité
- [ ] Clé de chiffrement dérivée depuis mot de passe utilisateur
- [ ] Permissions Windows (ACL)
- [ ] Système de versioning des migrations
- [ ] Logging complet avec rotation
- [ ] Backups dans %APPDATA%

#### v1.0.0 - Première Release Stable
- [ ] Documentation illustrée complète
- [ ] Anonymisation des exports
- [ ] Focus Mode robuste (détection rechargement)
- [ ] Couverture tests ≥ 80%

#### v2.0.0 - Multi-utilisateurs
- [ ] Support de plusieurs profils
- [ ] Authentification par mot de passe
- [ ] Statistiques avancées
- [ ] Première version mobile (Kivy/BeeWare)

#### v3.0.0 - Cloud Optionnel
- [ ] Synchronisation cloud chiffrée E2E
- [ ] App mobile native (React Native/Flutter)
- [ ] Notifications push
- [ ] API REST publique

---

## 🔒 Sécurité et vie privée

La protection de vos données est une **priorité absolue**.

### 🛡️ Mesures de sécurité

- ✅ **Données 100% locales** : Aucune connexion externe
- ✅ **IA locale** : Ollama fonctionne sur votre machine
- ✅ **Permissions restrictives** : DB (600), Dossier data (700)
- ✅ **Chiffrement optionnel** : Fernet AES 128-bit
- ✅ **Validation des entrées** : Protection contre les injections
- ✅ **Backups automatiques** : Au démarrage + manuels
- ✅ **Logging** : Traçabilité des opérations

### 📖 Pour en savoir plus

- [SECURITE.md](Documentations/SECURITE.md) - Politique de sécurité
- [GUIDE_SECURITE.md](Documentations/GUIDE_SECURITE.md) - Guide d'utilisation du chiffrement
- [KNOWN_ISSUES.md](Documentations/KNOWN_ISSUES.md) - Problèmes connus

---

## ⚠️ Avertissement

Cette application est un **outil de soutien personnel** et **ne remplace pas** un suivi professionnel médical ou psychologique.

Si tu traverses des difficultés importantes, **consulte un professionnel de santé**.

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Consulte [CONTRIBUTING.md](Documentations/CONTRIBUTING.md) pour :

- Signaler un bug
- Proposer une fonctionnalité
- Soumettre une Pull Request

---

## 📜 Licence

Ce projet est sous **GNU General Public License v3.0** - voir le fichier [LICENSE](Documentations/LICENSE) pour plus de détails.

---

## 🙏 Remerciements

Merci à :
- La communauté Python et Streamlit
- Les développeurs d'Ollama
- Tous ceux qui m'ont inspiré et aidé

Voir [REMERCIEMENTS.md](Documentations/REMERCIEMENTS.md) pour la liste complète.

---

## 📞 Contact

**Questions, suggestions, bugs ?**

Ouvre une [issue sur GitHub](https://github.com/IjustStartPython/Help-Desk/issues) !

---

<div align="center">

**Développé avec soin 💙 pour accompagner le quotidien de manière bienveillante et sécurisée.**

⭐ Si ce projet t'aide, n'hésite pas à mettre une étoile sur GitHub !

</div>
