from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.services.users import create_user_if_not_exists
from app.core.database import get_pool

router = Router()


@router.message(Command("achievements"))
async def achievements_handler(message: Message):
    db_user_id = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    pool = get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT type, achieved_at
            FROM achievements
            WHERE user_id = $1
            ORDER BY achieved_at DESC
        """, db_user_id)

    if not rows:
        await message.answer("No achievements yet.")
        return

    text = "🏅 Your Achievements:\n\n"

    for row in rows:
        text += f"• {row['type']} — {row['achieved_at'].date()}\n"

    await message.answer(text)