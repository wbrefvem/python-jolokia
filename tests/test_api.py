from jolokia.api import JolokiaClient
from tests.base import JolokiaTestCase
from requests.exceptions import ConnectionError

import logging
import pytest


LOGGER = logging.getLogger(__name__)


class TestAPI(JolokiaTestCase):

    def test_unresolvable_agent(self):

        self.jc = JolokiaClient('http://trythelandcrab.com')

        kwargs = {'mbean': 'java.lang:Memory', 'attribute': 'HeapMemoryUsage'}
        pytest.raises(ConnectionError, self.jc.get_attribute, **kwargs)

    def test_missing_agent(self):

        if self.mock:
            resp = self._prepare_response(self.responses['generic_404_page'], 404, False)
            LOGGER.debug(resp)
            self.jc.session.request = Mock(return_value=resp)
            resp_data = self.jc.execute(**self.requests['valid_exec'])
            LOGGER.debug(resp_data)
        else:
            resp_data = self.jc.execute(**self.requests['valid_exec'])
        self.jc = JolokiaClient('http://google.com')
        kwargs = {'mbean': 'java.lang:Memory', 'attribute': 'HeapMemoryUsage'}
        resp = self.jc.get_attribute(**kwargs)

        assert resp.status_code != 200
