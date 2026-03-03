import os
import asyncpg


DATABASE_URL = os.getenv("DATABASE_URL")

pool = None


async def init_db():
    global pool

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")

    pool = await asyncpg.create_pool(DATABASE_URL)

    async with pool.acquire() as conn:

        # ---------------- USERS ----------------
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                language TEXT DEFAULT 'ua'
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

        # ---------------- READING PLANS ----------------
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS reading_plans (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                duration_days INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

        # ---------------- READING PLAN DAYS ----------------
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS reading_plan_days (
                id SERIAL PRIMARY KEY,
                plan_id INTEGER REFERENCES reading_plans(id) ON DELETE CASCADE,
                day_number INTEGER NOT NULL,
                content TEXT NOT NULL
            );
        """)

        # ---------------- USER PROGRESS ----------------
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS reading_progress (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                plan_id INTEGER REFERENCES reading_plans(id) ON DELETE CASCADE,
                current_day INTEGER DEFAULT 1,
                started_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(user_id)
            );
        """)


async def get_pool():
    return pool