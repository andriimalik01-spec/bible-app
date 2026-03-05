from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.services.users import create_user_if_not_exists

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    await message.answer(f"Welcome. Your DB id: {user_id}")