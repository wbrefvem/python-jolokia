from .exceptions import UrlNotSpecifiedException, MalformedBaseUrlException
import requests


class JolokiaClient(object):

    def __init__(self, base_url=None, *args, **kwargs):
        if not base_url:
            raise UrlNotSpecifiedException('You must specify a base url.')
        if base_url.endswith('/'):
            raise MalformedBaseUrlException('Base url should be of the form http[s]://domain')
        self.url = base_url
        self.session = requests.Session()

    def get(self, *args, **kwargs):
        """Send GET request to Jolokia agent. Returns raw response"""
        pass

    def post(self, data=None, *args, **kwargs):
        """Send POST request to Jolokia agent. Returns raw response.
           :param data: dict or list, to be serialized to JSON and posted to Jolokia agent."""
        pass

    def read(self, domain=None, type=None, attribute=None, *args, **kwargs):
        """Read MBean data from Jolokia agent.
           :param domain: (required) MBean domain, e.g. java.lang or jboss.as
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

    def _build_url(self, *args, **kwargs):
        """Build URL based on base URL, operation, type, or, optionally, attribute or JMX operation."""
        pass
