from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from app.services.plans import get_all_plans
from app.services.progress import start_plan_for_user

router = Router()


# 📚 Кнопка "Обрати план"
@router.message(F.text == "📚 Обрати план")
async def choose_plan(message: Message):
    plans = await get_all_plans()

    if not plans:
        await message.answer("Наразі немає доступних планів.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{plan['name']} ({plan['duration_days']} днів)",
                    callback_data=f"select_plan:{plan['id']}"
                )
            ]
            for plan in plans
        ]
    )

    await message.answer(
        "📚 Оберіть план:",
        reply_markup=keyboard
    )


# ✅ Вибір плану через callback
@router.callback_query(F.data.startswith("select_plan:"))
async def plan_selected(callback: CallbackQuery):
    plan_id = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    await start_plan_for_user(telegram_id, plan_id)

    await callback.message.answer("✅ План успішно обрано!")
    await callback.answer()