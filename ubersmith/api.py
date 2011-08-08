# lower level api stuff, configuration, and http stuff goes here

import json as _json
from threading import local as _local
import urllib as _urllib
import urllib2 as _urllib2
import urlparse as _urlparse


_DEFAULT_REQUEST_HANDLER = _local()
_DEFAULT_REQUEST_HANDLER.value = None


class RequestHandler(object):
    """Handles all the HTTP requests and authentication."""

    def __init__(self, base_url, username=None, password=None):
        """Initialize request handler and attempt authentication.

            base_url: URL to send API requests
            username: Username for API access
            password: Password for API access

        >>> handler = RequestHandler('http://127.0.0.1:8088/')
        >>> 'http' in _urlparse.urlparse(handler.base_url).scheme
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
        >>> # test that auth_handle was installed into opener
        >>> auth_handlers = [item for item in handler.opener.handlers
        ...     if isinstance(item, _urllib2.HTTPBasicAuthHandler)]
        >>> for handler in auth_handlers:
        ...     passwords = getattr(  # gets pass_manager's passwords
        ...         getattr(handler, 'passwd', None),  # gets pass_manager
        ...         'passwd',
        ...         None
        ...     )
        ...     if passwords:
        ...         default_realm = passwords.get(None)
        ...         if default_realm:
        ...             test_user_pass = default_realm.get((('test1', '/'),))
        ...             if test_user_pass:
        ...                 print test_user_pass
        ...                 break
        ('test2', 'test3')
        """
        self.base_url = base_url
        self.username = username
        self.password = password

        # setup auth for requests
        pass_manager = _urllib2.HTTPPasswordMgrWithDefaultRealm()
        pass_manager.add_password(
            None,  # catch-all realm
            self.base_url,
            self.username,
            self.password
        )
        auth_handler = _urllib2.HTTPBasicAuthHandler(pass_manager)
        self.opener = _urllib2.build_opener(auth_handler)

    def process(self, method, data=None):
        """Send request to ubersmith instance.

            method: Ubersmith API method string
            data: dict of method arguments

        """
        data = data if data is not None else {}

        url = _append_qs(self.base_url, {'method': method})
        response = self.opener.open(url, _urllib.urlencode(data))

        # if response isn't json just return the response object
        if response.info().type != 'application/json':
            return response

        # response is json
        response = _json.load(response)

        # test for error in json response
        if not response['status']:
            raise UbersmithError(response)

        return response['data']


# exceptions

class UbersmithError(Exception):
    """Exception for Ubersmith API.

        response: decoded json response w/ error info
        msg: optional message to pass along w/ stacktrace

    """
    def __init__(self, response, msg=None):
        super(UbersmithError, self).__init__()
        self.status = response.get('status')
        self.error_message = response.get('error_message')
        self.error_code = response.get('error_code')
        self.msg = msg or \
                  'Error in response from Ubersmith API: {0}'.format(response)

    def __repr__(self):
        return self.msg

    def __str__(self):
        return repr(self)


# module functions

def get_default_request_handler():
    if not _DEFAULT_REQUEST_HANDLER.value:
        raise Exception("Request handler required but no default was found.")
    return _DEFAULT_REQUEST_HANDLER.value


def set_default_request_handler(request_handler):
    if not isinstance(request_handler, RequestHandler):
        raise TypeError(
            "Attempted to set an invalid request handler as default.")
    _DEFAULT_REQUEST_HANDLER.value = request_handler


# utility functions

def _append_qs(url, query_string):
    """Append query_string values to an existing URL and return it as a string.

    query_string can be:
        * an encoded string: 'test3=val1&test3=val2'
        * a dict of strings: {'test3': 'val'}
        * a dict of lists of strings: {'test3': ['val1', 'val2']}
        * a list of tuples: [('test3', 'val1'), ('test3', 'val2')]

    >>> url = 'http://domain.tld/path/?test1=val&test2#hash'
    >>> string_qs = 'test3=val1&test3=val2'
    >>> dict_qs = {'test3': 'val'}
    >>> nested_dict_qs = {'test3': ['val1', 'val2']}
    >>> list_qs = [('test3', 'val1'), ('test3', 'val2')]
    >>> _append_qs(url, string_qs)
    'http://domain.tld/path/?test1=val&test2=&test3=val1&test3=val2#hash'
    >>> _append_qs(url, dict_qs)
    'http://domain.tld/path/?test1=val&test2=&test3=val#hash'
    >>> _append_qs(url, nested_dict_qs)
    'http://domain.tld/path/?test1=val&test2=&test3=val1&test3=val2#hash'
    >>> _append_qs(url, list_qs)
    'http://domain.tld/path/?test1=val&test2=&test3=val1&test3=val2#hash'

    """
    parsed_url = _urlparse.urlsplit(url)
    parsed_qs = _urlparse.parse_qsl(parsed_url.query, True)

    if _isstr(query_string):
        parsed_qs += _urlparse.parse_qsl(query_string)
    elif _isdict(query_string):
        for item in query_string.items():
            if _islist(item[1]):
                for val in item[1]:
                    parsed_qs.append((item[0], val))
            else:
                parsed_qs.append(item)
    elif _islist(query_string):
        parsed_qs += query_string
    else:
        raise ValueError('Unexpected query_string value')

    return _urlparse.urlunsplit((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        _urllib.urlencode(parsed_qs),
        parsed_url.fragment,
    ))


def _isdict(value):
    """Return true if the value behaves like a dict, false if not."""
    return hasattr(value, 'keys') and hasattr(value, '__getitem__')


def _islist(value):
    """Return true if the value behaves like a list, false if not."""
    return hasattr(value, 'append') and hasattr(value, '__getitem__')


def _isstr(value):
    """Return true if the value behaves like a string, false if not."""
    return isinstance(value, basestring)


# run tests

if __name__ == '__main__':
    import doctest as _doctest
    _doctest.testmod()
