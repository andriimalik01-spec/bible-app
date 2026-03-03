from app.database.connection import get_pool


async def create_user_if_not_exists(telegram_id: int, username: str | None, first_name: str | None):
    pool = await get_pool()

    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT id FROM users WHERE telegram_id = $1",
            telegram_id
        )

        if not user:
            await conn.execute(
                """
                INSERT INTO users (telegram_id, username, first_name)
                VALUES ($1, $2, $3)
                """,
                telegram_id,
                username,
                first_name
            )