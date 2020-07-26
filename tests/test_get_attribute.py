from jolokia.exceptions import IllegalArgumentException
from tests.base import JolokiaTestCase
from mock import Mock
from requests import Response

import pytest
import logging

LOGGER = logging.getLogger(__name__)


class TestGetAttribute(JolokiaTestCase):

    def test_valid_request(self):

        if self.mock:
            resp = self._prepare_response(self.responses['valid_get_heap_memory_usage'], 200, True)
            self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.get_attribute(mbean='java.lang:type=Memory', attribute='HeapMemoryUsage', path='used')

        LOGGER.debug(resp_data)

        assert resp_data['status'] == 200
        assert type(resp_data['value']) is int

    def test_empty_request_body(self):

        pytest.raises(IllegalArgumentException, self.jc.get_attribute)

    def test_valid_bulk_request(self, *args, **kwargs):

        if self.mock:
            resp = self._prepare_response(self.responses['valid_bulk_read'], 200, True)
            self.jc.session.request = Mock(return_value=resp)

        attributes = ['HeapMemoryUsage', 'NonHeapMemoryUsage']
        resp_data = self.jc.get_attribute(mbean='java.lang:type=Memory', attribute=attributes)
        LOGGER.debug(resp_data)

        assert type(resp_data) is list
        assert len(resp_data) == 2

    def test_missing_mbean(self):

        kwargs = {'attribute': 'HeapMemoryUsage'}
        pytest.raises(IllegalArgumentException, self.jc.get_attribute, **kwargs)

    def test_missing_attribute(self):

        kwargs = {'mbean': 'java.lang:type=Memory'}
        pytest.raises(IllegalArgumentException, self.jc.get_attribute, **kwargs)
    
    def test_bulk_read_no_json_response(self):

        if self.mock:
            resp = self._prepare_response(self.responses['generic_404_page'], 404, False)
            self.jc.session.request = Mock(return_value=resp)
        
        attributes = ['HeapMemoryUsage', 'NonHeapMemoryUsage']
        resp_data = self.jc.get_attribute(mbean='java.lang:type=Memory', attribute=attributes)        
        
        assert type(resp_data) is Response
