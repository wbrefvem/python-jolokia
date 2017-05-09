class UrlNotSpecifiedException(Exception):

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = 'You must specify a URL.'


class MalformedUrlException(Exception):
    pass
