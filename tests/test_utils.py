import pytest
import logging

from jolokia.utils.validators import validate_url
from jolokia.utils.decorators import require_params
from jolokia.exceptions import UrlNotSpecifiedException, MalformedUrlException, IllegalArgumentException
from unittest import TestCase
from mock import Mock

logging.basicConfig(level=logging.DEBUG)


class TestValidateUrl(TestCase):

    def test_null_url(self):

        args = [None]

        pytest.raises(UrlNotSpecifiedException, validate_url, *args)

    def test_malformed_url(self):

        args = ['://herewego.com']

        pytest.raises(MalformedUrlException, validate_url, *args)


class TestRequireArgs(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRequireArgs, self).__init__(*args, **kwargs)

        self.func_ret = 'Method wrapped and executed successfully'
        mock = Mock(return_value=self.func_ret)
        mock.__name__ = 'require_args_mock'
        wrapper_func = require_params(['foo', 'bar'], 'Args not provided')
        self.func = wrapper_func(mock)

    def test_valid_args(self):
        ret = self.func(foo='baz', bar='bif')
        assert ret == self.func_ret

    def test_no_args(self):
        pytest.raises(IllegalArgumentException, self.func, [])
