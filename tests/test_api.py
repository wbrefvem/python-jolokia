from jolokia.api import JolokiaClient
from tests.base import JolokiaTestCase
from requests.exceptions import ConnectionError

import logging
import pytest

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class TestAPI(JolokiaTestCase):

    def test_unresolvable_agent(self):

        self.jc = JolokiaClient('http://trythelandcrab.com')

        kwargs = {'mbean': 'java.lang:Memory', 'attribute': 'HeapMemoryUsage'}
        pytest.raises(ConnectionError, self.jc.get_attribute, **kwargs)

    def test_missing_agent(self):

        self.jc = JolokiaClient('http://google.com')

        resp = self.jc.get_attribute(mbean='java.lang:Memory', attribute='HeapMemoryUsage')
        assert resp.status_code == 405
