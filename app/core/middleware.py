from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import traceback


class ErrorMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data):
        try:
            return await handler(event, data)
        except Exception as e:
            print("ERROR:", e)
            traceback.print_exc()