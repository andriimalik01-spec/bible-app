import asyncpg
from app.config import DATABASE_URL

pool: asyncpg.Pool | None = None


async def create_pool():
    global pool
    pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=1,
        max_size=5
    )


async def close_pool():
    global pool
    if pool:
        await pool.close()


def get_pool():
    return pool


async def init_db():
    async with pool.acquire() as conn:

        # =========================
        # USERS TABLE
        # =========================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            name TEXT,
            language TEXT DEFAULT 'ua',
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        # Safe migrations for users
        await conn.execute("""
        ALTER TABLE users ADD COLUMN IF NOT EXISTS current_streak INTEGER DEFAULT 0;
        """)

        await conn.execute("""
        ALTER TABLE users ADD COLUMN IF NOT EXISTS max_streak INTEGER DEFAULT 0;
        """)

        await conn.execute("""
        ALTER TABLE users ADD COLUMN IF NOT EXISTS total_days INTEGER DEFAULT 0;
        """)

        await conn.execute("""
        ALTER TABLE users ADD COLUMN IF NOT EXISTS last_read_date DATE;
        """)

        # =========================
        # READING PLANS
        # =========================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS reading_plans (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
            nt_per_day INTEGER NOT NULL,
            ot_per_day INTEGER NOT NULL,
            nt_index INTEGER DEFAULT 0,
            ot_index INTEGER DEFAULT 0
        );
        """)

        # =========================
        # READING LOGS
        # =========================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS reading_logs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            date DATE NOT NULL,
            UNIQUE(user_id, date)
        );
        """)
        
        # =========================
        # MONTHLY RESULTS
        # =========================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS monthly_results (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            rank INTEGER NOT NULL,
            days_count INTEGER NOT NULL,
            UNIQUE(user_id, year, month)
        );
        """)
        
        # =========================
        # JOURNAL
        # =========================
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            book TEXT,
            chapter TEXT,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)
        
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            type TEXT NOT NULL,
            achieved_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(user_id, type)
        );
        """)
        
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_content (
            id SERIAL PRIMARY KEY,
            type TEXT,
            text TEXT,
            author TEXT,
            language TEXT DEFAULT 'ua'
        );
        """)