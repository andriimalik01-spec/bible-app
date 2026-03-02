from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.services.user_service import UserService

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "🙏 Вітаю!\nЦе  Bible Bot"
    )