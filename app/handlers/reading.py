from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from app.services.reading import get_today_reading
from app.services.i18n import t
from aiogram import Router
from aiogram.types import Message
from app.services.plans import get_all_plans
from app.services.progress import start_plan_for_user

router = Router()

@router.message(lambda message: message.text in ["📖 Сьогоднішнє читання", "📖 Сегодняшнее чтение"])
async def today_reading_handler(message: Message):
    data = await get_today_reading(message.from_user.id)

    if not data:
        await message.answer("Спочатку оберіть план.")
        return

    current_day = data["current_day"]
    content = data["content"]

    await message.answer(
        f"📖 День {current_day}\n\n{content}"
    )

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

@router.message(lambda message: message.text == "30 днів з Притчами (30 днів)")
async def choose_30_days_plan(message: Message):

    plan = await get_plan_by_name("30 днів з Притчами (30 днів)")

    if not plan:
        await message.answer("❌ План не знайдено.")
        return

    await subscribe_user_to_plan(
        user_id=message.from_user.id,
        plan_id=plan["id"]
    )

    await message.answer(
        "✅ Ви обрали план «30 днів з Притчами».\n\n"
        "📖 Натисніть «Сьогоднішнє читання» щоб почати."
    )

# ✅ Вибір плану через callback
@router.callback_query(F.data.startswith("select_plan:"))
async def plan_selected(callback: CallbackQuery):
    plan_id = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    await start_plan_for_user(telegram_id, plan_id)

    await callback.message.answer("✅ План успішно обрано!")
    await callback.answer()