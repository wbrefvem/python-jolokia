"""Decorators for Jolokia API functions"""

import logging

from functools import wraps
from jolokia.exceptions import IllegalArgumentException

LOGGER = logging.getLogger(__name__)


def require_params(reqs, err_msg):
    """Enforces required parameters for a function"""
    def _wrapper(func):
        @wraps(func)
        def _new_func(*args, **kwargs):
            try:
                for arg in reqs:
                    argument = kwargs[arg]
                    LOGGER.debug(argument)
                return func(*args, **kwargs)
            except KeyError as e:
                raise IllegalArgumentException(err_msg) from e
        return _new_func
    return _wrapper
