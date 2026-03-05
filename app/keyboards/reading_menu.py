async def advance_reading(user_id: int):
    pool = get_pool()

    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE reading_plans
            SET nt_index = nt_index + nt_per_day,
                ot_index = ot_index + ot_per_day
            WHERE user_id = $1
        """, user_id)