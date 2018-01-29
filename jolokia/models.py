"""This module provides various models related to a Jolokia session"""

import logging

from requests import Session, Response

LOGGER = logging.getLogger(__name__)


class JolokiaResponse(Response):
    """Wraps requests.Response"""
    pass


class JolokiaSession(Session):
    """Wraps requests.Session"""

    def simple_post(self, url, data=None):
        """Posts to url and returns de-serialized response"""
        resp = self.post(url, json=data)

        LOGGER.debug(resp.json())

        return resp.json()
