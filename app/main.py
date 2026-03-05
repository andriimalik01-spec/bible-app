import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import BOT_TOKEN
from app.core.database import create_pool, init_db, close_pool
from app.handlers import start


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(start.router)

    await create_pool()
    await init_db()

    try:
        await dp.start_polling(bot)
    finally:
        await close_pool()


if name == "__main__":
    asyncio.run(main())