from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Reading")],
            [KeyboardButton(text="📓 Journal"), KeyboardButton(text="📊 Statistics")],
            [KeyboardButton(text="🏆 Rating"), KeyboardButton(text="🏅 Achievements")],
            [KeyboardButton(text="⚙️ Settings")],
        ],
        resize_keyboard=True
    )