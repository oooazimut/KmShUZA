from logging.handlers import RotatingFileHandler
import logging
import sys


class OnceLogger:
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._exceptions = set()

    def log_exceptions_for_once(self, func):
        async def wrapper(*args, **kwargs):
            try:
                await func(*args, **kwargs)
                self._exceptions.clear()
            except Exception as e:
                key = type(e), str(e)
                if key not in self._exceptions:
                    self._logger.error(e)
                    self._exceptions.add(key)

        return wrapper


def configure_logging(name: str):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    info_handler = RotatingFileHandler(
        f"logs/{name}.log",
        maxBytes=50_000_000,
        backupCount=5,
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    logger.addHandler(info_handler)

    error_handler = RotatingFileHandler(
        f"logs/{name}.err",
        maxBytes=50_000_000,
        backupCount=5,
    )
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    logging.raiseExceptions = False
