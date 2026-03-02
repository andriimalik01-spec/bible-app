from datetime import date
from .database import get_connection


def mark_done(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    today = str(date.today())

    cur.execute(
        "INSERT OR REPLACE INTO progress (user_id, date, status) VALUES (?, ?, ?)",
        (user_id, today, "done")
    )

    cur.execute("UPDATE users SET streak = streak + 1 WHERE id=?", (user_id,))
    cur.execute("""
        UPDATE users
        SET max_streak = CASE
            WHEN streak > max_streak THEN streak
            ELSE max_streak
        END
        WHERE id=?
    """, (user_id,))

    conn.commit()
    conn.close()