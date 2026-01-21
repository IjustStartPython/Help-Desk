# MODULE TDAH FONCTIONS
# toutes les features pour aider les personnes TDAH
# j'ai mis pleins de trucs motivants dedans

import streamlit as st
from datetime import datetime, timedelta, date
from db.database import get_connection
import json

# systeme de points____________________________________
# ca permet de gagner des points quand on fait des trucs


class PointsSystem:
    # les points qu'on gagne pour chaque action
    POINTS = {
        "mood_logged": 10,  # quand on log son humeur
        "task_completed": 20,  # quand on fini une tache
        "task_with_time": 30,  # quand on met le temps passé
        "streak_3_days": 50,  # 3 jours de suite
        "streak_7_days": 100,  # 1 semaine !
        "streak_14_days": 200,  # 2 semaines
        "streak_30_days": 500,  # 1 mois (ouf)
        "chat_used": 5,  # utilisation du chat
        "week_completed": 150,  # semaine complete
        "all_tasks_done": 40,  # toutes les taches du jour faites
        "early_bird": 15,  # humeur donné avant 9H du mat
        "consistency": 25,  # 5 jours sur 7 dans la semaine
    }

    @staticmethod
    def init_points_table():
        """crée la table points si elle existe pas"""
        conn = st.session_state.conn
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                points INTEGER NOT NULL,
                earned_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()

    @staticmethod
    def award_points(action: str) -> int:
        """donne des points pour une action"""
        points = PointsSystem.POINTS.get(action, 0)

        if points > 0:
            conn = st.session_state.conn
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO points (action, points)
                VALUES (?, ?)
            """,
                (action, points),
            )
            conn.commit()

            # affiche une notif pour que l'utilisateur soit content
            st.success(f"🎉 +{points} points ! ({action})")
        return points

    @staticmethod
    def get_total_points() -> int:
        """retourne le total des points"""
        conn = st.session_state.conn
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(points) FROM points")
        result = cursor.fetchone()[0]
        return result or 0  # 0 si None

    @staticmethod
    def get_points_history(days: int = 7):
        """historique des points sur X jours"""
        conn = st.session_state.conn
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                DATE(earned_at) as date,
                SUM(points) as daily_points
            FROM points
            WHERE earned_at >= date('now', ? || ' days')
            GROUP BY DATE(earned_at)
            ORDER BY date DESC
        """,
            (f"--{days}",),
        )
        results = cursor.fetchall()
        return results


# système de streaks (series de jours)


