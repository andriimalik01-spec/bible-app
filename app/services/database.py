import sqlite3
from pathlib import Path

DB_PATH = Path("data/database.sqlite3")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            lang TEXT DEFAULT 'ua',
            plan INTEGER DEFAULT 3,
            chapter_index INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            max_streak INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            user_id INTEGER,
            date TEXT,
            status TEXT,
            PRIMARY KEY (user_id, date)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            note TEXT
        )
    """)

    conn.commit()
    conn.close()