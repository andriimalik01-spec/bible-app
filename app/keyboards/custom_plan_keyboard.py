from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_number_keyboard(prefix: str):
    buttons = []
    for i in range(5):
        buttons.append(
            [InlineKeyboardButton(
                text=str(i),
                callback_data=f"{prefix}_{i}"
            )]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)