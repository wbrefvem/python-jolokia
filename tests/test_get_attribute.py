from jolokia import JolokiaClient
from .fixtures.responses import mock_get_heap_memory_usage
import pytest
from unittest import TestCase


class TestGetAttribute(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGetAttribute, self).__init__(*args, **kwargs)

        self.jc = JolokiaClient('http://localhost:8080/jolokia')

    def test_valid_request(self):

        setattr(self.jc.session, 'request', mock_get_heap_memory_usage)

        resp_json = self.jc.get_attribute('java.lang:Memory', 'HeapMemoryUsage')

        print(resp_json)

        assert resp_json['status'] == 200
        assert type(resp_json['value']) is int

    def test_empty_request_body(self):

        pytest.raises(TypeError, self.jc.get_attribute)
