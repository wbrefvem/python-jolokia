from requests import Session, Response


class JolokiaResponse(Response):
    pass


class JolokiaSession(Session):
    """Wraps requests.Session"""

    def simple_post(self, url, data=None):

        resp = self.post(url, json=data)

        return resp.json()
