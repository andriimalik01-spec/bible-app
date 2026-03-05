from app.core.database import get_pool


async def create_user_if_not_exists(telegram_id: int, name: str):
    pool = get_pool()

    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT id FROM users WHERE telegram_id = $1",
            telegram_id
        )

        if user:
            return user["id"]

        new_user = await conn.fetchrow(
            """
            INSERT INTO users (telegram_id, name)
            VALUES ($1, $2)
            RETURNING id
            """,
            telegram_id,
            name
        )

        return new_user["id"]