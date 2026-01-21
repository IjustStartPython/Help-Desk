import streamlit as st
import pandas as pd
from datetime import date
from db.database import get_connection


@st.cache_data
def get_mood_history():
    """Récupère l'historique des humeurs"""
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT 
            id,
            mood_value,
            emotion,
            motivation,
            notes,
            created_at
        FROM mood
        ORDER BY created_at DESC
    """,
        conn,
    )

    conn.close()

    return df.to_dict("records") if not df.empty else []


def check_mood_logged_today():
    """Vérifie si l'humeur a déjà été enregistrée aujourd'hui"""
    conn = st.session_state.conn
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute(
        """
        SELECT COUNT(*)
        FROM mood
        WHERE DATE(created_at) = ?
    """,
        (today,),
    )
    count = cur.fetchone()[0]
    return count > 0


def save_mood(mood, emotion, motivation, notes):
    """Enregistre l'humeur du jour"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO mood (mood_value, emotion, motivation, notes)
        VALUES (?, ?, ?, ?)
    """,
        (mood, emotion, motivation, notes),
    )

    conn.commit()
    conn.close()


def add_note(content):
    """Ajoute une note rapide dans la table notes"""
    conn = st.session_state.conn
    conn.execute("INSERT INTO notes(content) VALUES (?)", (content,))
    conn.commit()
