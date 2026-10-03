import os
import time

from celery import Celery

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", broker_url)

celery_app = Celery("worker", broker=broker_url, backend=result_backend)


@celery_app.task
def generate_heavy_report(user_id: int):
    """
    Simulates a time-consuming task, like aggregating data from PostgreSQL and
    generating a PDF.
    """
    time.sleep(1)  # Simulate 10 seconds of processing time

    # Return the result that will be saved in the Redis backend
    return {
        "status": "success",
        "user_id": user_id,
        "file_path": f"/downloads/report_{user_id}.pdf"
    }
