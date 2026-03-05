from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.services.rating import create_month_snapshot
from app.services.daily_content import get_random_content, get_all_users
from aiogram import Bot
from app.config import BOT_TOKEN

scheduler = AsyncIOScheduler()


def setup_scheduler():
    # Snapshot 1 числа кожного місяця о 00:05
    scheduler.add_job(
        create_month_snapshot,
        CronTrigger(day=1, hour=0, minute=5)
    )
    scheduler.add_job(
        send_daily_inspiration,
        CronTrigger(hour=8, minute=0)
    )

    scheduler.start()
    
async def send_daily_inspiration():
    bot = Bot(token=BOT_TOKEN)

    users = await get_all_users()

    for user in users:
        content = await get_random_content(user["language"])

        if content:
            text = f"🌅 Daily Inspiration\n\n{content['text']}"
            if content["author"]:
                text += f"\n\n— {content['author']}"

            try:
                await bot.send_message(user["telegram_id"], text)
            except:
                pass
                
await conn.execute("""
INSERT INTO daily_content (type, text, author, language)
VALUES ('quote', 'Stay faithful in small things.', 'Test', 'ua')
""")