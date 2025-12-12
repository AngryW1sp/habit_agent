from app.models.base import Base
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit import Habit, HabitCheckin


class CRUDBase:
    def __init__(self, model) -> None:
        self.model = model

    async def create(self, session: AsyncSession, data_in,) -> Habit | HabitCheckin:
        if hasattr(data_in, 'model_dump'):
            data_in = data_in.model_dump()
        data_db = self.model(
            **data_in
        )
        session.add(data_db)
        return data_db

    async def get(self, session: AsyncSession, id: int) -> Habit | HabitCheckin:
        result = await session.get(self.model, id)
        return result

    async def update(self, session: AsyncSession,
                     obj_in: dict,
                     db_data: Base) -> Habit | HabitCheckin:
        for key, value in obj_in.items():
            setattr(db_data, key, value)
        session.add(db_data)
        return db_data

    async def remove(self,
                     session: AsyncSession,
                     obj):
        await session.delete(obj)
        return obj
