from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.config import ADMIN_ID
from app.core.database import get_pool
from app.services.rating import create_month_snapshot

router = Router()


class AdminStates(StatesGroup):
    waiting_for_quote = State()


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(Command("admin"))
async def admin_menu(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "🛠 Admin Panel:\n\n"
        "/add_quote — Add daily quote\n"
        "/snapshot_now — Create snapshot\n"
        "/users_count — Show users count"
    )


@router.message(Command("add_quote"))
async def add_quote_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(AdminStates.waiting_for_quote)
    await message.answer("Send quote in format:\nText | Author | language")


@router.message(AdminStates.waiting_for_quote)
async def save_quote(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    try:
        text, author, language = map(str.strip, message.text.split("|"))
    except:
        await message.answer("Wrong format. Use:\nText | Author | language")
        return

    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO daily_content (type, text, author, language)
            VALUES ('quote', $1, $2, $3)
        """, text, author, language)

    await state.clear()
    await message.answer("✅ Quote added.")


@router.message(Command("snapshot_now"))
async def snapshot_now(message: Message):
    if not is_admin(message.from_user.id):
        return

    await create_month_snapshot()
    await message.answer("📅 Snapshot created.")


@router.message(Command("users_count"))
async def users_count(message: Message):
    if not is_admin(message.from_user.id):
        return

    pool = get_pool()
    async with pool.acquire() as conn:
        count = await conn.fetchval("SELECT COUNT(*) FROM users")

    await message.answer(f"👥 Total users: {count}")