import asyncio
from aiogram import Bot, Dispatcher
from app.config import TOKEN
from app.database.connection import init_db
from app.services.seed import seed_reading_plans


from app.handlers import start, reading

async def main():
    await init_db()
    await seed_reading_plans()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(reading.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())