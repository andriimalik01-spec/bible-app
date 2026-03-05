import datetime
from app.core.database import get_pool


async def mark_as_read(user_id: int):
    pool = get_pool()
    today = datetime.date.today()

    async with pool.acquire() as conn:
        try:
            await conn.execute("""
                INSERT INTO reading_logs (user_id, date)
                VALUES ($1, $2)
            """, user_id, today)
        except:
            # якщо вже є запис — просто ігноруємо
            pass


async def get_streak(user_id: int):
    pool = get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT date FROM reading_logs
            WHERE user_id = $1
            ORDER BY date DESC
        """, user_id)

    if not rows:
        return 0

    dates = [r["date"] for r in rows]

    streak = 0
    today = datetime.date.today()

    for d in dates:
        if d == today - datetime.timedelta(days=streak):
            streak += 1
        else:
            break

    return streak