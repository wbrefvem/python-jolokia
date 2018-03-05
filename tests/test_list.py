from tests.base import JolokiaTestCase


class TestList(JolokiaTestCase):

    def test_valid_request(self):

        resp_data = self.jc.list(path='java.lang/type=Memory/attr/HeapMemoryUsage')

        assert type(resp_data) is dict
        assert resp_data['status'] == 200
        assert type(resp_data['value']) is dict

    def test_invalid_path(self):

        resp_data = self.jc.list(path='java.lang/type=Memory/HeapMemoryUsage')

        assert type(resp_data) is dict
        assert resp_data['status'] == 400
        assert resp_data['error_type'] == 'java.lang.IllegalArgumentException'
