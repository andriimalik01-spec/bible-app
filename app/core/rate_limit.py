import time
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, cooldown: float = 1.0):
        self.cooldown = cooldown
        self.users = {}

    async def __call__(self, handler, event: TelegramObject, data):
        user = getattr(event, "from_user", None)

        if not user:
            return await handler(event, data)

        now = time.time()
        last_time = self.users.get(user.id)

        if last_time and now - last_time < self.cooldown:
            return  # блокуємо спам

        self.users[user.id] = now

        return await handler(event, data)