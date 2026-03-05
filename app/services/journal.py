from app.core.database import get_pool


import datetime


async def add_journal_entry(user_id: int, text: str):
    pool = get_pool()
    today = datetime.date.today()

    async with pool.acquire() as conn:
        reading = await conn.fetchrow("""
            SELECT content FROM daily_readings
            WHERE user_id = $1 AND date = $2
        """, user_id, today)

        reading_text = reading["content"] if reading else "No reading recorded"

        await conn.execute("""
            INSERT INTO journal_entries (user_id, book, chapter, text)
            VALUES ($1, $2, $3, $4)
        """, user_id, today.isoformat(), reading_text, text)


async def get_user_entries(user_id: int, limit: int = 10):
    pool = get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch("""
            SELECT book, chapter, text, created_at
            FROM journal_entries
            WHERE user_id = $1
            ORDER BY created_at DESC
            LIMIT $2
        """, user_id, limit)