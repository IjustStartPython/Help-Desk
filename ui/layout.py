import streamlit as st
import pandas as pd
from datetime import date, timedelta
from ui.components import card
from services.mood_service import get_mood_history, save_mood, add_note
from services.habit_service import get_today_tasks, add_task, toggle_task, delete_task
from services.chat_service import render_chat_section
from services.export_service import render_export_section, show_data_stats
from db.models import save_profile_to_db


#Profil_____________________________________________________________________________________
def render_profile_page():
    st.header("👋 Bienvenue !")
    card("Créons ton profil", profil_form)

def profil_form():
    with st.form("Profile_form"):
        prenom = st.text_input("Prénom")
        birth_date = st.date_input("Date de naissance", max_value=date.today())
        tags = st.text_input(
            "Informations utiles (séparées par des virgules)",
            placeholder="TDAH, anxiété, suivi psychiatrique..."
        )
        submitted = st.form_submit_button("Enregistrer mon profil")

    if submitted:
        if not prenom.strip():
            st.warning("⚠️ Merci d'indiquer au moins ton prénom.")
            return

        tags_list = [t.strip() for t in tags.split(",") if t.strip()]

        #Enregistrer dans la session____________________________________________________________
        st.session_state.profile = {
            "prenom": prenom,
            "birth_date": birth_date.isoformat(),
            "tags": tags_list
        }
        st.session_state.profile_created = True

        #Enregistrer dans la base_______________________________________________________________
        save_profile_to_db(prenom, birth_date.isoformat(), tags_list)

        st.success("✅ Profil enregistré ! On continue...")
        st.rerun()


# Intro_________________________________________________________________________________________
def render_intro_page():
    st.header(f"💙 Merci {st.session_state.profile['prenom']}")
    card("Comment ça va se passer ?", intro_text)
    if st.button("🚀 C'est parti", type="primary"):
        st.session_state.intro_done = True
        st.rerun()

def intro_text():
    st.markdown("""
    Ce compagnon est là pour t'aider **au fil de la journée**, sans pression.

    **Chaque jour tu peux :**
    - Noter ton humeur et tes ressentis
    - Planifier tes tâches à ton rythme
    - Écrire librement ce que tu ressens
    - Discuter avec le compagnon IA si besoin
    - Visualiser ton évolution

    **Il n'y a pas de bonne ou mauvaise journée.**  
    L'important c'est d'avancer à ton rythme 🌱
    """)


#Home / Mood du jour_____________________________________________________________________________________________
def render_home_page():
    st.header(f"☀️ Bonjour {st.session_state.profile['prenom']} !")
    card("Comment te sens-tu aujourd'hui ?", mood_form)
    
    if st.button("⏭️ Passer cette étape", type="secondary"):
        st.session_state.mood_logged_today = True
        st.rerun()

def mood_form():
    with st.form("mood_form"):
        mood = st.slider("📊 Humeur générale (1-10)", 1, 10, 5)
        emotion = st.text_input("💭 Ressenti émotionnel", placeholder="Ex: calme, anxieux, motivé...")
        motivation = st.text_input("🎯 Motivation du jour", placeholder="Ex: faire du sport, voir des amis...")
        notes = st.text_area("📝 Notes / Ressenti libre", placeholder="Tu peux écrire ce que tu veux ici...")

        submitted = st.form_submit_button("Enregistrer", type="primary")

        if submitted:
            save_mood(mood, emotion, motivation, notes)
            st.session_state.mood_logged_today = True
            st.success("✅ Merci ! Tes ressentis sont enregistrés 🚀")
            st.rerun()


#Dashboard__________________________________________________________________________________________________________
def render_dashboard():
    st.header(f"📊 Tableau de bord - {date.today().strftime('%d/%m/%Y')}")
    
    #Menu de navigation_____________________________________________________________________________________________
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Aujourd'hui", "💬 Mathi", "📈 Historique", "⚙️ Export"])
    
    with tab1:
        render_today_tab()
    
    with tab2:
        render_chat_section()
    
    with tab3:
        render_history_tab()
    
    with tab4:
        show_data_stats()
        st.divider()
        render_export_section()


