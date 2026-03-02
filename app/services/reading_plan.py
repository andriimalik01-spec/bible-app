from datetime import date

START_DATE = date(2026, 1, 1)

BIBLE_BOOKS = [
    ("Буття", 50), ("Вихід", 40), ("Левіт", 27),
    ("Числа", 36), ("Повторення Закону", 34),
    ("Ісус Навин", 24), ("Судді", 21),
    ("1 Самуїлова", 31), ("2 Самуїлова", 24),
    ("Матвія", 28), ("Марка", 16),
    ("Луки", 24), ("Івана", 21)
]

CHAPTERS = [(b, c) for b, n in BIBLE_BOOKS for c in range(1, n + 1)]


def get_reading(plan: int):
    today_index = (date.today() - START_DATE).days * plan
    return [
        f"{book} {ch}"
        for book, ch in CHAPTERS[today_index:today_index + plan]
    ]