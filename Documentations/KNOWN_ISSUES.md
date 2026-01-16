#  Issues Connues - Help-Desk v0.8.0

> Ce document liste toutes les issues identifiées dans le projet et leur plan de correction.

**Dernière mise à jour :** 16 janvier 2025

---

## 🔴 Problèmes critiques (Sécurité)

### #1 - Requêtes SQL avec f-strings dans render_today_mood()
- **Impact :** 🔴 Critique - Injection SQL possible
- **Fichier :** `ui/layout.py:744`
- **Description :** La fonction `render_today_mood()` construit des requêtes SQL dynamiques à l'aide de f-strings. Si des données utilisateur ou variables non maîtrisées sont injectées dans la requête, un attaquant peut modifier la logique SQL (exécution de requêtes arbitraires, accès ou suppression de données).
- **Solution prévue :** Remplacer les f-strings par des requêtes paramétrées (placeholders `?` ou `%s` selon le driver SQL utilisé) et valider strictement les entrées avant exécution.
- **Statut :** 🔜 À faire

### #2 - Pas de validation sur les inputs utilisateur
- **Impact :** 🔴 Critique - Injection, corruption de données
- **Fichier :** `ui/layout.py` (profil_form())
- **Description :** La fonction `profil_form()` ne valide ni ne sanitise les entrées utilisateur avant leur traitement ou enregistrement. Des valeurs malformées ou malveillantes peuvent être injectées (SQL, XSS, données incohérentes), entraînant des failles de sécurité ou une corruption des données.
- **Solution prévue :** 
  - Implémenter une validation stricte côté serveur (types, longueurs, formats, valeurs autorisées)
  - Nettoyer les entrées utilisateur (escaping/sanitization)
  - Rejeter explicitement toute donnée invalide avant traitement
- **Statut :** 🔜 À faire

### #3 - Clé de chiffrement stockée en clair
- **Impact :** 🔴 Critique - Sécurité compromise
- **Fichier :** `data/secret.key`
- **Description :** La clé de chiffrement est stockée en clair dans `data/secret.key`. N'importe qui ayant accès au fichier peut déchiffrer les données. Pas de protection supplémentaire.
- **Solution prévue :** Dériver la clé depuis un mot de passe utilisateur avec PBKDF2 (SHA-256, 100 000 itérations)
- **Statut :** 🔜 À faire

### #4 - Session Streamlit partagée entre utilisateurs
- **Impact :** 🔴 Critique - Fuite de données utilisateur
- **Fichier :** `db/database.py` (check_same_thread=False)
- **Description :** La connexion SQLite est créée avec `check_same_thread=False`, permettant le partage de session entre plusieurs utilisateurs potentiels. En environnement multi-utilisateurs, cela peut causer des fuites de données ou des corruptions.
- **Solution prévue :** 
  - Créer une connexion par session utilisateur
  - Utiliser un pool de connexions approprié
  - Activer `check_same_thread=True` et gérer correctement les threads
- **Statut :** 🔜 À faire

### #5 - Permissions Windows inexistantes
- **Impact :** 🔴 Critique - Fichiers accessibles à tous
- **Fichiers :** `db/database.py:126`, `utils/backup.py:29,58,99`
- **Description :** Sur Windows, les permissions NTFS par défaut sont appliquées. Les fichiers sensibles (DB, backups, clé de chiffrement) ne sont pas restreints explicitement.
- **Solution prévue :** Implémenter ACL Windows avec `icacls` ou `pywin32` pour restreindre l'accès au propriétaire uniquement
- **Statut :** 🔜 À faire

---

## 🟠 Problèmes critiques (Logique/Bugs)

### #6 - Division par zéro dans BadgeSystem
- **Impact :** 🟠 Critique - Crash possible
- **Fichier :** `services/gamification.py` (BadgeSystem)
- **Description :** Division par zéro possible dans `BadgeSystem` si aucune tâche n'existe lors du calcul de statistiques (ex: taux de complétion)
- **Solution prévue :** 
  - Vérifier que le dénominateur n'est pas zéro avant division
  - Retourner une valeur par défaut (0 ou None) si aucune donnée
- **Statut :** 🔜 À faire

### #7 - Gestion des exceptions manquante dans close_connection()
- **Impact :** 🟠 Critique - Fuites de connexions
- **Fichier :** `db/database.py` (close_connection())
- **Description :** Aucune gestion d'erreur si la fermeture de connexion échoue. Les connexions peuvent rester ouvertes et causer des fuites mémoire.
- **Solution prévue :** 
  - Entourer de try/except
  - Logger les erreurs
  - S'assurer que les ressources sont libérées même en cas d'erreur
