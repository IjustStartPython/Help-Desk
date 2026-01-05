import streamlit as st
from datetime import datetime, date 

def get_today_tasks(task_date=None):
    """Récupère les tâches pour une date donnée"""
    if task_date is None:
        task_date = date.today()
    
    conn = st.session_state.conn
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, done, created_at FROM tasks WHERE DATE(created_at)=?",
        (task_date.strftime("%Y-%m-%d"),)
    )
    return cur.fetchall()


def add_task(title, task_date=None):
    """Ajoute une nouvelle tâche"""
    if task_date is None:
        task_date = date.today()
    
    conn = st.session_state.conn
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks(title, created_at) VALUES (?, ?)",
        (title, task_date.strftime("%Y-%m-%d"))
    )
    conn.commit()


def toggle_task(task_id, done):
    """Change l'état d'une tâche (fait/pas fait)"""
    conn = st.session_state.conn
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET done=? WHERE id=?",
        (1 if done else 0, task_id)
    )
    conn.commit()


def delete_task(task_id):
    """Supprime une tâche"""
    conn = st.session_state.conn
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()