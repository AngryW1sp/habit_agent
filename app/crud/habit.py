"""CRUD-операции для сущности Habit."""

from datetime import date, timedelta
from app.crud.base import CRUDBase
from app.models.habit import Habit, HabitCheckin
from sqlalchemy import select, not_, exists, update
from sqlalchemy.ext.asyncio import AsyncSession


class HabitCrud(CRUDBase):
    """CRUD-обёртка с методами для выборок и массовых операций по привычкам."""

    async def get_multi(self, session: AsyncSession):
        """Вернуть все привычки."""
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def get_active(self, session: AsyncSession):
        """Вернуть идентификаторы активных привычек."""
        result = await session.execute(
            select(self.model.id).where(self.model.is_active.is_(True))
        )
        return result.scalars().all()

    async def get_not_complete(self, session: AsyncSession):
        """Вернуть привычки, которые не были отмечены за сегодня."""
        result = await session.execute(
            select(Habit)
            .where(Habit.is_active.is_(True))
            .where(
                not_(
                    exists()
                    .where(
                        HabitCheckin.habit_id == Habit.id,
                    )
                    .where(HabitCheckin.date == date.today())
                )
            )
        )
        return result.scalars().all()

    async def yesterday_not_complete(self, session: AsyncSession):
        """Сбросить счётчик completed_days_count для привычек, не отмеченных вчера.
        Возвращает количество изменённых записей."""
        yesterday = date.today() - timedelta(days=1)
        stmt = (
            update(Habit)
            .where(Habit.is_active.is_(True))
            .where(
                not_(
                    exists()
                    .where(
                        HabitCheckin.habit_id == Habit.id,
                    )
                    .where(HabitCheckin.date == yesterday)
                )
            )
            .values(completed_days_count=0)
        )
        result = await session.execute(stmt)
        return result.rowcount or 0


habit_crud = HabitCrud(Habit)
