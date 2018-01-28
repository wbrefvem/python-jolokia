import pytest
import logging

from jolokia import JolokiaClient
from jolokia.exceptions import IllegalArgumentException
from unittest import TestCase
from .fixtures.responses import mock_valid_write, mock_bulk_write


logging.basicConfig(level=logging.DEBUG)


class TestSetAttribute(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSetAttribute, self).__init__(*args, **kwargs)

        self.jc = JolokiaClient('http://localhost:8080/jolokia')

    def test_empty_body(self):

        pytest.raises(IllegalArgumentException, self.jc.set_attribute)

    def test_missing_mbean(self):

        args = ['Verbose', True]

        pytest.raises(IllegalArgumentException, self.jc.set_attribute, *args)

    def test_missing_attribute(self):

        kwargs = {'mbean': 'java.lang:type=ClassLoading', 'value': True}

        pytest.raises(IllegalArgumentException, self.jc.set_attribute, **kwargs)

    def test_missing_value(self):

        kwargs = {'mbean': 'java.lang:type=ClassLoading', 'attribute': 'Verbose'}

        pytest.raises(IllegalArgumentException, self.jc.set_attribute, **kwargs)

    def test_valid_request(self):

        setattr(self.jc.session, 'request', mock_valid_write)

        resp_data = self.jc.set_attribute(
            mbean='java.lang:type=ClassLoading', 
            attribute='Verbose', 
            value=True
        )

        assert not resp_data['value']

    def test_bulk_write(self):

        attr_map = {
            'HistoryMaxEntries': 20,
            'MaxDebugEntries': 200
        }

        setattr(self.jc.session, 'request', mock_bulk_write)

        resp_data = self.jc.set_attribute(
            mbean='jolokia:type=Config',
            attribute=['HistoryMaxEntries', 'MaxDebugEntries'],
            value=attr_map
        )

        for obj in resp_data:
            assert obj['status'] == 200

    def test_incorrect_attribute_type(self):

        kwargs = {
            'value': {
                'foo': 1,
                'bar': 2
            },
            'attribute': 'baz',
            'mbean': 'bang'
        }

        pytest.raises(IllegalArgumentException, self.jc.set_attribute, **kwargs)
