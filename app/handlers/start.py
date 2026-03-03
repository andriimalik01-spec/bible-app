from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.services.i18n import t

from app.services.users import create_user_if_not_exists
from app.keyboards.menus import main_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):

    await create_user_if_not_exists(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )

    text = await t(message.from_user.id, "welcome")

    await message.answer(
        text,
        reply_markup=main_menu()
    )