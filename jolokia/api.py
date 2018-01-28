from jolokia.exceptions import *
from jolokia.models import JolokiaSession
from jolokia.utils.validators import validate_url
from jolokia.utils.decorators import require_args
import logging


logging.basicConfig(level=logging.DEBUG)


class JolokiaClient(object):

    def __init__(self, base_url, *args, **kwargs):

        validate_url(base_url)

        self.base_url = base_url
        self.session = JolokiaSession()

    @require_args(['mbean', 'operation', 'arguments'], 'execute method has 3 required keyword argument: mbean, operation, and arguments')
    def execute(self, *args, **kwargs):
        """Execute JMX operation on MBean."""
        kwargs.update({'type': 'execute'})

        return self.session.simple_post(self.base_url, data=kwargs)

    def list(self, path=None, *args, **kwargs):
        """Returns a list of all MBeans on all available MBean servers."""
        data = {
            'type': 'list',
            'path': path
        }

        return self.session.simple_post(self.base_url, data=data)

    @require_args(['mbean'], 'search method has 1 required keyword argument: mbean')
    def search(self, data=None, *args, **kwargs):
        """Searches all available MBean servers for the desired MBean"""
        kwargs.update({'type': 'search'})

        return self.session.simple_post(self.base_url, data=kwargs)

    def version(self, *args, **kwargs):
        """Returns agent version"""
        return self.session.simple_post(self.base_url, data={'type': 'version'})

    @require_args(['mbean', 'attribute'], 'get_attribute method has 2 required keyword arguments: mbean and attribute')
    def get_attribute(self, mbean=None, attribute=None, path=None, *args, **kwargs):
        """Returns an attribute's value. Domain and MBean type must be specified

        :param mbean: The MBean to query.
        :param attribute: The MBean attribute to get
        :param path: (optional) Path to query into MBean attribute
        """

        if type(attribute) is list:
            return self._bulk_read(mbean, attribute)

        data = {
            'type': 'read',
            'mbean': mbean,
            'attribute': attribute,
            'path': path
        }

        return self.session.simple_post(self.base_url, data=data)

    @require_args(['mbean', 'attribute', 'value'], 'set_attribute method has 3 required arguments: mbean, attribute, and value')
    def set_attribute(self, mbean=None, attribute=None, value=None, path=None, *args, **kwargs):
        """Sets the value of an MBean's attribute"""

        if not mbean or not attribute or not value:
            raise IllegalArgumentException('set_attribute method has 3 required parameters: mbean, attribute, and value')

        if type(attribute) is list and type(value) is dict:
            return self._bulk_write(mbean, attribute, value, **kwargs)
        elif (type(attribute) is list and type(value) is not dict) or (type(attribute) is not list and type(value) is dict):
            raise IllegalArgumentException('Bulk writes must include an attribute list and an attribute map')

        data = {
            'type': 'write',
            'mbean': mbean,
            'attribute': attribute,
            'value': value,
            'path': path
        }

        return self.session.simple_post(self.base_url, data=data)

    def _bulk_write(self, mbean, attribute, attr_map, path=None, *args, **kwargs):

        data = []

        for a in attribute:
            data.append({
                'type': 'write',
                'mbean': mbean,
                'attribute': a,
                'value': attr_map[a]
            })

        return self.session.simple_post(self.base_url, data=data)

    def _bulk_read(self, mbean, attribute, path=None, *args, **kwargs):
        data = []

        for a in attribute:
            data.append({
                'type': 'read',
                'mbean': mbean,
                'attribute': a,
                'path': path
            })

        return self.session.simple_post(self.base_url, data=data)


class JBossJolokiaClient(JolokiaClient):

    def read(self, domain='jboss.as.expr', type=None, attribute=None, *args, **kwargs):
        pass
