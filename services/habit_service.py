# Service pour gérer les habitudes et tâches
# c'est ici qu'on gere les taches de l'utilisateur
import streamlit as st
from datetime import datetime, date

def get_today_tasks(task_date=None, show_completed=True):
    """Récupère les tâches pour une date donnée (ou aujourd'hui par defaut)"""
    if task_date is None:
        task_date = date.today()

    conn = st.session_state.conn
    cur = conn.cursor()

    # la requete sql pour avoir les taches
    query = "SELECT id, title, done, time_spent, task_date, start_time FROM tasks WHERE DATE(task_date)=?"
    params = [task_date.strftime("%Y-%m-%d")]

    # si on veut pas les taches terminées
    if not show_completed:
        query += " AND done = 0"

    cur.execute(query, params)
    return cur.fetchall()


def add_task(title, task_date=None, start_time=None):
    """Ajoute une nouvelle tâche dans la bdd"""
    if task_date is None:
        task_date = date.today()  # par defaut c'est aujourd'hui

    conn = st.session_state.conn
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks(title, created_at, task_date, start_time) VALUES (?, ?, ?, ?)",
        (title, datetime.now().isoformat(), task_date.strftime("%Y-%m-%d"), start_time)
    )
    conn.commit()
    # print(f"tache ajoutée: {title}")  # debug


def toggle_task(task_id, done):
    """Change l'état d'une tâche (fait/pas fait)"""
    conn = st.session_state.conn
    cur = conn.cursor()

    if done:
        # Tâche terminée, on met la date de completion
        cur.execute(
            "UPDATE tasks SET done=?, completed_at=? WHERE id=?",
            (1, datetime.now().isoformat(), task_id)
        )
    else:
        # Tâche pas terminée, on enlève la date
        cur.execute(
            "UPDATE tasks SET done=?, completed_at=NULL WHERE id=?",
            (0, task_id)
        )
    conn.commit()


def update_task_time(task_id, time_spent):
    """Met à jour le temps passé sur une tâche (en heures)"""
    conn = st.session_state.conn
    cur = conn.cursor()

    cur.execute(
        "UPDATE tasks SET time_spent=? WHERE id=?",
        (time_spent, task_id)
    )
    conn.commit()


def delete_task(task_id):
    """Supprime une tâche (attention c'est definitif!)"""
    conn = st.session_state.conn
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()