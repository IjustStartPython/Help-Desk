import sqlite3
from pathlib import Path
import os

DB_PATH = Path("data/journal.db")

def get_connection():
    """Crée et retourne une connexion à la base de données"""
    # Crée le dossier data s'il n'existe pas_______________________________________________________
    DB_PATH.parent.mkdir(exist_ok=True, mode=0o700)

    # Créer la connexion
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    # Définir les permissions du fichier de base de données (lecture/écriture propriétaire uniquement)__
    if os.path.exists(DB_PATH):
        os.chmod(DB_PATH, 0o600)

    return conn