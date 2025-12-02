from fastapi import APIRouter
from app.schemas.health import HealthResponse

router = APIRouter(prefix='/health')


@router.get(
    '',
    response_model=HealthResponse,
    summary='Health check',
    description='Проверка доступности сервисаю'
)
async def get_health() -> HealthResponse:
    return HealthResponse(status='ok', service='habit_service', version='0.1.0')
