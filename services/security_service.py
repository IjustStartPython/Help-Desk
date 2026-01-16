"""
Service de gestion de la sécurité et du chiffrement pour l'interface Streamlit
"""
import streamlit as st
from utils.encryption_config import EncryptionConfig
from pathlib import Path


def render_security_section():
    """Affiche la section de gestion de la sécurité"""
    st.header("🔐 Sécurité et chiffrement")

    # Introduction avec tooltip info
    col1, col2 = st.columns([0.97, 0.03])
    with col1:
        st.markdown("Cette section te permet de renforcer la sécurité de tes données en activant le **chiffrement**.")
    with col2:
        with st.expander("ℹ️", expanded=False):
            st.markdown("""
            **Qu'est-ce que le chiffrement ?**
            
            - 🔒 Tes notes et données sensibles seront chiffrées dans la base de données
            - 🔑 Seule ta clé de chiffrement (stockée localement) peut déchiffrer les données
            - 🛡️ Protection supplémentaire en cas d'accès non autorisé à ton ordinateur
            
            **Important :**
            - ⚠️ Si tu perds ta clé de chiffrement, tu perdras l'accès à tes données
            - 💾 Un backup automatique est créé avant chaque opération
            - 🔄 Tu peux activer/désactiver le chiffrement à tout moment
            """)

    st.divider()

    # Vérifier l'état du chiffrement
    config = EncryptionConfig()
    is_enabled = config.is_encryption_enabled()

    # Statut actuel
    st.subheader("📊 Statut actuel")

    if is_enabled:
        st.success("✅ Le chiffrement est **activé**")
        st.info("🔒 Tes notes et données sensibles sont chiffrées dans la base de données")

        # Informations sur la clé avec tooltip
        key_file = Path("data/secret.key")
        if key_file.exists():
            st.markdown("**Fichier de clé de chiffrement :**")
            st.code(str(key_file.absolute()))
            
            # Warning avec tooltip pour le chemin du fichier
            col1, col2 = st.columns([0.97, 0.03])
            with col1:
                st.warning("⚠️ **IMPORTANT** : Sauvegarde ce fichier en lieu sûr ! Sans lui, tes données seront irrécupérables.")
            with col2:
                with st.expander("ℹ️", expanded=False):
                    st.markdown(f"""
                    **📁 Emplacement du fichier :**
                    
                    ```
                    {key_file.absolute()}
                    ```
                    
                    **Comment sauvegarder :**
                    1. Copie ce fichier sur une clé USB
                    2. Stocke-le dans un cloud sécurisé
                    3. Garde-le dans un gestionnaire de mots de passe
                    """)
    else:
        st.warning("⚠️ Le chiffrement est **désactivé**")
        st.info("📄 Tes données sont stockées en clair dans la base de données")

    st.divider()

    # Actions
    st.subheader("⚙️ Actions")

    col1, col2 = st.columns(2)

    with col1:
        if not is_enabled:
            st.markdown("### 🔐 Activer le chiffrement")
            st.markdown("""
            Active le chiffrement pour protéger tes données sensibles.

            **Ce qui sera chiffré :**
            - Notes d'humeur
            - Notes personnelles
            - (Les titres de tâches restent en clair)
            """)

            if st.button("🔒 Activer le chiffrement", type="primary", use_container_width=True):
                with st.spinner("Activation du chiffrement en cours..."):
                    result = config.enable_encryption()

                    if result["success"]:
                        st.success("✅ Chiffrement activé avec succès !")
                        st.info(f"💾 Backup créé : {result['backup_path']}")
                        st.info(f"📊 Enregistrements migrés : {result['migrated_records']}")
                        st.rerun()
                    else:
                        st.error(f"❌ Erreur : {result['error']}")

    with col2:
        if is_enabled:
            st.markdown("### 🔓 Désactiver le chiffrement")
            st.markdown("""
            Désactive le chiffrement et déchiffre toutes les données.

            **⚠️ Attention :**
            - Tes données seront stockées en clair
            - Moins de protection en cas d'accès non autorisé
            """)

            # Initialiser l'état de confirmation
            if "confirm_disable_encryption" not in st.session_state:
                st.session_state.confirm_disable_encryption = False

            # Premier clic : afficher le bouton
            if not st.session_state.confirm_disable_encryption:
                if st.button("🔓 Désactiver le chiffrement", type="secondary", use_container_width=True):
                    st.session_state.confirm_disable_encryption = True
                    st.rerun()
            
            # Après le premier clic : afficher la confirmation
            else:
                st.warning("""
                **⚠️ CONFIRMATION REQUISE**
                
                En désactivant le chiffrement :
                - ✗ Tes données seront stockées **EN CLAIR** dans la base de données
                - ✗ N'importe qui ayant accès à ton ordinateur pourra les lire
                - ✗ Tu perds la protection supplémentaire contre les accès non autorisés
                
                ✓ Un backup sera créé automatiquement avant la désactivation.
                
                **Es-tu sûr(e) de vouloir continuer ?**
                """)
                
                col_yes, col_no = st.columns(2)
                
                with col_yes:
                    if st.button("✅ Oui, désactiver", type="primary", use_container_width=True):
                        with st.spinner("Désactivation du chiffrement en cours..."):
                            result = config.disable_encryption()

                            if result["success"]:
                                st.success("✅ Chiffrement désactivé avec succès !")
                                st.info(f"💾 Backup créé : {result['backup_path']}")
                                st.info(f"📊 Enregistrements déchiffrés : {result['decrypted_records']}")
                                st.session_state.confirm_disable_encryption = False
                                st.rerun()
                            else:
                                st.error(f"❌ Erreur : {result['error']}")
                                st.session_state.confirm_disable_encryption = False
                
                with col_no:
                    if st.button("❌ Non, annuler", use_container_width=True):
                        st.session_state.confirm_disable_encryption = False
                        st.rerun()

    st.divider()

    # Informations de sécurité générales
    st.subheader("🛡️ Bonnes pratiques de sécurité")

    with st.expander("📖 Lire les recommandations"):
        st.markdown("""
        **Protection des données :**
        1. **Backups réguliers** : Utilise l'onglet "Sauvegardes" pour créer des backups réguliers
        2. **Clé de chiffrement** : Si le chiffrement est activé, sauvegarde le fichier `data/secret.key` en lieu sûr
        3. **Permissions système** : Le dossier `data/` et ses fichiers ont des permissions restrictives (600/700)

        **En cas de perte de données :**
        - Vérifie les backups disponibles dans l'onglet "Sauvegardes"
        - Si le chiffrement est activé, tu dois avoir la clé `secret.key` pour restaurer les données

        **Stockage local uniquement :**
        - Toutes les données restent sur ton ordinateur
        - Aucune donnée n'est envoyée sur internet (sauf si tu utilises le chat IA avec Ollama)
        - Ollama fonctionne localement sur ta machine
        """)

    # Informations techniques
    with st.expander("🔧 Informations techniques"):
        st.markdown(f"""
        **Configuration actuelle :**
        - Chiffrement : {'✅ Activé' if is_enabled else '❌ Désactivé'}
        - Algorithme : Fernet (AES 128-bit en mode CBC)
        - Bibliothèque : cryptography (Python)
        - Fichier clé : `{Path('data/secret.key').absolute()}`
        - Base de données : `{config.db_path.absolute()}`

        **Limitations :**
        - Le chiffrement ne protège pas contre un attaquant ayant accès à ta machine en cours d'exécution
        - Le chiffrement protège les données au repos (dans la base de données)
        - Pour une protection maximale, utilise également le chiffrement du disque système (BitLocker, FileVault, LUKS)
        """)


def show_encryption_status():
    """Affiche un indicateur de statut du chiffrement dans la sidebar"""
    config = EncryptionConfig()

    if config.is_encryption_enabled():
        st.sidebar.markdown("🔒 Chiffrement activé")
    else:
        st.sidebar.markdown("🔓 Chiffrement désactivé")