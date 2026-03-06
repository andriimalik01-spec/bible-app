from app.texts import ua, de, ru


def get_texts(language: str):
    if language == "de":
        return de
    if language == "ru":
        return ru
    return ua