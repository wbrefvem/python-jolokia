import pytest
import logging
import json

from jolokia import JolokiaClient
from jolokia.exceptions import IllegalArgumentException
from jolokia.models import JolokiaResponse
from .fixtures.responses import mock_valid_exec, VALID_SEARCH_RESPONSE
from .fixtures.requests import *
from unittest import TestCase
from mock import Mock


logging.basicConfig(level=logging.DEBUG)


class TestExecute(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestExecute, self).__init__(*args, **kwargs)

        self.jc = JolokiaClient('http://localhost:8080/jolokia')

    def test_valid_execute(self):
        setattr(self.jc.session, 'request', mock_valid_exec)

        resp_data = self.jc.execute(**VALID_EXEC)

        assert resp_data['status'] == 200
        assert type(resp_data['value']) is list

    def test_empty_body(self):

        pytest.raises(IllegalArgumentException, self.jc.execute)


class TestSearch(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSearch, self).__init__(*args, **kwargs)

        self.jc = JolokiaClient('http://localhost:8080/jolokia')

    def test_valid_search(self):

        resp_json = json.dumps(VALID_SEARCH_RESPONSE)
        resp = JolokiaResponse()
        setattr(JolokiaResponse, 'content', resp_json.encode('utf-8'))
        resp.status_code = 200
        setattr(JolokiaResponse, 'ok', True)
        mock = Mock(return_value=resp)
        mock.__name__ = 'test_valid_search'

        setattr(self.jc.session, 'request', mock)

        resp_data = self.jc.search(**VALID_SEARCH)

        assert resp_data['status'] == 200
        assert type(resp_data['value']) is list
