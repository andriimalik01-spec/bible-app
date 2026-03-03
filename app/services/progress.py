from app.database.connection import get_pool


async def start_plan_for_user(telegram_id: int, plan_id: int):
    pool = await get_pool()

    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT id FROM users WHERE telegram_id = $1",
            telegram_id
        )

        if not user:
            return

        await conn.execute(
            """
            INSERT INTO user_reading_progress (user_id, plan_id, current_day)
            VALUES ($1, $2, 1)
            ON CONFLICT (user_id)
            DO UPDATE SET
                plan_id = EXCLUDED.plan_id,
                current_day = 1,
                updated_at = NOW()
            """,
            user["id"],
            plan_id
        )