- **Statut :** 🔜 À faire


- **Impact :** 🟠 Critique - Schéma incomplet
- **Fichier :** `db/models.py:60-69`
- **Description :** La migration `database()` peut échouer si la table `tasks` n'existe pas encore lors de l'exécution d'`ALTER TABLE`. Utilise `try/except` sans versioning.
- **Solution prévue :** 
  - Vérifier l'existence de la table avant ALTER
  - Créer une table `schema_version` pour tracker les migrations
  - Implémenter un système de migrations versionnées
- **Statut :** 🔜 À faire

### #9 - Mode Focus actualise toutes les secondes
- **Impact :** 🟠 Critique - Surcharge serveur
- **Fichier :** `services/focus_mode.py`
- **Description :** Le Mode Focus force un refresh Streamlit toutes les secondes pour mettre à jour le timer, causant une surcharge serveur inutile.
- **Solution prévue :** 
  - Utiliser JavaScript côté client pour le timer
  - Ne rafraîchir que quand nécessaire (fin du timer)
  - Implémenter avec `st.components.v1.html`
- **Statut :** 🔜 À faire

### #10 - st.session_state.conn non vérifié
- **Impact :** 🟠 Critique - Erreurs runtime
- **Fichier :** Plusieurs fonctions dans `ui/layout.py`
- **Description :** Plusieurs fonctions utilisent `st.session_state.conn` sans vérifier son existence préalable, causant des KeyError si la connexion n'est pas initialisée.
- **Solution prévue :** 
  - Vérifier systématiquement `if 'conn' in st.session_state and st.session_state.conn`
  - Initialiser la connexion dans un hook de session
  - Créer une fonction wrapper sécurisée
- **Statut :** 🔜 À faire

### #11 - check_mood_logged_today() ne gère pas les erreurs DB
- **Impact :** 🟠 Critique - Crash silencieux
- **Fichier :** `services/mood.py` (check_mood_logged_today())
- **Description :** Aucune gestion d'erreur si la requête SQL échoue (connexion perdue, DB corrompue). L'application peut crasher silencieusement.
- **Solution prévue :** 
  - Entourer de try/except
  - Logger les erreurs
  - Retourner une valeur par défaut sûre (False)
- **Statut :** 🔜 À faire

### #12 - StreakSystem retourne 0 silencieusement
- **Impact :** 🟠 Moyen - Données incorrectes
- **Fichier :** `services/gamification.py` (StreakSystem.calculate_streak())
- **Description :** Si le parsing de date échoue, la fonction retourne 0 sans erreur ni log. L'utilisateur ne sait pas pourquoi son streak est perdu.
- **Solution prévue :** 
  - Logger les erreurs de parsing
  - Retourner un tuple (streak, error_message)
  - Afficher un avertissement à l'utilisateur
- **Statut :** 🔜 À faire

### #13 - FocusMode bug si durée > 1h
- **Impact :** 🟠 Critique - Timer incorrect
- **Fichier :** `services/focus_mode.py` (get_remaining_time())
- **Description :** Utilise `.seconds` au lieu de `.total_seconds()` sur un timedelta. Pour une durée > 1h, `.seconds` ne compte que les secondes restantes après les heures complètes (max 3599s).
- **Solution prévue :** Remplacer `.seconds` par `.total_seconds()` puis convertir en int
- **Statut :** 🔜 À faire

---

## 🟡 Problèmes moyens (Performance)

### #14 - Requêtes SQL répétées dans render_sidebar()
- **Impact :** 🟡 Moyen - Performance dégradée
- **Fichier :** `ui/layout.py` (render_sidebar())
- **Description :** `render_sidebar()` exécute les mêmes requêtes SQL à chaque refresh de page (statistiques, badges, streaks). Avec beaucoup de données, cela ralentit l'application.
- **Solution prévue :** 
  - Utiliser `@st.cache_data` avec TTL (ex: 60 secondes)
  - Invalider le cache uniquement quand les données changent
- **Statut :** 🔜 À faire

### #15 - Pas de cache sur get_mood_history() et get_today_tasks()
- **Impact :** 🟡 Moyen - Requêtes inutiles
- **Fichier :** `services/mood.py`, `services/tasks.py`
- **Description :** Ces fonctions sont appelées plusieurs fois par page sans cache. Les mêmes données sont re-fetchées à chaque fois.
- **Solution prévue :** 
  - Ajouter `@st.cache_data(ttl=60)` avec invalidation sur mutation
  - Utiliser un hash des paramètres comme clé de cache
