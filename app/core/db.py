from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


engine = create_async_engine(
    settings.database_url,
    echo=(settings.ENV == "local"),
)

async_session_maker = async_sessionmaker(engine,
                                         expire_on_commit=False,)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def session_scope() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
