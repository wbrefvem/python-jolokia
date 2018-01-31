import pytest
import logging

from jolokia.exceptions import IllegalArgumentException
from tests.base import JolokiaTestCase
from mock import Mock


logging.basicConfig(level=logging.DEBUG)


class TestSetAttribute(JolokiaTestCase):

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

        resp = self._prepare_response(self.responses['valid_write_classloading_response'], 200, True)
        self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.set_attribute(
            mbean='java.lang:type=ClassLoading',
            attribute='Verbose',
            value=True
        )

        assert resp_data['value']

    def test_bulk_write(self):

        attr_map = {
            'HistoryMaxEntries': 20,
            'MaxDebugEntries': 200
        }

        resp = self._prepare_response(self.responses['valid_bulk_write'], 200, True)
        self.jc.session.request = Mock(return_value=resp)

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
