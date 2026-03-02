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