import logging

from tests.base import JolokiaTestCase
from mock import Mock

LOGGER = logging.getLogger(__name__)


class TestVersion(JolokiaTestCase):

    def test_valid_version(self):

        if self.mock:
            resp = self._prepare_response(self.responses['valid_version'], 200, True)
            self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.version()
        LOGGER.debug(resp_data)
        value = resp_data['value']

        assert value['agent'] == self.agent_version
        assert value['protocol'] == self.protocol_version
