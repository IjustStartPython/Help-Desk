# layout.py - toute l'interface utilisateur de l'app
# c'est le fichier le plus gros du projet lol

import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime

# mes imports
from ui.components import card
from services.mood_service import get_mood_history, save_mood, add_note
from services.habit_service import get_today_tasks, add_task, toggle_task, delete_task
from services.chat_service import render_chat_section
from services.export_service import render_export_section, show_data_stats, export_to_excel, export_to_pdf
from services.backup_service import render_backup_section
from services.security_service import render_security_section
from db.models import save_profile_to_db
from services.tdah_features import StreakSystem, PointsSystem, FocusMode, show_encouragement

def get_manual_streak():
    """Calcule la série de jours actifs manuellement
    (je l'ai fait en double avec StreakSystem mais flemme de changer)"""
    conn = st.session_state.conn
    cursor = conn.cursor()

    # compte les jours distincts des 7 derniers jours
    cursor.execute("""
        SELECT COUNT(DISTINCT DATE(created_at))
        FROM mood
        WHERE DATE(created_at) >= DATE('now', '-7 days')
    """)

    return cursor.fetchone()[0]


#profil_____________________________________________________________________________________
def render_profile_page():
    st.header("👋 Bienvenue !")
    card("Créons ton profil", profil_form)

def profil_form():
    with st.form("Profile_form"):
        prenom = st.text_input("Prénom")
        # date de naissance avec min/max pour eviter les dates bizarres
        birth_date = st.date_input("Date de naissance", max_value=date.today(), min_value=date.today().replace(year=date.today().year -100))
        tags = st.text_input(
            "Informations Utiles (séparées par des virgules)",
            placeholder="TDAH, anxiété, suivi psychiatrique..."
        )
        submitted = st.form_submit_button("Enregistrer mon profil")

    if submitted:
        # verif que le prenom est pas vide
        if not prenom.strip():
            st.warning("Merci d'indiquer au moins ton prénom")
            return

        # on split les tags par virgule
        tags_list = [t.strip() for t in tags.split(",") if t.strip()]

        #Enregistrer dans la bdd_____________________________________________________________
        save_profile_to_db(prenom, birth_date.isoformat(), tags_list)
        st.success("✅ Profil enregistré ! On continue...")
        st.rerun()
#intro______________________________________________________________________________________
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
#Ajout des espacements_______________________________________________________________________
def add_space(size='medium'):
    """Ajoute un espace entre les sections (j'ai fait ca parce que st.write("") c'est moche)"""
    spaces = {
        'small': 1,
        'medium': 2,
        'large': 3
    }
    # on fait des st.write vides pour faire de l'espace
    for _ in range(spaces.get(size, 2)):
        st.write("")

#sidebar_____________________________________________________________________________________
def render_sidebar():
    """la sidebar avec le mode focus dedans"""
    FocusMode.render_toggle() # le bouton mode focus 25min
    st.sidebar.divider()

#Home/mood du jour____________________________________________________________________________
def render_home_page():
    """page d'accueil pour l'humeur du jour"""

    #affiche la serie en premier
    StreakSystem.display_streak()
    add_space('small')

    #message de bienvenue
    st.header(f"☀️ Bonjour {st.session_state.profile['prenom']} !")

    #formulaire d'humeur dans un cadre
    card("Comment te sens-tu aujourd'hui ?", mood_form)

    #contenu secondaire masqué en mode focus
    if not FocusMode.is_enabled():
        with st.expander("📋 Voir mes tâches du jour"):
            render_task_calendar()
        
        show_encouragement() # <- encouragement aléatoire

def mood_form():
    """Formulaire pour l'humeure du jour"""
    with st.form("mood_form"):
        mood = st.slider("Humeur générale (1-10)", 1, 10, 5)  # 5 par defaut c'est le milieu
        emotion = st.text_input("💭 Ressenti émotionnel", placeholder="Ex: calme, anxieux, motivé...")
        motivation = st.text_input("🎯 Motivation du jour", placeholder="Ex: faire du sport, voir des amis...")
        notes = st.text_area("📝 Notes / Ressenti libre", placeholder="Tu peut écrire ce que tu veux ici...")

        submitted = st.form_submit_button("Enregistrer", type="primary")

        if submitted:
            save_mood(mood, emotion, motivation, notes)
            st.session_state.mood_logged_today = True
            st.success("✅ Merci ! Tes ressentis sont enregistrés 🚀")

            #petit bonus si on log tot le matin (avant 9h)
            if datetime.now().hour < 9:
                st.info("🌅 Bravo ! Tu commences la journée du bon pied !")

            st.rerun()