- **Statut :** 🔜 À faire

### #16 - Backup automatique sans throttling
- **Impact :** 🟡 Moyen - I/O disque excessif
- **Fichier :** `utils/backup.py:13`
- **Description :** Un backup automatique est créé à chaque démarrage de l'application sans vérifier la date du dernier backup. Si l'utilisateur relance l'app 10 fois/jour, 10 backups sont créés.
- **Solution prévue :** 
  - Vérifier la date du dernier backup
  - Ne créer un backup que si >24h depuis le dernier
  - Implémenter un système de rotation (garder 7 derniers jours)
- **Statut :** 🔜 À faire

### #17 - check_achievements() vérifie tous les badges
- **Impact :** 🟡 Moyen - CPU gaspillé
- **Fichier :** `services/gamification.py` (check_achievements())
- **Description :** À chaque appel, tous les badges sont re-vérifiés même si déjà débloqués. Avec 50+ badges, cela devient lent.
- **Solution prévue :** 
  - Filtrer les badges déjà débloqués avant vérification
  - Indexer la table badges par (user_id, unlocked)
  - Mettre en cache la liste des badges débloqués
- **Statut :** 🔜 À faire

---

## 🟡 Problèmes moyens (Mauvaises pratiques)

### #18 - Variables globales implicites via st.session_state
- **Impact :** 🟡 Moyen - Code difficile à tester
- **Fichier :** Partout dans le code
- **Description :** L'état de l'application est géré via `st.session_state` qui agit comme une variable globale. Rend le code difficile à tester et à maintenir.
- **Solution prévue :** 
  - Créer une classe AppState pour encapsuler l'état
  - Passer explicitement l'état aux fonctions
  - Faciliter les tests unitaires
- **Statut :** 🔜 À faire

### #19 - Imports dans les fonctions
- **Impact :** 🟡 Moyen - Performance et lisibilité
- **Fichier :** `ui/layout.py:278,358`, etc.
- **Description :** Des imports sont effectués à l'intérieur des fonctions au lieu d'être en haut du fichier. Ralentit l'exécution et rend le code moins lisible.
- **Solution prévue :** Déplacer tous les imports en haut des fichiers
- **Statut :** 🔜 À faire

### #20 - Fonctions trop longues
- **Impact :** 🟡 Moyen - Maintenabilité
- **Fichier :** `ui/layout.py` (render_more_tab = 250+ lignes)
- **Description :** Certaines fonctions dépassent 200-300 lignes, violant le principe de responsabilité unique. Difficile à comprendre et à tester.
- **Solution prévue :** 
  - Découper en sous-fonctions logiques
  - Extraire la logique métier dans les services
  - Limiter à 50 lignes max par fonction
- **Statut :** 🔜 À faire

### #21 - Pas de séparation models/controllers/views claire
- **Impact :** 🟡 Moyen - Architecture confuse
- **Fichier :** Structure globale du projet
- **Description :** Logique métier, accès DB et UI sont mélangés. Pas de pattern MVC ou architecture claire.
- **Solution prévue :** 
  - Séparer models (DB), services (logique), controllers (orchestration), views (UI)
  - Définir des interfaces claires entre couches
- **Statut :** 🔜 À faire

### #22 - Magic numbers partout
- **Impact :** 🟡 Moyen - Code illisible
- **Fichier :** Partout (25*60, 0.25, etc.)
- **Description :** Des nombres "magiques" sont hardcodés (durées, seuils, multiplicateurs) au lieu d'être définis comme constantes nommées.
- **Solution prévue :** 
  - Créer un fichier `constants.py`
  - Définir FOCUS_DURATION = 25 * 60, etc.
  - Documenter la signification de chaque constante
- **Statut :** 🔜 À faire

### #23 - Noms de variables pas clairs
- **Impact :** 🟡 Moyen - Lisibilité
- **Fichier :** Partout (cur, conn, df)
- **Description :** Variables avec des noms trop courts ou ambigus (cur → cursor, conn → connection, df → dataframe). Rend le code difficile à comprendre.
- **Solution prévue :** 
  - Renommer avec des noms explicites
  - Suivre PEP 8 (snake_case, noms descriptifs)
  - Ajouter des type hints
- **Statut :** 🔜 À faire

### #24 - Mélange français/anglais
- **Impact :** 🟡 Moyen - Cohérence
- **Fichier :** Partout
- **Description :** Mélange de français (commentaires, variables) et anglais (noms de fonctions, code). Incohérent et confus.
- **Solution prévue :** 
  - Choisir une langue unique (anglais recommandé)
  - Traduire progressivement
  - Garder le français uniquement dans l'UI
