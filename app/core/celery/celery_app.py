"""Конфигурация Celery — брокер, бекенд и расписание задач."""

from celery import Celery
from celery.schedules import crontab
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

celery_app = Celery(
    "habit_agent",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["app.core.celery.celery_tasks"],
)

celery_app.conf.update(
    timezone="Europe/Amsterdam",
    enable_utc=False,
)

celery_app.conf.beat_schedule = {
    "daily-init-incomplete": {
        "task": "app.core.celery.celery_tasks.daily_init_incomplete",
        "schedule": crontab(hour=0, minute=5),
    }
}
