from jolokia import JolokiaClient
from .fixtures.responses import mock_valid_attribute_request


def test_valid_request():

    jc = JolokiaClient()

    setattr(jc.session, 'request', mock_valid_attribute_request)

    resp_json = jc.get_attribute(domain='java.lang', mbean_type='Memory', attribute='HeapMemoryUsage')

    assert resp_json['status'] == 200
    assert 'init' in resp_json['value']
