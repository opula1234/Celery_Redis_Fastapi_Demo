# Celery Demo

A FastAPI app that queues report-generation tasks with Celery and stores task
results in Redis.

## Run with Docker Compose

From the project root, build and start the API, Celery worker, Redis, and Flower:

```powershell
docker compose up --build
```

The services are available at:

- API: <http://localhost:8000>
- Interactive API docs: <http://localhost:8000/docs>
- Flower task monitor: <http://localhost:5555>

Create a report task:

```powershell
$task = Invoke-RestMethod -Method Post -Uri http://localhost:8000/reports/123
$task.task_id
```

Check the task status using the returned task ID:

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/reports/status/$($task.task_id)"
```

Stop the services:

```powershell
docker compose down
```

Redis data is kept in the `redis_data` volume when the containers are stopped.
To remove the containers and persisted Redis data, run `docker compose down -v`.

## Run locally

When running the API or worker outside Docker, Redis must be available at
`localhost:6379`. The `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`
environment variables can override the default Redis URLs.