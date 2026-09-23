import logging
from pathlib import Path


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

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)