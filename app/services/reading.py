from app.database.connection import get_pool


async def get_today_reading(telegram_id: int):
    pool = await get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT rp.current_day, rpd.content
            FROM user_reading_progress rp
            JOIN reading_plan_days rpd
                ON rp.plan_id = rpd.plan_id
                AND rp.current_day = rpd.day_number
            JOIN users u
                ON u.id = rp.user_id
            WHERE u.telegram_id = $1
        """, telegram_id)

        return row