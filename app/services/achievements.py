from app.core.database import get_pool


async def add_achievement(user_id: int, achievement_type: str):
    pool = get_pool()

    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO achievements (user_id, type)
            VALUES ($1, $2)
            ON CONFLICT (user_id, type) DO NOTHING
        """, user_id, achievement_type)


async def check_achievements(user_id: int):
    pool = get_pool()

    async with pool.acquire() as conn:
        user = await conn.fetchrow("""
            SELECT current_streak, total_days
            FROM users
            WHERE id = $1
        """, user_id)

    achievements = []

    # Streak achievements
    if user["current_streak"] >= 7:
        achievements.append("streak_7")

    if user["current_streak"] >= 30:
        achievements.append("streak_30")

    if user["current_streak"] >= 100:
        achievements.append("streak_100")

    # Total reading achievements
    if user["total_days"] >= 10:
        achievements.append("total_10")

    if user["total_days"] >= 50:
        achievements.append("total_50")

    for ach in achievements:
        await add_achievement(user_id, ach)

    return achievements