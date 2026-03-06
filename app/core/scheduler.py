from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
import datetime

from app.config import BOT_TOKEN
from app.services.rating import create_month_snapshot
from app.services.daily_content import get_random_content, get_all_users
from app.services.reading_plan import get_backlog

scheduler = AsyncIOScheduler()


def setup_scheduler():
    # 📅 Snapshot 1 числа кожного місяця о 00:05
    scheduler.add_job(
        create_month_snapshot,
        CronTrigger(day=1, hour=0, minute=5)
    )

    # 🌅 Щоденне натхнення о 08:00
    scheduler.add_job(
        send_daily_inspiration,
        CronTrigger(hour=8, minute=0)
    )
    
    scheduler.add_job(
        send_evening_reminder,
        CronTrigger(hour=2, minute=10)
    )

    scheduler.start()
    


async def send_daily_inspiration():
    bot = Bot(token=BOT_TOKEN)

    users = await get_all_users()

    for user in users:
        user_id = user["id"]
        telegram_id = user["telegram_id"]
        language = user["language"]

        # 🔔 Перевірка backlog
        backlog = await get_backlog(user_id)

        if len(backlog) > 0:
            reminder_text = (
                f"🙏 У тебе є {len(backlog)} незакритих днів.\n"
                "Можливо сьогодні — хороший день надолужити."
            )

            try:
                await bot.send_message(telegram_id, reminder_text)
            except:
                pass

        # 🌅 Основне натхнення
        content = await get_random_content(language)

        if content:
            text = f"🌅 Daily Inspiration\n\n{content['text']}"

            if content["author"]:
                text += f"\n\n— {content['author']}"

            try:
                await bot.send_message(telegram_id, text)
            except:
                pass
                
                
from app.services.reading_plan import get_backlog


async def send_evening_reminder():
    bot = Bot(token=BOT_TOKEN)
    users = await get_all_users()

    for user in users:
        user_id = user["id"]
        telegram_id = user["telegram_id"]

        if await needs_evening_reminder(user_id):
            text = (
                "🌙 День добігає кінця.\n\n"
                "Не забудь сьогоднішнє читання 🙏\n"
                "Можливо це займе лише 5–10 хвилин."
            )

            try:
                await bot.send_message(telegram_id, text)
            except:
                pass