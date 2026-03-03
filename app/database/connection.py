import os
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")

pool = None


async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)


async def get_pool():
    return pool