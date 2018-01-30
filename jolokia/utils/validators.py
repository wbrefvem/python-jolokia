"""Utilities for validating data passed to Jolokia agent"""

import re

from jolokia.exceptions import UrlNotSpecifiedException, MalformedUrlException


def validate_url(url):
    """Ensures URL is well-formed"""
    if not url:
        raise UrlNotSpecifiedException()

    regex = re.compile(r'^https?://([\w\d]+\.)*[\w\d]+(:[\d]{2,})*(/+[\w\d]*)*$')
    if not regex.match(url):
        raise MalformedUrlException('Base url should be of the form \
        	http[s]://hostname[:port][path]')
