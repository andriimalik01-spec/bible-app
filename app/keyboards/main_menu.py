from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    keyboard = [
        [KeyboardButton(text="📖 Почати читання")],
        [KeyboardButton(text="📅 План читання")],
        [KeyboardButton(text="📊 Моя статистика")],
        [KeyboardButton(text="✨ Побажання дня")],
        [KeyboardButton(text="⚙️ Налаштування")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )