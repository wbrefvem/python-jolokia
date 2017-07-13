from jolokia.exceptions import *
import re


def validate_url(url):
    if not url:
        raise UrlNotSpecifiedException()

    regex = re.compile(r'^https?://([\w\d]+\.)*[\w\d]+(:[\d]{2,})*(/+[\w\d]*)*$')
    if not regex.match(url):
        raise MalformedUrlException('Base url should be of the form http[s]://hostname[:port][path]')
