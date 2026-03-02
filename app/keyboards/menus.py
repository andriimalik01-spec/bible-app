from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def home_menu(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Почати читання")],
            [KeyboardButton(text="📊 Мій шлях"),
             KeyboardButton(text="🏆 Топ рейтинг")],
            [KeyboardButton(text="⚙️ Налаштування")]
        ],
        resize_keyboard=True
    )


def reading_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Показати сьогоднішнє читання")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )