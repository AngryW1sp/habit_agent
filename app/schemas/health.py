from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Стандартный ответ health-check endpoint."""
    status: str
    service: str
    version: str | None = None
