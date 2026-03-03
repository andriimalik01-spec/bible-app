from app.locales.ua import TEXTS as UA
from app.locales.ru import TEXTS as RU
from app.services.users import get_user_language

LANGUAGES = {
    "ua": UA,
    "ru": RU
}


async def t(telegram_id: int, key: str) -> str:
    lang = await get_user_language(telegram_id)
    return LANGUAGES.get(lang, UA).get(key, key)