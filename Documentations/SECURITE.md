# 🔒 Sécurité et Confidentialité des Données

## Protection de vos données personnelles

### Stockage local et sécurisé

Toutes vos données sont stockées **uniquement sur votre appareil local** dans le dossier `data/`. Aucune donnée n'est transmise sur Internet ou à des serveurs externes.

### Mesures de sécurité implémentées

1. **Permissions de fichiers restrictives**
   - Le dossier `data/` est configuré avec des permissions `700` (accessible uniquement par vous)
   - La base de données `journal.db` utilise des permissions `600` (lecture/écriture uniquement pour vous)

2. **Pas de transmission externe**
   - Aucune connexion à Internet pour les données personnelles
   - Le modèle IA (Ollama) fonctionne localement
   - Les exports restent sous votre contrôle total

3. **Protection des exports**
   - Les fichiers PDF et Excel exportés contiennent vos données
   - Conservez-les en sécurité et chiffrez-les si nécessaire
   - Ne partagez ces exports qu'avec des professionnels de santé de confiance

### Recommandations supplémentaires

Pour une sécurité maximale, je vous recommande :

1. **chiffrement du disque**
   - **Windows** : BitLocker
   - **macOS** : FileVault
   - **Linux** : LUKS/dm-crypt

2. **Protéger la  session utilisateur**
   - Utilisez un mot de passe fort pour votre compte utilisateur
   - Verrouillez votre ordinateur quand vous vous absentez

3. **Sauvegardes sécurisées**
   - Sauvegardez régulièrement le dossier `data/`
   - Stockez les sauvegardes dans un endroit sûr et chiffré

4. **Exports professionnels**
   - Partagez les exports PDF/Excel uniquement via des canaux sécurisés
   - Supprimez les exports après utilisation si non nécessaires

### Fichiers sensibles

Les fichiers suivants contiennent vos données personnelles :
- `data/journal.db` - Base de données principale
- `data/secret.key` - Clé de chiffrement (si utilisée)

**Ne partagez jamais ces fichiers** et assurez-vous qu'ils sont inclus dans vos sauvegardes chiffrées.

### Questions de sécurité

Si vous avez des préoccupations concernant la sécurité de vos données, n'hésitez pas à consulter ce document ou à examiner le code source de l'application.

---

**Important** : Cette application est un outil de soutien personnel et ne remplace pas un suivi professionnel médical ou psychologique.
