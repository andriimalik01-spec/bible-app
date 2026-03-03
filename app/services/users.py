from app.database.connection import get_pool


async def create_user_if_not_exists(telegram_id, username=None, first_name=None):
    pool = await get_pool()

    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (telegram_id, username, first_name)
            VALUES ($1, $2, $3)
            ON CONFLICT (telegram_id) DO NOTHING
        """, telegram_id, username, first_name)


async def get_user_by_telegram_id(telegram_id):
    pool = await get_pool()

    async with pool.acquire() as conn:
        return await conn.fetchrow("""
            SELECT * FROM users
            WHERE telegram_id = $1
        """, telegram_id)