import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.core.scheduler import setup_scheduler

from app.config import BOT_TOKEN
from app.core.database import create_pool, init_db, close_pool
from app.handlers import start
import app.handlers.journal as journal
from app.core.middleware import ErrorMiddleware
import app.handlers.achievements as achievements
import app.handlers.settings as settings



async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())
    
    dp.message.middleware(ErrorMiddleware())
    dp.callback_query.middleware(ErrorMiddleware())
    
    dp.include_router(start.router)
    dp.include_router(journal.router)
    dp.include_router(achievements.router)
    dp.include_router(settings.router)
    
    
    

    await create_pool()
    await init_db()
    setup_scheduler()

    try:
        await dp.start_polling(bot)
    finally:
        await close_pool()


if __name__ == "__main__":
    asyncio.run(main())