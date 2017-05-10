from requests import Session

from jolokia.api import JolokiaClient

from .fixtures.responses import mock_illegal_arg, mock_root_ok


def test_malformed_url(monkeypatch):

    monkeypatch.setattr(Session, 'request', mock_illegal_arg)

    jc = JolokiaClient()

    resp_json = jc.get('http://localhost:8080/jolokia/foo')

    assert resp_json['status'] == 400
    assert resp_json['error'] == "java.lang.IllegalArgumentException : No type with name 'foo' exists"


def test_well_formed_url(monkeypatch):

    monkeypatch.setattr(Session, 'request', mock_root_ok)

    jc = JolokiaClient()

    resp_json = jc.get('http://localhost:8080/jolokia')

    assert resp_json['status'] == 200
    assert resp_json['value']['info']['product'] == 'JBoss EAP'
