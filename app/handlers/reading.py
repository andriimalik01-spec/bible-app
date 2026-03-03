from aiogram import Router
from aiogram.types import Message
from app.services.reading_plan import get_reading
from app.services.stats import mark_done

router = Router()


@router.message(lambda m: m.text == "📖 Почати читання")
async def open_reading(message: Message):
    await message.answer(
        "📖 Режим читання",
    )


@router.message(lambda m: m.text == "📖 Показати сьогоднішнє читання")
async def today_reading(message: Message):
    reading = get_reading(3)
    text = "📖 Сьогодні читаємо:\n\n" + "\n".join(reading)
    await message.answer(text)


@router.message(lambda m: m.text == "✅ Я прочитав")
async def done(message: Message):
    mark_done(message.from_user.id)
    await message.answer("✅ Записано! 🙏")
    
from aiogram import Router
from aiogram.types import Message
from app.services.plans import get_all_plans, select_plan_for_user, get_today_reading

router = Router()


@router.message(lambda m: m.text == "📚 Обрати план")
async def choose_plan(message: Message):
    plans = await get_all_plans()

    if not plans:
        await message.answer("Плани поки що недоступні.")
        return

    text = "📚 Доступні плани:\n\n"

    for plan in plans:
        text += f"{plan['id']}. {plan['name']} ({plan['duration_days']} днів)\n"

    text += "\nНапишіть номер плану для вибору."

    await message.answer(text)


@router.message(lambda m: m.text.isdigit())
async def select_plan(message: Message):
    plan_id = int(message.text)

    await select_plan_for_user(
        message.from_user.id,
        plan_id
    )

    await message.answer("✅ План обрано! Починаємо з 1 дня 🙏")


@router.message(lambda m: m.text == "📖 Сьогоднішнє читання")
async def today_reading(message: Message):
    content = await get_today_reading(message.from_user.id)

    if not content:
        await message.answer("Спочатку оберіть план 📚")
        return

    await message.answer(content)