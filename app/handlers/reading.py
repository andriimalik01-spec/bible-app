from aiogram import Router
from aiogram import F
from aiogram.types import Message, CallbackQuery
from app.services.users import create_user_if_not_exists
from app.services.reading_plan import peek_today_reading, advance_reading, save_daily_reading,get_backlog
from app.services.streak import mark_as_read
from app.keyboards.reading_menu import get_reading_menu
from app.texts.loader import get_texts
from app.core.database import get_pool
  

router = Router()


@router.message(F.text == "📖 Reading")
async def reading_menu(message: Message):
    db_user_id = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    # 🔹 Отримуємо мову користувача
    pool = get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow("""
            SELECT language FROM users WHERE id = $1
        """, db_user_id)

    user_language = user["language"]
    texts = get_texts(user_language)  # ← ОСЬ ТУТ

    backlog = await get_backlog(db_user_id)
    backlog_count = len(backlog)

    await message.answer(
        texts.reading_menu_title,
        reply_markup=get_reading_menu(backlog_count)
    )


@router.callback_query(lambda c: c.data == "reading_today")
async def show_today(callback: CallbackQuery):
    db_user_id = await create_user_if_not_exists(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    today = datetime.date.today()
    pool = get_pool()

    async with pool.acquire() as conn:
        existing = await conn.fetchrow("""
            SELECT content FROM daily_readings
            WHERE user_id = $1 AND date = $2
        """, db_user_id, today)

    if existing:
        text = f"📖 Today:\n\n{existing['content']}"
        await callback.message.answer(text)
        await callback.answer()
        return

    # якщо ще не було згенеровано
    reading = await peek_today_reading(db_user_id)

    await save_daily_reading(db_user_id, reading)

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
    
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

@router.callback_query(lambda c: c.data == "reading_backlog")
async def show_backlog(callback: CallbackQuery):
    db_user_id = await create_user_if_not_exists(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    backlog = await get_backlog(db_user_id)

    if not backlog:
        await callback.message.answer("Немає пропущених днів 🙌")
        await callback.answer()
        return

    for row in backlog:
        date_str = row["date"].isoformat()
        text = f"📅 {row['date']} — {row['content']}"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Закрити",
                    callback_data=f"close_backlog_{date_str}"
                )
            ]
        ])

        await callback.message.answer(text, reply_markup=keyboard)

    await callback.answer()
    
@router.callback_query(lambda c: c.data.startswith("close_backlog_"))
async def close_backlog(callback: CallbackQuery):
    db_user_id = await create_user_if_not_exists(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    date_str = callback.data.replace("close_backlog_", "")
    date_obj = datetime.date.fromisoformat(date_str)

    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE daily_readings
            SET completed = TRUE
            WHERE user_id = $1 AND date = $2
        """, db_user_id, date_obj)

    await callback.message.edit_text("✅ День закрито")
    await callback.answer()
    
async def needs_evening_reminder(user_id: int):
    pool = get_pool()
    today = datetime.date.today()

    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT completed
            FROM daily_readings
            WHERE user_id = $1 AND date = $2
        """, user_id, today)

    if not row:
        return False  # ще навіть не відкривав читання

    return row["completed"] is False