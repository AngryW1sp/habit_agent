from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.habit import HabitCheckin


class HabitCheckinCrud(CRUDBase):
    async def get_complete_habit(self, session: AsyncSession, day: date, habit_id: int):
        result = await session.execute(select(self.model)
                                       .where(self.model.date == day,
                                              self.model.habit_id == habit_id))
        return result.scalars().first()

    async def create(self, session: AsyncSession, data_in,) -> HabitCheckin:
        data_db = self.model(
            **data_in
        )
        session.add(data_db)
        return data_db


habit_checkin_crud = HabitCheckinCrud(HabitCheckin)
