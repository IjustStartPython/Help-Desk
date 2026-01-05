# Help-Desk - Compagnon du quotidien

> Un compagnon de soutien personnel pour faciliter le quotidien des personnes ayant un TDAH, de l'anxiété ou des difficultés émotionnelles.

## À propos de ce projet

Help-Desk est un projet personnel que j'ai développé pour apprendre à créer une application complète en Python tout en répondant à un vrai besoin : offrir un espace sécurisé et privé pour suivre son humeur, ses habitudes et dialoguer avec un assistant IA bienveillant.

### Pourquoi ce projet ?

J'ai voulu créer une application qui :
- Respecte la vie privée (données 100% locales)
- Soit simple et accessible à utiliser
- Intègre une IA qui fonctionne sans envoyer de données dans le cloud
- Aide les personnes à mieux comprendre leurs émotions et habitudes

## Captures d'écran

_[TODO: Ajouter captures d'écran de l'interface]_

## Fonctionnalités

- **Profil personnalisé** : Création d'un profil avec tags personnalisables
- **Journal d'humeur** : Suivi quotidien de l'état émotionnel avec émojis
- **Suivi d'habitudes** : Définir et suivre des habitudes quotidiennes
- **Chat IA local** : Discussion avec un assistant bienveillant (Ollama)
- **Exports** : Génération de rapports PDF et Excel pour partager avec des professionnels
- **Sécurité** : Toutes les données restent sur votre machine

## Technologies utilisées

- **Python 3.13** - Langage de programmation
- **Streamlit** - Framework pour l'interface utilisateur
- **SQLite** - Base de données locale
- **Ollama** - Modèle IA local (llama3.1:8b)
- **Pandas** - Analyse de données
- **Matplotlib** - Graphiques de visualisation
- **FPDF2** - Génération de PDF
- **Cryptography** - Sécurisation des données

## Architecture du projet

J'ai organisé le code de manière modulaire pour faciliter la maintenance et l'évolution :

```
help-desk/
├── main.py                 # Point d'entrée de l'application
├── requirements.txt        # Dépendances Python
├── SECURITE.md            # Documentation sécurité
│
├── assets/                # Ressources (CSS, images)
│   └── theme.css
│
├── db/                    # Couche base de données
│   ├── database.py        # Connexion et configuration
│   └── models.py          # Schéma et requêtes
│
├── services/              # Logique métier
│   ├── chat_ai.py         # Interaction avec Ollama
│   ├── chat_service.py    # Gestion des conversations
│   ├── export_service.py  # Génération PDF/Excel
│   ├── habit_service.py   # Gestion des habitudes
│   ├── mood_service.py    # Suivi de l'humeur
│   └── profile_service.py # Gestion du profil
│
├── ui/                    # Interface utilisateur
│   ├── components.py      # Composants réutilisables
│   └── layout.py          # Pages de l'application
│
└── utils/                 # Utilitaires
    ├── dates.py           # Gestion des dates
    ├── safety.py          # Détection de détresse
    └── security.py        # Chiffrement (préparé)
```

### Points techniques intéressants

**Séparation des responsabilités**
- Les services gèrent la logique métier
- Les modèles gèrent l'accès aux données
- L'UI se concentre sur l'affichage

**Sécurité et confidentialité**
- Base de données SQLite avec permissions restrictives (600)
- Dossier data protégé (permissions 700)
- Aucune connexion externe pour les données personnelles
- IA qui tourne localement via Ollama

**IA locale avec Ollama**
- Utilisation du modèle llama3.1:8b
- Prompt système personnalisé pour un ton bienveillant
- Détection de détresse avec réponses appropriées
- Pas de dépendance à une API cloud

## Installation

### Prérequis

- Python 3.13+
- [Ollama](https://ollama.ai/) (optionnel, pour le chat IA)

### Étapes

1. Cloner le dépôt
```bash
git clone https://github.com/votre-username/help-desk.git
cd help-desk
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. (Optionnel) Installer Ollama et télécharger le modèle
```bash
ollama pull llama3.1:8b
```

5. Lancer l'application
```bash
streamlit run main.py
```

L'application s'ouvrira dans votre navigateur à l'adresse `http://localhost:8501`

## Utilisation

1. **Première utilisation** : Créez votre profil avec votre prénom et vos tags personnalisés
2. **Quotidien** : Enregistrez votre humeur du jour et suivez vos habitudes
3. **Chat** : Discutez avec l'assistant IA pour clarifier vos pensées
4. **Dashboard** : Visualisez vos statistiques et tendances
5. **Export** : Générez des rapports à partager avec un professionnel si besoin

## Ce que j'ai appris

En développant Help-Desk, j'ai approfondi mes connaissances en :
- Architecture d'application Python (pattern MVC)
- Gestion d'état avec Streamlit
- Manipulation de bases de données SQLite
- Intégration d'IA locale
- Sécurité et protection de données sensibles
- Génération de documents (PDF, Excel)
- UX pour des utilisateurs en situation de vulnérabilité

## Limitations et améliorations futures

**Actuellement :**
- Mono-utilisateur (une seule personne par installation)
- IA nécessite Ollama installé localement
- Interface desktop uniquement

**Améliorations envisagées :**
- Multi-utilisateurs avec authentification
- Application mobile
- Chiffrement de la base de données (fonction déjà préparée)
- Synchronisation cloud optionnelle et chiffrée
- Plus de types de visualisations
- Rappels et notifications

## Sécurité et vie privée

La protection de vos données est une priorité. Consultez [SECURITE.md](SECURITE.md) pour plus de détails.

**Résumé :**
- Aucune donnée n'est envoyée sur Internet
- L'IA fonctionne 100% en local
- Permissions restrictives sur les fichiers
- Chiffrement préparé pour les données sensibles

## Avertissement

Cette application est un outil de soutien personnel et **ne remplace pas** un suivi professionnel médical ou psychologique. Si vous traversez des difficultés importantes, consultez un professionnel de santé.

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## Contact

Si vous avez des questions ou suggestions sur ce projet, n'hésitez pas à ouvrir une issue sur GitHub.

---

Développé avec soin pour accompagner le quotidien de manière bienveillante et sécurisée.
