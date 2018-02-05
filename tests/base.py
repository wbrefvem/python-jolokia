from unittest import TestCase
from jolokia import JolokiaClient
from jolokia.models import JolokiaResponse
from mock import Mock

import json


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
        self.jc = JolokiaClient('http://localhost:8080/jolokia-1.0.0')

    def _prepare_response(self, response_json, status_code, ok):

        resp_string = json.dumps(response_json)
        resp_obj = JolokiaResponse()

        setattr(JolokiaResponse, 'content', resp_string.encode('utf-8'))
        resp_obj.status_code = status_code
        setattr(JolokiaResponse, 'ok', ok)

        return resp_obj

    def test_missing_agent(self):

        self.jc = JolokiaClient('http://google.com')
        resp = self._prepare_response(self.responses['method_not_allowed'], 405, False)
        self.jc.session.request = Mock(return_value=resp)

        resp = self.jc.get_attribute(mbean='java.lang:Memory', attribute='HeapMemoryUsage')
        assert resp['status'] == 405
