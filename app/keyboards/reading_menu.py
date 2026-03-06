from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_reading_menu(backlog_count: int = 0):
    buttons = [
        [InlineKeyboardButton(text="📖 Читати сьогодні", callback_data="reading_today")]
    ]

    if backlog_count > 0:
        buttons.append([
            InlineKeyboardButton(
                text=f"📚 Надолужити ({backlog_count})",
                callback_data="reading_backlog"
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="✅ Я прочитав", callback_data="reading_done")
    ])

    buttons.append([
        InlineKeyboardButton(text="📝 Записати думку", callback_data="reading_note")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)