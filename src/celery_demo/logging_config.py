import logging
import logging.config
import os
from datetime import date


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", "app.log")


class DailyDateFolderFileHandler(logging.Handler):
    """Write logs to logs/YYYY-MM-DD/app.log and reopen automatically each day."""

    def __init__(self, base_dir: str = LOG_DIR, file_name: str = LOG_FILE_NAME):
        super().__init__()
        self.base_dir = base_dir
        self.file_name = file_name
        self.stream = None
        self.current_date = None
        self._open_file()

    def _get_log_path(self) -> str:
        today = date.today().strftime("%Y-%m-%d")
        folder = os.path.join(self.base_dir, today)
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, self.file_name)

    def _open_file(self) -> None:
        if self.stream is not None and not self.stream.closed:
            self.stream.close()

        self.current_date = date.today().strftime("%Y-%m-%d")
        path = self._get_log_path()
        self.baseFilename = os.path.abspath(path)
        self.stream = open(path, "a", encoding="utf-8")

    def emit(self, record: logging.LogRecord) -> None:
        today = date.today().strftime("%Y-%m-%d")
        if self.current_date != today:
            self._open_file()

        try:
            msg = self.format(record)
            stream = self.stream
            if stream is not None:
                stream.write(msg + "\n")
                stream.flush()
        except Exception:
            self.handleError(record)

    def close(self) -> None:
        if self.stream is not None and not self.stream.closed:
            self.stream.close()
        super().close()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "celery_demo.logging_config.DailyDateFolderFileHandler",
            "level": LOG_LEVEL,
            "formatter": "standard",
            "base_dir": LOG_DIR,
            "file_name": LOG_FILE_NAME,
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console", "file"],
    },
    "loggers": {
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
