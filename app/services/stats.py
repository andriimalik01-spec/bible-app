from datetime import date
from app.database.connection import get_pool


# ✅ Позначити день як прочитаний
async def mark_done(user_id: int):
    pool = await get_pool()

    async with pool.acquire() as conn:
        # перевіряємо чи вже є запис за сьогодні
        existing = await conn.fetchrow(
            """
            SELECT id FROM reading_logs
            WHERE user_id = $1 AND reading_date = $2
            """,
            user_id,
            date.today()
        )

        if existing:
            return False  # вже відмічено

        await conn.execute(
            """
            INSERT INTO reading_logs (user_id, reading_date)
            VALUES ($1, $2)
            """,
            user_id,
            date.today()
        )

        return True


# ✅ Загальна статистика користувача
async def get_user_stats(user_id: int):
    pool = await get_pool()

    async with pool.acquire() as conn:
        total_done = await conn.fetchval(
            """
            SELECT COUNT(*) FROM reading_logs
            WHERE user_id = $1
            """,
            user_id
        )

        return {
            "total_done": total_done or 0
        }


# ✅ Топ користувачів (по всіх днях)
async def get_top_users(limit: int = 10):
    pool = await get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT u.full_name, COUNT(r.id) AS total
            FROM users u
            LEFT JOIN reading_logs r ON u.id = r.user_id
            GROUP BY u.id
            ORDER BY total DESC
            LIMIT $1
            """,
            limit
        )

        return rows


# ✅ Статистика за місяць
async def get_monthly_stats(user_id: int, year: int, month: int):
    pool = await get_pool()

    async with pool.acquire() as conn:
        total = await conn.fetchval(
            """
            SELECT COUNT(*) FROM reading_logs
            WHERE user_id = $1
            AND EXTRACT(YEAR FROM reading_date) = $2
            AND EXTRACT(MONTH FROM reading_date) = $3
            """,
            user_id,
            year,
            month
        )

        return total or 0