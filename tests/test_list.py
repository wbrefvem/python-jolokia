import pytest
import logging

from jolokia import JolokiaClient
from jolokia.exceptions import IllegalArgumentException
from unittest import TestCase
from .fixtures.responses import mock_valid_list, mock_invalid_path

logging.basicConfig(level=logging.DEBUG)


class TestList(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestList, self).__init__(*args, **kwargs)
        self.jc = JolokiaClient('http://localhost:8080/jolokia')

    def test_valid_request(self):
        setattr(self.jc.session, 'request', mock_valid_list)

        resp_data = self.jc.list(path='java.lang/type=Memory/attr/HeapMemoryUsage')

        assert type(resp_data) is dict
        assert resp_data['status'] == 200
        assert type(resp_data['value']) is dict

    def test_invalid_path(self):
        setattr(self.jc.session, 'request', mock_invalid_path)

        resp_data = self.jc.list(path='java.lang/type=Memory/HeapMemoryUsage')

        assert type(resp_data) is dict
        assert resp_data['status'] == 400
        assert resp_data['error_type'] == 'java.lang.IllegalArgumentException'
