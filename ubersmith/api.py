"""Lower level API, configuration, and HTTP stuff."""

import json as json
from threading import local
import urllib
import urlparse

import httplib2

from ubersmith.exceptions import UbersmithResponseError
from ubersmith.utils import append_qs

__all__ = [
    'RequestHandler',
    'get_default_request_handler',
    'set_default_request_handler',
]

_DEFAULT_REQUEST_HANDLER = local()
_DEFAULT_REQUEST_HANDLER.value = None


class RequestHandler(object):
    """Handles all the HTTP requests and authentication."""

    def __init__(self, base_url, username=None, password=None):
        """Initialize request handler with authentication.

            base_url: URL to send API requests
            username: Username for API access
            password: Password for API access

        >>> handler = RequestHandler('http://127.0.0.1:8088/')
        >>> 'http' in urlparse.urlparse(handler.base_url).scheme
        True
        >>> config = {
        ...     'base_url': 'test1',
        ...     'username': 'test2',
        ...     'password': 'test3',
        ... }
        >>> handler = RequestHandler(**config)
        >>> # test that all config values were set as instance members
        >>> [False for k, v in config.items()
        ...     if getattr(handler, k, None) is not config[k]]
        []

        """
        self.base_url = base_url
        self.username = username
        self.password = password

        self._http = httplib2.Http(".cache")
        self._http.add_credentials(self.username, self.password,
                                   urlparse.urlparse(self.base_url)[1])

    def process(self, method, data=None, raw=False):
        """Send request to ubersmith instance.

            method: Ubersmith API method string
            data: dict of method arguments ready to urllib.urlencode
            raw: Set to True to return the raw response vs the default
                 behavior of returning JSON data

        """
        data = data if data is not None else {}
        url = append_qs(self.base_url, {'method': method})
        body = urllib.urlencode(data)
        # httplib2 requires that you manually send Content-Type on POSTs :/
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response, content = self._http.request(url, "POST", body, headers)

        # just return the raw response
        if raw:
            return response, content

        # response isn't json
        if response.get('content-type') != 'application/json':
            UbersmithResponseError("Response wasn't application/json")

        # response is json
        response_dict = json.loads(content)

        # test for error in json response
        if not response_dict['status']:
            raise UbersmithResponseError(response=response_dict)

        return response_dict['data']


def get_default_request_handler():
    """Return the local default request handler."""
    if not _DEFAULT_REQUEST_HANDLER.value:
        raise Exception("Request handler required but no default was found.")
    return _DEFAULT_REQUEST_HANDLER.value


def set_default_request_handler(request_handler):
    """Set the local default request handler."""
    if not isinstance(request_handler, RequestHandler):
        raise TypeError(
            "Attempted to set an invalid request handler as default.")
    _DEFAULT_REQUEST_HANDLER.value = request_handler
