from requests import Session

from jolokia.api import JolokiaClient


# FIXME Needs to be more DRY
def test_malformed_url(monkeypatch):

    # FIXME Refactor to read response data from .json file.
    def mock_jolokia_response(self, *args, **kwargs):

        import json
        from requests import Response
        resp_json = json.dumps({
            'error_type': "java.lang.IllegalArgumentException",
            'error': "java.lang.IllegalArgumentException : No type with name 'foo' exists",
            'status': 400
        })

        resp = Response()
        monkeypatch.setattr(Response, 'content', bytes(resp_json, 'utf-8'))
        resp.status_code = 400
        monkeypatch.setattr(Response, 'ok', False)

        return resp.json()

    monkeypatch.setattr(Session, 'request', mock_jolokia_response)

    jc = JolokiaClient()

    resp_json = jc.get('http://localhost:8080/jolokia/foo')

    assert resp_json['status'] == 400
    assert resp_json['error'] == "java.lang.IllegalArgumentException : No type with name 'foo' exists"


def test_well_formed_url(monkeypatch):

    # FIXME Refactor to read response data from .json file.
    def mock_jolokia_response(self, *args, **kwargs):

        import json
        from requests import Response
        resp_json = json.dumps({
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

        resp = Response()
        monkeypatch.setattr(Response, 'content', bytes(resp_json, 'utf-8'))
        resp.status_code = 200
        monkeypatch.setattr(Response, 'ok', True)

        return resp.json()

    monkeypatch.setattr(Session, 'request', mock_jolokia_response)

    jc = JolokiaClient()

    resp_json = jc.get('http://localhost:8080/jolokia')

    assert resp_json['status'] == 200
    assert resp_json['value']['info']['product'] == 'JBoss EAP'
