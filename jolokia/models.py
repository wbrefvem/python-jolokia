from requests import Session, Response


class JolokiaResponse(Response):
    pass


class JolokiaSession(Session):
    """Wraps requests.Session"""

    def post(self, url, data=None, *args, **kwargs):
        resp = super(JolokiaSession, self).post(url, data, *args, **kwargs)

        return resp.json()
