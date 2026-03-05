from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.services.rating import create_month_snapshot

scheduler = AsyncIOScheduler()


def setup_scheduler():
    # Snapshot 1 числа кожного місяця о 00:05
    scheduler.add_job(
        create_month_snapshot,
        CronTrigger(day=1, hour=0, minute=5)
    )

    scheduler.start()