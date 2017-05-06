from exceptions import UrlNotSpecifiedException


class JolokiaClient(object):

    def __init__(self, url=None, *args, **kwargs):
        if url:
            self.url = url
        else:
            raise UrlNotSpecifiedException("You must specify a url\
                for the Jolokia agent you wish to connect to.")
