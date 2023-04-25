"""
Script with all the necessary information for the library loggers.
You can use this script by importing it as follows::

    from library_name import _logging
    logger = _logging.get_logger(name)

"""
import functools
import logging
import time

LEVEL = logging.DEBUG
"""The general level of the loggers in the library."""

# Configure a formatter
FORMATTER: logging.Formatter = logging.Formatter("%(asctime)s: %(levelname)s [%(name)s:%(lineno)s]\n> %(message)s")
"""The generic formatter of the loggers."""

# Creating a Stream
STREAM_HANDLER: logging.Handler = logging.StreamHandler()
"""The generic handler in the library"""
STREAM_HANDLER.setFormatter(FORMATTER)

# The list of possibles handlers
HANDLERS: list[logging.Handler] = [STREAM_HANDLER]
"""The list of handlers handled by the library."""


def attach_handlers(logger: logging.Logger, handlers: list[logging.Handler] = None):
    """
    Add handlers from the handler list to the logger, if they are not already in the logger.
    If they are already in the logger, it does not add them.

    :param logger: The logger instance.
    :param handlers: The list of handlers. Default is the list of handlers managed.
    """
    # Set the default handlers
    if handlers is None:
        handlers = HANDLERS

    for handler in handlers:
        if handler not in logger.handlers:
            logger.addHandler(handler)


def get_logger(name: str, handlers: list[logging.Handler] = None, level=LEVEL) -> logging.Logger:
    """
    Gets the logger by its name. Additionally, attach the handlers and sets the level.

    :param name: The name of the logger
    :param handlers: A list of handlers to attach to the logger.
    :param level: The level of the logger
    :return: The logger with the associated name.
    """
    logger = logging.getLogger(name)
    attach_handlers(logger, handlers)
    logger.setLevel(level)
    return logger


def register_total_time(logger: logging.Logger):
    """Wrapper that records the total time it takes to execute a function, and shows it with the logger."""

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
