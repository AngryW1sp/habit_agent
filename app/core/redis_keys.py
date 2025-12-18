"""Вспомогательные функции для формирования ключей в Redis."""

from datetime import date


def get_incomplete_key(day: date) -> str:
    """Ключ для множества привычек, не выполненных в указанный день."""
    return f"habit:incomplete:{day.isoformat()}"


def checkin_key(habit_id: int, day: date) -> str:
    """Ключ для конкретной отметки о выполнении привычки в Redis."""
    return f"habit:checkin:{habit_id}:{day.isoformat()}"
