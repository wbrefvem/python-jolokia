from unittest import TestCase
from jolokia import JolokiaClient
from jolokia.models import JolokiaResponse
from jolokia.exceptions import MissingEnvironmentVariableException

import json
import os
import logging

LOGGER = logging.getLogger(__name__)


class JolokiaTestCase(TestCase):

    @classmethod
    def setUpClass(cls):

        f_requests = open('tests/fixtures/requests.json', 'r')
        cls.requests = json.load(f_requests)
        f_requests.close()

        f_responses = open('tests/fixtures/responses.json', 'r')
        cls.responses = json.load(f_responses)
        f_responses.close()

    def setUp(self):
        try:
            self.jolokia_host = os.environ['JOLOKIA_HOST']
        except KeyError:
            raise MissingEnvironmentVariableException('JOLOKIA_HOST environment variable must be set.')

        self.jc = JolokiaClient('http://{0}:8080/jolokia'.format(self.jolokia_host))

    def _prepare_response(self, response_json, status_code, ok):

        resp_string = json.dumps(response_json)
        resp_obj = JolokiaResponse()

        setattr(JolokiaResponse, 'content', resp_string.encode('utf-8'))
        resp_obj.status_code = status_code
        setattr(JolokiaResponse, 'ok', ok)

        return resp_obj
