from functools import wraps
from jolokia.exceptions import *

import logging


logging.basicConfig(level=logging.DEBUG)


def require_args(reqs, err_msg):
    def wrapper(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            try:
                for arg in reqs:
                    kwargs[arg]
                return func(*args, **kwargs)
            except KeyError:
                raise IllegalArgumentException(err_msg)
        return new_func
    return wrapper
