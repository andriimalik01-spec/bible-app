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


async def init_db():
    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            name TEXT,
            language TEXT DEFAULT 'ua',
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

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
        
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS reading_logs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            date DATE NOT NULL,
            UNIQUE(user_id, date)
        );
        """)
        
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            name TEXT,
            language TEXT DEFAULT 'ua',
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        # додаємо відсутні колонки, якщо їх нема
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
def get_pool():
    return pool