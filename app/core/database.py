import os
import asyncpg
from typing import Optional

DATABASE_URL = os.getenv("DATABASE_URL")

_pool: Optional[asyncpg.Pool] = None


async def init_db():
    global _pool

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL not set")

    _pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=1,
        max_size=5,
    )

    async with _pool.acquire() as conn:

        # ================= USERS =================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            language TEXT DEFAULT 'ua',
            chapters_per_day INTEGER DEFAULT 1,
            start_testament TEXT DEFAULT 'old',
            current_book TEXT,
            current_chapter INTEGER DEFAULT 1,
            streak INTEGER DEFAULT 0,
            last_read_date DATE,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        # ================= READING LOGS =================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS reading_logs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            read_date DATE NOT NULL,
            chapters_completed INTEGER DEFAULT 0
        );
        """)

        # ================= MONTHLY STATS =================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS monthly_stats (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            chapters_read INTEGER DEFAULT 0,
            UNIQUE(user_id, month, year)
        );
        """)

        # ================= DIARY =================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS diary_entries (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            entry_date DATE NOT NULL,
            content TEXT NOT NULL
        );
        """)

        # ================= PLANS =================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS reading_plans (
            id SERIAL PRIMARY KEY,
            chapters_per_day INTEGER UNIQUE NOT NULL
        );
        """)

        # ================= DAILY QUOTES =================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_quotes (
            id SERIAL PRIMARY KEY,
            quote_date DATE UNIQUE NOT NULL,
            text_ua TEXT NOT NULL,
            text_ru TEXT NOT NULL
        );
        """)

        # Insert default plans safely
        await conn.execute("""
        INSERT INTO reading_plans (chapters_per_day)
        VALUES (1), (2), (3), (4)
        ON CONFLICT (chapters_per_day) DO NOTHING;
        """)


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Database not initialized")
    return _pool