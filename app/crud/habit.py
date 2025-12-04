from app.models.habit import Habit
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.schemas.habit import HabitUpdate


class CRUDBase:

    def __init__(self, model) -> None:
        self.model = model

    async def create(self, session: AsyncSession, data_in,):
        data_in = data_in.model_dump()
        data_db = self.model(
            **data_in
        )
        session.add(data_db)
        await session.commit()
        await session.refresh(data_db)
        return data_db

    async def get_multi(self, session: AsyncSession):
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def get(self, session: AsyncSession, id: int) -> Habit:
        result = await session.get(self.model, id)
        if not result:
            raise HTTPException(
                status_code=404,
                detail='Не найдено'
            )
        return result

    async def update(self, session: AsyncSession,
                     obj_in: dict,
                     db_data: Habit):
        obj_data = jsonable_encoder(db_data)
        for field in obj_data:
            if field in obj_in:
                setattr(db_data, field, obj_in[field])
        session.add(db_data)
        await session.commit()
        await session.refresh(db_data)
        return db_data


habit_crud = CRUDBase(Habit)
