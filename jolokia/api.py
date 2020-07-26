"""Forms high-level API for Jolokia Python client"""
import logging

from jolokia.exceptions import IllegalArgumentException
from jolokia.models import JolokiaSession
from jolokia.utils.validators import verify_url
from jolokia.utils.decorators import require_params

LOGGER = logging.getLogger(__name__)


class JolokiaClient(object):
    """Main class for interacting with a single Jolokia agent"""

    def __init__(self, base_url, username=None, password=None):

        verify_url(base_url)

        self.base_url = base_url
        self.session = JolokiaSession(username, password)

    @require_params(['mbean', 'operation', 'arguments'], 'execute method has 3 required keyword argument: mbean, operation, and arguments')
    def execute(self, **kwargs):
        """Execute JMX operation on MBean."""
        kwargs.update({'type': 'exec'})

        resp = self.session.simple_post(self.base_url, data=kwargs)

        LOGGER.debug('Return type of {0} with return value of {1}'.format(type(resp), resp.text))

        try:
            return resp.json()
        except ValueError:
            return resp
        finally:
            LOGGER.debug(resp.content)

    def list(self, path=None):
        """Returns a list of all MBeans on all available MBean servers."""
        data = {
            'type': 'list',
            'path': path
        }

        LOGGER.debug(data)

        resp = self.session.simple_post(self.base_url, data=data)

        try:
            return resp.json()
        except ValueError:
            return resp
        finally:
            LOGGER.debug(resp.content)

    @require_params(['mbean'], 'search method has 1 required keyword argument: mbean')
    def search(self, **kwargs):
        """Searches all available MBean servers for the desired MBean"""
        kwargs.update({'type': 'search'})

        resp = self.session.simple_post(self.base_url, data=kwargs)

        try:
            return resp.json()
        except ValueError:
            return resp
        finally:
            LOGGER.debug(resp.content)

    def version(self):
        """Returns agent version"""
        resp = self.session.simple_post(self.base_url, data={'type': 'version'})

        try:
            return resp.json()
        except ValueError:
            return resp
        finally:
            LOGGER.debug(resp.content)

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

        try:
            return resp.json()
        except ValueError:
            return resp
        finally:
            LOGGER.debug(resp.content)

    @require_params(['mbean', 'attr_value_pairs'], 'set_attribute method has 2 required arguments: mbean, attr_value_pairs')
    def set_attribute(self, mbean=None, attr_value_pairs=None, bulk=False, path=None):
        """Sets the value of an MBean's attribute

        :param mbean: string, the mbean to query
        :param attr_value_pairs: If bulk is false, a 2-tuple consisting of (attribute, value). If bulk is true, a list of such tuples.
        :param bulk: (optional) Whether or not multiple attributes are to be set.
        :param path: (optional) Inner path for nesteed mbean values
        """

        if not _attr_value_pairs_is_valid(bulk, attr_value_pairs):
            raise IllegalArgumentException('attr_value_pairs must either be a single 2-tuple or a list of 2-tuples.')

        if bulk:
            return self._bulk_write(mbean, attr_value_pairs)

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
        try:
            return resp.json()
        except ValueError:
            return resp
        finally:
            LOGGER.debug(resp.content)

    def _bulk_write(self, mbean, attr_value_pairs):

        data = []

        for avp in attr_value_pairs:
            attr, value = avp
            data.append({
                'type': 'write',
                'mbean': mbean,
                'attribute': attr,
                'value': value
            })

        LOGGER.debug(data)

        resp = self.session.simple_post(self.base_url, data=data)

        try:
            return resp.json()
        except ValueError:
            return resp
        finally:
            LOGGER.debug(resp.content)

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

        try:
            return resp.json()
        except ValueError:
            return resp
        finally:
            LOGGER.debug(resp.content)


def _attr_value_pairs_is_valid(bulk, attr_value_pairs):

    if not bulk:
        return isinstance(attr_value_pairs, tuple) and len(attr_value_pairs) == 2

    LOGGER.debug('Validating bulk write...')

    if not isinstance(attr_value_pairs, list):
        LOGGER.debug('Attribute-value pairs not a list')
        return False

    for avp in attr_value_pairs:
        if not (isinstance(avp, tuple) and len(avp) == 2):
            LOGGER.debug('At least one of the attribute-value pairs is invalid')
            return False

    return True
