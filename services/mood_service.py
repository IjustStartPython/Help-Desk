import streamlit as st
from datetime import date

@st.cache_data
def get_mood_history():
    conn = st.session_state.conn
    cur = conn.cursor()
    cur.execute("""
        SELECT created_at, mood_value
        FROM mood
        ORDER BY created_at
    """)
    return cur.fetchall()

def check_mood_logged_today():
    """Vérifie si l'humeur a déjà été enregistrée aujourd'hui"""
    conn = st.session_state.conn
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute("""
        SELECT COUNT(*)
        FROM mood
        WHERE DATE(created_at) = ?
    """, (today,))
    count = cur.fetchone()[0]
    return count > 0

def save_mood(mood, emotion, motivation, notes):
    conn = st.session_state.conn
    conn.execute("""
        INSERT INTO mood (mood_value, emotion, motivation, notes)
        VALUES (?, ?, ?, ?)
    """, (mood, emotion, motivation, notes))
    conn.commit()
    get_mood_history.clear()

def add_note(content):
    """Ajoute une note rapide dans la table notes"""
    conn = st.session_state.conn
    conn.execute(
        "INSERT INTO notes(content) VALUES (?)",
        (content,)
    )
    conn.commit()