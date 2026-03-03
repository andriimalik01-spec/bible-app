from app.database.connection import get_pool


async def create_user_if_not_exists(user):
    pool = await get_pool()

    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT id FROM users WHERE telegram_id = $1",
            user.id
        )

        if not existing:
            await conn.execute(
                """
                INSERT INTO users (telegram_id, username, first_name)
                VALUES ($1, $2, $3)
                """,
                user.id,
                user.username,
                user.first_name
            )