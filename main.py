# Fichier principal de l'application Help-Desk
# c'est ici que tout commence !
# Gère l'initialisation et la navigation

import streamlit as st
import atexit
from pathlib import Path

# imports de mes fichiers
from db.models import init_db, load_profile_from_db
from db.database import get_connection, close_connection, migrate_database
from services.mood_service import check_mood_logged_today
from services.backup_service import perform_auto_backup
from services.security_service import show_encryption_status
from services.tdah_features import init_tdah_features
from ui.layout import (
    render_profile_page,
    render_intro_page,
    render_home_page,
    render_dashboard,
)

# TODO: ajouter un systeme de notification push un jour

# Configuration de la page Streamlit (doit etre en premier sinon ca bug)
st.set_page_config(
    page_title="Help-Desk - Compagnon du quotidien",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Forcer le mode clair le mode sombre du navigateur et c'est moche
st.markdown(
    """
    <style>
        @media (prefers-color-scheme: dark) {
            :root { color-scheme: light !important; }
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Créer les tables si elles existent pas
init_db()

# Initialisation de la base de données
# Migration des anciennes données (j'ai du faire ca parce que j'ai changé la structure des tables)
if "migration_done" not in st.session_state:
    migrate_database()
    st.session_state.migration_done = True

# Connexion à la base (on garde la connection ouverte pour pas la réouvrir a chaque fois)
if "conn" not in st.session_state:
    st.session_state.conn = get_connection()
    atexit.register(close_connection)  # ferme la connection quand on quitte

# Initialiser les features TDAH (faut le faire apres la connexion sinon ca marche pas)
init_tdah_features()

# backup auto au demarage (au cas ou)
if "auto_backup_done" not in st.session_state:
    backup_result = perform_auto_backup()
    if backup_result["success"]:
        st.session_state.auto_backup_done = True
    # print("backup fait")  # pour debug

# Initialiser les variables de session
defaults = {
    "profile_created": False,
    "profile": None,
    "intro_done": False,
    "mood_logged_today": False,
    "selected_day": None,
    "focus_mode": False,
}

# Mettre les valeurs par défaut (j'ai trouvé cette technique sur stackoverflow)
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# charger le profil si il existe deja
if not st.session_state.profile_created:
    profile = load_profile_from_db()
    if profile:
        st.session_state.profile = profile
        st.session_state.profile_created = True
        st.session_state.intro_done = True

# Verifier si l'humeur a deja été mis aujourd'hui
if st.session_state.profile_created and not st.session_state.mood_logged_today:
    if check_mood_logged_today():
        st.session_state.mood_logged_today = True

# charger le css pour le style (j'ai mis le fichier dans assets/)
css_file = Path("assets/theme.css")
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar (le menu a gauche)
with st.sidebar:
    st.title("💙 Help-Desk")
    st.caption("💡 Ton compagnon du quotidien")
    st.markdown("---")

    # Afficher le profil si connecté
    if st.session_state.profile_created and st.session_state.profile:
        st.markdown(
            f"**Connecté en tant que :**  \n{st.session_state.profile['prenom']}"
        )

        # Afficher les tags
        if st.session_state.profile.get("tags"):
            st.markdown("**Tags :**")
            for tag in st.session_state.profile["tags"]:
                st.markdown(f"- {tag}")

        st.markdown("---")

        # Bouton pour recommencer la journée (si on veut refaire l'humeur)
        if st.button(
            "🔄 Recommencer la journée", type="secondary", use_container_width=True
        ):
            if "confirm_restart_day" not in st.session_state:
                st.session_state.confirm_restart_day = False

            if not st.session_state.confirm_restart_day:
                st.session_state.confirm_restart_day = True
                st.warning(
                    "⚠️ Tu vas recommencer l'enregistrement de ton humeur du jour. Clique à nouveau pour confirmer."
                )
            else:
                st.session_state.mood_logged_today = False
                st.session_state.confirm_restart_day = False
                st.rerun()

        # Bouton pour recréer le profil (si l'utilisateur veut tout recommencer)
        if st.button(
            "👤 Recréer mon profil", type="secondary", use_container_width=True
        ):
            if "confirm_reset_profile" not in st.session_state:
                st.session_state.confirm_reset_profile = False

            if not st.session_state.confirm_reset_profile:
                st.session_state.confirm_reset_profile = True
                st.warning(
                    "⚠️ Attention ! Cela va réinitialiser ton profil. Clique à nouveau pour confirmer."
                )
            else:
                # on reset tout
                st.session_state.profile_created = False
                st.session_state.profile = None
                st.session_state.intro_done = False
                st.session_state.mood_logged_today = False
                st.session_state.confirm_reset_profile = False
                st.rerun()

    st.markdown("---")
    show_encryption_status()

# Navigation selon l'état (c'est comme un switch case mais en python y'en a pas)
if not st.session_state.profile_created or not st.session_state.profile:
    render_profile_page()  # pas encore de profil
elif not st.session_state.intro_done:
    render_intro_page()  # intro pas encore vue
elif not st.session_state.mood_logged_today:
    render_home_page()  # humeur pas encore faite
else:
    render_dashboard()  # tout est ok, on affiche le dashboard
