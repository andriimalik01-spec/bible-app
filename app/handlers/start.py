from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.services.streak import mark_as_read, get_streak
from app.keyboards.reading_keyboard import get_reading_keyboard
from app.core.database import get_pool
from app.services.streak import get_month_stats
from app.services.rating import get_month_leaderboard
from app.services.rating import get_user_rank

from app.services.users import create_user_if_not_exists
from app.services.reading_plan import (
    create_or_update_plan,
    get_today_reading,
    get_user_plan
)

from app.keyboards.plan_keyboard import get_plan_keyboard
from app.keyboards.custom_plan_keyboard import get_number_keyboard
from app.states.plan_states import CustomPlan

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    db_user_id = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    plan = await get_user_plan(db_user_id)

    if not plan:
        await message.answer(
            "Choose your reading plan:",
            reply_markup=get_plan_keyboard()
        )
        return

    reading = await get_today_reading(db_user_id)

    text = "Today:\n"
    for book, ch in reading:
        text += f"{book} {ch}\n"

    await message.answer(text, reply_markup=get_reading_keyboard())


@router.callback_query(lambda c: c.data.startswith("plan_"))
async def plan_callback(callback: CallbackQuery, state: FSMContext):
    db_user_id = await create_user_if_not_exists(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    if callback.data == "plan_1_1":
        await create_or_update_plan(db_user_id, 1, 1)

    elif callback.data == "plan_2_1":
        await create_or_update_plan(db_user_id, 2, 1)

    elif callback.data == "plan_2_2":
        await create_or_update_plan(db_user_id, 2, 2)

    elif callback.data == "plan_custom":
        await state.set_state(CustomPlan.choosing_nt)
        await callback.message.answer(
            "Choose number of NT chapters per day:",
            reply_markup=get_number_keyboard("nt")
        )
        await callback.answer()
        return

    reading = await get_today_reading(db_user_id)

    text = "Today:\n"
    for book, ch in reading:
        if isinstance(ch, list):
            if len(ch) == 1:
                text += f"{book} {ch[0]}\n"
            else:
                text += f"{book} {ch[0]}–{ch[-1]}\n"
        else:
            text += f"{book} {ch}\n"

    await callback.message.answer(text, reply_markup=get_reading_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("nt_"))
async def choose_nt(callback: CallbackQuery, state: FSMContext):
    nt_value = int(callback.data.split("_")[1])

    await state.update_data(nt=nt_value)
    await state.set_state(CustomPlan.choosing_ot)

    await callback.message.answer(
        "Choose number of OT chapters per day:",
        reply_markup=get_number_keyboard("ot")
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("ot_"))
async def choose_ot(callback: CallbackQuery, state: FSMContext):
    ot_value = int(callback.data.split("_")[1])

    data = await state.get_data()
    nt_value = data.get("nt", 0)

    db_user_id = await create_user_if_not_exists(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    await create_or_update_plan(db_user_id, nt_value, ot_value)

    reading = await get_today_reading(db_user_id)

    text = "Today:\n"
    for book, ch in reading:
        text += f"{book} {ch}\n"

    await callback.message.answer(text)

    await state.clear()
    await callback.answer()
    
@router.callback_query(lambda c: c.data == "mark_read")
async def mark_read_callback(callback: CallbackQuery):
    db_user_id = await create_user_if_not_exists(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    streak = await mark_as_read(db_user_id)

    await callback.message.answer(f"🔥 Current streak: {streak} days")
    await callback.answer()
    
    
@router.message(Command("stats"))
async def stats_handler(message: Message):
    db_user_id = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    pool = get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow("""
            SELECT current_streak, max_streak, total_days
            FROM users
            WHERE id = $1
        """, db_user_id)

    month_count, days_in_month, percentage = await get_month_stats(db_user_id)

    text = (
        f"📊 Your Statistics:\n\n"
        f"🔥 Current streak: {user['current_streak']} days\n"
        f"🏆 Max streak: {user['max_streak']} days\n"
        f"📖 Total reading days: {user['total_days']}\n\n"
        f"📅 This month: {month_count}/{days_in_month} days\n"
        f"📈 Completion: {percentage}%"
    )

    await message.answer(text)
    
    
@router.message(Command("rating"))
async def rating_handler(message: Message):
    db_user_id = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    leaderboard = await get_month_leaderboard()

    if not leaderboard:
        await message.answer("No data yet.")
        return

    text = "🏆 Monthly Leaderboard:\n\n"

    for i, row in enumerate(leaderboard, start=1):
        name = row["name"] or "Anonymous"
        days = row["days_count"]
        text += f"{i}. {name} — {days} days\n"

    # додаємо твою позицію
    rank, user_days = await get_user_rank(db_user_id)

    text += "\n"
    text += f"📍 Your position: #{rank}\n"
    text += f"📖 Your days this month: {user_days}"

    await message.answer(text)