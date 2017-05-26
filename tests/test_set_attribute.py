import pytest
import logging

from jolokia import JolokiaClient
from unittest import TestCase
from .fixtures.responses import mock_valid_write, mock_missing_mbean


logging.basicConfig(level=logging.DEBUG)


class TestSetAttribute(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSetAttribute, self).__init__(*args, **kwargs)

        self.jc = JolokiaClient('http://localhost:8080/jolokia')

    def test_empty_body(self):

        pytest.raises(TypeError, self.jc.set_attribute)

    def test_missing_mbean(self):

        args = ['Verbose', True]

        pytest.raises(TypeError, self.jc.set_attribute, *args)

    def test_missing_attribute(self):
        pass

    def test_missing_value(self):
        pass

    def test_valid_request(self):

        setattr(self.jc.session, 'request', mock_valid_write)

        resp_data = self.jc.set_attribute('java.lang:type=ClassLoading', 'Verbose', True)

        assert not resp_data['value']
