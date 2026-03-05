from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_reading_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ I read today", callback_data="mark_read")]
    ])