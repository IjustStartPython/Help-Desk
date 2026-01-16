# 🗺️ Roadmap Help-Desk

**Projet :** Compagnon personnel TDAH-friendly  
**Statut actuel :** v0.8.0-alpha (développement actif)  
**Objectif :** Application desktop complète, sécurisée et stable

---

## 📍 Version actuelle : 0.8.0-alpha

**Date de release :** 16 janvier 2026

**Fonctionnalités :**
- ✅ Profil utilisateur
- ✅ Journal d'humeur
- ✅ Suivi des habitudes
- ✅ Chat IA local (Ollama)
- ✅ Gamification (points, badges, streaks)
- ✅ Mode Focus TDAH
- ✅ Exports PDF/Excel
- ✅ Sauvegardes automatiques
- ✅ Chiffrement optionnel (Fernet)

**Limitations connues :**
Voir [KNOWN_ISSUES.md](KNOWN_ISSUES.md)

---

## 🎯 Version 0.9.0 - "Sécurité et Stabilité"

**📅 Date prévue :** Février 2026  
**🎯 Objectif :** Corriger les problèmes critiques de sécurité et stabilité

### Corrections prioritaires

#### 🔐 Sécurité (issues #1, #2)
- [ ] **Issue #1** - Dériver clé de chiffrement depuis mot de passe utilisateur
  - Utiliser PBKDF2-HMAC-SHA256 (100 000 itérations)
  - Stocker le salt de manière sécurisée
  - Demander mot de passe au démarrage si chiffrement activé
  - Ajouter option "Changer mot de passe"
  - **Durée estimée :** 3-4h

- [ ] **Issue #2** - Implémenter permissions Windows
  - Utiliser `icacls` pour restreindre l'accès
  - Appliquer sur DB, backups, logs, clé de chiffrement
  - Tester sur Windows 10/11
  - **Durée estimée :** 3-4h

#### 🗄️ Base de données (issue #3)
- [ ] **Issue #3** - Système de versioning des migrations
  - Créer table `schema_version` (version, applied_at, description)
  - Refactoriser migrations en fonctions numérotées
  - Ajouter fonction `get_current_version()`
  - Logger chaque migration appliquée
  - **Durée estimée :** 4-5h

#### 📝 Logging (issues #5, #6)
- [ ] **Issue #5** - Compléter le logging
  - Ajouter logs dans tous les services
  - Niveaux : INFO (succès), WARNING (comportement inattendu), ERROR (erreurs)
  - Loguer les opérations critiques (création profil, backup, export)
  - **Durée estimée :** 2-3h

- [ ] **Issue #6** - Rotation des logs
  - Implémenter `TimedRotatingFileHandler`
  - Rétention : 28 jours (4 semaines)
  - Compression automatique des anciens logs (gzip)
  - **Durée estimée :** 1-2h

#### 💾 Backups (issue #4)
- [ ] **Issue #4** - Déplacer backups dans %APPDATA%
  - Windows : `%APPDATA%/Help-Desk/backups/`
  - Linux/Mac : `~/.local/share/Help-Desk/backups/`
  - Migrer backups existants automatiquement
  - **Durée estimée :** 1-2h

#### ✅ Tests (issue #8)
- [ ] **Issue #8** - Configurer pytest-cov
  - Créer `pytest.ini` avec config couverture
  - Lancer tests et mesurer couverture
  - Objectif : 60% minimum pour v0.9.0
  - Ajouter badge dans README
  - **Durée estimée :** 2h

### Critères de release 0.9.0
- ✅ Toutes les issues critiques (🔴) corrigées
- ✅ Toutes les issues moyennes (🟡) corrigées
- ✅ Tests passent à 100%
- ✅ Couverture ≥ 60%
- ✅ Documentation mise à jour
- ✅ Testé sur Windows 10/11, Ubuntu 22.04, macOS

**Durée totale estimée :** 2-3 semaines

---

## 🚀 Version 1.0.0 - "Première Release Stable"

**📅 Date prévue :** Mars 2026  
**🎯 Objectif :** Application complète, documentée et production-ready

### Fonctionnalités

#### 📖 Documentation (issue #9)
- [ ] **Issue #9** - Guide Ollama complet
  - Instructions Windows/Linux/Mac
  - Screenshots de chaque étape
  - Dépannage des erreurs courantes
  - FAQ

- [ ] Guide utilisateur illustré
  - Captures d'écran de toutes les pages
  - Tutoriel pas-à-pas première utilisation
  - Cas d'usage TDAH

#### 📊 Exports (issue #7)
- [ ] **Issue #7** - Anonymisation des exports
  - Checkbox "Anonymiser" dans l'UI
  - Remplace prénom par "Utilisateur"
  - Masque date de naissance (affiche âge seulement)
  - Garde les données statistiques intactes

#### 🎯 UX (issue #10)
- [ ] **Issue #10** - Focus Mode robuste
  - Détection rechargement intempestif
  - Message bienveillant : "Veux-tu reprendre ta session ?"
  - Sauvegarde progression dans `st.session_state`
  - Statistiques : nombre de sessions complétées

#### 🎨 UI
- [ ] Thème personnalisable (clair/sombre/TDAH-friendly)
- [ ] Animations subtiles (feedback visuel)
- [ ] Sons optionnels (notifications, fin focus)
- [ ] Raccourcis clavier (accessibilité)

#### 🧪 Qualité
- [ ] Couverture tests ≥ 80%
- [ ] Tests d'intégration (DB + services)
- [ ] Tests de sécurité (injection SQL, validation)
- [ ] Analyse statique (pylint, mypy)

