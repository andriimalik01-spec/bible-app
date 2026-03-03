from app.database.connection import get_pool


async def get_all_plans():
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM reading_plans ORDER BY id")


async def select_plan_for_user(user_id: int, plan_id: int):
    pool = await get_pool()

    async with pool.acquire() as conn:

        # перевіряємо чи користувач вже має запис
        existing = await conn.fetchrow("""
            SELECT id FROM user_reading_progress
            WHERE user_id = $1
        """, user_id)

        if existing:
            await conn.execute("""
                UPDATE user_reading_progress
                SET plan_id = $1,
                    current_day = 1,
                    updated_at = NOW()
                WHERE user_id = $2
            """, plan_id, user_id)
        else:
            await conn.execute("""
                INSERT INTO user_reading_progress (user_id, plan_id, current_day)
                VALUES ($1, $2, 1)
            """, user_id, plan_id)


async def get_today_reading(user_id: int):
    pool = await get_pool()

    async with pool.acquire() as conn:

        progress = await conn.fetchrow("""
            SELECT plan_id, current_day
            FROM user_reading_progress
            WHERE user_id = $1
        """, user_id)

        if not progress:
            return None

        content = await conn.fetchrow("""
            SELECT content
            FROM reading_plan_days
            WHERE plan_id = $1 AND day_number = $2
        """, progress["plan_id"], progress["current_day"])

        return content["content"] if content else None