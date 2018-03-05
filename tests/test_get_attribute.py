from jolokia.exceptions import IllegalArgumentException
from tests.base import JolokiaTestCase

import pytest
import logging

LOGGER = logging.getLogger(__name__)


class TestGetAttribute(JolokiaTestCase):

    def test_valid_request(self):

        resp_data = self.jc.get_attribute(mbean='java.lang:type=Memory', attribute='HeapMemoryUsage', path='used')

        LOGGER.debug(resp_data)

        assert resp_data['status'] == 200
        assert type(resp_data['value']) is int

    def test_empty_request_body(self):

        pytest.raises(IllegalArgumentException, self.jc.get_attribute)

    def test_valid_bulk_request(self, *args, **kwargs):

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
