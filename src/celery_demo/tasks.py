import logging
import os
import time

from celery import Celery
from celery.utils.log import get_task_logger

from .logging_config import setup_logging

setup_logging()

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", broker_url)

celery_app = Celery("worker", broker=broker_url, backend=result_backend)
logger = get_task_logger(__name__)


@celery_app.task
def generate_heavy_report(user_id: int):
    """
    Simulates a time-consuming task, like aggregating data from PostgreSQL and
    generating a PDF.
    """
    logger.info("Starting report generation for user_id=%s", user_id)
    time.sleep(1)  # Simulate 10 seconds of processing time

    result = {
        "status": "success",
        "user_id": user_id,
        "file_path": f"/downloads/report_{user_id}.pdf",
    }
    logger.info("Finished report generation for user_id=%s: %s", user_id, result)
    return result
