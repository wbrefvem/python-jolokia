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

    def test_valid_request(self):

        resp = self._prepare_response(self.responses['valid_write_classloading_response'], 200, True)
        self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.set_attribute(
            mbean='java.lang:type=ClassLoading',
            attr_value_pairs=('Verbose', True)
        )

        assert resp_data['value']

    def test_bulk_write(self):

        resp = self._prepare_response(self.responses['valid_bulk_write'], 200, True)
        self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.set_attribute(
            mbean='jolokia:type=Config',
            attr_value_pairs=[('HistoryMaxEntries', 20), ('MaxDebugEntries', 200)],
            bulk=True
        )

        for obj in resp_data:
            assert obj['status'] == 200

    def test_invalid_bulk_write(self):

        kwargs = {'bulk': True, 'attr_value_pairs': ('', '')}

        pytest.raises(IllegalArgumentException, self.jc.set_attribute, **kwargs)
