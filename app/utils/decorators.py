from collections.abc import Callable
from time import sleep
from typing import Any

from app.utils.logger import logger


def retry(
    max_retries: int = 3,
    sleep_time: int | float = 0,
    raises_on_exception: bool = True,
    non_retry_exceptions: tuple[type[Exception], ...] = (),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to retry a function call on exception.

    Args:
        max_retries (int): Maximum number of retries before giving up.
        sleep_time (int | float): Time to sleep between retries.
        raises_on_exception (bool): If True, re-raises the exception after max retries.
        non_retry_exceptions (tuple[type[Exception], ...]): Exceptions that should not trigger a retry.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]: Decorated function that retries on exception.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs):  # noqa: ANN202, ANN002, ANN003
            for i in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if i == max_retries - 1 or (
                        non_retry_exceptions and isinstance(e, non_retry_exceptions)
                    ):
                        if raises_on_exception:
                            raise e
                        else:
                            logger.exception(e)
                    if sleep_time:
                        sleep(sleep_time)

        return wrapper

    return decorator



