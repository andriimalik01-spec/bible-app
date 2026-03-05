import datetime
from app.core.database import get_pool


async def mark_as_read(user_id: int):
    pool = get_pool()
    today = datetime.date.today()

    async with pool.acquire() as conn:

        user = await conn.fetchrow("""
            SELECT current_streak, max_streak, last_read_date, total_days
            FROM users
            WHERE id = $1
        """, user_id)

        if user["last_read_date"] == today:
            return user["current_streak"]

        # додаємо запис у logs
        await conn.execute("""
            INSERT INTO reading_logs (user_id, date)
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING
        """, user_id, today)

        yesterday = today - datetime.timedelta(days=1)

        if user["last_read_date"] == yesterday:
            new_streak = user["current_streak"] + 1
        else:
            new_streak = 1

        new_max = max(new_streak, user["max_streak"])
        new_total = user["total_days"] + 1

        await conn.execute("""
            UPDATE users
            SET current_streak = $1,
                max_streak = $2,
                total_days = $3,
                last_read_date = $4
            WHERE id = $5
        """, new_streak, new_max, new_total, today, user_id)

        return new_streak


async def get_streak(user_id: int):
    pool = get_pool()

    async with pool.acquire() as conn:
        user = await conn.fetchrow("""
            SELECT current_streak FROM users WHERE id = $1
        """, user_id)

    return user["current_streak"] if user else 0