from requests import Session, Response
import logging


logging.basicConfig(level=logging.DEBUG)


class JolokiaResponse(Response):
    pass


class JolokiaSession(Session):
    """Wraps requests.Session"""

    def simple_post(self, url, data=None):
        """Posts to url and returns de-serialized response"""
        log = logging.getLogger('JolokiaSession.simple_post')
        resp = self.post(url, json=data)

        #log.debug(resp.json())

        return resp.json()
