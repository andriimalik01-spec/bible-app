from app.core.database import get_pool


async def add_journal_entry(user_id: int, book: str, chapter: str, text: str):
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO journal_entries (user_id, book, chapter, text)
            VALUES ($1, $2, $3, $4)
        """, user_id, book, chapter, text)


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