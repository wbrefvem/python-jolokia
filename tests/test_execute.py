import pytest
import logging

from jolokia import JolokiaClient
from jolokia.exceptions import IllegalArgumentException
from .fixtures.responses import mock_valid_exec
from .fixtures.requests import *
from unittest import TestCase


logging.basicConfig(level=logging.DEBUG)


class TestExecute(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestExecute, self).__init__(*args, **kwargs)

        self.jc = JolokiaClient('http://localhost:8080/jolokia')

    def test_valid_execute(self):
        setattr(self.jc.session, 'request', mock_valid_exec)

        resp_data = self.jc.execute(data=VALID_EXEC)

        assert resp_data['status'] == 200
        assert type(resp_data['value']) is list

    def test_empty_body(self):

        pytest.raises(IllegalArgumentException, self.jc.execute)
