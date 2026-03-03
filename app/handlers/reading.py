from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from app.services.plans import get_all_plans
from app.services.progress import start_plan_for_user
from app.services.users import get_user_by_telegram_id

router = Router()


# Кнопка "Обрати план"
@router.message(F.text == "📚 Обрати план")
async def choose_plan(message: Message):
    plans = await get_all_plans()

    if not plans:
        await message.answer("Наразі немає доступних планів.")
        return

    text = "📚 Оберіть план:\n\n"

    for plan in plans:
        text += f"{plan['id']}. {plan['name']} ({plan['duration_days']} днів)\n"

    await message.answer(text)


# Вибір плану цифрою (1,2,3...)
@router.message(F.text.regexp(r"^\d+$"))
async def plan_selected(message: Message):
    plan_id = int(message.text)

    user = await get_user_by_telegram_id(message.from_user.id)

    if not user:
        await message.answer("Помилка користувача.")
        return

    await start_plan_for_user(
        telegram_id=message.from_user.id,
        plan_id=plan_id
    )

    await message.answer("✅ План успішно обрано!\nНатисніть «📖 Сьогоднішнє читання»")