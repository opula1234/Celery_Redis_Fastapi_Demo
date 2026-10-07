import logging
import time

from fastapi import FastAPI, Request
from celery.result import AsyncResult

from .logging_config import setup_logging
from .tasks import generate_heavy_report, celery_app

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(
        "%s %s -> %s in %.3fs",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )
    return response


@app.post("/reports/{user_id}")
async def create_report(user_id: int):
    logger.info("Submitting report generation for user_id=%s", user_id)
    task = generate_heavy_report.delay(user_id)

    logger.info("Task queued with id=%s for user_id=%s", task.id, user_id)
    return {
        "message": "Report generation started in the background",
        "task_id": task.id,
    }


@app.get("/reports/status/{task_id}")
async def get_report_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    logger.info("Checking report status for task_id=%s status=%s", task_id, task_result.status)

    return {
        "task_id": task_id,
        "task_status": task_result.status,
        "result": task_result.result if task_result.ready() else None,
    }