class StreakSystem:
    """gere les series de jours consecutifs"""

    @staticmethod
    def calculate_streak() -> int:
        """calcule combien de jours de suite on a log son humeur"""
        conn = st.session_state.conn
        cursor = conn.cursor()

        # on prend toutes les dates distinctes ou on a log
        cursor.execute(
            """
            SELECT DISTINCT DATE(created_at) as date
            FROM mood
            ORDER BY date DESC
        """
        )
        dates = [row[0] for row in cursor.fetchall()]

        if not dates:
            return 0  # aucune humeur enregistrée

        streak = 1
        current_date = date.today()

        # verif si l'humeur a été mis aujourd'hui ou hier
        latest_date = datetime.strptime(dates[0], "%Y-%m-%d").date()
        if (current_date - latest_date).days > 1:
            return 0  # serie cassée :(

        # compte les jours d'affilé
        for i in range(len(dates) - 1):
            date1 = datetime.strptime(dates[i], "%Y-%m-%d").date()
            date2 = datetime.strptime(dates[i + 1], "%Y-%m-%d").date()

            if (date1 - date2).days == 1:
                streak += 1
            else:
                break  # y'a un trou donc on arrete
        return streak

    @staticmethod
    def display_streak():
        """affiche la série actuelle avec un joli design"""
        streak = StreakSystem.calculate_streak()

        if streak == 0:
            st.info("🔥 Commence ta série aujourd'hui !")
        elif streak == 1:
            st.success("🔥 **1 jour** - Continue !")
        else:
            # si 30 jours on fait la fete !
            if streak >= 30:
                st.balloons()

            st.markdown(
                f"""
            <div style='
                background: linear-gradient(135deg, #FFE082, #FFD54F);
                padding: 24px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            '>
                <div style='color: #2D3748; margin: 0; font-size: 56px; font-weight: 700; line-height: 1.2;'>
                    🔥 {streak}
                </div>
                <div style='color: #718096; margin: 8px 0 0 0; font-size: 18px; font-weight: 500;'>
                    jour{'s' if streak > 1 else ''} de suite !
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # attribuer les points
            if streak == 3:
                PointsSystem.award_points("streak_3_days")
            elif streak == 7:
                PointsSystem.award_points("streak_7_days")
            elif streak == 14:
                PointsSystem.award_points("streak_14_days")
            elif streak == 30:
                PointsSystem.award_points("streak_30_days")


# les badges_____________________________________________________________________________
# systeme de badges pour motiver (comme dans les jeux video)


class BadgeSystem:

    # tous les badges possibles
    BADGES = {
        "first_day": {
            "name": "🌱 Premier Jour",
            "description": "Tu as commencé ton chemin",
            "icon": "🌱",
            "condition": lambda: StreakSystem.calculate_streak() >= 1,  # juste 1 jour
        },
        "first_week": {
            "name": "🌟 Première Semaine",
            "description": "7 jours consécutifs",
            "icon": "🌟",
            "condition": lambda: StreakSystem.calculate_streak() >= 7,
        },
        "mood_master": {
            "name": "😊 Maître des Émotions",
            "description": "30 humeurs enregistrées",
            "icon": "😊",
            "condition": lambda: BadgeSystem._count_moods() >= 30,
        },
        "task_warrior": {
            "name": "⚔️ Guerrier des Tâches",
            "description": "50 tâches complétées",
            "icon": "⚔️",
            "condition": lambda: BadgeSystem._count_completed_tasks() >= 50,
        },
        "consistency_king": {
            "name": "👑 Roi de la Régularité",
            "description": "30 jours de suite",
            "icon": "👑",
            "condition": lambda: StreakSystem.calculate_streak() >= 30,
        },
        "point_collector": {
            "name": "💰 Collectionneur",
            "description": "1000 points gagnés",
            "icon": "💰",
            "condition": lambda: PointsSystem.get_total_points() >= 1000,
        },
        "chat_buddy": {
            "name": "💬 Ami de Mathi",
            "description": "20 conversations",
            "icon": "💬",
            "condition": lambda: BadgeSystem._count_chats() >= 20,
        },
    }

    @staticmethod
    def _count_moods() -> int:
        conn = st.session_state.conn
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM mood")
        count = cursor.fetchone()[0]
        return count

    @staticmethod
    def _count_completed_tasks() -> int:
        conn = st.session_state.conn
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
        count = cursor.fetchone()[0]
        return count

    @staticmethod
    def _count_chats() -> int:
        # TODO: a implementer quand j'aurai le temps
        return 0

    @staticmethod
    def get_unlocked_badges() -> list:
        unlocked = []
        for badge_id, badge in BadgeSystem.BADGES.items():
            if badge["condition"]():
                unlocked.append(
                    {"id": badge_id, "name": badge["name"], "icon": badge["icon"]}
                )
        return unlocked

    @staticmethod
    def display_badges():
        st.markdown("### 🏆 Tes Badges")

        cols = st.columns(3)
        for idx, (badge_id, badge) in enumerate(BadgeSystem.BADGES.items()):
            with cols[idx % 3]:
                is_unlocked = badge["condition"]()

                if is_unlocked:
                    st.markdown(
                        f"""
                    <div style='
                        background: linear-gradient(135deg, #7BA7D7, #5A8AC5);
                        color: white;
                        padding: 20px;
                        border-radius: 12px;
                        text-align: center;
                        margin-bottom: 10px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                    '>
                        <div style='font-size: 48px; margin-bottom: 8px;'>{badge['icon']}</div>
                        <div style='font-size: 16px; font-weight: 600; margin-bottom: 4px;'>{badge['name']}</div>
                        <div style='font-size: 13px; opacity: 0.9; line-height: 1.4;'>{badge['description']}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                    <div style='
                        background: #F0F4F8;
                        color: #A0AEC0;
                        padding: 20px;
                        border-radius: 12px;
                        text-align: center;
                        margin-bottom: 10px;
                        opacity: 0.5;
                    '>
                        <div style='font-size: 48px; margin-bottom: 8px;'>🔒</div>
                        <div style='font-size: 16px; font-weight: 600; margin-bottom: 4px;'>{badge['name']}</div>
                        <div style='font-size: 13px; line-height: 1.4;'>{badge['description']}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )


# mode focus__________________________________________________________________________________________________
# le mode pomodoro de 25 minutes pour aider a se concentrer


class FocusMode:
    """mode focus avec timer pomodoro"""

    @staticmethod
    def is_enabled() -> bool:
        """verifie si le mode focus est activé"""
        return st.session_state.get("focus_mode", False)

    @staticmethod
    def start():
        """Démarre le mode Focus avec un timer de 25 minutes"""
        st.session_state.focus_mode = True
        st.session_state.focus_start_time = datetime.now()
        st.session_state.focus_duration = 25 * 60  # 25 min en secondes (25*60=1500)

    @staticmethod
    def stop():
        """Arrête le mode Focus"""
        st.session_state.focus_mode = False
        st.session_state.focus_start_time = None
        st.session_state.focus_duration = None

    @staticmethod
    def get_remaining_time() -> int:
        """Retourne le temps restant en secondes"""
        if not st.session_state.get("focus_start_time"):
            return 0

        # calcul du temps passé
        elapsed = (datetime.now() - st.session_state.focus_start_time).seconds
        remaining = st.session_state.get("focus_duration", 0) - elapsed
        return max(0, remaining)  # jamais negatif

    @staticmethod
    def is_finished() -> bool:
        """Vérifie si le timer est terminé"""
        return FocusMode.get_remaining_time() == 0

    @staticmethod
    def render_full_screen():
        """Affiche le mode Focus en plein écran"""
        import time

        remaining = FocusMode.get_remaining_time()

        if remaining > 0:
            # Timer en cours
            minutes = remaining // 60
            seconds = remaining % 60
            total_duration = st.session_state.get("focus_duration", 1500)
            progress = 1 - (remaining / total_duration)
            progress_percent = int(progress * 100)

            # Déterminer la couleur de la progress bar selon l'avancement
            if progress < 0.33:
                progress_color = "#7BA7D7"  # Bleu au début
            elif progress < 0.66:
                progress_color = "#FFD54F"  # Jaune au milieu
            else:
                progress_color = "#81C784"  # Vert à la fin

            # Style CSS pour centrer, bloquer le scroll et prendre tout l'écran
            st.markdown(
                f"""
                <style>
                /* Bloquer le scroll de la page */
                body, .main {{
                    overflow: hidden !important;
                }}

                .focus-container {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    width: 100%;
                    position: fixed;
                    top: 0;
                    left: 0;
                    background: #F7FAFC;
                    text-align: center;
                    padding: 40px;
                    z-index: 9999;
                }}
                .focus-timer {{
                    font-size: 120px;
                    font-weight: 700;
                    color: {progress_color};
                    margin: 30px 0;
                    line-height: 1.1;
                    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
                }}
                .focus-message {{
                    font-size: 28px;
                    font-weight: 600;
                    color: #2D3748;
                    margin: 20px 0;
                    max-width: 700px;
                }}
                .focus-encouragement {{
                    font-size: 20px;
                    color: #718096;
                    font-style: italic;
                    margin-top: 30px;
                }}
                .custom-progress {{
                    width: 80%;
                    max-width: 600px;
                    height: 40px;
                    background: #E8E8E8;
                    border-radius: 20px;
                    margin: 30px auto;
                    overflow: hidden;
                    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                .custom-progress-bar {{
                    height: 100%;
                    background: linear-gradient(90deg, {progress_color} 0%, {progress_color} 100%);
                    border-radius: 20px;
                    transition: width 0.3s ease;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: 600;
                    font-size: 18px;
                }}
                </style>
            """,
                unsafe_allow_html=True,
            )

            # Message d'encouragement selon le temps restant
            if minutes >= 20:
                message = "💪 Continue ! Tu commences fort !"
            elif minutes >= 15:
                message = "🌟 Excellent ! Tu es bien concentré(e) !"
            elif minutes >= 10:
                message = "🚀 Tu es à mi-chemin ! Continue comme ça !"
            elif minutes >= 5:
                message = "⚡ Plus que quelques minutes ! Tu assures !"
            else:
                message = "🔥 Dernière ligne droite ! Tu vas y arriver !"

            # Conseils TDAH-friendly
            tips = [
                "Respire profondément",
                "Tu fais du bon travail",
                "Chaque minute compte",
                "Reste concentré(e) sur ta tâche",
                "Tu es plus fort(e) que tu ne le penses",
                "Un pas à la fois",
                "Tu progresses bien",
                "Continue sur cette lancée",
            ]
            import random

            tip_index = (remaining // 5) % len(tips)
            tip = tips[tip_index]

            # Tout en HTML pur
            st.markdown(
                f"""
                <div class="focus-container">
                    <h1 style="font-size: 36px; margin-bottom: 20px;">🎯 Mode Focus Actif</h1>
                    <div class="focus-timer">{minutes:02d}:{seconds:02d}</div>
                    <div class="custom-progress">
                        <div class="custom-progress-bar" style="width: {progress_percent}%;">
                            {progress_percent}%
                        </div>
                    </div>
                    <div class="focus-message">{message}</div>
                    <div class="focus-encouragement">💡 {tip}</div>
                    <div style="margin-top: 30px; padding: 12px 20px; background: #E3F2FD; border-radius: 8px; color: #1976D2;">
                        ⏳ Le mode Focus se désactivera automatiquement à la fin du timer.
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

            # Auto-refresh toutes les 5 secondes
            time.sleep(5)
            st.rerun()

        else:
            # Timer terminé
            st.balloons()
            st.success("🎉 Félicitations ! Tu as terminé ta session de Focus !")
            st.markdown("### ✅ 25 minutes de concentration complétées")

            # Donner des points
            PointsSystem.award_points("task_completed")

            # Bouton pour quitter le mode Focus
            if st.button(
                "✨ Quitter le mode Focus", type="primary", use_container_width=True
            ):
                FocusMode.stop()
                st.rerun()

    @staticmethod
    def render_toggle():
        """Affiche le bouton pour activer le mode Focus"""
        is_focused = FocusMode.is_enabled()

        if not is_focused:
            if st.sidebar.button(
                "🎯 Mode Focus", use_container_width=True, type="primary"
            ):
                FocusMode.start()
                st.rerun()

    @staticmethod
    def hide_if_not_focus(content_key: str):
        if FocusMode.is_enabled() and content_key != "main_action":
            return True
        return False


# dashboard tdah__________________________________________________________________________
def render_tdah_dashboard():
    # Header avec informations clés
    col1, col2, col3 = st.columns(3)

    with col1:
        streak = StreakSystem.calculate_streak()
        st.metric(
            "🔥 Série",
            f"{streak} jour{'s' if streak > 1 else ''}",
            delta="+1" if streak > 0 else None,
        )

    with col2:
        points = PointsSystem.get_total_points()
        st.metric("⭐ Points", points)

    with col3:
        badges = len(BadgeSystem.get_unlocked_badges())
        total_badges = len(BadgeSystem.BADGES)
        st.metric("🏆 Badges", f"{badges}/{total_badges}")

    st.divider()

    # Badges en aperçu
    unlocked = BadgeSystem.get_unlocked_badges()
    if unlocked:
        st.markdown("### 🏆 Derniers badges débloqués")
        cols = st.columns(min(len(unlocked), 4))
        for idx, badge in enumerate(unlocked[-4:]):  # 4 derniers
            with cols[idx]:
                st.markdown(
                    f"<div style='text-align: center; font-size: 36px;'>{badge['icon']}</div>",
                    unsafe_allow_html=True,
                )
                st.caption(badge["name"])


# encouragement__________________________________________________________________________________________


def show_encouragement():
    import random

    messages = [
        "💪 Continue comme ça !",
        "🌟 Tu fais un super travail !",
        "🎯 Chaque petit pas compte !",
        "✨ Tu progresses chaque jour !",
        "🚀 Tu es sur la bonne voie !",
        "🌈 Fier de toi !",
        "💖 Prends soin de toi !",
        "🎉 Excellente progression !",
    ]

    st.success(random.choice(messages))


def check_achievements():
    """Vérifie et affiche les nouveaux badges débloqués"""
    unlocked = BadgeSystem.get_unlocked_badges()

    if "seen_badges" not in st.session_state:
        st.session_state.seen_badges = set()

    if "pending_badge_notifications" not in st.session_state:
        st.session_state.pending_badge_notifications = []

    # Détecter les nouveaux badges
    for badge in unlocked:
        if badge["id"] not in st.session_state.seen_badges:
            st.balloons()
            st.session_state.pending_badge_notifications.append(badge)
            st.session_state.seen_badges.add(badge["id"])

    # Afficher les notifications de badges avec bouton de fermeture
    for i, badge in enumerate(st.session_state.pending_badge_notifications[:]):
        col1, col2 = st.columns([0.95, 0.05])

        with col1:
            st.success(f"🎉 Nouveau badge débloqué: {badge['name']} {badge['icon']}")

        with col2:
            # Bouton X pour fermer (couleur du fond légèrement plus foncée)
            if st.button("✕", key=f"close_badge_{badge['id']}", help="Fermer"):
                st.session_state.pending_badge_notifications.remove(badge)
                st.rerun()


# initialisation______________________________________________________________________________
def init_tdah_features():
    PointsSystem.init_points_table()
    check_achievements()


# utilisation___________________________________________________________________________________
if __name__ == "__main__":
    st.set_page_config(page_title="Fonctionnalités TDAH", page_icon="🎯")

    init_tdah_features()

    st.title("Fonctionnalités TDAH")

    tab1, tab2, tab3 = st.tabs(["Dashboard", "Badges", "Focus"])

    with tab1:
        render_tdah_dashboard()
        StreakSystem.display_streak()

    with tab2:
        BadgeSystem.display_badges()

    with tab3:
        st.markdown("### 🎯 Mode Focus")
        FocusMode.render_toggle()

        if FocusMode.is_enabled():
            st.info("Mode Focus activé - Distractions minimisées")
        else:
            st.info("Mode Focus désactivé - Vue complète")


def check_scheduled_tasks():
    """Vérifie si une tâche programmée doit démarrer maintenant"""
    from datetime import datetime, date

    now = datetime.now()
    current_time = now.time()

    conn = st.session_state.conn
    cursor = conn.cursor()

    # Récupère les tâches d'aujourd'hui avec une heure programmée
    cursor.execute(
        """
        SELECT id, title, start_time 
        FROM tasks 
        WHERE start_time IS NOT NULL 
        AND done = 0 
        AND DATE(task_date) = ?
    """,
        (date.today().strftime("%Y-%m-%d"),),
    )

    for task_id, title, start_time in cursor.fetchall():
        if start_time:
            # Parser l'heure de la tâche
            task_hour, task_minute = map(int, start_time.split(":"))

            # Vérifier si c'est l'heure (±2 minutes de tolérance)
            time_diff = abs(
                (current_time.hour * 60 + current_time.minute)
                - (task_hour * 60 + task_minute)
            )

            if time_diff <= 2:  # Dans les 2 minutes
                return task_id, title

    return None, None
