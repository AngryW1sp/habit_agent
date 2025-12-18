"""Сервисный слой с бизнес-логикой для операций над привычками."""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


from app.crud.habit import habit_crud
from app.crud.habit_checkin import habit_checkin_crud
from app.schemas.habit import HabitComplete, HabitCreate, HabitUpdate


async def habit_update(obj_in: HabitUpdate, habit_id: int, session: AsyncSession):
    """Обновить существующую привычку, возвращает обновлённую модель."""
    async with session.begin():
        habit = await habit_crud.get(session, habit_id)
        update_data = obj_in.model_dump(exclude_unset=True)
        if not habit:
            raise HTTPException(status_code=404, detail="Не найдено")
        await habit_crud.update(session, update_data, habit)
    await session.refresh(habit)
    return habit


async def complete_habit_for_today(
    session: AsyncSession,
    habit_id: int,
    habit_in: HabitComplete,
):
    """Пометить привычку как выполненную на указанную дату; обновляет счётчик и флаг success."""
    day = habit_in.date
    async with session.begin():
        habit = await habit_crud.get(session, habit_id)
        if not habit:
            raise HTTPException(404, "Привычка не найдена")

        if not habit.is_active:  # type: ignore
            raise HTTPException(409, "Привычка не активна")

        # Проверяем только для этой привычки
        habit_check = await habit_checkin_crud.get_complete_habit(
            session=session, habit_id=habit_id, day=day
        )
        if habit_check:
            raise HTTPException(400, "Привычка уже выполнена!")

        habit_check = await habit_checkin_crud.create(
            session,
            {
                "habit_id": habit_id,
                "date": day,
            },
        )

        # 2. Увеличиваем счетчик
        habit.completed_days_count += 1  # type: ignore
        if habit.completed_days_count >= 21:  # type: ignore
            habit.success = True  # type: ignore
    await session.refresh(habit)

    return habit


async def remove_habit(session: AsyncSession, habit_id: int):
    """Удалить привычку по идентификатору, вернуть удалённый объект."""
    async with session.begin():
        result = await habit_crud.get(session, habit_id)
        if not result:
            raise HTTPException(status_code=404, detail="Привычка не найдена")
        await habit_crud.remove(session, result)
    return result


async def create_habit_service(session: AsyncSession, habit: HabitCreate):
    """Сервис: создать новую привычку и вернуть объект модели."""
    async with session.begin():
        result = await habit_crud.create(session, habit)
    return result
