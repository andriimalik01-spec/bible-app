import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config import TOKEN
from app.handlers import start
from app.database import init_db

async def main():
    init_db()
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Реєстрація хендлерів
    dp.include_router(start.router)

    print("🚀 Bot started successfully")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())