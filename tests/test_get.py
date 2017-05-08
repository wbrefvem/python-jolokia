import pytest
import json
from requests import Session

from jolokia.api import JolokiaClient


# @pytest.fixture(autouse=True)
# def no_requests(monkeypatch):
#     monkeypatch.delattr("requests.Session.request")


def test_malformed_url(monkeypatch):

    def mock_jolokia_response(url):

        return json.dumps({
            'error_type': "java.lang.IllegalArgumentException",
            'error': "java.lang.IllegalArgumentException : No type with name 'foo' exists",
            'status': 400
        })

    monkeypatch.setattr(Session, 'request', mock_jolokia_response)

    jc = JolokiaClient('http://localhost:8080/jolokia/foo')

    resp_json = jc.get().json()

    assert resp_json['status'] == 400
    assert resp_json['error'] == "java.lang.IllegalArgumentException : No type with name 'foo' exists"


def test_well_formed_url(monkeypatch):

    # FIXME Refactor to read response data from .json file
    def mock_jolokia_response(url):

        return json.dumps({
            "request": {
                "type": "version"
            },
            "value": {
                "agent": "1.3.6",
                "protocol": "7.2",
                "config": {
                    "maxCollectionSize": "0",
                    "agentId": "10.195.20.189-18288-6b59e8eb-servlet",
                    "debug": "false",
                    "agentType": "servlet",
                    "serializeException": "false",
                    "detectorOptions": "{}",
                    "dispatcherClasses": "org.jolokia.jsr160.Jsr160RequestDispatcher",
                    "maxDepth": "15",
                    "discoveryEnabled": "false",
                    "canonicalNaming": "true",
                    "historyMaxEntries": "10",
                    "includeStackTrace": "true",
                    "maxObjects": "0",
                    "debugMaxEntries": "100"
                },
                "info": {
                    "product": "JBoss EAP",
                    "vendor": "RedHat",
                    "version": "7.0.0.GA"
                }
            },
            "timestamp": 1494275547,
            "status": 200
        })

    monkeypatch.setattr(Session, 'request', mock_jolokia_response)

    jc = JolokiaClient('http://localhost:8080/jolokia')

    resp_json = jc.get().json()

    assert resp_json['status'] == 200
    assert resp_json['value']['info']['product'] == 'JBoss EAP'
