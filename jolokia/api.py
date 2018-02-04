"""Forms high-level API for Jolokia Python client"""
import logging

from jolokia.exceptions import IllegalArgumentException
from jolokia.models import JolokiaSession
from jolokia.utils.validators import verify_url
from jolokia.utils.decorators import require_params

LOGGER = logging.getLogger(__name__)


class JolokiaClient(object):
    """Main class for interacting with a single Jolokia agent"""

    def __init__(self, base_url):

        verify_url(base_url)

        self.base_url = base_url
        self.session = JolokiaSession()

    @require_params(['mbean', 'operation', 'arguments'], 'execute method has 3 required keyword argument: mbean, operation, and arguments')
    def execute(self, **kwargs):
        """Execute JMX operation on MBean."""
        kwargs.update({'type': 'execute'})

        resp = self.session.simple_post(self.base_url, data=kwargs)

        if resp.status_code == 200:
            return resp.json()

        return resp

    def list(self, path=None):
        """Returns a list of all MBeans on all available MBean servers."""
        data = {
            'type': 'list',
            'path': path
        }

        LOGGER.debug(data)

        resp = self.session.simple_post(self.base_url, data=data)

        if resp.status_code == 200:
            return resp.json()

        return resp

    @require_params(['mbean'], 'search method has 1 required keyword argument: mbean')
    def search(self, **kwargs):
        """Searches all available MBean servers for the desired MBean"""
        kwargs.update({'type': 'search'})

        resp = self.session.simple_post(self.base_url, data=kwargs)

        if resp.status_code == 200:
            return resp.json()

        return resp

    def version(self):
        """Returns agent version"""
        resp = self.session.simple_post(self.base_url, data={'type': 'version'})

        if resp.status_code == 200:
            return resp.json()

        return resp

    @require_params(['mbean', 'attribute'], 'get_attribute method has 2 required keyword arguments: mbean and attribute')
    def get_attribute(self, mbean=None, attribute=None, path=None):
        """Returns an attribute's value. Domain and MBean type must be specified

        :param mbean: The MBean to query.
        :param attribute: The MBean attribute to get
        :param path: (optional) Path to query into MBean attribute
        """

        if isinstance(attribute, list):
            return self._bulk_read(mbean, attribute)

        data = {
            'type': 'read',
            'mbean': mbean,
            'attribute': attribute,
            'path': path
        }

        LOGGER.debug(data)

        resp = self.session.simple_post(self.base_url, data=data)

        LOGGER.debug(resp.text)

        if resp.status_code == 200:
            return resp.json()

        return resp

    @require_params(['mbean', 'attr_value_pairs'], 'set_attribute method has 2 required arguments: mbean, attr_value_pairs')
    def set_attribute(self, mbean=None, attr_value_pairs=None, bulk=False, path=None, **kwargs):
        """Sets the value of an MBean's attribute

        :param mbean: string, the mbean to query
        :param attr_value_pairs: If bulk is false, a 2-tuple consisting of (attribute, value). If bulk is true, a list of such tuples.
        :param bulk: (optional) Whether or not multiple attributes are to be set.
        :param path: (optional) Inner path for nesteed mbean values
        """

        if bulk:
            if not isinstance(attr_value_pairs, list):
                raise IllegalArgumentException('Bulk writes require attribute to be a list of tuples.')
            return self._bulk_write(mbean, attr_value_pairs, **kwargs)

        if not isinstance(attr_value_pairs, tuple) or len(attr_value_pairs) != 2:
            raise IllegalArgumentException('Attribute must a 2-tuple')

        attribute, value = attr_value_pairs

        data = {
            'type': 'write',
            'mbean': mbean,
            'attribute': attribute,
            'value': value,
            'path': path
        }

        LOGGER.debug(data)

        resp = self.session.simple_post(self.base_url, data=data)

        if resp.status_code == 200:
            return resp.json()

        return resp

    def _bulk_write(self, mbean, attribute):

        data = []

        for attr in attribute:
            if not isinstance(attr, tuple) or len(attr) != 2:
                raise IllegalArgumentException('Attribute must be a 2-tuple')
            attr, value = attr
            data.append({
                'type': 'write',
                'mbean': mbean,
                'attribute': attr,
                'value': value
            })

        LOGGER.debug(data)

        resp = self.session.simple_post(self.base_url, data=data)

        if resp.status_code == 200:
            return resp.json()

        return resp

    def _bulk_read(self, mbean, attribute, path=None):
        data = []

        for att in attribute:
            data.append({
                'type': 'read',
                'mbean': mbean,
                'attribute': att,
                'path': path
            })

        LOGGER.debug(data)

        resp = self.session.simple_post(self.base_url, data=data)

        if resp.status_code == 200:
            return resp.json()

        return resp
