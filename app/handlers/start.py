from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.services.users import create_user_if_not_exists
from app.services.reading_plan import (
    create_or_update_plan,
    get_today_reading,
    get_user_plan
)
from app.keyboards.plan_keyboard import get_plan_keyboard

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

    await message.answer(text)


@router.callback_query()
async def plan_callback(callback: CallbackQuery):
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
        await callback.message.answer("Custom plan coming soon.")
        await callback.answer()
        return

    reading = await get_today_reading(db_user_id)

    text = "Today:\n"
    for book, ch in reading:
        text += f"{book} {ch}\n"

    await callback.message.answer(text)
    await callback.answer()