"""
Service de gestion des backups pour l'interface Streamlit
"""
import streamlit as st
from utils.backup import BackupManager
from pathlib import Path


def render_backup_section():
    """Affiche la section de gestion des backups"""
    st.header("💾 Gestion des sauvegardes")

    st.markdown("""
    Protège tes données en créant des sauvegardes régulières de ta base de données.

    **Pourquoi faire des backups ?**
    - 🛡️ Protection contre la perte de données
    - 🔄 Possibilité de restaurer une version antérieure
    - ✨ Tranquillité d'esprit
    """)

    # Initialiser le gestionnaire de backup
    from db.database import DB_PATH
    backup_manager = BackupManager(str(DB_PATH))

    # Créer un backup manuel
    st.subheader("📥 Créer un backup")
    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button("🔄 Créer un backup maintenant", type="primary", use_container_width=True):
            try:
                backup_path = backup_manager.create_backup(prefix="manual_backup")
                st.success(f"✅ Backup créé avec succès : {backup_path.name}")
            except Exception as e:
                st.error(f"❌ Erreur lors de la création du backup : {str(e)}")

    with col2:
        if st.button(" Nettoyer les anciens", use_container_width=True):
            deleted = backup_manager.clean_old_backups(keep_count=10)
            st.info(f"🗑️ {deleted} ancien(s) backup(s) supprimé(s)")

    st.divider()

    # Liste des backups disponibles
    st.subheader("📋 Backups disponibles")
    backups = backup_manager.list_backups()

    if not backups:
        st.info("Aucun backup disponible. Crée-en un pour commencer !")
    else:
        st.markdown(f"**{len(backups)} backup(s) trouvé(s)**")

        for backup in backups:
            info = backup_manager.get_backup_info(backup)

            with st.expander(f"📦 {info['name']} - {info['created_str']}"):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(f"**Taille :** {info['size_mb']} MB")
                    st.write(f"**Date :** {info['created_str']}")

                with col2:
                    if st.button("♻️ Restaurer", key=f"restore_{info['name']}", use_container_width=True):
                        try:
                            backup_manager.restore_backup(backup)
                            st.success("✅ Backup restauré avec succès ! Redémarre l'application.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erreur : {str(e)}")

                with col3:
                    if st.button("🗑️ Supprimer", key=f"delete_{info['name']}", use_container_width=True):
                        try:
                            Path(backup).unlink()
                            st.success("✅ Backup supprimé")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erreur : {str(e)}")

    st.divider()

    # Configuration du backup automatique
    st.subheader("⚙️ Backup automatique")
    st.markdown("""
    Les backups automatiques sont créés au démarrage de l'application.
    Tu peux configurer le nombre de backups à conserver.
    """)

    col1, col2 = st.columns([3, 1])
    with col1:
        keep_count = st.slider("Nombre de backups à conserver", min_value=3, max_value=30, value=10)

    with col2:
        st.write("")  # Espace
        st.write("")  # Espace
        if st.button("💾 Sauvegarder", use_container_width=True):
            st.session_state.backup_keep_count = keep_count
            st.success(f"✅ Configuration sauvegardée : {keep_count} backups")


def perform_auto_backup():
    """
    Effectue un backup automatique au démarrage de l'application

    Returns:
        dict: Résultat du backup
    """
    from db.database import DB_PATH
    backup_manager = BackupManager(str(DB_PATH))

    # Utiliser le nombre de backups à conserver depuis la session ou valeur par défaut
    keep_count = st.session_state.get("backup_keep_count", 10)

    return backup_manager.auto_backup(keep_count=keep_count)
