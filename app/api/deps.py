"""Dependency-инъекции для FastAPI (Redis и DB сессии)."""

from typing import Annotated

from redis.asyncio import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.redis_init import redis_client

RedisDep = Annotated[Redis, Depends(lambda: redis_client)]
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
