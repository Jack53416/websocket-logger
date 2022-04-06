import logging
from pprint import pformat
from typing import Dict, Any

from loguru import logger
from loguru._defaults import LOGURU_FORMAT


class InterceptHandler(logging.Handler):
    """
    Loguru's recipe for Intercept handler, which intercepts standard logging message and passes it towards Loguru
    sinks
    """

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

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class AppLogger(object):
    @staticmethod
    def format_record(record: dict) -> str:
        """
        Custom format for loguru loggers. Uses pformat for log any data like request/response body during debug.
        """

        format_string = LOGURU_FORMAT
        if record['extra'].get('payload') is not None:
            record['extra']['payload'] = pformat(
                record['extra']['payload'], indent=4, compact=True, width=120
            )
            format_string += '\n<level>{extra[payload]}</level>'

        format_string += '{exception}\n'
        return format_string

    @classmethod
    def make_logger(cls, *handlers: Dict[str, Any]) -> Any:
        """
        Initializes logger. Removes handlers from default python loggers and adds interceptor to pass logging to
        Loguru.

        :param handlers: Loguru handlers. See logger.config() function argument for details
        :type handlers:  Dict[str, Any]
        :return: Configured logger instance
        :rtype: Logger
        """
        logger.remove()
        loggers = (
            logging.getLogger(name)
            for name in logging.root.manager.loggerDict
            if name.startswith('uvicorn') or name.startswith('huey')
        )
        for service_logger in loggers:
            service_logger.handlers = []

        # change handler for default logger

        intercept_handler = InterceptHandler()
        logging.getLogger().handlers = [intercept_handler]
        logging.getLogger('uvicorn.access').handlers = [intercept_handler]
        logging.basicConfig(handlers=[intercept_handler], level=0)

        # set logs output, level and format
        for handler in handlers:
            if not handler.get('format'):
                handler['format'] = cls.format_record

        logger.configure(handlers=handlers)
        return logger
