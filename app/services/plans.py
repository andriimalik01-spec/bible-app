from app.database.connection import get_pool


async def get_all_plans():
    pool = await get_pool()

    async with pool.acquire() as conn:
        plans = await conn.fetch(
            """
            SELECT id, name, duration_days
            FROM reading_plans
            ORDER BY id
            """
        )

    return plans