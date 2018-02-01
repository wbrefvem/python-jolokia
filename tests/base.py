from unittest import TestCase
from jolokia import JolokiaClient
from jolokia.models import JolokiaResponse

import json


class JolokiaTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(JolokiaTestCase, self).__init__(*args, **kwargs)

        self.jc = JolokiaClient('http://localhost:8080/jolokia-1.0.0')

        f_requests = open('tests/fixtures/requests.json', 'r')
        self.requests = json.load(f_requests)
        f_requests.close()

        f_responses = open('tests/fixtures/responses.json', 'r')
        self.responses = json.load(f_responses)
        f_responses.close()

    def _prepare_response(self, response_json, status_code, ok):

        resp_string = json.dumps(response_json)
        resp_obj = JolokiaResponse()

        setattr(JolokiaResponse, 'content', resp_string.encode('utf-8'))
        resp_obj.status_code = status_code
        setattr(JolokiaResponse, 'ok', ok)

        return resp_obj
