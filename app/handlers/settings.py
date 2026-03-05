from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.services.users import create_user_if_not_exists
from app.core.database import get_pool
from app.keyboards.plan_keyboard import get_plan_keyboard

router = Router()


def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_ua")],
        [InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
    ])


def settings_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌍 Change Language", callback_data="change_lang")],
        [InlineKeyboardButton(text="📖 Change Reading Plan", callback_data="change_plan")],
    ])


@router.message(Command("settings"))
async def settings_menu(message: Message):
    await message.answer(
        "⚙️ Settings:",
        reply_markup=settings_keyboard()
    )


@router.callback_query(lambda c: c.data == "change_lang")
async def change_language(callback: CallbackQuery):
    await callback.message.answer(
        "Choose your language:",
        reply_markup=language_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]

    db_user_id = await create_user_if_not_exists(
        telegram_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE users
            SET language = $1
            WHERE id = $2
        """, lang, db_user_id)

    await callback.message.answer("✅ Language updated.")
    await callback.answer()


@router.callback_query(lambda c: c.data == "change_plan")
async def change_plan(callback: CallbackQuery):
    await callback.message.answer(
        "Choose new reading plan:",
        reply_markup=get_plan_keyboard()
    )
    await callback.answer()