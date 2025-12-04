from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.crud.habit import habit_crud
from app.models.habit import Habit
from app.schemas.habit import HabitUpdate


async def habit_completely(obj_in: HabitUpdate, habit_id: int, session: AsyncSession):
    habit = await session.get(Habit, habit_id)
    update_data = obj_in.model_dump(exclude_unset=True)
    if not habit:
        raise HTTPException(
            status_code=404,
            detail='Не найдено'
        )
    if update_data['completed_today']:
        if habit.completed_days_count == 20:
            update_data['completed_days_count'] = 21
            update_data['is_active'] = False
            update_data['success'] = True
        else:
            update_data['completed_days_count'] = habit.completed_days_count + 1
    await habit_crud.update(session, update_data, habit)
    return habit
