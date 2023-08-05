"""This module implements the safely API."""

import functools
from typing import Any, Callable, Optional, TypeVar, Union, overload

from safely.core import SafeResult


T = TypeVar("T", bound=Callable[..., Any])


@overload
def safely(f: T, /) -> Callable[..., SafeResult]:
    ...


@overload
def safely(
    *, logger: Optional[T] = None, message: str = ...
) -> Callable[[T], Callable[..., SafeResult]]:
    ...


def safely(
    f: Optional[T] = None,
    /,
    *,
    logger: Optional[T] = None,
    message: str = "{exc_type} raised: {exc_value}",
) -> Union[Callable[[T], Callable[..., SafeResult]], Callable[..., SafeResult]]:
    """Second-order decorator used to capture side effects from a function call.

    Args:
        f (T): The function to decorate. Defaults to None.
        logger (T): The logger to use to log the exception. Defaults to None.
        message (str): The message to log. Defaults to "{exc_type} raised: {exc_value}".

    Returns:
        A (nested) callable which returns a SafeResult object.
    """

    def decorator(f: T) -> Callable[..., SafeResult]:
        @functools.wraps(f)
        def inner(*args: Any, **kwargs: Any) -> SafeResult:
            try:
                result = f(*args, **kwargs)
                return SafeResult(result, None)
            except Exception as exc:
                if logger:
                    log_message = message.format(exc_type=type(exc).__name__, exc_value=exc)
                    logger(log_message)
                return SafeResult(None, exc)

        return inner

    return decorator if f is None else decorator(f)
