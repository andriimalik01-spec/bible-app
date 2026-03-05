from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.services.users import create_user_if_not_exists
from app.services.reading_plan import create_or_update_plan, get_today_reading

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    db_user_id = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    # Тимчасово ставимо план 1+1
    await create_or_update_plan(db_user_id, 1, 1)

    reading = await get_today_reading(db_user_id)

    if not reading:
        await message.answer("Plan not found.")
        return

    text = "Today:\n"
    for book, ch in reading:
        text += f"{book} {ch}\n"

    await message.answer(text)