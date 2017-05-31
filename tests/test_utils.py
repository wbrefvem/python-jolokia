import pytest
import logging

from jolokia.utils import validate_url
from jolokia.exceptions import UrlNotSpecifiedException, MalformedUrlException
from unittest import TestCase


class TestValidateUrl(TestCase):

    def test_null_url(self):

        args = [None]

        pytest.raises(UrlNotSpecifiedException, validate_url, *args)

    def test_malformed_url(self):

        args = ['://herewego.com']

        pytest.raises(MalformedUrlException, validate_url, *args)
