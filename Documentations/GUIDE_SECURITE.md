#  Guide de sécurité - Help-Desk

Ce guide t'explique comment utiliser les nouvelles fonctionnalités de sécurité de Help-Desk.

## 📋 Table des matières

1. [Validation automatique](#validation-automatique)
2. [Système de backup](#système-de-backup)
3. [Chiffrement des données](#chiffrement-des-données)
4. [Bonnes pratiques](#bonnes-pratiques)

---

##  Validation automatique

### Qu'est-ce que c'est ?

La validation automatique vérifie toutes tes entrées pour s'assurer qu'elles sont correctes et sécurisées.

### Ce qui est validé

| Type de donnée | Limites | Validation |
|----------------|---------|------------|
| **Prénom** | 2-50 caractères | Lettres, espaces, tirets, apostrophes uniquement |
| **Date de naissance** | Pas dans le futur, max 150 ans | Format YYYY-MM-DD |
| **Titres de tâches** | 1-200 caractères | Texte libre |
| **Notes personnelles** | 1-10000 caractères | Texte libre |
| **Notes d'humeur** | 0-5000 caractères | Texte libre (optionnel) |

### Comment ça fonctionne ?

- **Automatique** : Toute validation se fait automatiquement quand tu sauvegardes
- **Messages d'erreur** : Si une donnée est invalide, tu verras un message clair
- **Pas d'impact** : Si tout est valide, tu ne remarques rien !

---

##  Système de backup

### Accéder aux backups

1. Va dans le **tableau de bord**
2. Clique sur l'onglet **"💾 Sauvegardes"**

### Fonctionnalités disponibles

####  Créer un backup manuel

- Clique sur **"Créer un backup maintenant"**
- Le backup est créé instantanément
- Tu verras le nom du fichier créé

####  Voir les backups disponibles

- Tous tes backups sont listés du plus récent au plus ancien
- Pour chaque backup, tu peux voir :
  -  La date et l'heure de création
  -  La taille du fichier
  -  Option de restauration
  -  Option de suppression

####  Restaurer un backup

⚠️ **Attention** : Restaurer un backup remplace toutes tes données actuelles !

1. Clique sur le backup que tu veux restaurer
2. Clique sur **"♻️ Restaurer"**
3. Un backup de tes données actuelles est créé automatiquement avant la restauration
4. Redémarre l'application

####  Nettoyer les anciens backups

- Clique sur **"Nettoyer les anciens"**
- Garde les 10 backups les plus récents par défaut
- Les anciens backups sont supprimés automatiquement

####  Backup automatique

- Un backup est créé **automatiquement au démarrage** de l'application
- Tu n'as rien à faire !
- Les anciens backups sont nettoyés automatiquement

### Où sont stockés les backups ?

Les backups sont dans le dossier `data/backups/` :

```
Help-Desk/
└── data/
    ├── journal.db              # Ta base de données principale
    └── backups/
        ├── auto_backup_20260106_143022.db
        ├── manual_backup_20260106_150530.db
        └── pre_encryption_backup_20260106_151045.db
```

---

##  Chiffrement des données

### Qu'est-ce que le chiffrement ?

Le chiffrement transforme tes données en un format illisible sans la clé de déchiffrement.

**Avantages** :
-  Protection supplémentaire de tes données sensibles
-  Sécurité en cas d'accès non autorisé à ton ordinateur
-  Seule ta clé peut déchiffrer les données

**Inconvénients** :
-  Si tu perds la clé, **tu perds tes données définitivement**
-  Légère baisse de performance (négligeable)

### Accéder au chiffrement

1. Va dans le **tableau de bord**
2. Clique sur l'onglet **"🔐 Sécurité"**

### Activer le chiffrement

#### Avant d'activer

⚠️ **Lis ceci attentivement** :

1. Un backup automatique sera créé
2. Toutes tes notes seront chiffrées
3. Une clé de chiffrement sera générée : `data/secret.key`
4. **Tu dois sauvegarder ce fichier en lieu sûr !**

#### Étapes d'activation

1. Dans l'onglet **"🔐 Sécurité"**
2. Clique sur **"🔒 Activer le chiffrement"**
3. Attends la fin de l'opération
4. **IMPORTANT** : Sauvegarde le fichier `data/secret.key` en lieu sûr !

#### Après activation

-  Le statut dans la sidebar affichera "🔒 Chiffrement activé"
-  Tes données sensibles sont maintenant chiffrées
-  La clé est dans `data/secret.key`

### Désactiver le chiffrement

⚠️ **Attention** : Tes données seront stockées en clair !

1. Dans l'onglet **"🔐 Sécurité"**
2. Clique sur **"🔓 Désactiver le chiffrement"**
3. Un backup est créé automatiquement
4. Toutes tes données sont déchiffrées

### Que faire si je perds ma clé ?

❌ **Malheureusement, sans la clé, tes données chiffrées sont perdues.**

Solutions :
1. **Restaurer un backup** créé **avant** l'activation du chiffrement
2. **Prévention** : Sauvegarde toujours `data/secret.key` en plusieurs endroits sûrs

### Que faire si je change d'ordinateur ?

Pour transférer tes données chiffrées :

1. Copie le dossier `data/` complet (incluant `secret.key`)
2. Installe Help-Desk sur le nouvel ordinateur
3. Remplace le dossier `data/` par ta copie
4. Redémarre l'application

---

## 🛡️ Bonnes pratiques

### 1. Backups réguliers

-  Crée un backup manuel avant toute opération importante
-  Vérifie régulièrement que tu as des backups récents
-  Garde au moins 10 backups (configuré par défaut)

### 2. Protection de la clé de chiffrement

Si tu actives le chiffrement :

-  Sauvegarde `data/secret.key` immédiatement
-  Stocke la clé dans plusieurs endroits sûrs :
  - Clé USB chiffrée
  - Cloud sécurisé (Dropbox, Google Drive, etc.)
  - Gestionnaire de mots de passe
-  Ne partage JAMAIS ta clé avec personne
-  Ne stocke pas la clé sur un support non sécurisé

### 3. Sécurité générale

-  Verrouille ton ordinateur quand tu t'absentes
-  Utilise un mot de passe fort pour ta session
-  Fais des backups réguliers (même sans chiffrement)
-  Envisage d'activer le chiffrement du disque système (BitLocker, FileVault, LUKS)

### 4. Avant de faire des changements importants

Avant de :
- Activer/désactiver le chiffrement
- Mettre à jour l'application
- Modifier la base de données manuellement

Fais toujours :
-  Un backup manuel
-  Vérifie que le backup fonctionne (regarde sa taille, date, etc.)

---

##  En cas de problème

### Mes données ont disparu !

1. **Ne panique pas** - Tes backups sont là pour ça
2. Va dans l'onglet **"💾 Sauvegardes"**
3. Restaure le backup le plus récent
4. Redémarre l'application

### Le chiffrement ne fonctionne pas

Vérifie que :
- Le fichier `data/secret.key` existe
- Tu as bien cliqué sur "Activer le chiffrement"
- L'application a redémarré après activation

### J'ai perdu ma clé de chiffrement

Malheureusement, sans la clé :
1. Restaure un backup **créé avant l'activation** du chiffrement
2. À l'avenir, sauvegarde toujours ta clé !

---

## 📞 Besoin d'aide ?

-  Lis le `README.md` pour plus d'informations
-  Consulte le `CHANGELOG.md` pour les nouveautés
-  Reporte les bugs sur GitHub Issues

**Rappel** : Help-Desk n'est pas un outil médical. En cas de détresse, contacte un professionnel de santé.

---

**Stay safe! 🔐💙**
