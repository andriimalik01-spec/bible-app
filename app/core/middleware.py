from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import traceback


import logging

class ErrorMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except Exception:
            logging.exception("Unhandled error")