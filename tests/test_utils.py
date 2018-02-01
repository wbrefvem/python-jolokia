import pytest
import logging

from jolokia.utils.validators import verify_url
from jolokia.utils.decorators import require_params
from jolokia.exceptions import UrlNotSpecifiedException, MalformedUrlException, IllegalArgumentException
from unittest import TestCase
from mock import Mock

logging.basicConfig(level=logging.DEBUG)


class TestValidateUrl(TestCase):

    def test_null_url(self):

        args = [None]

        pytest.raises(UrlNotSpecifiedException, verify_url, *args)

    def test_malformed_no_protocol(self):

        args = ['://herewego.com']

        pytest.raises(MalformedUrlException, verify_url, *args)

    def test_well_formed(self):

        args = ['http://localhost:8080/jolokia']

        assert verify_url(*args) is True

    def test_well_formed_with_non_alpha_chars(self):

        args = ['http://localhost:8080/joloki-1.0.0']

        assert verify_url(*args) is True

    def test_weird_machiney_url(self):

        args = ['http://url-23497fdca787d87b.az.example.com']

        assert verify_url(*args) is True


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
