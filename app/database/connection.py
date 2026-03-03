import os
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")

pool = None


async def init_db():
    global pool

    pool = await asyncpg.create_pool(DATABASE_URL)

    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                language TEXT DEFAULT 'ua',
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS reading_progress (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                total_days INTEGER DEFAULT 0,
                last_read_date DATE,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)