def render_today_tab():
    """Onglet principal avec tâches et notes"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        card("✅ Mes tâches", render_task_calendar)
    
    with col2:
        card("💭 Notes rapides", render_quick_notes)
        card("📊 Humeur d'aujourd'hui", render_today_mood)


def render_history_tab():
    """Onglet historique"""
    card("📈 Évolution de ton humeur", render_mood_summary)
    
    col1, col2 = st.columns(2)
    with col1:
        card("📋 Historique des tâches", render_task_history)
    with col2:
        card("📝 Dernières notes", render_notes_history)


#Tâches / Calendrier_________________________________________________________________________
def render_task_calendar():
    """Affiche les tâches filtrées par date"""
    today = date.today()
    if st.session_state.selected_day is None:
        st.session_state.selected_day = today

    # Sélection du jour____________________________________________________________
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_day = st.date_input(
            "📅 Sélectionne un jour",
            value=st.session_state.selected_day,
            key="cal_picker"
        )
        st.session_state.selected_day = selected_day

    # Affichage des tâches____________________________________________________
    tasks = get_today_tasks(task_date=selected_day)
    
    if tasks:
        for task_id, title, done, task_date in tasks:
            col1, col2 = st.columns([4, 1])
            with col1:
                checked = st.checkbox(
                    title, 
                    value=bool(done), 
                    key=f"task_{task_id}"
                )
                if checked != bool(done):
                    toggle_task(task_id, checked)
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{task_id}"):
                    delete_task(task_id)
                    st.rerun()
    else:
        st.info("Aucune tâche pour cette date 📝")

    # Ajouter une tâche_______________________________________________________________
    with st.form("new_task_form", clear_on_submit=True):
        new_task = st.text_input("", placeholder="➕ Ajouter une tâche...")
        submitted = st.form_submit_button("Ajouter", type="primary")
        
        if submitted and new_task.strip():
            add_task(new_task, task_date=selected_day)
            st.rerun()


def render_task_history():
    """Affiche l'historique des tâches"""
    conn = st.session_state.conn
    df = pd.read_sql("""
        SELECT title, done, created_at 
        FROM tasks 
        ORDER BY created_at DESC 
        LIMIT 20
    """, conn)
    
    if not df.empty:
        df['done'] = df['done'].map({0: '⬜', 1: '✅'})
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.info("Pas encore d'historique")


#Notes__________________________________________________________________________________________________
def render_quick_notes():
    """Bloc notes rapide"""
    with st.form("note_form", clear_on_submit=True):
        note = st.text_area(
            "", 
            placeholder="💬 Une pensée, une émotion...",
            height=150
        )
        submitted = st.form_submit_button("📝 Enregistrer", type="primary")
        
        if submitted and note.strip():
            add_note(note)
            st.success("✅ Note sauvegardée !")
            st.rerun()


def render_notes_history():
    """Affiche les dernières notes"""
    conn = st.session_state.conn
    df = pd.read_sql("""
        SELECT content, created_at 
        FROM notes 
        ORDER BY created_at DESC 
        LIMIT 5
    """, conn)
    
    if not df.empty:
        for _, row in df.iterrows():
            st.markdown(f"**{row['created_at'][:10]}**")
            st.text(row['content'][:100] + ("..." if len(row['content']) > 100 else ""))
            st.divider()
    else:
        st.info("Pas encore de notes")


#Humeur______________________________________________________________________________________________
def render_today_mood():
    """Affiche l'humeur du jour"""
    conn = st.session_state.conn
    today = date.today().isoformat()
    
    df = pd.read_sql(f"""
        SELECT mood_value, emotion, motivation 
        FROM mood 
        WHERE DATE(created_at) = '{today}'
        ORDER BY created_at DESC 
        LIMIT 1
    """, conn)
    
    if not df.empty:
        mood = df.iloc[0]
        st.metric("Humeur", f"{mood['mood_value']}/10")
        if mood['emotion']:
            st.write(f"💭 {mood['emotion']}")
        if mood['motivation']:
            st.write(f"🎯 {mood['motivation']}")
    else:
        st.info("Pas encore d'humeur pour aujourd'hui")


def render_mood_summary():
    """Graphique de l'évolution de l'humeur"""
    data = get_mood_history()
    
    if not data:
        st.info("Pas encore d'humeur enregistrée 📊")
        return

    df = pd.DataFrame(data, columns=["Date", "Humeur"])
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Graphique__________________________________________________________________________________
    st.line_chart(df.set_index("Date")["Humeur"])
    
    # Statistiques_______________________________________________________________________________
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Moyenne", f"{df['Humeur'].mean():.1f}/10")
    with col2:
        st.metric("Maximum", f"{df['Humeur'].max()}/10")
    with col3:
        st.metric("Minimum", f"{df['Humeur'].min()}/10")