"""Custom exceptions for for various modules in Jolokia Python client"""


class UrlNotSpecifiedException(Exception):
    """Indicates that Jolokia agent URL has not been provided"""


class MalformedUrlException(Exception):
    """Indicates that the Jolokia agent URL is malformed"""


class IllegalArgumentException(Exception):
    """Generic exception for enforcing required arguments"""


class MissingEnvironmentVariableException(Exception):
    """Should be thrown when expected environment variable is not found"""