- **Statut :** 🔜 À faire

### #25 - Pas de docstrings complètes
- **Impact :** 🟡 Moyen - Documentation
- **Fichier :** Toutes les fonctions
- **Description :** La plupart des fonctions n'ont pas de docstrings ou des docstrings incomplètes (pas de types, returns, examples).
- **Solution prévue :** 
  - Ajouter docstrings Google Style à toutes les fonctions
  - Documenter paramètres, types, retours, exceptions
  - Ajouter des exemples pour les fonctions complexes
- **Statut :** 🔜 À faire

---

## 🟢 Améliorations souhaitées (UI/UX)

### #26 - Sidebar scrollable si petit écran
- **Impact :** 🟢 Faible - UX mobile
- **Fichier :** `ui/layout.py` (render_sidebar())
- **Description :** Sur petits écrans (<768px), la sidebar n'est pas scrollable et coupe du contenu.
- **Solution prévue :** 
  - Ajouter CSS custom pour scrollbar sur sidebar
  - Tester sur mobile
- **Statut :** 🔜 À faire

### #27 - Notifications de badges non persistantes
- **Impact :** 🟢 Faible - UX gamification
- **Fichier :** `services/gamification.py`
- **Description :** Les notifications de badges débloqués disparaissent après un refresh de page. L'utilisateur peut les manquer.
- **Solution prévue :** 
  - Stocker les badges non-vus dans la DB
  - Afficher une alerte persistante jusqu'à ce qu'elle soit fermée
- **Statut :** 🔜 À faire

### #28 - Pas de confirmation avant suppression
- **Impact :** 🟢 Faible - UX sécurité
- **Fichier :** `ui/layout.py` (suppression de tâche)
- **Description :** Les tâches peuvent être supprimées sans confirmation. Risque de suppression accidentelle.
- **Solution prévue :** 
  - Ajouter un dialog de confirmation
  - Proposer un bouton "Annuler" pendant 5 secondes
- **Statut :** 🔜 À faire

