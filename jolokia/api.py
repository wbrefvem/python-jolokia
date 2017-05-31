from .exceptions import *
from .models import JolokiaSession
import re


class JolokiaClient(object):

    def __init__(self, base_url, *args, **kwargs):

        if not base_url:
            raise UrlNotSpecifiedException()

        self.base_url = base_url
        self.session = JolokiaSession()

    def execute(self, *args, **kwargs):
        """Execute JMX operation on MBean."""
        pass

    def list(self, *args, **kwargs):
        """Return a list of all MBeans on all available MBean servers."""
        pass

    def search(self, *args, **kwargs):
        """Search all available MBean servers for the desired MBean"""
        pass

    def version(self, *args, **kwargs):
        pass

    def get_attribute(self, mbean=None, attribute=None, path=None, *args, **kwargs):
        """Returns an attribute's value. Domain and MBean type must be specified"""

        if not mbean or not attribute:
            raise IllegalArgumentException('get_attribute method has 2 required arguments: mbean and attribute')

        if type(attribute) is list:
            return self._bulk_read(mbean, attribute)

        data = {
            'type': 'read',
            'mbean': mbean,
            'attribute': attribute,
            'path': path
        }

        return self.session.simple_post(self.base_url, data=data)

    def set_attribute(self, mbean=None, attribute=None, value=None, path=None, *args, **kwargs):

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

    """Private methods are not guaranteed to be stable. Use at your peril!"""
    def _validate_url(self, url):
        if not url:
            raise UrlNotSpecifiedException()

        regex = re.compile(r'^https?://([\w\d]+\.)*[\w\d]+(:[\d]{2,})*(/+[\w\d]*)*$')
        if not regex.match(url):
            raise MalformedUrlException('Base url should be of the form http[s]://hostname[:port][path]')

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
