from fastapi import FastAPI
from celery.result import AsyncResult
from .tasks import generate_heavy_report, celery_app

app = FastAPI()


@app.post("/reports/{user_id}")
async def create_report(user_id: int):
    # .delay() pushes the task to the queue and returns immediately
    task = generate_heavy_report.delay(user_id)

    # The API responds in milliseconds, giving the user a tracking ID
    return {
        "message": "Report generation started in the background",
        "task_id": task.id
    }


@app.get("/reports/status/{task_id}")
async def get_report_status(task_id: str):
    # Retrieve the task from the Redis backend using the task_id
    task_result = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "task_status": task_result.status,  # e.g., PENDING, STARTED, SUCCESS
        "result": task_result.result if task_result.ready() else None
    }
