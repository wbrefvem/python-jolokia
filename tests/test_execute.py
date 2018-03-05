import pytest
import logging

from jolokia import JolokiaClient
from jolokia.exceptions import IllegalArgumentException
from tests.base import JolokiaTestCase

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestExecute(JolokiaTestCase):

    def test_valid_execute(self):

        resp_data = self.jc.execute(**self.requests['valid_exec'])
        LOGGER.debug(self.requests['valid_exec'])
        assert resp_data['status'] == 200
        assert isinstance(resp_data['value'], list)

    def test_empty_body(self):

        pytest.raises(IllegalArgumentException, self.jc.execute)

    def test_not_found(self):

        # Assuming there is no Jolokia agent at /foo
        self.jc = JolokiaClient('http://{0}:8080/foo'.format(self.jolokia_host))
        resp_data = self.jc.execute(**self.requests['valid_exec'])

        assert resp_data.status_code == 404

    def test_illegal_argument_exception(self):

        # Assuming a Jolokia agent at /jolokia
        self.jc = JolokiaClient('http://{0}:8080/jolokia/foo'.format(self.jolokia_host))
        resp_data = self.jc.execute(**self.requests['valid_exec'])

        assert resp_data['status'] == 400
        assert resp_data['error_type'] == 'java.lang.IllegalArgumentException'


class TestSearch(JolokiaTestCase):

    def test_valid_search(self):

        resp_data = self.jc.search(**self.requests['valid_search'])

        assert resp_data['status'] == 200
        assert isinstance(resp_data['value'], list)
