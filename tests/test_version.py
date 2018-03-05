import logging
import os

from tests.base import JolokiaTestCase
from jolokia.exceptions import MissingEnvironmentVariableException

LOGGER = logging.getLogger(__name__)


class TestVersion(JolokiaTestCase):

    def test_valid_version(self):

        resp_data = self.jc.version()
        LOGGER.debug(resp_data)
        value = resp_data['value']

        try:
            expected_agent_version = os.environ['JOLOKIA_AGENT_VERSION']
        except KeyError:
            raise MissingEnvironmentVariableException('JOLOKIA_AGENT_VERSION environment variable must be set.')

        try:
            expected_protocol_version = os.environ['JOLOKIA_PROTOCOL_VERSION']
        except KeyError:
            raise MissingEnvironmentVariableException('JOLOKIA_PROTOCOL_VERSION environment variable must be set.')

        assert value['agent'] == expected_agent_version
        assert value['protocol'] == expected_protocol_version