### #29 - Boutons "Supprimer" en rouge agressif
- **Impact :** 🟢 Faible - UX TDAH
- **Fichier :** `ui/layout.py`
- **Description :** Les boutons de suppression sont en rouge vif, ce qui peut être stressant pour les utilisateurs TDAH.
- **Solution prévue :** 
  - Utiliser un rouge plus doux (#DC3545 → #E57373)
  - Proposer un thème "Calme" dans les paramètres
- **Statut :** 🔜 À faire

---

## 🟢 Améliorations souhaitées (Architecture)

### #30 - database.py importe streamlit
- **Impact :** 🟢 Faible - Couplage fort
- **Fichier :** `db/database.py`
- **Description :** La couche DB importe Streamlit, créant un couplage fort. Impossible d'utiliser la DB sans Streamlit (tests, CLI, etc.).
- **Solution prévue :** 
  - Retirer tous les imports streamlit de db/
  - Passer les paramètres explicitement
  - Rendre la couche DB indépendante
- **Statut :** 🔜 À faire

### #31 - Pas de gestion des migrations versionnées
- **Impact :** 🟢 Faible - Maintenabilité
- **Fichier :** `db/models.py:60-69`
- **Description :** Les migrations utilisent `try/except` sur `ALTER TABLE` sans versioning. Impossible de savoir quelle version de schéma est installée, de rollback, ou de tracer l'historique.
- **Solution prévue :** 
  - Créer une table `schema_version`
  - Numéroter les migrations (001_initial.sql, 002_add_column.sql)
  - Implémenter un runner de migrations
- **Statut :** 🔜 À faire

### #32 - Pas de tests unitaires
- **Impact :** 🟢 Faible - Qualité
- **Fichier :** `tests/` vide
- **Description :** Aucun test unitaire n'existe. Impossible de vérifier que les modifications ne cassent pas l'existant.
- **Solution prévue :** 
  - Créer `pytest.ini`
  - Écrire tests pour services critiques (mood, tasks, gamification)
  - Viser 80%+ de couverture de code
- **Statut :** 🔜 À faire

### #33 - Pas de logging structuré
- **Impact :** 🟢 Faible - Debugging
- **Fichier :** Utilise `print()` partout
- **Description :** Le logging utilise `print()` au lieu d'un logger structuré. Impossible de filtrer par niveau, de router vers des fichiers, ou d'analyser les logs.
- **Solution prévue :** 
  - Implémenter `logging` Python standard
  - Créer des loggers par module
  - Ajouter rotation des logs (28 jours)
- **Statut :** 🔜 À faire

### #34 - Configuration en dur dans le code
- **Impact :** 🟢 Faible - Flexibilité
- **Fichier :** Partout (DB_PATH, durées, etc.)
- **Description :** Toute la configuration est hardcodée (chemins, durées, seuils). Impossible de changer sans modifier le code.
- **Solution prévue :** 
  - Créer `config.py` ou `settings.yaml`
  - Utiliser variables d'environnement
  - Permettre override par fichier de config utilisateur
- **Statut :** 🔜 À faire

---

## 🟢 Améliorations souhaitées (Documentation)


### #35 - Pas de CONTRIBUTING.md à jour
- **Impact :** 🟢 Faible - Contribution
- **Fichier :** `CONTRIBUTING.md` obsolète
- **Description :** Le guide de contribution n'est pas à jour avec la structure actuelle du projet.
- **Solution prévue :** 
  - Mettre à jour avec architecture actuelle
  - Documenter workflow Git
  - Ajouter guide de style de code
- **Statut :** 🔜 À faire

### #36 - Commentaires manquants sur logique complexe
- **Impact :** 🟢 Faible - Compréhension
- **Fichier :** `services/gamification.py` (streaks, points)
- **Description :** Les calculs complexes (streaks, multiplicateurs de points) ne sont pas commentés. Difficile de comprendre la logique.
- **Solution prévue :** 
  - Ajouter commentaires explicatifs sur algorithmes
  - Documenter les formules de calcul
  - Ajouter des exemples concrets
- **Statut :** 🔜 À faire


### #37 - Backups dans dossier local (incohérent)
- **Impact :** 🟢 Faible - Cohérence
- **Fichier :** `utils/backup.py:13`
- **Description :** Les backups sont stockés dans `data/backups/` (relatif au projet) alors que la DB est dans `%APPDATA%`. Si le projet est supprimé, les backups sont perdus.
- **Solution prévue :** Déplacer vers `%APPDATA%/Help-Desk/backups/` (Windows) ou `~/.local/share/Help-Desk/backups/` (Linux/Mac)
- **Statut :** 🔜 À faire

### #38 - Exports non anonymisables
- **Impact :** 🟢 Faible - Vie privée
- **Fichier :** Services d'export PDF/Excel
- **Description :** Les exports contiennent le prénom, empêchant leur partage anonyme avec un professionnel.
- **Solution prévue :** Ajouter checkbox "Anonymiser" dans l'UI (remplace prénom par "Utilisateur")
- **Statut :** 🔜 À faire

### #39 - Focus Mode contournable (F5)
- **Impact :** 🟢 Faible - UX TDAH
- **Fichier :** `services/focus_mode.py`
- **Description :** Le timer redémarre si l'utilisateur recharge la page (F5).
- **Solution prévue :** Détecter rechargement et proposer de reprendre la session
- **Statut :** 🔜 À faire

---

## 📊 Statistiques

- **Total issues :** 39
- **Critiques Sécurité (🔴) :** 5
- **Critiques Logique (🟠) :** 8
- **Moyennes Performance (🟡) :** 4
- **Moyennes Pratiques (🟡) :** 8
- **Faibles UI/UX (🟢) :** 4
- **Faibles Architecture (🟢) :** 5
- **Faibles Documentation (🟢) :** 5

### Répartition par priorité
- **🔴 Haute :** #1, #2, #3, #4, #5, #6, #7, #8, #9, #10, #11, #13 (12 issues)
- **🟠 Moyenne :** #12, #14, #15, #16, #17, #18, #19, #20, #21 (9 issues)
- **🟡 Basse :** #22-#41 (20 issues)

---


## 🤝 Contribuer

Tu veux corriger une de ces issues ? 

1. Choisis une issue
2. Crée une branche : `git checkout -b fix/issue-XX`
3. Fais tes modifications
4. Teste bien
5. Commit : `git commit -m "Fix #XX: Description"`
6. Push et crée une Pull Request

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails !

---

## ⚠️ Note importante

**L'application est fonctionnelle** mais contient des issues de sécurité et de stabilité qui doivent être corrigées avant utilisation en production ou partage public.

**Utilisation recommandée :** Développement/test personnel uniquement jusqu'à la version 1.0.0.

---

**Note :** Ce document est mis à jour régulièrement. Chaque issue corrigée sera marquée ✅ et déplacée dans le [CHANGELOG.md](CHANGELOG.md).