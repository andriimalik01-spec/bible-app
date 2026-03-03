from app.database.connection import get_pool


async def mark_done(telegram_id: int):
    pool = get_pool()

    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE reading_progress
            SET total_days = total_days + 1,
                last_read_date = CURRENT_DATE
            WHERE user_id = (
                SELECT id FROM users WHERE telegram_id = $1
            )
        """, telegram_id)