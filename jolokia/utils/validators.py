"""Utilities for validating data passed to Jolokia agent"""

import re

from jolokia.exceptions import UrlNotSpecifiedException, MalformedUrlException


def verify_url(url):
    """Ensures URL is well-formed. Does not verify that domain is ICANN-compliant"""
    if not url:
        raise UrlNotSpecifiedException()

    regex = re.compile(r'^https?://([\S]+\.)*[\S]+(:[\d]{2,})*(/+[\S+]*)*$')
    if not regex.match(url):
        raise MalformedUrlException('Base url should be of the form http[s]://hostname[:port][path]')

    # For testing purposes
    return True
