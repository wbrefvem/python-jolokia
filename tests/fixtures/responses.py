ILLEGAL_ARGUMENT = {
    'error_type': "java.lang.IllegalArgumentException",
    'status': 400
}

ROOT_URL_OK = {
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
}

VALID_GET_HEAP_MEMORY_USAGE = {
    "request": {
        "path": "used",
        "mbean": "java.lang:type=Memory",
        "attribute": "HeapMemoryUsage",
        "type": "read"
    },
    "value": 321815952,
    "timestamp": 1494560184,
    "status": 200
}

VALID_BULK_READ = [
    {
        "request": {
            "path": "used",
            "mbean": "java.lang:type=Memory",
            "attribute": "HeapMemoryUsage",
            "type": "read"
        },
        "value": 75977776,
        "timestamp": 1495078549,
        "status": 200
    },
    {
        "request": {
            "path": "used",
            "mbean": "java.lang:type=Memory",
            "attribute": "NonHeapMemoryUsage",
            "type": "read"
        },
        "value": 80981104,
        "timestamp": 1495078549,
        "status": 200
    }
]

VALID_BULK_WRITE = [
    {
        "request": {
            "mbean": "jolokia:type=Config",
            "attribute": "HistoryMaxEntries",
            "type": "write",
            "value": 20
        },
        "value": 10,
        "timestamp": 1496203111,
        "status": 200
    },
    {
        "request": {
            "mbean": "jolokia:type=Config",
            "attribute": "MaxDebugEntries",
            "type": "write",
            "value": 200
        },
        "value": 100,
        "timestamp": 1496203111,
        "status": 200
    }
]

VALID_WRITE_CLASSLOADING_RESPONSE = {
    "request": {
        "mbean": "java.lang:type=ClassLoading",
        "attribute": "Verbose",
        "type": "write",
        "value": True
    },
    "value": False,
    "timestamp": 1495480324,
    "status": 200
}

MISSING_MBEAN_RESPONSE = {
    "error_type": "java.lang.IllegalArgumentException",
    "error": "java.lang.IllegalArgumentException : Objectname can not be null",
    "status": 400
}

VALID_EXEC_RESPONSE = {
    'status': 200,
    'request': {
        'operation': 'dumpAllThreads',
        'type': 'exec',
        'arguments': [True, True],
        'mbean': 'java.lang:type=Threading'
    },
    'value': ['', '', '']
}

VALID_SEARCH_RESPONSE = {
    "request": {
        "mbean": "java.lang:*",
        "type": "search"
    },
    "value": [
        "java.lang:name=Metaspace,type=MemoryPool",
        "java.lang:name=PS Old Gen,type=MemoryPool",
        "java.lang:name=PS Scavenge,type=GarbageCollector",
        "java.lang:name=PS Eden Space,type=MemoryPool",
        "java.lang:type=Runtime",
        "java.lang:type=Threading",
        "java.lang:type=OperatingSystem",
        "java.lang:name=Code Cache,type=MemoryPool",
        "java.lang:type=Compilation",
        "java.lang:name=CodeCacheManager,type=MemoryManager",
        "java.lang:name=Compressed Class Space,type=MemoryPool",
        "java.lang:type=Memory",
        "java.lang:name=PS Survivor Space,type=MemoryPool",
        "java.lang:type=ClassLoading",
        "java.lang:name=Metaspace Manager,type=MemoryManager",
        "java.lang:name=PS MarkSweep,type=GarbageCollector"
    ],
    "timestamp": 1500261449,
    "status": 200
}


def _mock_base(resp_data, status_code, ok, *args, **kwargs):

    import json
    from jolokia.models import JolokiaResponse
    resp_json = json.dumps(resp_data)

    resp = JolokiaResponse()
    setattr(JolokiaResponse, 'content', resp_json.encode('utf-8'))
    resp.status_code = status_code
    setattr(JolokiaResponse, 'ok', ok)

    return resp


def mock_request(self, url=None, method=None, data=None, *args, **kwargs):
    pass


# FIXME These need to be DRY
def mock_illegal_arg(self, *args, **kwargs):

    return _mock_base(ILLEGAL_ARGUMENT, 400, False)


def mock_root_ok(*args, **kwargs):

    return _mock_base(ROOT_URL_OK, 200, True)


def mock_empty_body(*args, **kwargs):

    return _mock_base(ILLEGAL_ARGUMENT, 400, False)


def mock_valid_body(*args, **kwargs):

    return _mock_base(VALID_GET_HEAP_MEMORY_USAGE, 200, True)


def mock_write_valid(*args, **kwargs):

    return _mock_base(VALID_WRITE_CLASSLOADING_RESPONSE, 200, True)


def mock_get_heap_memory_usage(*args, **kwargs):

    return _mock_base(VALID_GET_HEAP_MEMORY_USAGE, 200, True)


def mock_bulk_read(*args, **kwargs):

    return _mock_base(VALID_BULK_READ, 200, True)


def mock_bulk_write(*args, **kwargs):

    return _mock_base(VALID_BULK_WRITE, 200, True)


def mock_valid_write(*args, **kwargs):

    return _mock_base(VALID_WRITE_CLASSLOADING_RESPONSE, 200, True)


def mock_missing_mbean(*args, **kwargs):

    return _mock_base(MISSING_MBEAN_RESPONSE, 400, False)


def mock_valid_exec(*args, **Kwargs):

    return _mock_base(VALID_EXEC_RESPONSE, 200, True)
