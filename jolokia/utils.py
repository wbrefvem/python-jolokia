from .exceptions import *
from functools import wraps
import re
import logging


logging.basicConfig(level=logging.DEBUG)


def validate_url(url):
    if not url:
        raise UrlNotSpecifiedException()

    regex = re.compile(r'^https?://([\w\d]+\.)*[\w\d]+(:[\d]{2,})*(/+[\w\d]*)*$')
    if not regex.match(url):
        raise MalformedUrlException('Base url should be of the form http[s]://hostname[:port][path]')


def require_args(reqs, err_msg):
    def wrapper(func):
        def new_func(self, *args, **kwargs):
            try:
                for arg in reqs:
                    kwargs[arg]
                return func(self, *args, **kwargs)
            except KeyError:
                raise IllegalArgumentException(err_msg)
        return new_func
    return wrapper
