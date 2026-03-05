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
    
async def get_user_rank(user_id: int):
    pool = get_pool()
    today = datetime.date.today()

    first_day = today.replace(day=1)
    last_day = today.replace(day=monthrange(today.year, today.month)[1])

    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT u.id, COUNT(r.date) as days_count
            FROM users u
            LEFT JOIN reading_logs r
                ON u.id = r.user_id
                AND r.date BETWEEN $1 AND $2
            GROUP BY u.id
            ORDER BY days_count DESC
        """, first_day, last_day)

    for index, row in enumerate(rows, start=1):
        if row["id"] == user_id:
            return index, row["days_count"]

    return None, 0
    
async def create_month_snapshot():
    pool = get_pool()
    today = datetime.date.today()

    year = today.year
    month = today.month

    first_day = today.replace(day=1)
    last_day = today.replace(day=monthrange(year, month)[1])

    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT u.id, COUNT(r.date) as days_count
            FROM users u
            LEFT JOIN reading_logs r
                ON u.id = r.user_id
                AND r.date BETWEEN $1 AND $2
            GROUP BY u.id
            ORDER BY days_count DESC
        """, first_day, last_day)

        for index, row in enumerate(rows, start=1):
            await conn.execute("""
                INSERT INTO monthly_results (user_id, year, month, rank, days_count)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (user_id, year, month) DO NOTHING
            """, row["id"], year, month, index, row["days_count"])