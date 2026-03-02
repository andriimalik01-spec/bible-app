import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database.sqlite3"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            lang TEXT,
            plan INTEGER DEFAULT 3,
            start_book TEXT,
            current_index INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            max_streak INTEGER DEFAULT 0,
            mute_today TEXT
        )
    """)

    # READING LOG
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reading_logs (
            user_id INTEGER,
            date TEXT,
            status TEXT,
            PRIMARY KEY (user_id, date)
        )
    """)

    # USER NOTES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            text TEXT
        )
    """)

    conn.commit()
    conn.close()