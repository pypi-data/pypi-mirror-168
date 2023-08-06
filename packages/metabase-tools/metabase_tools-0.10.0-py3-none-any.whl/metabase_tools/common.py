"""Module for common tools used throughout the project
"""

import logging
from functools import wraps
from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def log_details(logger: logging.Logger, func: F, *args: Any, **kwargs: Any) -> F:
    """Logs details of a function call

    Args:
        logger (logging.Logger)
        func (F)

    Returns:
        F
    """
    logger = logging.getLogger(func.__module__)
    logger.debug(
        "%s called\n\targs: %s\n\tkwargs: %s",
        func.__name__,
        "\n\t\t".join([str(s) for s in args]),
        "\n\t\t".join(
            [f"{key}: {value}" for key, value in kwargs.items()],
        ),
    )
    return_ = func(*args, **kwargs)
    logger.debug("Returning: %s", return_)
    return cast(F, return_)


def log_call(func: F) -> F:
    """Used to log calls to the function provided"""

    @wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore
        logger = logging.getLogger(func.__module__)
        return log_details(logger, func, *args, **kwargs)

    return cast(F, wrapper)


def untested(func: F) -> F:
    """Used to log a warning that the decorated function has not been tested"""

    @wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore
        logger = logging.getLogger(func.__module__)
        logger.warning("Calling untested function: %s", func.__name__)
        return log_details(logger, func, *args, **kwargs)

    return cast(F, wrapper)
