"""This module provides various models related to a Jolokia session"""

import logging

from requests import Session, Response, Request

LOGGER = logging.getLogger(__name__)


class JolokiaResponse(Response):
    """Wraps requests.Response"""
    pass


class JolokiaRequest(Request):
    """Wraps requests.Request"""
    pass


class JolokiaSession(Session):
    """Wraps requests.Session"""

    def __init__(self, username=None, password=None):
        """Initialize the session with http authentication if provided"""

        super().__init__()

        if username and password:
            self.auth = (username, password)

    def simple_post(self, url, data=None):
        """Posts to url and returns de-serialized response"""
        try:
            resp = self.post(url, json=data)
            LOGGER.debug(resp)
            return resp
        except Exception as error:
            raise error
        finally:
            LOGGER.debug(data)
