from jolokia import JolokiaClient
from .fixtures.responses import mock_get_heap_memory_usage, mock_bulk_request
import pytest
from unittest import TestCase


class TestGetAttribute(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGetAttribute, self).__init__(*args, **kwargs)

        self.jc = JolokiaClient('http://localhost:8080/jolokia')

    def test_valid_request(self):

        setattr(self.jc.session, 'request', mock_get_heap_memory_usage)

        resp_data = self.jc.get_attribute('java.lang:Memory', 'HeapMemoryUsage')

        print(resp_data)

        assert resp_data['status'] == 200
        assert type(resp_data['value']) is int

    def test_empty_request_body(self):

        pytest.raises(TypeError, self.jc.get_attribute)

    def test_valid_bulk_request(self, *args, **kwargs):

        setattr(self.jc.session, 'request', mock_bulk_request)

        attributes = ['HeapMemoryUsage', 'NonHeapMemoryUsage']

        resp_data = self.jc.get_attribute('java.lang:Memory', attributes)

        assert type(resp_data) is list
        assert len(resp_data) == 2
