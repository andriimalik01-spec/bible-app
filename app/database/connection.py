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
            id BIGINT PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            language TEXT DEFAULT 'ua',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS reading_logs (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
            reading_date DATE NOT NULL,
            chapters_read INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)


async def get_pool():
    return pool