#DashBoard_______________________________________________________________________________________________________________________________
# c'est la page principale une fois qu'on a fait l'humeur
from ui.tdah_dashboard import render_dashboard as render_tdah_dashboard

def render_dashboard():
    """le dashboard principal avec tout dedans"""
    render_sidebar()

    #si le mode focus est activé on affiche que ca
    if FocusMode.is_enabled():
        FocusMode.render_full_screen()
        return  # on sort de la fonction

    # verifie si y'a une tache programmée maintenant
    from services.tdah_features import check_scheduled_tasks
    task_id, task_title = check_scheduled_tasks()
    
    if task_id and not st.session_state.get('notification_dismissed'):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, #FFE082, #FFD54F);
                padding: 24px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                margin-bottom: 20px;
            '>
                <div style='font-size: 48px; margin-bottom: 12px;'>⏰</div>
                <div style='font-size: 20px; font-weight: 600; color: #2D3748; margin-bottom: 8px;'>
                    C'est l'heure !
                </div>
                <div style='font-size: 16px; color: #718096;'>
                    {task_title}
                </div>
            </div>
            """.replace('{task_title}', task_title), unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 1, 1])
            with col_a:
                if st.button("🎯 Lancer le timer", type="primary", use_container_width=True):
                    st.session_state.current_focus_task = task_title
                    st.session_state.current_focus_task_id = task_id
                    FocusMode.start()
                    st.rerun()
            
            with col_b:
                if st.button("⏰ Rappeler dans 5 min", use_container_width=True):
                    st.session_state.notification_dismissed = True
                    st.session_state.snooze_until = datetime.now() + timedelta(minutes=5)
                    st.rerun()
            
            with col_c:
                if st.button("❌ Ignorer", use_container_width=True):
                    st.session_state.notification_dismissed = True
                    st.rerun()
    
    st.header(f"Tableau de bord - {date.today().strftime('%d/%m/%Y')}")

    #navigation
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Accueil", "💬 Mathi", "📊 Progrès", "⚙️ Plus"])
    with tab1:
        render_today_tab()
    with tab2:
        render_chat_section()
    with tab3:
        render_tdah_dashboard()
    with tab4:
        render_more_tab()


def render_today_tab():
    """Onglet principal - j'ai essayé de le rendre joli et motivant"""

    # ========== CONNEXION BDD ==========
    conn = st.session_state.conn
    cursor = conn.cursor()
    today = date.today().isoformat()

    # ========== EN-TÊTE : les 3 metriques importantes ==========

    # 3 colonnes pour les stats
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        tasks_finish()
    
    with col2:
    # Humeur du jour - CORRIGÉ pour mood_value
        render_today_mood_card()

    
    with col3:
        render_streak_card()
    
    render_quick_notes()
    
    st.markdown("---")
    
    # ========== ZONE PRINCIPALE : 2 COLONNES ==========
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # === FOCUS DU JOUR ===
        
        render_task_calendar()
        st.markdown("<br>", unsafe_allow_html=True)
        

    # === TÂCHES DU JOUR ===
    render_focus_of_day()
        
    
    with col_right:
        
        # === PROCHAINS OBJECTIFS ===
        render_next_goals()
        
        st.markdown("<br>", unsafe_allow_html=True)



#nouvelle fonction que j'ai ajoutée________________________________________________________

