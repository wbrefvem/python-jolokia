import pytest
import logging

from jolokia import JolokiaClient
from jolokia.exceptions import IllegalArgumentException
from tests.base import JolokiaTestCase
from mock import Mock


logging.basicConfig(level=logging.DEBUG)


class TestExecute(JolokiaTestCase):

    def test_valid_execute(self):

        resp = self._prepare_response(self.responses['valid_exec_response'], 200, True)
        self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.execute(**self.requests['valid_exec'])

        assert resp_data['status'] == 200
        assert isinstance(resp_data['value'], list)

    def test_empty_body(self):

        pytest.raises(IllegalArgumentException, self.jc.execute)

    def test_not_found(self):

        # Assuming there is no Jolokia agent at /foo
        self.jc = JolokiaClient('http://localhost:8080/foo')
        resp = self._prepare_response(self.responses['valid_exec_response'], 404, False)
        self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.execute(**self.requests['valid_exec'])

        assert resp_data.status_code == 404

    def test_illegal_argument_exception(self):

        # Assuming a Jolokia agent at /jolokia
        self.jc = JolokiaClient('http://localhost:8080/jolokia/foo')
        resp = self._prepare_response(self.responses['illegal_argument'], 400, False)
        self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.execute(**self.requests['valid_exec'])

        assert resp_data['status'] == 400
        assert resp_data['error_type'] == 'java.lang.IllegalArgumentException'


class TestSearch(JolokiaTestCase):

    def test_valid_search(self):

        resp = self._prepare_response(self.responses['valid_search_response'], 200, True)
        self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.search(**self.requests['valid_search'])

        assert resp_data['status'] == 200
        assert isinstance(resp_data['value'], list)
