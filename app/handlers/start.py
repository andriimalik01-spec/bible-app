from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.services.users import create_user_if_not_exists

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):

    await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )

    await message.answer(
        "📖 Ласкаво просимо до Bible Bot!\n\n"
        "Нехай кожен день буде кроком ближче до Бога 🙏"
    )