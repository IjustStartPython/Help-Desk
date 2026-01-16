# 📜 Changelog - Help-Desk

Tous les changements notables du projet Help-Desk sont documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet suit le [Semantic Versioning](https://semver.org/lang/fr/).

---

## [Non publié]

### À venir dans v0.9.0
- Correction problèmes sécurité critiques (#1, #2)
- Système de versioning des migrations (#3)
- Logging complet avec rotation (#5, #6)
- Déplacement backups dans %APPDATA% (#4)
- Couverture tests ≥ 60% (#8)

---

## [1.0.0] - 10 janvier 2026 *(Interne - Non publié)*

###  Release Majeure : Première Version test

**Version créée lors du développement, pas encore publiée publiquement.**

### Ajouté
-  **Installateur Windows professionnel** (Inno Setup)
  - Installation dans Program Files
  - Raccourcis bureau et menu Démarrer
  - Désinstallation propre
  - Taille : 101 MB (normale pour une app Streamlit/Pandas/Plotly)

-  **Audit de sécurité complet**
  - Script Python de scan automatique
  - Détection API keys, secrets, tokens
  - Détection données personnelles
  - Validation .gitignore
  - Aucune fuite de données détectée 

-  **Launcher GUI avec Tkinter**
  - Interface graphique pour lancer l'app
  - System tray avec icône personnalisée
  - Gestion processus Streamlit en arrière-plan

### Corrigé
-  **Processus Streamlit persistant après fermeture GUI**
  - Ajout de psutil pour terminaison propre
  - Méthode quit_app() améliorée
  - Tous les processus enfants terminés correctement


---

## [0.8.0] - 16 janvier 2026

###  Release TDAH : Fonctionnalités d'Optimisation Cognitive

**Basé sur 8 articles scientifiques** sur le TDAH et l'optimisation de l'engagement utilisateur.

### Ajouté

####  Système de Gamification Complet
- **Points automatiques** :
  - 10 pts : Humeur enregistrée
  - 20 pts : Tâche complétée
  - 30 pts : Tâche avec temps défini
  - 50-500 pts : Streaks (3, 7, 14, 30 jours)
  - 150 pts : Semaine complète
  - 40 pts : Toutes tâches terminées
  - 15 pts : Early bird (humeur avant 9h)
  - 25 pts : Consistance (5 jours/7)

- **7 Badges à débloquer** :
  - 🌱 Premier Jour (1 jour de suite)
  - 🌟 Première Semaine (7 jours)
  - 😊 Maître des Émotions (30 humeurs)
  - ⚔️ Guerrier des Tâches (50 tâches)
  - 👑 Roi de la Régularité (30 jours)
  - 💰 Collectionneur (1000 points)
  - 💬 Ami de Mathi (20 conversations)

- **Système de Streaks** :
  - Calcul automatique des jours consécutifs
  - Affichage visuel avec gradient animé
  - Confettis à 30 jours ! 

####  Mode Focus TDAH-Friendly
- **Timer Pomodoro 25 minutes** :
  - Affichage immersif plein écran
  - Minuteur géant (minutes:secondes)
  - Barre de progression personnalisée avec %
  - Messages d'encouragement adaptatifs selon temps restant
  - 8 tips bienveillants qui alternent toutes les 5 secondes
  - Auto-refresh pour mise à jour temps réel
  - Points bonus à la fin de session
  - Confettis de célébration ! 

- **Interface anti-distraction** :
  - Cache tous les éléments non essentiels
  - Focus total sur le timer
  - Couleurs apaisantes (bleus, verts, lavande)
  - Design épuré sans surcharge cognitive

####  Dashboard TDAH Dédié
- **Métriques clés en un coup d'œil** :
  -  Série actuelle (jours consécutifs)
  -  Points totaux
  -  Badges débloqués / Total
  
- **Aperçu des badges** :
  - 4 derniers badges débloqués
  - Icônes grande taille
  - Descriptions courtes


#### Thème CSS TDAH-Optimisé
- **Palette de couleurs** :
  - Primaire : #3B82F6 (Ocean Blue)
  - Secondaire : #10B981 (Mint Green)
  - Accent : #A78BFA (Lavender)
  - Texte : #2D3748 (Soft Charcoal)
  - Fond : #F7FAFC (Cloud White)

- **Design Principles** :
  - Espacement généreux (pas de claustrophobie visuelle)
  - Boutons larges et tactiles (min 48px)
  - Coins arrondis (border-radius: 12px)
  - Ombres douces pour profondeur
  - Pas de noir pur (éviter fatigue oculaire)

####  Architecture Backend
- **Table `points` (SQLite)** :
  ```sql
  CREATE TABLE points (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      action TEXT NOT NULL,
      points INTEGER NOT NULL,
      earned_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
  ```

- **4 Classes Python** :
  - `PointsSystem` : Gestion attribution/calcul points
  - `StreakSystem` : Calcul/affichage séries
  - `BadgeSystem` : Logique déblocage badges
  - `FocusMode` : Gestion timer et état

- **Fonctions utilitaires** :
  - `show_encouragement()` : Messages motivants aléatoires
  - `check_achievements()` : Détection nouveaux badges
  - `init_tdah_features()` : Initialisation au démarrage
  - `render_tdah_dashboard()` : Affichage dashboard complet

### Modifié
-  **Interface utilisateur complète repensée**
  - Ajout onglet "TDAH" dans dashboard
  - Intégration Mode Focus dans sidebar
  - Affichage streaks sur page d'accueil

- **Base de données étendue**
  - Nouvelle table `points` pour historique
  - Migration automatique au démarrage

- **Exports améliorés**
  - Graphiques avec palette TDAH
  - Inclusion statistiques gamification

### Corrigé (Phase 4.1)
-  **7 bugs critiques identifiés et corrigés** :
  1. Méthode `is_enable()` → `is_enabled()` (typo)
  2. Double import `datetime` et `date`
  3. Appel double `FocusMode.render_toggle()`
  4. Chemin CSS incorrect (`assets/theme.css` → `theme.css`)
  5. Table `points` manquante (ajout `init_points_table()`)
  6. Import manquant `time` dans FocusMode
  7. Erreurs syntaxe diverses


---

## [0.7.0] - 5 janvier 2026 *(Estimé)*

### Ajouté
-  **Profil utilisateur complet**
  - Nom, prénom, date de naissance
  - Tags personnalisés (TDAH, Anxiété, etc.)
  
-  **Journal d'humeur quotidien**
  - 6 émojis d'humeur
  - Notes textuelles optionnelles
  - Vérification "1 humeur par jour"

-  **Suivi des habitudes**
  - Création habitudes personnalisées
  - Marquage "fait/pas fait"
  - Calcul automatique streaks

-  **Chat IA local (Ollama)**
  - Intégration llama3.1:8b
  - Assistant bienveillant
  - Historique conversations

-  **Exports professionnels**
  - Export PDF (rapports)
  - Export Excel (données brutes)
  - Graphiques intégrés

-  **Système de backup**
  - Backup automatique au démarrage
  - Backup manuel sur demande
  - Conservation backups avec timestamps

### Architecture
-  **Structure MVC** :
  - `main.py` : Point d'entrée
  - `database.py` : Gestion SQLite
  - `models.py` : Schéma base de données
  - `*_service.py` : Logique métier
  - `layout.py` : Interface Streamlit

-  **Base de données SQLite** :
  - Table `profile`
  - Table `mood`
  - Table `tasks`
  - Table `habits`

---

## [0.6.0] - 30 décembre 2025 *(Estimé)*

### Ajouté
-  **Sécurité de base**
  - Validation inputs utilisateur
  - Module `validation.py`
  - Protection injections SQL basique

-  **Chiffrement optionnel**
  - Fernet (AES 128-bit)
  - Configuration `encryption_config.py`
  - Statut visible dans sidebar

### Modifié
-  Amélioration performances requêtes DB
-  Interface plus épurée

---

## [0.5.0] - 20 décembre 2025 *(Estimé)*

### Ajouté
-  **Tests unitaires**
  - `test_validation.py` (100% couverture)
  - `test_backup.py` (100% couverture)
  - Framework pytest

-  **Logging basique**
  - Module `logger.py`
  - Logs dans fichier

---

## [0.4.0] - 10 décembre 2025 *(Estimé)*

### Ajouté
-  Dashboard principal avec statistiques
-  Graphiques Matplotlib basiques
-  Page "Mes Habitudes"

---

## [0.3.0] - 1 décembre 2025 *(Estimé)*

### Ajouté
-  Système d'humeur avec emojis
-  Calendrier de visualisation
-  Zone de notes

---

## [0.2.0] - 20 novembre 2025 *(Estimé)*

### Ajouté
-  Page de création de profil
-  Premier thème CSS
-  Interface Streamlit de base

---

## [0.1.0] - 10 novembre 2025 *(Estimé)*

### Ajouté
-  Initialisation du projet
-  Configuration environnement Python
-  Première connexion SQLite
-  README initial

---

## Légende

-  **Ajouté** : Nouvelle fonctionnalité
-  **Modifié** : Changement fonctionnalité existante
-  **Corrigé** : Correction de bug
-  **Supprimé** : Fonctionnalité retirée
-  **Sécurité** : Correction vulnérabilité
-  **Documentation** : Changements docs uniquement

---

## Notes de Versioning

### Nomenclature
```
MAJOR.MINOR.PATCH-TAG

Exemples :
- 1.0.0       : Release stable
- 0.8.0-alpha : Développement actif
- 0.9.0-beta  : Tests pré-release
```

### Règles
- **MAJOR** : Changements incompatibles API
- **MINOR** : Nouvelles fonctionnalités (compatibles)
- **PATCH** : Corrections bugs (compatibles)

### Tags
- `-alpha` : Développement actif, instable
- `-beta` : Pré-release, tests utilisateurs
- `-rc` : Release Candidate, quasi-stable
- (aucun) : Release stable

---

## Contribution

Pour proposer des changements :
1. Consulte [CONTRIBUTING.md](CONTRIBUTING.md)
2. Ouvre une issue pour discuter
3. Crée une PR avec une description claire

Chaque PR doit mettre à jour ce CHANGELOG dans la section `[Non publié]`.

---

## Ressources

- **Repo GitHub** : [IjustStartPython/Help-Desk](https://github.com/IjustStartPython/Help-Desk)
- **Issues** : [github.com/IjustStartPython/Help-Desk/issues](https://github.com/IjustStartPython/Help-Desk/issues)
- **Roadmap** : [ROADMAP.md](ROADMAP.md)

---

**Dernière mise à jour** : 16 janvier 2026
