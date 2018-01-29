"""Custom exceptions for for various modules in Jolokia Python client"""


class UrlNotSpecifiedException(Exception):
    """Indicates that Jolokia agent URL has not been provided"""
    pass


class MalformedUrlException(Exception):
    """Indicates that the Jolokia agent URL is malformed"""
    pass


class IllegalArgumentException(Exception):
    """Generic exception for enforcing required arguments"""
    pass