### Critères de release 1.0.0
- ✅ Toutes les issues fermées
- ✅ Documentation complète (guides + screenshots)
- ✅ Couverture tests ≥ 80%
- ✅ Aucun bug critique connu
- ✅ Testé par 3+ utilisateurs réels
- ✅ Performance optimisée (< 1s startup)

**Durée totale estimée :** 1 mois

---

## 🌟 Version 2.0.0 - "Multi-utilisateurs"

**📅 Date prévue :** T2 2026 (Avril-Juin)  
**🎯 Objectif :** Support de plusieurs profils sur une même machine

### Fonctionnalités majeures

#### 👥 Multi-profils
- [ ] Écran de sélection de profil au démarrage
- [ ] Création/suppression de profils
- [ ] Isolation complète des données par profil
- [ ] Permissions par utilisateur OS

#### 🔑 Authentification
- [ ] Login avec mot de passe (hash bcrypt)
- [ ] Protection par code PIN (4-6 chiffres)
- [ ] Session auto-verrouillée après inactivité
- [ ] Changement de mot de passe
- [ ] Récupération mot de passe (question secrète)

#### 📊 Statistiques avancées
- [ ] Graphiques interactifs (Plotly)
- [ ] Comparaison périodes (semaine/mois)
- [ ] Export format JSON/CSV
- [ ] Analyse tendances (ML basique)

#### 📱 Première version mobile
- [ ] App cross-platform (Kivy ou BeeWare)
- [ ] Sync locale (USB/réseau local)
- [ ] UI adaptée mobile TDAH-friendly

### Critères de release 2.0.0
- ✅ Multi-profils fonctionnel
- ✅ Authentification sécurisée
- ✅ Tests de sécurité (pentesting basique)
- ✅ App mobile beta fonctionnelle
- ✅ Migration depuis v1.x automatique

**Durée totale estimée :** 2 mois

---

## ☁️ Version 3.0.0 - "Cloud Optionnel"

**📅 Date prévue :** T4 2026 (Octobre-Décembre)  
**🎯 Objectif :** Synchronisation cloud chiffrée end-to-end (opt-in)

### Fonctionnalités majeures

#### ☁️ Synchronisation cloud
- [ ] Chiffrement E2E (clé jamais envoyée au serveur)
- [ ] Sync sélectif (choisir quoi synchroniser)
- [ ] Conflit résolution automatique
- [ ] Backend self-hostable (Docker)
- [ ] Support NextCloud/Syncthing

#### 📱 App mobile native
- [ ] React Native ou Flutter
- [ ] Notifications push
- [ ] Widget home screen
- [ ] Mode hors-ligne complet

#### 🔔 Notifications & Rappels
- [ ] Rappels habitudes quotidiennes
- [ ] Notification fin focus
- [ ] Encouragements personnalisés
- [ ] Smart reminders (ML basé sur historique)

#### 🌐 API REST
- [ ] API publique documentée (OpenAPI)
- [ ] Webhooks pour intégrations
- [ ] Support IFTTT/Zapier
- [ ] SDK Python

### Critères de release 3.0.0
- ✅ Sync cloud E2E fonctionnel
- ✅ App mobile stable (iOS + Android)
- ✅ API documentée et testée
- ✅ Audit sécurité externe
- ✅ RGPD compliant

**Durée totale estimée :** 3-4 mois

---

## 🎯 Backlog (fonctionnalités futures)

### Intégrations
- [ ] Export Notion/Obsidian
- [ ] Import données Google Fit/Apple Health
- [ ] Intégration calendriers (Google/Outlook)

### IA avancée
- [ ] Détection patterns comportementaux
- [ ] Suggestions personnalisées (ML)
- [ ] Prédiction humeur (séries temporelles)
- [ ] Résumés hebdomadaires automatiques

### Communauté
- [ ] Mode "buddy" (accountability partner)
- [ ] Groupes de soutien anonymes
- [ ] Partage badges/achievements (opt-in)

### Accessibilité
- [ ] Support lecteurs d'écran
- [ ] Navigation clavier complète
- [ ] Thème dyslexie-friendly
- [ ] Support langues (i18n)

---

## 📊 Métriques de succès

### v1.0.0
- 🎯 10+ utilisateurs actifs
- 🎯 80% satisfaction utilisateur
- 🎯 0 bugs critiques
- 🎯 Documentation complète

### v2.0.0
- 🎯 50+ utilisateurs actifs
- 🎯 5+ profils par installation
- 🎯 App mobile 100+ téléchargements

### v3.0.0
- 🎯 500+ utilisateurs cloud
- 🎯 API utilisée par 10+ intégrations
- 🎯 Communauté active (forum/Discord)

---

## 🤝 Comment contribuer ?

Tu veux participer à une fonctionnalité de la roadmap ?

1. Consulte [CONTRIBUTING.md](CONTRIBUTING.md)
2. Ouvre une issue pour discuter de l'implémentation
3. Crée une branche `feature/nom-fonctionnalite`
4. Soumets une PR vers `dev`

---

## 📝 Notes

- Cette roadmap est **indicative** et peut évoluer selon :
  - Les retours utilisateurs
  - Les contraintes techniques découvertes
  - Les nouvelles idées communautaires

- Les **dates sont estimatives** et basées sur un travail à temps partiel

- **Priorité toujours donnée à :**
  1. Sécurité
  2. Stabilité
  3. Expérience utilisateur TDAH
  4. Nouvelles fonctionnalités

---

**Dernière mise à jour :** 15 janvier 2026
