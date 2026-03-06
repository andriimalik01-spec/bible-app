from aiogram import Router
from aiogram.types import Message, CallbackQuery
from app.services.users import create_user_if_not_exists
from app.services.reading_plan import peek_today_reading, advance_reading, save_daily_reading
from app.services.streak import mark_as_read
from app.keyboards.reading_menu import get_reading_menu

router = Router()


@router.message(F.text == "📖 Reading")
async def reading_menu(message: Message):
    db_user_id = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    backlog = await get_backlog(db_user_id)
    backlog_count = len(backlog)

    await message.answer(
        "📖 Reading Menu:",
        reply_markup=get_reading_menu(backlog_count)
    )


@router.callback_query(lambda c: c.data == "reading_today")
async def show_today(callback: CallbackQuery):
    db_user_id = await create_user_if_not_exists(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    reading = await peek_today_reading(db_user_id)

    if not reading:
        await callback.message.answer("No plan found.")
        return

    text = "📖 Today:\n\n"

    for book, ch in reading:
        if isinstance(ch, list):
            if len(ch) == 1:
                text += f"{book} {ch[0]}\n"
            else:
                text += f"{book} {ch[0]}–{ch[-1]}\n"
        else:
            text += f"{book} {ch}\n"

    await callback.message.answer(text)
    await callback.answer()


import datetime
from app.core.database import get_pool

@router.callback_query(lambda c: c.data == "reading_done")
async def mark_done(callback: CallbackQuery):
    db_user_id = await create_user_if_not_exists(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    pool = get_pool()
    today = datetime.date.today()

    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE daily_readings
            SET completed = TRUE
            WHERE user_id = $1 AND date = $2
        """, db_user_id, today)

    streak = await mark_as_read(db_user_id)
    await advance_reading(db_user_id)

    await callback.message.answer(
        f"🔥 Streak: {streak} days",
        reply_markup=get_reading_menu(0)
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "reading_note")
async def write_note(callback: CallbackQuery):
    await callback.message.answer("Use /note to write your journal entry.")
    await callback.answer()
    
@router.callback_query(lambda c: c.data == "reading_backlog")
async def show_backlog(callback: CallbackQuery):
    db_user_id = await create_user_if_not_exists(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    backlog = await get_backlog(db_user_id)

    if not backlog:
        await callback.message.answer("Немає пропущених днів 🙌")
        return

    text = "📚 Пропущені дні:\n\n"

    for row in backlog:
        text += f"📅 {row['date']} — {row['content']}\n"

    await callback.message.answer(text)
    await callback.answer()