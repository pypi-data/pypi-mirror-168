"""Decorators module."""
from functools import wraps
from time import time

from loguru import logger

from ..bootstrap import _CLI


DEFAULTS = _CLI().get_config()
logger.add(DEFAULTS.logfile, format="{time} | {level} | {message}")


def given(fn):
    """Set a function as a given precondition."""

    def _(instance, *args, **kwargs):
        fn(instance, *args, **kwargs)
        return instance
    setattr(_, "__name__", fn.__name__)
    return _


def then(fn):
    """Set a function as a then action."""

    def _(instance, *args, **kwargs):
        msg = (
            f"{instance.method.upper()} {DEFAULTS.base_url}{instance.endpoint}"
        )
        try:
            fn(instance, *args, **kwargs)
            logger.success(f"PASSED {msg} {fn.__name__}")
            return instance
        except AssertionError as err:
            logger.error(f"FAILED: {msg} {fn.__name__} {err}")
            raise err
    setattr(_, "__name__", fn.__name__)
    return _


def when(fn):
    """Set a function as a when assertion."""

    def _(instance, *args, **kwargs):
        fn(instance, *args, **kwargs)
        return instance
    setattr(_, "__name__", fn.__name__)
    return _


def log_test(fn):
    """Add a simple log message when a test starts."""
    def _(*args, **kwargs):
        logger.info(f"{fn.__name__} started")
        fn(*args, **kwargs)
    setattr(_, "__name__", fn.__name__)
    return _


def weight(value: int):
    """Add a function a weight attr."""
    def attr_decorator(fn):
        @wraps(fn)
        def _(*args, **kwargs):
            return fn(*args, **kwargs)

        setattr(_, "weight", value)
        return _

    return attr_decorator


def timeit(fn):
    """Add a simple temporizer to function."""
    def _(*args, **kwargs):
        starting = time()
        request = fn(*args, **kwargs)
        elapsed = time() - starting
        logger.info(f"ELAPSED TIME: {elapsed}")
        return request
    setattr(_, "__name__", fn.__name__)
    return _
