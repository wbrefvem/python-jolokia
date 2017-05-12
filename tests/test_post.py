from jolokia import JolokiaClient
from .fixtures.responses import mock_empty_body, mock_valid_body

VALID_POST_DATA = {
    "type": "read",
    "mbean": "java.lang:type=Memory",
    "attribute": "HeapMemoryUsage",
    "path": "used",
}

URL = 'http://localhost:8080/jolokia'


def _test_post(function=None, data=None, url=None, *args, **kwargs):

    jc = JolokiaClient()

    setattr(jc.session, 'request', function)

    return jc.post(url, data=data)


def test_empty_body():

    resp_json = _test_post(function=mock_empty_body, data={}, url=URL)

    assert resp_json['status'] == 400
    assert resp_json['error_type'] == "java.lang.IllegalArgumentException"


def test_valid_body():

    resp_json = _test_post(function=mock_valid_body, data=VALID_POST_DATA, url=URL)

    assert resp_json['status'] == 200
    assert resp_json['value'] == 321815952
