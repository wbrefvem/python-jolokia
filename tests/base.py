from unittest import TestCase
from jolokia import JolokiaClient
from requests import Response

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
            self.mock = True
            self.jolokia_host = 'localhost'

        try:
            self.agent_version = os.environ['JOLOKIA_AGENT_VERSION']
        except KeyError:
            self.agent_version = '1.5.0'

        try:
            self.protocol_version = os.environ['JOLOKIA_PROTOCOL_VERSION']
        except KeyError:
            self.protocol_version = '7.2'

        self.jc = JolokiaClient('http://{0}:8080/jolokia'.format(self.jolokia_host))

    def _prepare_response(self, response, status_code, ok):

        if not isinstance(response, str):
            resp_string = json.dumps(response)
        else:
            resp_string = response

        resp_obj = Response()

        setattr(Response, 'content', resp_string.encode('utf-8'))
        resp_obj.status_code = status_code
        setattr(Response, 'ok', ok)

        return resp_obj
