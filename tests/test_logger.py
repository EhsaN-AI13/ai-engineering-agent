from logger import logger


def test_logger_has_console_handler():
    assert len(logger.handlers) >= 1


def test_logger_has_file_handler():
    assert any(
        hasattr(handler, "baseFilename")
        for handler in logger.handlers
    )