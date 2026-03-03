from app.database.connection import get_pool


async def seed_reading_plans():
    pool = await get_pool()

    async with pool.acquire() as conn:

        # Перевіряємо, чи вже існує план
        existing = await conn.fetchrow(
            "SELECT id FROM reading_plans WHERE name = $1",
            "30 днів з Притчами"
        )

        if existing:
            return  # вже є

        # Створюємо план
        plan_id = await conn.fetchval("""
            INSERT INTO reading_plans (name, description, duration_days)
            VALUES ($1, $2, $3)
            RETURNING id
        """,
            "30 днів з Притчами",
            "Щоденні мудрі думки з книги Притч",
            30
        )

        # Додаємо перші 3 дні (для тесту)
        days = [
            "📖 Притчі 1:1-7 — Початок мудрості.",
            "📖 Притчі 2 — Пошук мудрості.",
            "📖 Притчі 3:5-6 — Довірся Господу всім серцем."
        ]

        for i, content in enumerate(days, start=1):
            await conn.execute("""
                INSERT INTO reading_plan_days (plan_id, day_number, content)
                VALUES ($1, $2, $3)
            """, plan_id, i, content)