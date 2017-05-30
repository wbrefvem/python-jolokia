import pytest
import logging

from jolokia import JolokiaClient
from jolokia.exceptions import IllegalArgumentException
from .fixtures.responses import mock_get_heap_memory_usage, mock_bulk_request
from unittest import TestCase


logging.basicConfig(level=logging.DEBUG)


class TestGetAttribute(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGetAttribute, self).__init__(*args, **kwargs)

        self.jc = JolokiaClient('http://localhost:8080/jolokia')

    def test_valid_request(self):

        setattr(self.jc.session, 'request', mock_get_heap_memory_usage)

        resp_data = self.jc.get_attribute('java.lang:Memory', 'HeapMemoryUsage')

        assert resp_data['status'] == 200
        assert type(resp_data['value']) is int

    def test_empty_request_body(self):

        pytest.raises(IllegalArgumentException, self.jc.get_attribute)

    def test_valid_bulk_request(self, *args, **kwargs):
        log = logging.getLogger('TestGetAttribute.test_valid_bulk_request')

        setattr(self.jc.session, 'request', mock_bulk_request)

        attributes = ['HeapMemoryUsage', 'NonHeapMemoryUsage']

        resp_data = self.jc.get_attribute('java.lang:Memory', attributes)

        log.debug('Bulk resp. data: {0}'.format(resp_data))

        assert type(resp_data) is list
        assert len(resp_data) == 2

    def test_missing_mbean(self):

        kwargs = {'attribute': 'HeapMemoryUsage'}

        pytest.raises(IllegalArgumentException, self.jc.get_attribute, **kwargs)

    def test_missing_attribute(self):

        kwargs = {'mbean': 'java.lang:type=Memory'}

        pytest.raises(IllegalArgumentException, self.jc.get_attribute, **kwargs)
