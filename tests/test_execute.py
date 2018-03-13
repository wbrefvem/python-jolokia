import pytest
import logging

from jolokia import JolokiaClient
from jolokia.exceptions import IllegalArgumentException
from tests.base import JolokiaTestCase
from mock import Mock

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestExecute(JolokiaTestCase):

    def test_valid_execute(self):

        if self.mock:
            resp = self._prepare_response(self.responses['valid_exec_response'], 200, True)
            self.jc.session.request = Mock(return_value=resp)
            resp_data = self.jc.execute(**self.requests['valid_exec'])
        else:
            resp_data = self.jc.execute(**self.requests['valid_exec'])
            LOGGER.debug(self.requests['valid_exec'])

        assert resp_data['status'] == 200
        assert isinstance(resp_data['value'], list)

    def test_empty_body(self):

        pytest.raises(IllegalArgumentException, self.jc.execute)

    def test_not_found(self):

        # Assuming there is no Jolokia agent at /foo
        self.jc = JolokiaClient('http://{0}:8080/foo'.format(self.jolokia_host))

        if self.mock:
            resp = self._prepare_response(self.responses['generic_404_page'], 404, False)
            LOGGER.debug(resp)
            self.jc.session.request = Mock(return_value=resp)
            resp_data = self.jc.execute(**self.requests['valid_exec'])
            LOGGER.debug(resp_data)
        else:
            resp_data = self.jc.execute(**self.requests['valid_exec'])

        assert resp_data.status_code == 404
