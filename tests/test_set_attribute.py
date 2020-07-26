import pytest
import logging

from jolokia.exceptions import IllegalArgumentException
from tests.base import JolokiaTestCase
from mock import Mock
from requests import Response


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

        if self.mock:
            resp = self._prepare_response(self.responses['valid_write_classloading_response'], 200, True)
            self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.set_attribute(
            mbean='java.lang:type=ClassLoading',
            attr_value_pairs=('Verbose', True)
        )

        LOGGER.debug(resp_data)

        assert resp_data['status'] == 200
        assert not resp_data['value']

        if self.mock:
            resp = self._prepare_response(self.responses['valid_read_classloading_response_verbose'], 200, True)
            self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.get_attribute(
            mbean='java.lang:type=ClassLoading',
            attribute='Verbose'
        )

        assert resp_data['status'] == 200
        assert resp_data['value']

    def test_valid_bulk_write(self):

        if self.mock:
            resp = self._prepare_response(self.responses['valid_bulk_write'], 200, True)
            self.jc.session.request = Mock(return_value=resp)

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
    
    def test_no_json_response(self):

        if self.mock:
            resp = self._prepare_response(self.responses['generic_404_page'], 404, False)
            self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.set_attribute(
            mbean='java.lang:type=ClassLoading',
            attr_value_pairs=('Verbose', True)
        )

        assert type(resp_data) is Response
    
    def test_bulk_write_no_json_response(self):
        
        if self.mock:
            resp = self._prepare_response(self.responses['generic_404_page'], 404, False)
            self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.set_attribute(
            mbean='jolokia:type=Config',
            attr_value_pairs=[('HistoryMaxEntries', 20), ('MaxDebugEntries', 200)],
            bulk=True
        )

        assert type(resp_data) is Response
