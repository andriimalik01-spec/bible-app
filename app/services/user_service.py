from app.database import get_connection
from datetime import date


class UserService:

    @staticmethod
    def get_or_create(user_id: int, name: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if not user:
            cursor.execute("""
                INSERT INTO users (id, name, lang)
                VALUES (?, ?, ?)
            """, (user_id, name, None))
            conn.commit()

            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()

        conn.close()
        return user

    @staticmethod
    def set_language(user_id: int, lang: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET lang = ?
            WHERE id = ?
        """, (lang, user_id))

        conn.commit()
        conn.close()

    @staticmethod
    def get_language(user_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT lang FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()

        conn.close()
        return result[0] if result else None

    @staticmethod
    def mark_read(user_id: int):
        today = str(date.today())

        conn = get_connection()
        cursor = conn.cursor()

        # запис у лог
        cursor.execute("""
            INSERT OR REPLACE INTO reading_logs (user_id, date, status)
            VALUES (?, ?, 'done')
        """, (user_id, today))

        # streak
        cursor.execute("SELECT streak, max_streak FROM users WHERE id = ?", (user_id,))
        streak, max_streak = cursor.fetchone()

        streak += 1
        max_streak = max(max_streak, streak)

        cursor.execute("""
            UPDATE users
            SET streak = ?, max_streak = ?
            WHERE id = ?
        """, (streak, max_streak, user_id))

        conn.commit()
        conn.close()

    @staticmethod
    def get_stats(user_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM reading_logs
            WHERE user_id = ? AND status = 'done'
        """, (user_id,))
        done = cursor.fetchone()[0]

        cursor.execute("""
            SELECT streak, max_streak
            FROM users
            WHERE id = ?
        """, (user_id,))
        streak, max_streak = cursor.fetchone()

        conn.close()

        return {
            "done": done,
            "streak": streak,
            "max_streak": max_streak
        }