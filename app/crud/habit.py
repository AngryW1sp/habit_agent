from app.models.habit import Habit
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


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

    async def get(self, session: AsyncSession, id: int):
        result = await session.get(self.model, id)
        if not result:
            raise HTTPException(
                status_code=404,
                detail='Не найдено'
            )
        return result


habit_crud = CRUDBase(Habit)
