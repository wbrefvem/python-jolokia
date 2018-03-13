from tests.base import JolokiaTestCase
from mock import Mock


class TestSearch(JolokiaTestCase):

    def test_valid_search(self):

        if self.mock:
            resp = self._prepare_response(self.responses['valid_search_response'], 200, True)
            self.jc.session.request = Mock(return_value=resp)

        resp_data = self.jc.search(**self.requests['valid_search'])

        assert resp_data['status'] == 200
        assert isinstance(resp_data['value'], list)
