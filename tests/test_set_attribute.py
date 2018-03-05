import pytest
import logging

from jolokia.exceptions import IllegalArgumentException
from tests.base import JolokiaTestCase


LOGGER = logging.getLogger(__name__)


class TestSetAttribute(JolokiaTestCase):

    def test_empty_body(self):

        pytest.raises(IllegalArgumentException, self.jc.set_attribute)

    def test_missing_mbean(self):

        args = ['Verbose', True]
        pytest.raises(IllegalArgumentException, self.jc.set_attribute, *args)

    def test_missing_attribute(self):

        kwargs = {'mbean': 'java.lang:type=ClassLoading', 'value': True, 'attribute': 'Verbose'}
        pytest.raises(IllegalArgumentException, self.jc.set_attribute, **kwargs)

    def test_valid_request(self):

        resp_data = self.jc.set_attribute(
            mbean='java.lang:type=ClassLoading',
            attr_value_pairs=('Verbose', True)
        )

        assert resp_data['value']

    def test_valid_bulk_write(self):

        resp_data = self.jc.set_attribute(
            mbean='jolokia:type=Config',
            attr_value_pairs=[('HistoryMaxEntries', 20), ('MaxDebugEntries', 200)],
            bulk=True
        )

        for obj in resp_data:
            assert obj['status'] == 200

    def test_bulk_no_list(self):

        with pytest.raises(IllegalArgumentException):

            kwargs = {'mbean': 'java.lang:Memory', 'bulk': True, 'attr_value_pairs': ('', '')}
            self.jc.set_attribute(**kwargs)

    def test_bulk_malformed_tuple(self):

        with pytest.raises(IllegalArgumentException):

            kwargs = {'mbean': 'java.lang:Memory', 'bulk': True, 'attr_value_pairs': [('', '', ''), ('', '', '')]}
            self.jc.set_attribute(**kwargs)
