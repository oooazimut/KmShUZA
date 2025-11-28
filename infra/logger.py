import logging

logger = logging.getLogger(__name__)


class OnceLogger:
    def __init__(self) -> None:
        self._exceptions = set()

    def log_exceptions_for_once(self, func):
        async def wrapper(*args, **kwargs):
            try:
                await func(*args, **kwargs)
                self._exceptions.clear()
            except Exception as e:
                key = type(e), str(e)
                if key not in self._exceptions:
                    logger.error(e)
                    self._exceptions.add(key)

        return wrapper


def configure_logging(level):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
