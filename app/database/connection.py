import os
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")

_pool = None


async def init_db():
    global _pool

    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL)


async def get_pool():
    return _pool