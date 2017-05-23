import pytest
import logging

from jolokia import JolokiaClient
from unittest import TestCase


logging.basicConfig(level=logging.DEBUG)


class TestSetAttribute(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSetAttribute, self).__init__(*args, **kwargs)

        self.jc = JolokiaClient('http://localhost:8080/jolokia')

    def test_empty_body(self):

        pytest.raises(TypeError, self.jc.set_attribute)

    def test_valid_request(self):

        pass
