import random
from app.core.database import get_pool


async def get_random_content(language: str = "ua"):
    pool = get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT text, author
            FROM daily_content
            WHERE language = $1
        """, language)

    if not rows:
        return None

    return random.choice(rows)


async def get_all_users():
    pool = get_pool()

    async with pool.acquire() as conn:
        return await conn.fetch("""
            SELECT telegram_id, language
            FROM users
        """)