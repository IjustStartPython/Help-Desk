# Gestion de la connexion à la base de données SQLite
# j'utilise sqlite parce que c'est simple et ca fait pas de serveur a installer
import sqlite3
from pathlib import Path
import os
import streamlit as st

# Chemin de la base de données (dans le dossier data)
DB_PATH = Path("data/journal.db")

def get_connection():
    """Crée et retourne une connexion à la base"""
    # Créer le dossier data si il existe pas encore
    DB_PATH.parent.mkdir(exist_ok=True, mode=0o700)

    # ouvrir la connexion
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)  # check_same_thread=False car streamlit utilise plusieurs threads

    # Mettre les permissions du fichier (pour la sécurité)
    if os.path.exists(DB_PATH):
        os.chmod(DB_PATH, 0o600)

    return conn


def close_connection():
    """Ferme la connexion quand on quitte"""
    try:
        if hasattr(st, 'session_state') and "conn" in st.session_state and st.session_state.conn:
            st.session_state.conn.close()
            # print("connection fermée")
    except Exception:
        pass  # on ignore les erreurs ici c'est pas grave


def migrate_database():
    """Ajoute les colonnes manquantes dans la base
    j'ai du faire cette fonction car j'ai ajouté des colonnes apres coup
    et je voulais pas perdre les données existantes"""
    conn = get_connection()
    cursor = conn.cursor()

    # Ajouter 'done' si elle existe pas
    try:
        cursor.execute("SELECT done FROM tasks LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE tasks ADD COLUMN done INTEGER DEFAULT 0")
        conn.commit()
        # print("colonne done ajoutée")

    # Ajouter 'time_spent' si elle existe pas
    try:
        cursor.execute("SELECT time_spent FROM tasks LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE tasks ADD COLUMN time_spent REAL DEFAULT 0.0")
        conn.commit()

    # Ajouter 'completed_at' si elle existe pas
    try:
        cursor.execute("SELECT completed_at FROM tasks LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE tasks ADD COLUMN completed_at DATETIME")
        conn.commit()

    # Ajouter 'task_date' si elle existe pas (pour pouvoir choisir la date de la tache)
    try:
        cursor.execute("SELECT task_date FROM tasks LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE tasks ADD COLUMN task_date DATE")
        # on met la date de creation pour les anciennes taches
        cursor.execute("UPDATE tasks SET task_date = DATE(created_at) WHERE task_date IS NULL")
        conn.commit()

    #ajoute une colonne 'strat_time' pour l'heure de debut
    try:
        cursor.execute("SELECT start_time FROM tasks LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE tasks ADD COLUMN start_time TEXT")
        conn.commit()

    conn.close()