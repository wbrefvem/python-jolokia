from .exceptions import *
import requests
import re


class JolokiaClient(object):

    def __init__(self, *args, **kwargs):

        self.session = requests.Session()

    def get(self, url=None, *args, **kwargs):
        """Send GET request to Jolokia agent. Returns raw response."""

        self._validate_url(url)
        return self.session.get(url or self.base_url)

    def post(self, url=None, data=None, *args, **kwargs):
        """Send POST request to Jolokia agent. Returns raw response.
           :param data: dict or list, to be serialized to JSON and posted to Jolokia agent."""

        self._validate_url(url)
        return self.session.post(url, data=data)

    def read(self, domain='java.lang', type=None, attribute=None, raw=False, *args, **kwargs):
        """Read MBean data from Jolokia agent.
           :param domain: (required) MBean domain, defaults to java.lang
           :param type: (required) MBean type
           :param attribute: (optional) Causes read request to return single attribute of MBean. Defaults to all attributes."""
        pass

    def write(self, *args, **kwargs):
        """Write Mbean data to Jolokia agent."""
        pass

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

    def get_attribute(self, attribute=None, *args, **kwargs):
        if not attribute:
            raise IllegalArgumentException('You must specify an attribute.')

    """Private methods are not guaranteed to be stable. Use at your peril!"""
    def _build_url(self, *args, **kwargs):
        """Build URL based on base URL, operation, type, or, optionally, attribute or JMX operation."""
        pass

    def _validate_url(self, url):
        if not url:
            raise UrlNotSpecifiedException()

        regex = re.compile(r'^https?://([\w\d]+\.)*[\w\d]+(:[\d]{2,})*(/+[\w\d]*)*$')
        if not regex.match(url):
            raise MalformedUrlException('Base url should be of the form http[s]://hostname[:port][path]')


class JBossJolokiaClient(JolokiaClient):

    def read(self, domain='jboss.as.expr', type=None, attribute=None, *args, **kwargs):
        pass
