"""Forms high-level API for Jolokia Python client"""
import logging

from jolokia.exceptions import IllegalArgumentException
from jolokia.models import JolokiaSession
from jolokia.utils.validators import validate_url
from jolokia.utils.decorators import require_params

LOGGER = logging.getLogger(__name__)


class JolokiaClient(object):
    """Main class for interacting with a single Jolokia agent"""

    def __init__(self, base_url):

        validate_url(base_url)

        self.base_url = base_url
        self.session = JolokiaSession()

    @require_params(
        ['mbean', 'operation', 'arguments'],
        'execute method has 3 required keyword argument: mbean, operation, and arguments'
    )
    def execute(self, **kwargs):
        """Execute JMX operation on MBean."""
        kwargs.update({'type': 'execute'})

        return self.session.simple_post(self.base_url, data=kwargs)

    def list(self, path=None):
        """Returns a list of all MBeans on all available MBean servers."""
        data = {
            'type': 'list',
            'path': path
        }

        LOGGER.debug(data)

        return self.session.simple_post(self.base_url, data=data)

    @require_params(['mbean'], 'search method has 1 required keyword argument: mbean')
    def search(self, **kwargs):
        """Searches all available MBean servers for the desired MBean"""
        kwargs.update({'type': 'search'})

        return self.session.simple_post(self.base_url, data=kwargs)

    def version(self):
        """Returns agent version"""
        return self.session.simple_post(self.base_url, data={'type': 'version'})

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

        return self.session.simple_post(self.base_url, data=data)

    @require_params(['mbean', 'attribute', 'value'], 'set_attribute method has 3 required arguments: mbean, attribute, and value')
    def set_attribute(self, mbean=None, attribute=None, value=None, path=None, **kwargs):
        """Sets the value of an MBean's attribute"""

        if not mbean or not attribute or not value:
            raise IllegalArgumentException(
                'set_attribute method has 3 required parameters: mbean, attribute, and value'
            )

        if isinstance(attribute, list) and isinstance(value, dict):
            return self._bulk_write(mbean, attribute, value, **kwargs)
        elif (isinstance(attribute, list) and isinstance(value, dict)) or (not isinstance(attribute, list) and isinstance(value, dict)):
            raise IllegalArgumentException('Bulk writes must include an attribute list and an attribute map')

        data = {
            'type': 'write',
            'mbean': mbean,
            'attribute': attribute,
            'value': value,
            'path': path
        }

        LOGGER.debug(data)

        return self.session.simple_post(self.base_url, data=data)

    def _bulk_write(self, mbean, attribute, attr_map):

        data = []

        for att in attribute:
            data.append({
                'type': 'write',
                'mbean': mbean,
                'attribute': att,
                'value': attr_map[att]
            })

        LOGGER.debug(data)

        return self.session.simple_post(self.base_url, data=data)

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

        return self.session.simple_post(self.base_url, data=data)
