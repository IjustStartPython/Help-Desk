import streamlit as st
from services.tdah_features import (
    PointsSystem,
    StreakSystem,
    BadgeSystem,
)

def render_dashboard():
    """Dashboard TDAH-friendly avec stats et badges"""
    
    st.title("📊 Ton Tableau de Bord")

    # === 1. EN-TÊTE : 3 MÉTRIQUES EN CARTES BLEUES ===
    render_metrics_cards()

    st.divider()

    # === 2. DERNIERS BADGES DÉBLOQUÉS ===
    render_recent_badges()

    st.divider()

    # === 3. TOUS LES BADGES (grille 3 colonnes) ===
    render_all_badges()

def render_metrics_cards():
    col1, col2, col3 = st.columns(3)

    streak = StreakSystem.calculate_streak()
    points = PointsSystem.get_total_points()
    unlocked_badges = BadgeSystem.get_unlocked_badges()
    total_badges = len(BadgeSystem.BADGES)

    with col1:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #FFCC80, #FFB300);
            color: white;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        '>
            <div style='font-size: 36px; margin-bottom: 8px;'>🔥</div>
            <div style='font-size: 16px; font-weight: 500; margin-bottom: 4px;'>Série</div>
            <div style='font-size: 32px; font-weight: 700;'>{streak} jour{'s' if streak > 1 else ''}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #FFE082, #FFD54F);
            color: white;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        '>
            <div style='font-size: 36px; margin-bottom: 8px;'>⭐</div>
            <div style='font-size: 16px; font-weight: 500; margin-bottom: 4px;'>Points</div>
            <div style='font-size: 32px; font-weight: 700;'>{points}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #F6E27F, #D4AF37);
            color: white;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        '>
            <div style='font-size: 36px; margin-bottom: 8px;'>🏆</div>
            <div style='font-size: 16px; font-weight: 500; margin-bottom: 4px;'>Badges</div>
            <div style='font-size: 32px; font-weight: 700;'>{len(unlocked_badges)}/{total_badges}</div>
        </div>
        """, unsafe_allow_html=True)

def render_recent_badges():
    st.markdown("### 🏆 Derniers badges débloqués")

    unlocked = BadgeSystem.get_unlocked_badges()

    if not unlocked:
        st.info("Pas encore de badgesdébloqués. Continue à utiliser l'app !")

    recent_badges = unlocked[-6:] if len(unlocked) > 6 else unlocked
    recent_badges.reverse()

    cols = st.columns(min(len(recent_badges), 6))

    for idx, badge in enumerate(recent_badges):
        with cols[idx]:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #FFD699, #FFB74D);
                color: white;
                padding: 16px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                margin-bottom: 8px;
            '>
                <div style='font-size: 32px; margin-bottom: 4px;'>{badge['icon']}</div>
                <div style='font-size: 13px; font-weight: 600;'>{badge['name'].replace(badge['icon'], '').strip()}</div>
            </div>
            """, unsafe_allow_html=True)

def render_all_badges():
    st.markdown("### 🏆 Tes Badges")

    unlocked_ids = [b['id'] for b in BadgeSystem.get_unlocked_badges()]

    badges_list = list(BadgeSystem.BADGES.items())

    for i in range(0, len(badges_list), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j 
            if idx < len(badges_list):
                badge_id, badge = badges_list[idx]
                is_unlocked = badge_id in unlocked_ids

                with cols[j]:
                    if is_unlocked:
                        st.markdown(f"""
                            <div style='
                                background: linear-gradient(135deg, #F6E27F, #D4AF37);
                                color: white;
                                padding: 20px;
                                border-radius: 12px;
                                text-align: center;
                                margin-bottom: 12px;
                                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                                min-height: 180px;
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                            '>
                                <div style='font-size: 48px; margin-bottom: 12px;'>{badge['icon']}</div>
                                <div style='font-size: 16px; font-weight: 600; margin-bottom: 8px;'>{badge['name']}</div>
                                <div style='font-size: 13px; opacity: 0.9; line-height: 1.4;'>{badge['description']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        # Badge locked : fond gris clair
                        st.markdown(f"""
                            <div style='
                                background: #F0F4F8;
                                color: #A0AEC0;
                                padding: 20px;
                                border-radius: 12px;
                                text-align: center;
                                margin-bottom: 12px;
                                opacity: 0.6;
                                border: 2px dashed #E2E8F0;
                                min-height: 180px;
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                            '>
                                <div style='font-size: 48px; margin-bottom: 12px;'>🔒</div>
                                <div style='font-size: 16px; font-weight: 600; margin-bottom: 8px;'>{badge['name']}</div>
                                <div style='font-size: 13px; line-height: 1.4;'>{badge['description']}</div>
                            </div>
                            """, unsafe_allow_html=True)


    
    