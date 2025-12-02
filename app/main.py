from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.habit import router as habit_router
from fastapi import FastAPI


app = FastAPI(
    title="Habit Service",
    version="0.1.0"
)
API_PREFIX = "/api/v1"

app.include_router(health_router, prefix=API_PREFIX)
app.include_router(habit_router, prefix=API_PREFIX)
