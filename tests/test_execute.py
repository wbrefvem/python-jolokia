import pytest
import logging

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
        assert type(resp_data['value']) is list

    def test_empty_body(self):

        pytest.raises(IllegalArgumentException, self.jc.execute)


class TestSearch(JolokiaTestCase):

    def test_valid_search(self):

        resp = self._prepare_response(self.responses['valid_search_response'], 200, True)
        self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.search(**self.requests['valid_search'])

        assert resp_data['status'] == 200
        assert type(resp_data['value']) is list
