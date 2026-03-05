from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_reading_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 What to read today", callback_data="reading_today")],
        [InlineKeyboardButton(text="✅ I read today", callback_data="reading_done")],
        [InlineKeyboardButton(text="📝 Write note", callback_data="reading_note")],
    ])