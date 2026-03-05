from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_plan_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 NT + 1 OT", callback_data="plan_1_1")],
        [InlineKeyboardButton(text="2 NT + 1 OT", callback_data="plan_2_1")],
        [InlineKeyboardButton(text="2 NT + 2 OT", callback_data="plan_2_2")],
        [InlineKeyboardButton(text="Custom Plan", callback_data="plan_custom")],
    ])