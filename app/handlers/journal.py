from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.services.users import create_user_if_not_exists
from app.services.journal import add_journal_entry, get_user_entries

router = Router()


class JournalStates(StatesGroup):
    waiting_for_text = State()


@router.message(Command("journal"))
async def show_journal(message: Message):
    db_user_id = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    entries = await get_user_entries(db_user_id)

    if not entries:
        await message.answer("No journal entries yet.")
        return

    text = "📓 Your latest entries:\n\n"

    for entry in entries:
        text += (
            f"{entry['created_at'].date()} — "
            f"{entry['book']} {entry['chapter']}\n"
            f"{entry['text']}\n\n"
        )

    await message.answer(text)


@router.message(Command("note"))
async def add_note_start(message: Message, state: FSMContext):
    await state.set_state(JournalStates.waiting_for_text)
    await message.answer("✍️ Send me your journal text.")


@router.message(JournalStates.waiting_for_text)
async def save_note(message: Message, state: FSMContext):
    db_user_id = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name
    )

    await add_journal_entry(
        user_id=db_user_id,
        book="Unknown",
        chapter="Unknown",
        text=message.text
    )

    await state.clear()
    await message.answer("✅ Journal entry saved.")