def render_focus_of_day():
    """la grande carte focus du jour - montre la tache prioritaire"""
    conn = st.session_state.conn
    cursor = conn.cursor()
    today = date.today().isoformat()

    # on prend la premiere tache pas encore finie
    cursor.execute("""
        SELECT id, title, time_spent
        FROM tasks
        WHERE task_date = ? AND done = 0
        ORDER BY created_at ASC
        LIMIT 1
    """, (today,))
    
    task = cursor.fetchone()

    if task:
        task_id, title, time_spent = task
        # calcul du progres (j'ai mis 1h comme objectif par defaut)
        progress = min((time_spent / 1.0) * 100, 100) if time_spent else 0
        
        # Carte HTML stylée
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
            color: white;
            margin-bottom: 16px;
        '>
            <div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>
                🎯 Focus du jour
            </div>
            <h2 style='margin: 12px 0; font-size: 24px; font-weight: 600;'>
                {title}
            </h2>
            <div style='background: rgba(255,255,255,0.2); height: 8px; border-radius: 4px; overflow: hidden;'>
                <div style='background: white; width: {progress}%; height: 100%; transition: width 0.3s;'></div>
            </div>
            <div style='margin-top: 12px; font-size: 14px; opacity: 0.9;'>
                ⏱️ {time_spent:.1f}h investies
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bouton terminer
        if st.button(f"✅ Marquer '{title}' comme terminée", key=f"complete_focus_{task_id}"):
            from services.tdah_features import PointsSystem
            cursor.execute("UPDATE tasks SET done = 1, completed_at = CURRENT_TIMESTAMP WHERE id = ?", (task_id,))
            conn.commit()
            PointsSystem.award_points('task_completed')
            st.success("🎉 Bravo ! Tâche terminée !")
            st.rerun()
    
    else:
        # Aucune tâche : message encourageant
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            color: #2D3748;
        '>
            <h2 style='margin: 0;'>🎉 Aucune tâche en cours !</h2>
            <p style='margin-top: 12px; opacity: 0.8;'>
                Profite de cette pause ou ajoute une nouvelle tâche
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_motivation_block():
    """Affiche un message motivant basé sur les statistiques"""
    conn = st.session_state.conn
    cursor = conn.cursor()
    
    # Calculer la série manuellement
    cursor.execute("""
        SELECT COUNT(DISTINCT DATE(created_at)) 
        FROM mood 
        WHERE DATE(created_at) >= DATE('now', '-7 days')
    """)
    streak = cursor.fetchone()[0]
    
    # Messages selon la série
    if streak >= 7:
        message = "🔥 Incroyable ! 7 jours de suite !"
        color = "#10B981"
    elif streak >= 3:
        message = f"💪 Belle série de {streak} jours !"
        color = "#3B82F6"
    elif streak >= 1:
        message = f"🌱 Continue, {streak} jour(s) !"
        color = "#8B5CF6"
    else:
        message = "🚀 Commence une nouvelle série !"
        color = "#6B7280"
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {color}22, {color}11);
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid {color};
        text-align: center;
    '>
        <div style='font-size: 18px; font-weight: 600; color: #2D3748;'>
            {message}
        </div>
        <div style='font-size: 14px; color: #6B7280; margin-top: 4px;'>
            {streak} jour(s) actifs cette semaine
        </div>
    </div>
    """, unsafe_allow_html=True)



def render_next_goals():
    """Affiche les prochains objectifs de badges"""
    st.markdown("""
    <div style='
        background: white;
        padding: 6px;
        border-radius: 12px;
        border: 2px solid #E5E7EB;
        text-align: center;
    '>
        <h4 style='margin-top: 0; color: #374151;'>🏆 Prochain badge</h4>
    """, unsafe_allow_html=True)
    
    from services.tdah_features import BadgeSystem
    
    # Vérifier quel badge est proche
    conn = st.session_state.conn
    cursor = conn.cursor()
    
    # Exemple : badge premiers pas (5 tâches)
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
    tasks_done = cursor.fetchone()[0]
    
    if tasks_done < 5:
        remaining = 5 - tasks_done
        progress = (tasks_done / 5) * 100
        
        st.markdown(f"""
        <div style='margin: 12px 0;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                <span>🌟 Premiers pas</span>
                <span style='color: #6B7280;'>{tasks_done}/5</span>
            </div>
            <div style='background: #E5E7EB; height: 6px; border-radius: 3px; overflow: hidden;'>
                <div style='background: #10B981; width: {progress}%; height: 100%;'></div>
            </div>
            <div style='font-size: 12px; color: #6B7280; margin-top: 4px;'>
                Plus que {remaining} tâches !
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Badge série 7 jours
    from services.tdah_features import StreakSystem
    streak = get_manual_streak()
    
    if streak < 7:
        remaining_days = 7 - streak
        progress = (streak / 7) * 100
        
        st.markdown(f"""
        <div style='margin: 12px 0;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                <span>🔥 Semaine parfaite</span>
                <span style='color: #6B7280;'>{streak}/7</span>
            </div>
            <div style='background: #E5E7EB; height: 6px; border-radius: 3px; overflow: hidden;'>
                <div style='background: #F59E0B; width: {progress}%; height: 100%;'></div>
            </div>
            <div style='font-size: 12px; color: #6B7280; margin-top: 4px;'>
                Plus que {remaining_days} jours !
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_mini_mood_chart():
    """Mini graphique d'évolution de l'humeur (7 derniers jours)"""
    conn = st.session_state.conn
    
    try:
        # Requête CORRECTE avec mood_value et created_at
        df = pd.read_sql("""
            SELECT 
                DATE(created_at) as date,
                mood_value
            FROM mood
            ORDER BY created_at DESC
            LIMIT 7
        """, conn)
        
        if not df.empty and len(df) > 0:
            # Inverser pour avoir l'ordre chronologique
            df = df.iloc[::-1].reset_index(drop=True)
            df['date'] = pd.to_datetime(df['date'])
            
            # Graphique matplotlib
            fig, ax = plt.subplots(figsize=(6, 3))
            
            ax.plot(df['date'], df['mood_value'], 
                    marker='o', linewidth=2.5, 
                    color='#667eea', markersize=8)
            
            ax.fill_between(df['date'], df['mood_value'], alpha=0.2, color='#667eea')
            
            ax.set_ylim(0, 10)
            ax.set_ylabel('Humeur', fontsize=10)
            ax.grid(True, alpha=0.2, linestyle='--')
            ax.set_facecolor('#F9FAFB')
            
            plt.xticks(rotation=45, ha='right', fontsize=9)
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close()
        else:
            st.info("📊 Enregistre ton humeur plusieurs jours pour voir l'évolution")
    
    except Exception as e:
        st.error(f"Erreur graphique: {e}")



    

#plus____________________________________________________________________________________________________________________

def render_section_title(icon, title):
    """Crée un titre de section dans une carte arrondie"""
    st.markdown(f"""
    <div style='
        background: white;
        padding: 12px 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        display: inline-block;
    '>
        <span style='font-size: 18px; font-weight: 600; color: #2D3748;'>{icon} {title}</span>
    </div>
    """, unsafe_allow_html=True)


def render_more_tab():
    """Onglet Plus - Design EXACT selon plus.jpg"""
    
    # === 1. PRÉFÉRENCES ===
    render_section_title("⚙️", "Préférences")
    render_preferences_section()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === 2. GESTION DES SAUVEGARDES ===
    render_section_title("💾", "Gestion des sauvegardes")
    render_backup_management()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === 3. EXPORT DE TES DONNÉES ===
    render_section_title("📥", "Export de tes données")
    render_export_section_styled()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === 4. BACKUPS ===
    render_section_title("💾", "Backups")
    render_backups_section()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === 5. SÉCURITÉ ET CHIFFREMENT ===
    render_section_title("🔐", "Sécurité et chiffrement")
    render_security_section_styled()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === 6. BONNES PRATIQUES ===
    render_section_title("🛡️", "Bonnes pratiques de sécurité")
    render_best_practices()


def render_preferences_section():
    """Section Préférences - Layout exact de plus.jpg"""
    
    # Layout 2 colonnes pour Apparence + Notifications
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("🎨 **Apparence**")
        
        text_size = st.slider(
            "",
            min_value=14,
            max_value=20,
            value=st.session_state.get('text_size', 16),
            label_visibility="collapsed"
        )
        st.session_state.text_size = text_size
        st.caption(f"Taille: {text_size}")
    
    with col2:
        st.markdown("🔔 **Notifications**")
        
        notifications = st.checkbox(
            "Activer les notifications",
            value=st.session_state.get('notifications_enabled', True)
        )
        st.session_state.notifications_enabled = notifications
        
        animations = st.checkbox(
            "Activer les animations de célébrations",
            value=st.session_state.get('animations_enabled', True)
        )
        st.session_state.animations_enabled = animations
    
    # Concentration (pleine largeur en dessous)
    st.markdown("")
    st.markdown("🎯 **Concentration**")
    
    focus_default = st.checkbox(
        "Démarrer en mode Focus par défaut",
        value=st.session_state.get('focus_default', False)
    )
    st.session_state.focus_default = focus_default
    
    # Bouton sauvegarder (pleine largeur, bleu)
    st.markdown("")
    if st.button("💾 Sauvegarder les préférences", type="primary", use_container_width=True):
        st.success("✅ Préférences sauvegardées !")


def render_backup_management():
    """Section Gestion des sauvegardes - Layout 2 colonnes avec boutons à droite EMPILÉS"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Protège tes données en créant des sauvegardes régulières de ta base de données.
        """)
        
        with st.expander("📖 Pourquoi faire des backups ?"):
            st.markdown("""
            - 🛡️ **Protection contre la perte de données**
            - 🔄 **Possibilité de restaurer une version antérieure**
            - ✨ **Tranquillité d'esprit**
            """)
    
    with col2:
        # Boutons empilés verticalement (pas côte à côte)
        if st.button("📥 Créer un backup maintenant", type="primary", use_container_width=True):
            from db.database import DB_PATH
            from utils.backup import BackupManager
            try:
                backup_manager = BackupManager(str(DB_PATH))
                backup_path = backup_manager.create_backup(prefix="manual_backup")
                st.success(f"✅ Backup créé !")
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
        
        # Bouton en dessous (pas à côté)
        if st.button("🧹 Nettoyer les anciens", use_container_width=True):
            from db.database import DB_PATH
            from utils.backup import BackupManager
            backup_manager = BackupManager(str(DB_PATH))
            deleted = backup_manager.clean_old_backups(keep_count=10)
            st.info(f"🗑️ {deleted} supprimé(s)")


def render_export_section_styled():
    """Section Export - Layout 2 colonnes avec boutons à droite EMPILÉS"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Tu peux exporter toutes tes données pour :
        
        - Les sauvegarder
        - Les analyser ailleurs
        - Les partager avec un professionnel de santé
        """)
        
        st.warning("⚠️ **Note de confidentialité** : Tes données sont stockées localement et chiffrées sur ton appareil.")
    
    with col2:
        # Boutons empilés verticalement (pas côte à côte)
        if st.button("📊 Export Excel", type="primary", use_container_width=True):
            export_to_excel()
        
        # Bouton en dessous
        if st.button("📄 Export PDF", use_container_width=True):
            export_to_pdf()


def render_backups_section():
    """Section Backups avec layout 2 colonnes"""
    from db.database import DB_PATH
    from utils.backup import BackupManager
    from pathlib import Path
    
    backup_manager = BackupManager(str(DB_PATH))
    backups = backup_manager.list_backups()
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown(f"**{len(backups)} backup(s) trouvé(s)**")
        st.markdown("")
        
        if backups:
            for backup in backups[:3]:  # Afficher max 10
                info = backup_manager.get_backup_info(backup)
                
                # Ligne arrondie pour chaque backup
                st.markdown(f"""
                <div style='
                    background: white;
                    padding: 12px 16px;
                    border-radius: 8px;
                    border: 1px solid #E2E8F0;
                    margin-bottom: 8px;
                '>
                    <div style='font-size: 14px; color: #2D3748;'>{info['name']}</div>
                    <div style='font-size: 12px; color: #718096;'>{info['created_str']} • {info['size_mb']} MB</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucun backup disponible")
    
    with col2:
        st.markdown("### ⚙️ Backup automatique")
        st.caption("Les backups sont créés au démarrage de l'application. Tu peux configurer le nombre de backups à conserver.")
        
        st.markdown("")
        st.markdown("**Nombre de backups à conserver**")
        
        keep_count = st.slider(
            "",
            min_value=5,
            max_value=30,
            value=st.session_state.get('backup_keep_count', 16),
            label_visibility="collapsed"
        )
        st.session_state.backup_keep_count = keep_count
        
        st.markdown("")
        
        if st.button("💾 Sauvegarder", type="primary", use_container_width=True):
            st.success(f"✅ Configuration sauvegardée : {keep_count} backups")


def render_security_section_styled():
    """Section Sécurité avec badges colorés"""
    from utils.encryption_config import EncryptionConfig
    from pathlib import Path
    
    # Intro avec tooltip
    col1, col2 = st.columns([0.97, 0.03])
    with col1:
        st.markdown("Cette section te permet de renforcer la sécurité de tes données en activant le **chiffrement**.")
    with col2:
        with st.expander("ℹ️", expanded=False):
            st.markdown("""
            **Qu'est-ce que le chiffrement ?**
            
            - 🔒 Tes notes et données sensibles seront chiffrées
            - 🔑 Seule ta clé peut déchiffrer les données
            - 🛡️ Protection supplémentaire
            
            **Important :**
            - ⚠️ Si tu perds la clé, tu perds les données
            - 💾 Backup automatique avant chaque opération
            """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    config = EncryptionConfig()
    is_enabled = config.is_encryption_enabled()
    
    # Statut actuel
    st.markdown("### 📊 Statut actuel")
    st.markdown("")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if is_enabled:
            # Badge vert
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, #C8E6C9, #81C784);
                padding: 12px 20px;
                border-radius: 8px;
                display: inline-block;
                margin-bottom: 12px;
            '>
                <span style='color: white; font-weight: 600;'>✅ Le chiffrement est activé</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Badge bleu info
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, #BBDEFB, #90CAF9);
                padding: 12px 20px;
                border-radius: 8px;
                display: inline-block;
                margin-bottom: 12px;
            '>
                <span style='color: white; font-weight: 500;'>🔒 Tes notes et données sensibles sont chiffrées</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Warning jaune avec tooltip
            col_warn1, col_warn2 = st.columns([0.97, 0.03])
            with col_warn1:
                st.warning("⚠️ **IMPORTANT** : Sauvegarde ce fichier en lieu sûr !")
            with col_warn2:
                key_file = Path("data/secret.key")
                with st.expander("ℹ️", expanded=False):
                    st.markdown(f"""
                    **📁 Emplacement :**
                    ```
                    {key_file.absolute()}
                    ```
                    """)
        else:
            # Badge orange
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, #FFE082, #FFB74D);
                padding: 12px 20px;
                border-radius: 8px;
                display: inline-block;
                margin-bottom: 12px;
            '>
                <span style='color: white; font-weight: 600;'>⚠️ Le chiffrement est désactivé</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if is_enabled:
            # Bouton Désactiver
            if "confirm_disable_encryption" not in st.session_state:
                st.session_state.confirm_disable_encryption = False
            
            if not st.session_state.confirm_disable_encryption:
                if st.button("🔓 Désactiver le chiffrement", use_container_width=True):
                    st.session_state.confirm_disable_encryption = True
                    st.rerun()
            else:
                st.warning("**Confirmer ?**")
                if st.button("✅ Oui", type="primary", use_container_width=True):
                    result = config.disable_encryption()
                    if result["success"]:
                        st.success("✅ Désactivé !")
                        st.session_state.confirm_disable_encryption = False
                        st.rerun()
                if st.button("❌ Non", use_container_width=True):
                    st.session_state.confirm_disable_encryption = False
                    st.rerun()
        else:
            # Bouton Activer
            if st.button("🔒 Activer le chiffrement", type="primary", use_container_width=True):
                result = config.enable_encryption()
                if result["success"]:
                    st.success("✅ Activé !")
                    st.rerun()


def render_best_practices():
    """Section Bonnes pratiques avec 2 boutons arrondis"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📖 Lire les recommandations", expanded=False):
            st.markdown("""
            **Protection des données :**
            1. Backups réguliers
            2. Sauvegarde de la clé de chiffrement
            3. Permissions système restrictives
            
            **En cas de perte :**
            - Vérifie les backups
            - Restaure depuis un backup récent
            """)
    
    with col2:
        with st.expander("🔧 Information techniques", expanded=False):
            st.markdown("""
            **Configuration :**
            - Algorithme : Fernet (AES 128-bit)
            - Stockage : Local uniquement
            - Chiffrement : Au repos
            """)


# ============================================================================
# FIN ONGLET PLUS
# ============================================================================

#Tâches/calendrier etc___________________________________________________________________________________________________________________
def render_task_calendar():
    """affiche les tâches avec selecteur de date formulaire"""
    from services.habit_service import update_task_time

    if st.session_state.selected_day is None:
        st.session_state.selected_day = date.today()

    #formulaire d'ajout horizontale avec date et heure
    with st.form("new_task_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        with col1:
            new_task = st.text_input("", placeholder="Ajoute une tâche...", label_visibility="collapsed")
        with col2:
            task_date = st.date_input(
                "📅",
                value=st.session_state.selected_day,
                label_visibility="collapsed"
            )
            st.session_state.selected_day = task_date
        with col3:
            start_time = st.time_input("⏰", value=None, label_visibility="collapsed", help="Heure de début (optionnel)")
        with col4:
            submitted = st.form_submit_button("Ajouter", type="primary", use_container_width=True)
        if submitted and new_task.strip():
            # Convertir l'heure en string si elle existe
            time_str = start_time.strftime("%H:%M") if start_time else None
            add_task(new_task, task_date=task_date, start_time=time_str)
            PointsSystem.award_points('task_completed')
            st.rerun()
    st.markdown("---")

    #Affichage des tâches pour la date selectionné
    tasks = get_today_tasks(task_date=st.session_state.selected_day, show_completed=False)
    
    if tasks:
        for task_id, title, done, time_spent, task_date_str, start_time in tasks:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                checked = st.checkbox(
                    title,
                    value=bool(done),
                    key=f"task_{task_id}"
                )
                if checked != bool(done):
                    toggle_task(task_id, checked)
                    if checked:
                        PointsSystem.award_points('task_completed')
                    st.rerun()
            with col2:
                time_value = st.number_input(
                    "⏱️",
                    min_value=0.0,
                    max_value=24.0,
                    value=float(time_spent) if time_spent else 0.0,
                    step=0.25,
                    key=f"time_{task_id}",
                    label_visibility="collapsed"
                )
                if time_value != (time_spent or 0.0):
                    update_task_time(task_id, time_value)
                    if time_value > 0:
                        PointsSystem.award_points('task_with_time')
            with col3:
                if st.button("🗑️", key=f"del_{task_id}"):
                    delete_task(task_id)
                    st.rerun()
    else:
        st.info("Aucune tâche en cours pour cette date 📋")

def render_task_history():
    """Affiche l'historique des tâches par jour"""
    conn = st.session_state.conn
    df = pd.read_sql("""
        SELECT title, done, time_spent, created_at, completed_at
        FROM tasks
        ORDER BY created_at DESC
        LIMIT 50
    """, conn)
    if not df.empty:
        df['date'] = pd.to_datetime(df['created_at']).dt.date

        grouped = df.groupby('date')
        for date_value, group in grouped:
            completed = group[group['done'] == 1].shape[0]
            total = group.shape[0]
            total_time = group['time_spent'].sum()

            st.markdown(f"### 📅 {date_value.strftime('%d/%m/%Y')}")
            st.markdown(f"**{completed}/{total} tâches terminées** | ⏱️ Temps total: {total_time:.1f}h")

            for _, row in group.iterrows():
                status_icon = '✅' if row['done'] == 1 else '⬜'
                time_str = f"⏱️ {row['time_spent']:.1f}h" if row['time_spent'] > 0 else ""
                completed_str = ""

                if row['done'] == 1 and pd.notna(row['completed_at']):
                    completed_str = f" (Terminée le {row['completed_at'][:16]})"
                st.markdown(f"{status_icon} **{row['title']}** {time_str}{completed_str}")

            st.divider()
    
    else: 
        st.info("Pas encore d'historique")
#tâches________________________________________________________________________________________________________________________________
def tasks_finish():
    """Affiche les tâches terminées aujourd'hui avec style"""
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #E8F4F8, #C7E0F4);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 16px;
    </div>
    """, unsafe_allow_html=True)
    conn = st.session_state.conn
    today = date.today().isoformat()

    df = pd.read_sql(f"""
        SELECT id, title, done, time_spent, task_date
        FROM tasks 
        WHERE DATE(task_date) = '{today}' AND done = 1
        ORDER BY completed_at DESC
    """, conn)

    if not df.empty:
        # Calculer les statistiques
        total_tasks = len(df)
        total_time = df['time_spent'].sum()
        
        # Emoji selon le nombre de tâches
        if total_tasks >= 5:
            emoji = "🏆"
        elif total_tasks >= 3:
            emoji = "⭐"
        else:
            emoji = "✅"

        
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #11998E, #38EF7D);
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 16px;
        '>
            <div style='font-size: 48px; margin-bottom: 8px;'>{emoji}</div>
            <div style='font-size: 32px; font-weight: 700; margin-bottom: 4px;'>
                {total_tasks} tâche{'s' if total_tasks > 1 else ''}
            </div>
            <div style='font-size: 16px; opacity: 0.9;'>
                Terminée{'s' if total_tasks > 1 else ''} aujourd'hui
            </div>
            <div style='
                border-top: 2px solid rgba(255,255,255,0.3);
                padding-top: 16px;
                margin-top: 16px;
                display: flex;
                gap: 24px;
                justify-content: center;
            '>
                <div style='flex: 1;'>
                    <div style='font-size: 14px; opacity: 0.8; margin-bottom: 4px;'>⏱️ Temps total</div>
                    <div style='font-size: 24px; font-weight: 600;'>{total_time:.1f}h</div>
                </div>
                <div style='flex: 1;'>
                    <div style='font-size: 14px; opacity: 0.8; margin-bottom: 4px;'>📊 Moyenne</div>
                    <div style='font-size: 24px; font-weight: 600;'>{total_time/total_tasks:.1f}h</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        
    
    else:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #F3F4F6, #E5E7EB);
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        '>
            <div style='font-size: 40px; margin-bottom: 8px;'>📝</div>
            <div style='font-size: 18px; font-weight: 600; color: #6B7280;'>
                Aucune tâche terminée aujourd'hui
            </div>
            <div style='font-size: 14px; color: #9CA3AF; margin-top: 8px;'>
                C'est le moment de commencer ! 💪
            </div>
        </div>
        """, unsafe_allow_html=True)


        


#Notes________________________________________________________________________________________________________________________________
def render_quick_notes():
    """Bloc notes rapide"""
    # Carte visuelle (HTML)
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #F3E8FF, #E9D5FF);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 16px;
    '>
        <div style='font-size: 14px; color: #6B7280; margin-bottom: 8px; text-align: center;'>
            ✍️ Note rapide
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("note_form", clear_on_submit=True):
        note = st.text_area(
            "",
            placeholder="💬 Une pensée, une émotion...",
            height=110,
            label_visibility="collapsed"
        )

        submitted = st.form_submit_button(
            "📝 Enregistrer",
            type="primary",
            use_container_width=True
        )

        if submitted and note.strip():
            add_note(note)
            st.success("✅ Note sauvegardée !")
            st.rerun()


def render_notes_history():
    from utils.encryption_config import get_decrypted_text
    """affiche les dernière notes"""
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
            content = get_decrypted_text(row['content'])
            st.text(content[:100] + ("..." if len(content) > 100 else ""))
    else:
        st.info("Pas encore de notes")

#Humeurs_______________________________________________________________________________________________________________________
def render_today_mood_card():
    """Carte de l'humeur du jour"""
    conn = st.session_state.conn
    today = date.today().isoformat()
    
    # REQUÊTE CORRIGÉE
    df = pd.read_sql(f"""
        SELECT mood_value, emotion, motivation 
        FROM mood 
        WHERE DATE(created_at) = '{today}'
        ORDER BY created_at DESC 
        LIMIT 1
    """, conn) 
        # ... reste du code HTML inchangé

    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #E8F4F8, #C7E0F4);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 16px;
    </div>
    """, unsafe_allow_html=True)
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
        mood_value = mood["mood_value"]
        emotion = mood["emotion"]
        motivation = mood["motivation"]

        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #E8F4F8, #C7E0F4);
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        '>
            <div style='font-size: 40px; margin-bottom: 8px;'>😊</div>
            <div style='font-size: 32px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>
                {mood_value}/10
            </div>
            <div style='font-size: 16px; color: #718096;'>
                Humeur du jour
            </div>
            <div style='
                border-top: 2px solid rgba(0,0,0,0.1);
                padding-top: 16px;
                margin-top: 16px;
                display: flex;
                gap: 24px;
                justify-content: center;
            '>
                <div style='flex: 1;'>
                    <div style='font-size: 14px; color: #718096; margin-bottom: 4px;'>💭 Émotion</div>
                    <div style='font-size: 24px; font-weight: 600; color: #2D3748;'>{emotion}</div>
                </div>
                    <div style='flex: 1;'>
                    <div style='font-size: 14px; color: #718096; margin-bottom: 4px;'>🎯 Objectif</div>
                    <div style='font-size: 24px; font-weight: 600; color: #2D3748;'>{motivation}</div>
                </div>
            </div>

        </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Pas encore d'humeur pour aujourd'hui")

def render_streak_card():
    """Affiche la carte série/points - Colonne droite"""
    """Affiche un message motivant basé sur les statistiques"""
    conn = st.session_state.conn
    cursor = conn.cursor()
    
    # Calculer la série manuellement
    cursor.execute("""
        SELECT COUNT(DISTINCT DATE(created_at)) 
        FROM mood 
        WHERE DATE(created_at) >= DATE('now', '-7 days')
    """)
    streak = cursor.fetchone()[0]
    
    # Messages selon la série
    if streak >= 7:
        message = "🔥 Incroyable ! 7 jours de suite !"
        color = "#10B981"
    elif streak >= 3:
        message = f"💪 Belle série de {streak} jours !"
        color = "#3B82F6"
    elif streak >= 1:
        message = f"🌱 Continue, {streak} jour(s) !"
        color = "#8B5CF6"
    else:
        message = "🚀 Commence une nouvelle série !"
        color = "#6B7280"

    # Carte visuelle (HTML)
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #FFE082, #FFD54F);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 16px;
    </div>
    """, unsafe_allow_html=True)
    streak = StreakSystem.calculate_streak()
    points = PointsSystem.get_total_points()
    
    
    # Carte jaune/orange comme dans le design
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #FFE082, #FFD54F);
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    '>
        <div style='font-size: 18px; font-weight: 600; color: #2D3748;'>
            {message}
        </div>
        <div style='font-size: 14px; color: #6B7280; margin-top: 4px;'>
        </div>
        <div style='font-size: 32px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>{streak}</div>
        <div style='font-size: 16px; color: #718096; margin-bottom: 16px;'>jour{'s' if streak > 1 else ''} de suite !</div>
        <div style='border-top: 2px solid rgba(0,0,0,0.1); padding-top: 16px; margin-top: 16px;'>
            <div style='font-size: 14px; color: #718096; margin-bottom: 4px;'>⭐ Points</div>
            <div style='font-size: 24px; font-weight: 600; color: #2D3748;'>{points}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_mood_summary():
    """Graphique de l'évolution de l'humeur avec Plotly"""
    from services.mood_service import get_mood_history
    
    data = get_mood_history()
    
    if not data:
        st.info("Pas encore d'humeur enregistrée 📊")
        return
    
    # Créer le DataFrame avec les BONNES colonnes
    df = pd.DataFrame(data)
    
    # S'assurer que les colonnes sont correctes
    if 'created_at' in df.columns and 'mood_value' in df.columns:
        df['date'] = pd.to_datetime(df['created_at']).dt.date
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['mood_value'],
            mode='lines+markers',
            name='Humeur',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Évolution de l'humeur",
            xaxis_title="Date",
            yaxis_title="Humeur (1-10)",
            yaxis=dict(range=[0, 10]),
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Structure de données incorrecte")

    
    # Statistiques_______________________________________________________________________________
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Moyenne", f"{df['Humeur'].mean():.1f}/10")
    with col2:
        st.metric("Maximum", f"{df['Humeur'].max()}/10")
    with col3:
        st.metric("Minimum", f"{df['Humeur'].min()}/10")