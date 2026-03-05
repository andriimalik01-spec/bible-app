import datetime
from calendar import monthrange
from app.core.database import get_pool


async def get_month_leaderboard(limit: int = 10):
    pool = get_pool()
    today = datetime.date.today()

    first_day = today.replace(day=1)
    last_day = today.replace(day=monthrange(today.year, today.month)[1])

    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT u.name, COUNT(r.date) as days_count
            FROM users u
            LEFT JOIN reading_logs r
                ON u.id = r.user_id
                AND r.date BETWEEN $1 AND $2
            GROUP BY u.id
            ORDER BY days_count DESC
            LIMIT $3
        """, first_day, last_day, limit)

    return rows