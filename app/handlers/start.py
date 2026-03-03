from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.keyboards.main_menu import get_main_menu
from app.services.users import create_user_if_not_exists

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await create_user_if_not_exists(message.from_user)

    await message.answer(
        "📖 Ласкаво просимо до Біблійного бота!\n\n"
        "Обери дію з меню нижче 👇",
        reply_markup=get_main_menu()
    )