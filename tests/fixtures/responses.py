from _pytest.monkeypatch import MonkeyPatch

ILLEGAL_ARGUMENT_RESPONSE = {
    'error_type': "java.lang.IllegalArgumentException",
    'error': "java.lang.IllegalArgumentException : No type with name 'foo' exists",
    'status': 400
}


monkeypatch = MonkeyPatch()


def mock_illegal_arg(self, *args, **kwargs):

    import json
    from requests import Response
    resp_json = json.dumps(ILLEGAL_ARGUMENT_RESPONSE)

    resp = Response()
    monkeypatch.setattr(Response, 'content', resp_json.encode('utf-8'))
    resp.status_code = 400
    monkeypatch.setattr(Response, 'ok', False)

    return resp.json()


def mock_root_ok(self, *args, **kwargs):

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
    monkeypatch.setattr(Response, 'content', resp_json.encode('utf-8'))
    resp.status_code = 200
    monkeypatch.setattr(Response, 'ok', True)

    return resp.json()
