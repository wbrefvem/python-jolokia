from jolokia import JolokiaClient
from .fixtures.responses import mock_empty_body


def test_empty_body():

    jc = JolokiaClient()

    setattr(jc.session, 'request', mock_empty_body)

    resp_json = jc.post('http://localhost:8080/jolokia', data={})

    assert resp_json['status'] == 400
    assert resp_json['error_type'] == "java.lang.IllegalArgumentException"


def test_valid_url():
    pass
