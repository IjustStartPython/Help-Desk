from db.database import get_connection

def init_db():
    """Initialise toutes les tables si elles n'existent pas déjà."""
    conn = get_connection()
    cursor = conn.cursor()

    create_user_table(cursor)
    create_mood_table(cursor)
    create_tasks_table(cursor)
    create_notes_table(cursor)

    conn.commit()
    conn.close()


def create_user_table(cursor):
    """Crée la table users"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prenom TEXT,
            birth_date TEXT,
            tags TEXT,
            tdah INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)


def create_mood_table(cursor):
    """Crée la table mood"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood_value INTEGER NOT NULL,
            emotion TEXT,
            motivation TEXT,
            tags TEXT,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)


def create_tasks_table(cursor):
    """Crée la table tasks"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0,
            created_at DATE DEFAULT CURRENT_DATE
        )
    """)


def create_notes_table(cursor):
    """Crée la table notes"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)


def save_profile_to_db(prenom, birth_date, tags):
    """Sauvegarde le profil utilisateur"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (prenom, birth_date, tags)
        VALUES (?, ?, ?)
    """, (prenom, birth_date, ",".join(tags)))
    conn.commit()
    conn.close()


def load_profile_from_db():
    """Charge le dernier profil créé"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT prenom, birth_date, tags FROM users ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        prenom, birth_date, tags = row
        return {
            "prenom": prenom,
            "birth_date": birth_date,
            "tags": [t.strip() for t in tags.split(",") if t.strip()]
        }
    return None