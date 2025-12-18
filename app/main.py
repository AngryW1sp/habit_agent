"""Приложение FastAPI для сервиса привычек (маршруты и конфигурация)."""

from fastapi import FastAPI
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.habit import router as habit_router

API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    """Создаёт и настраивает экземпляр FastAPI приложения."""
    app = FastAPI(title="Habit Service", version="0.1.0")

    app.include_router(health_router, prefix=API_PREFIX)
    app.include_router(habit_router, prefix=API_PREFIX)

    return app


app = create_app()
