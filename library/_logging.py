"""
Script with all the necessary information for the library loggers.
You can use this script by importing it as follows::

    from library_name import _logging
    logger = _logging.get_logger(name)

And change the level of any logger with

    from library_name import _logging
    _logging.set_level(_logging.DEBUG, name="name of the logger")

If you want to change the level of every logger, omit the name.
"""
import functools
import logging
import time
from threading import Lock


# The levels of the severity as in the package 'logging'
CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


# Configure a formatter
FORMATTER: logging.Formatter = logging.Formatter(
    "%(asctime)s: %(levelname)s [%(name)s:%(lineno)s]\n> %(message)s"
)
"""The generic formatter of the loggers."""

# Generic Handler of the package
STREAM_HANDLER: logging.Handler = logging.StreamHandler()
"""The generic handler in the library"""
STREAM_HANDLER.setFormatter(FORMATTER)


class _SingletonMeta(type):
    """Metaclass to implements Singleton Pattern. Obtained from
    https://refactoring.guru/design-patterns/singleton/python/example#example-1 """
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class LoggerConfiguration(metaclass=_SingletonMeta):
    """A singleton that manages the configuration of the loggers in the library."""

    LEVEL: int = WARNING
    """The general level of the loggers in the library."""

    HANDLERS: list[logging.Handler] = [STREAM_HANDLER]
    """The list of handlers handled by the library."""

    loggers: dict[str, logging.Logger] = dict()
    """The loggers instances of the package"""

    def attach_handlers(self, logger: logging.Logger, handlers: list[logging.Handler] = None):
        """
        Add handlers from the handler list to the logger, if they are not already in the logger.
        If they are already in the logger, it does not add them.

        :param logger: The logger instance.
        :param handlers: The list of handlers. Default is the list of handlers managed.
        """
        # Set the default handlers
        if handlers is None:
            handlers = self.HANDLERS

        for handler in handlers:
            if handler not in logger.handlers:
                logger.addHandler(handler)

    def get_logger(self,
                   name: str,
                   level: int = LEVEL,
                   handlers: list[logging.Handler] = None) -> logging.Logger:
        """
        Gets the logger by its name. Additionally, attach the handlers and sets the level.

        :param name: The name of the logger
        :param handlers: A list of handlers to attach to the logger.
        :param level: The level of the logger
        :return: The logger with the associated name.
        """
        if name in self.loggers:
            logger = self.loggers[name]
        else:
            logger = logging.getLogger(name)
        self.loggers[name] = logger
        self.attach_handlers(logger, handlers)
        logger.setLevel(level)The name must correspond to a logger with that name. There is currently no logger with this name.
        return logger

    def set_level(self, level: int, name: str = None):
        r"""
        Set the level of severity of the loggers in the library. You can specify the logger name
        to change the level to a single logger.

        :param level: The level of severity. See
            `levels <https://docs.python.org/es/3/library/logging.html#levels>` from the logging
            package for further information.
        :param name: The name of the logger to change the level. If it is None (default),
            change the severity of every logger in the package.
        """
        if name in self.loggers:
            self.loggers[name].setLevel(level)
            return None
        # If name not in loggers, AND it is not a None value...
        elif name is not None:
            raise ValueError(
                "The name must correspond to a logger with that name. There is currently no "
                "logger with this name."
            )
        # Otherwise, iterate over every logger
        for logger in self.loggers.values():
            logger.setLevel(level)


# Create the (single) instance of LoggerConfiguration
log_config = LoggerConfiguration()


# Alias of the methods in the instance of LoggerConfiguration
def get_logger(name: str,
               level: int = log_config.LEVEL,
               handlers: list[logging.Handler] = None) -> logging.Logger:
    return log_config.get_logger(name, handlers, level)


def set_level(level: int, name: str = None): log_config.set_level(level, name)


get_logger.__doc__ = LoggerConfiguration.get_logger.__doc__
set_level.__doc__ = LoggerConfiguration.set_level.__doc__


def register_total_time(logger: logging.Logger):
    """Wrapper that records the total time it takes to execute a function, and shows it with the
    logger."""

    def decorator_register_total_time(func):
        @functools.wraps(func)
        def timeit_wrapper(*args, **kwargs):
            tic = time.perf_counter()
            result = func(*args, **kwargs)
            toc = time.perf_counter()
            logger.debug(f"The function '{func.__name__}' takes {toc - tic:.4f} [seg]")
            return result

        return timeit_wrapper

    return decorator_register_total_time
