from datetime import date


def get_incomplete_key(day: date) -> str:
    return f'habit:incomplete:{day.isoformat()}'


def checkin_key(habit_id: int, day: date) -> str:
    return f"habit:checkin:{habit_id}:{day.isoformat()}"
