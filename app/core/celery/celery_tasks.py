
import asyncio
from datetime import date, timedelta
import time
import logging
from app.crud.habit import habit_crud
from app.core.celery.celery_app import celery_app
from app.core.db import session_scope

logger = logging.getLogger("celery.habit")


@celery_app.task(name="app.core.celery.celery_tasks.daily_init_incomplete", bind=True)
def daily_init_incomplete(self):
    started = time.perf_counter()
    try:
        changed = asyncio.run(_daily_init_incomplete_async())
        elapsed = time.perf_counter() - started
        logger.info(
            "finalize_yesterday OK | task_id=%s | changed=%s | elapsed=%.3fs",
            self.request.id, changed, elapsed
        )
        return changed
    except Exception:
        elapsed = time.perf_counter() - started
        logger.exception(
            "finalize_yesterday FAIL | task_id=%s | elapsed=%.3fs",
            self.request.id, elapsed
        )
        raise


async def _daily_init_incomplete_async():
    day = date.today() - timedelta(days=1)
    async with session_scope() as session:
        async with session.begin():
            changed = await habit_crud.yesterday_not_complete(session)
    logger.info("finalize_yesterday | day=%s | changed=%s",
                day.isoformat(), changed)
    return changed
