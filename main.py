import streamlit as st
from pathlib import Path
from db.models import init_db, load_profile_from_db
from db.database import get_connection
from services.mood_service import check_mood_logged_today
from ui.layout import (
    render_profile_page,
    render_intro_page,
    render_home_page,
    render_dashboard
)

# ________________________________________
# Configuration de la page
# _______________________________________
st.set_page_config(
    page_title="Help-Desk - Compagnon du quotidien",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ________________________________________
# Initialisation de la base de données
# ________________________________________
# Créer le dossier data s'il n'existe pas
Path("data").mkdir(exist_ok=True)

# Initialiser les tables____________________
init_db()

# Connexion à la base______________________
if "conn" not in st.session_state:
    st.session_state.conn = get_connection()

# ________________________________________
# Initialisation du session_state
# _______________________________________
defaults = {
    "profile_created": False,
    "profile": None,
    "intro_done": False,
    "mood_logged_today": False,
    "selected_day": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# _______________________________________
# Charger le profil existant depuis la DB
# _______________________________________
if not st.session_state.profile_created:
    profile = load_profile_from_db()
    if profile:
        st.session_state.profile = profile
        st.session_state.profile_created = True
        st.session_state.intro_done = True  # Si le profil existe, intro est déjà passée__________________

# _____________________________________________________
# Vérifier si l'humeur a été enregistrée aujourd'hui
# _____________________________________________________
if st.session_state.profile_created and not st.session_state.mood_logged_today:
    if check_mood_logged_today():
        st.session_state.mood_logged_today = True

# _______________________________________
# Chargement du thème CSS (optionnel)
# ________________________________________
css_file = Path("assets/theme.css")
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ________________________________________
# Sidebar avec navigation et infos
# _______________________________________
with st.sidebar:
    st.title("💙 Help-Desk")
    st.markdown("---")
    
    if st.session_state.profile_created and st.session_state.profile:
        st.markdown(f"**Connecté en tant que :**  \n{st.session_state.profile['prenom']}")
        
        if st.session_state.profile.get('tags'):
            st.markdown("**Tags :**")
            for tag in st.session_state.profile['tags']:
                st.markdown(f"- {tag}")
        
        st.markdown("---")
        
        # Bouton pour recommencer le parcours____________________________
        if st.button("🔄 Recommencer"):
            st.session_state.mood_logged_today = False
            st.rerun()
    
    st.markdown("---")
    st.caption("💡 Ton compagnon du quotidien")
    st.caption("🔒 Tes données sont stockées localement et protégées")

# ________________________________________
# Navigation principale
# _______________________________________
if not st.session_state.profile_created or not st.session_state.profile:
    # Étape 1 : Création du profil___________________________________
    render_profile_page()

elif not st.session_state.intro_done:
    # Étape 2 : Introduction________________________________________
    render_intro_page()

elif not st.session_state.mood_logged_today:
    # Étape 3 : Humeur du jour________________________________________
    render_home_page()

else:
    # Étape 4 : Dashboard principal___________________________________
    render_dashboard()