import logging
from contextvars import ContextVar
from pathlib import Path

request_id_context = ContextVar(
    "request_id",
    default="-"
)

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "ehsan.log"


logger = logging.getLogger("EhSaN")
logger.setLevel(logging.INFO)


if not logger.handlers:

    console_handler = logging.StreamHandler()

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    class RequestIdFilter(logging.Filter):

        def filter(self, record):
            record.request_id = request_id_context.get()
            return True


    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [request_id=%(request_id)s] - %(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    request_id_filter = RequestIdFilter()

    console_handler.addFilter(request_id_filter)
    file_handler.addFilter(request_id_filter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)