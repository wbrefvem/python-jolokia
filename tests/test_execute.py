import pytest
import logging
import json

from jolokia.exceptions import IllegalArgumentException
from jolokia.models import JolokiaResponse
from tests.base import JolokiaTestCase
from .fixtures.responses import *
from .fixtures.requests import *
from mock import Mock


logging.basicConfig(level=logging.DEBUG)


class TestExecute(JolokiaTestCase):

    def test_valid_execute(self):

        resp = self._prepare_response(VALID_EXEC_RESPONSE, 200, True)
        self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.execute(**VALID_EXEC)

        assert resp_data['status'] == 200
        assert type(resp_data['value']) is list

    def test_empty_body(self):

        pytest.raises(IllegalArgumentException, self.jc.execute)


class TestSearch(JolokiaTestCase):

    def test_valid_search(self):

        resp = self._prepare_response(VALID_SEARCH_RESPONSE, 200, True)
        self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.search(**VALID_SEARCH)

        assert resp_data['status'] == 200
        assert type(resp_data['value']) is list
