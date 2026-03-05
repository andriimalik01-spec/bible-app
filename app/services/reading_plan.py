from app.core.database import get_pool
from app.data.bible_structure import NEW_TESTAMENT, OLD_TESTAMENT


def flatten_structure(structure):
    result = []
    for book, chapters in structure:
        for ch in range(1, chapters + 1):
            result.append((book, ch))
    return result


NT_LIST = flatten_structure(NEW_TESTAMENT)
OT_LIST = flatten_structure(OLD_TESTAMENT)


async def create_or_update_plan(user_id: int, nt: int, ot: int):
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO reading_plans (user_id, nt_per_day, ot_per_day)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id)
        DO UPDATE SET nt_per_day = $2, ot_per_day = $3
        """, user_id, nt, ot)


async def get_today_reading(user_id: int):
    pool = get_pool()

    async with pool.acquire() as conn:
        plan = await conn.fetchrow("""
            SELECT * FROM reading_plans WHERE user_id = $1
        """, user_id)

        if not plan:
            return None

        nt_index = plan["nt_index"]
        ot_index = plan["ot_index"]

        nt_per_day = plan["nt_per_day"]
        ot_per_day = plan["ot_per_day"]

        nt_today = NT_LIST[nt_index: nt_index + nt_per_day]
        ot_today = OT_LIST[ot_index: ot_index + ot_per_day]

        await conn.execute("""
            UPDATE reading_plans
            SET nt_index = nt_index + $1,
                ot_index = ot_index + $2
            WHERE user_id = $3
        """, nt_per_day, ot_per_day, user_id)

        return nt_today + ot_today
async def get_user_plan(user_id: int):
    pool = get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            "SELECT * FROM reading_plans WHERE user_id = $1",
            user_id
        )