import logging
import sys

from loguru import logger
from config import settings


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def init_log_conf() -> None:
    """
    custom project logging with loguru
    """
    logging.basicConfig(handlers=[InterceptHandler()],
                        level=settings["log_level"])

    # add set logger level
    logger.remove()
    logger.add(sys.stderr, level=settings["log_level"])
