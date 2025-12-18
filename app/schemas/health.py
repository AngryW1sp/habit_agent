from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Стандартный ответ для проверки состояния сервиса (health-check)."""

    status: str
    service: str
    version: str | None = None
